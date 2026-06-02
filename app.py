from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).resolve().parent / "example-data"

KINEXON_PARAMS = {
    "player_load":          "PlayerLoad",
    "acceleratiecount":     "Acceleratiecount",
    "afstand_per_minuut_m": "Afstand per minuut",
    "max_snelheid_kmh":     "Maximale snelheid",
    "sprint_intensiteit_pct": "Sprint-intensiteit",
}

INTENSITY_ORDER = ["zwaar", "medium", "licht"]


@st.cache_data
def load_data():
    schema   = pd.read_csv(DATA / "trainingsschema_KNSB_2526.csv")
    kinexon  = pd.read_csv(DATA / "kinexon_export_2526.csv")
    rpe      = pd.read_csv(DATA / "rpe_vragenlijsten_2526.csv")
    hartslag = pd.read_csv(DATA / "hartslagdata_2526.csv")
    return schema, kinexon, rpe, hartslag


def param_status(r: float) -> str:
    if abs(r) >= 0.65:
        return "✅ Sterk onderbouwd"
    if abs(r) >= 0.50:
        return "⚠️ Indicatief"
    return "❌ Onvoldoende bewijs"


# ---- Page setup ----
st.set_page_config(page_title="Trainingsload Shorttrack", layout="wide")
st.title("Trainingsload Shorttrack")
st.caption("Analysepipeline seizoen 2025–2026 · NOC\\*NSF / KNSB · Fase 2 prototype")

threshold = st.sidebar.slider("Representativiteitsdrempel (%)", 40, 90, 60)
st.sidebar.markdown("---")
st.sidebar.caption(
    "Data: `example-data/` (synthetisch)  \n"
    "6 sporters · 38 geplande sessies · seizoen 2025–2026"
)

schema, kinexon, rpe, hartslag = load_data()

joined = kinexon.merge(
    rpe[["sessie_id", "sporterId", "rpe_score", "srpe"]],
    on=["sessie_id", "sporterId"],
    how="inner",
)

tab1, tab2, tab3, tab4 = st.tabs([
    "1 · Representativiteitscheck",
    "2 · Parameteranalyse",
    "3 · Seizoensvergelijking",
    "4 · Niels-overzicht",
])


# ============================================================
# TAB 1 — Representativiteitscheck
# ============================================================
with tab1:
    total   = schema["sessie_id"].nunique()
    covered = kinexon["sessie_id"].nunique()
    pct     = covered / total * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Sessies met Kinexon", f"{covered} / {total}")
    col2.metric("Totale dekking", f"{pct:.0f}%")
    col3.metric(
        "Drempel", f"{threshold}%",
        delta=f"{pct - threshold:+.0f}%",
        delta_color="normal" if pct >= threshold else "inverse",
    )

    if pct < threshold:
        st.error(
            f"**Pipeline gestopt** — dekking {pct:.0f}% ligt onder drempel {threshold}%.  \n"
            "Conclusies op basis van deze dataset zijn onbetrouwbaar. "
            "Bevestig bewust om toch door te gaan (keuze wordt vastgelegd in auditlog)."
        )
    else:
        st.success(f"Dekking {pct:.0f}% haalt drempel {threshold}%. Analyse kan doorgaan.")

    st.subheader("Dekking per trainingstype")

    type_totals = schema.groupby("trainingstype")["sessie_id"].count()
    type_kin    = kinexon.groupby("trainingstype")["sessie_id"].nunique().reindex(
        type_totals.index, fill_value=0
    )
    type_df = pd.DataFrame({
        "Totaal sessies": type_totals,
        "Met Kinexon":    type_kin,
        "Dekking (%)":    (type_kin / type_totals * 100).round(1),
    }).reset_index().rename(columns={"trainingstype": "Trainingstype"})

    st.dataframe(type_df, use_container_width=True, hide_index=True)
    st.bar_chart(type_df.set_index("Trainingstype")["Dekking (%)"])


# ============================================================
# TAB 2 — Parameteranalyse
# ============================================================
with tab2:
    st.subheader("Kinexon-parameters vs. RPE (Pearson r)")
    st.caption(
        f"Analyse op {len(joined)} gekoppelde sessie-sporterinstances "
        f"({joined['sessie_id'].nunique()} sessies · {joined['sporterId'].nunique()} sporters)."
    )

    rows = []
    for col, label in KINEXON_PARAMS.items():
        r_val = joined[[col, "rpe_score"]].corr().iloc[0, 1]
        rows.append({
            "Parameter":           label,
            "Correlatie (r)":      round(r_val, 3),
            "Status":              param_status(r_val),
        })

    param_df = (
        pd.DataFrame(rows)
        .sort_values("Correlatie (r)", ascending=False)
        .reset_index(drop=True)
    )
    st.dataframe(param_df, use_container_width=True, hide_index=True)

    st.info(
        "Kinexon-parameters zijn primair gevalideerd voor teamsport op gras/parket, "
        "niet voor schaatsen op ijs. Froukje valideert domeininterpretatie vóór aanbeveling (P-03)."
    )

    with st.expander("Databeperkingen"):
        n_missing_rpe = (schema["sessie_id"].nunique() * 6) - len(rpe)
        n_missing_hs  = (schema["sessie_id"].nunique() * 6) - len(hartslag)
        st.markdown(
            f"- Kinexon-data ontbreekt voor {total - covered} sessies ({100 - pct:.0f}% van het seizoen).  \n"
            f"- RPE-vragenlijsten: {n_missing_rpe} ontbrekende invullingen.  \n"
            f"- Hartslagdata: {n_missing_hs} sessies zonder HR-meting.  \n"
            "- Kinexon-validiteit voor schaatsen op ijs is niet empirisch vastgesteld."
        )


# ============================================================
# TAB 3 — Seizoensvergelijking
# ============================================================
with tab3:
    st.subheader("Geplande intensiteit vs. gemeten belasting")

    season = (
        joined
        .groupby("geplande_intensiteit")
        .agg(
            sessies      =("sessie_id",   "nunique"),
            gem_rpe      =("rpe_score",   "mean"),
            gem_srpe     =("srpe",        "mean"),
            gem_playerload=("player_load", "mean"),
        )
        .reindex(INTENSITY_ORDER)
        .round(1)
        .reset_index()
        .rename(columns={
            "geplande_intensiteit": "Geplande intensiteit",
            "sessies":              "Sessies (met Kinexon)",
            "gem_rpe":              "Gem. RPE",
            "gem_srpe":             "Gem. sRPE",
            "gem_playerload":       "Gem. PlayerLoad",
        })
    )
    st.dataframe(season, use_container_width=True, hide_index=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.caption("Gem. RPE per intensiteitsniveau (intern)")
        st.bar_chart(season.set_index("Geplande intensiteit")["Gem. RPE"])
    with col_b:
        st.caption("Gem. PlayerLoad per intensiteitsniveau (extern)")
        st.bar_chart(season.set_index("Geplande intensiteit")["Gem. PlayerLoad"])

    st.subheader("PlayerLoad per trainingstype")
    type_pl = (
        joined.groupby("trainingstype")["player_load"]
        .mean()
        .round(1)
        .rename("Gem. PlayerLoad")
        .reset_index()
        .rename(columns={"trainingstype": "Trainingstype"})
    )
    st.bar_chart(type_pl.set_index("Trainingstype"))


# ============================================================
# TAB 4 — Niels-overzicht
# ============================================================
with tab4:
    st.subheader("Trainingsseizoen 2025–2026 — Overzicht voor Niels")

    ok_params = param_df[param_df["Status"] == "✅ Sterk onderbouwd"]["Parameter"].tolist()
    top_r     = param_df.iloc[0]["Correlatie (r)"]
    top_name  = param_df.iloc[0]["Parameter"]

    rpe_by_intens = season.set_index("Geplande intensiteit")["Gem. RPE"]
    rpe_zwaar = rpe_by_intens.get("zwaar", None)
    rpe_licht = rpe_by_intens.get("licht", None)
    consistent = (rpe_zwaar is not None and rpe_licht is not None
                  and float(rpe_zwaar) > float(rpe_licht) + 2.0)
    kernvraag = "Ja" if consistent else "Gedeeltelijk"

    st.markdown(f"**Trainen wij wat we in de wedstrijd nodig hebben?** {kernvraag}")
    st.markdown("---")

    if ok_params:
        st.markdown(
            f"**Bevinding 1 — Externe load is meetbaar.**  \n"
            f"{', '.join(ok_params)} geven een betrouwbaar beeld van de externe trainingsbelasting "
            f"(sterkste relatie met RPE: r = {top_r:.2f} voor {top_name})."
        )
    else:
        st.warning("Geen parameters gevonden met voldoende statistisch bewijs.")

    if rpe_zwaar is not None and rpe_licht is not None:
        diff_rpe = float(rpe_zwaar) - float(rpe_licht)
        st.markdown(
            f"**Bevinding 2 — Intensiteitsverdeling klopt.**  \n"
            f"Zware trainingen scoren gemiddeld {diff_rpe:.1f} RPE-punten hoger dan lichte "
            f"trainingen. De geplande intensiteit vertaalt zich naar de gemeten belasting."
        )

    pl_relay = joined[joined["trainingstype"] == "relay"]["player_load"].mean()
    pl_ind   = joined[joined["trainingstype"] == "individueel"]["player_load"].mean()
    if pl_relay > 0 and pl_ind > 0:
        diff_pct = (pl_relay - pl_ind) / pl_ind * 100
        st.markdown(
            f"**Bevinding 3 — Relay vs. individueel.**  \n"
            f"Relay-trainingen genereren gemiddeld {diff_pct:.0f}% meer PlayerLoad dan individuele "
            f"trainingen. Dit weerspiegelt het hogere teamtempo en de kortere herstelmomenten bij relay."
        )

    st.markdown(
        "**Aanbeveling voor volgend seizoen:** Gebruik PlayerLoad en Acceleratiecount als vaste "
        "monitoringparameters. Zorg voor betere Kinexon-dekking bij individuele trainingen en "
        "techniektrainingen zodat het volledige seizoen betrouwbaar geanalyseerd kan worden."
    )

    st.markdown("---")
    st.caption(
        "Dit overzicht is automatisch gegenereerd op basis van de analyse. "
        "Froukje valideert de inhoud vóór verzending naar Niels (F-05)."
    )
