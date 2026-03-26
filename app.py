import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Collapse Risk Intelligence", layout="wide")

st.title("🌍 Collapse Risk Intelligence Platform")

st.markdown("""
A decision-support system to monitor societal instability, identify risk drivers,  
and provide early warning signals for intervention.
""")

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("collapse_early_warning_final.csv")

df = load_data()

# ----------------------------
# SIDEBAR
# ----------------------------
country = st.sidebar.selectbox("Select Country", sorted(df["Entity"].unique()))

country_data = df[df["Entity"] == country]
latest = country_data.sort_values("Year").iloc[-1]

risk = latest["Risk_Band"]
score = latest["Cumulative_CRI"]

# =========================================================
# 🔥 GLOBAL KPI SECTION (NEW)
# =========================================================
st.header("📊 Country Risk Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Cumulative Risk", round(score, 2))
col2.metric("Risk Band", risk)
col3.metric("Year", int(latest["Year"]))

if risk == "Danger":
    st.error("🔴 High Risk – Immediate intervention required")
elif risk == "Warning":
    st.warning("🟡 Warning – Monitor closely")
else:
    st.success("🟢 Stable")

# ----------------------------
# TABS
# ----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "🌍 Global View",
    "📈 Trends & Drivers",
    "🚨 Early Warning"
])

# =========================================================
# 📊 OVERVIEW (NOW ONLY ALERTS)
# =========================================================
with tab1:
    st.subheader("🚨 Top Risk Countries")

    latest_global = df.sort_values("Year").groupby("Entity").tail(1)
    top5 = latest_global.sort_values("Cumulative_CRI", ascending=False).head(5)

    st.dataframe(top5[["Entity", "Cumulative_CRI", "Risk_Band"]])

# =========================================================
# 🌍 GLOBAL VIEW
# =========================================================
with tab2:
    st.subheader("Global Collapse Risk Map")

    latest_global = df.sort_values("Year").groupby("Entity").tail(1)

    fig_map = px.choropleth(
        latest_global,
        locations="Entity",
        locationmode="country names",
        color="Cumulative_CRI",
        color_continuous_scale="Reds"
    )

    st.plotly_chart(fig_map, use_container_width=True)

    st.subheader("Country Comparison")

    selected = st.multiselect(
        "Select Countries",
        df["Entity"].unique(),
        default=[country]
    )

    for c in selected:
        temp = df[df["Entity"] == c]
        st.line_chart(temp.set_index("Year")["Cumulative_CRI"])

# =========================================================
# 📈 TRENDS & DRIVERS
# =========================================================
with tab3:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Risk Trend")

        fig1, ax1 = plt.subplots()
        ax1.plot(country_data["Year"], country_data["Cumulative_CRI"], marker='o')
        st.pyplot(fig1)

    with col2:
        st.subheader("Key Drivers")

        drivers = pd.DataFrame({
            "Factor": ["Climate", "Food", "Economic", "Human"],
            "Impact": [
                latest["Climate_Stress"],
                latest["Food_Stress"],
                latest["Economic_Stress"],
                latest["Human_Stress"]
            ]
        }).sort_values("Impact", ascending=True)

        fig2, ax2 = plt.subplots()
        ax2.barh(drivers["Factor"], drivers["Impact"])
        st.pyplot(fig2)

# =========================================================
# 🚨 EARLY WARNING
# =========================================================
with tab4:
    st.subheader("Early Warning Dashboard")

    st.markdown("### Overall Risk Status")

    if risk == "Danger":
        st.error(f"🔴 DANGER\n\nRisk Score: {score:.2f}")
    elif risk == "Warning":
        st.warning(f"🟡 WARNING\n\nRisk Score: {score:.2f}")
    else:
        st.success(f"🟢 SAFE\n\nRisk Score: {score:.2f}")

    st.markdown("### Warning Signal")

    if latest["Emigration_Tipping_Point"]:
        st.error("🚨 Migration Surge Detected")
    else:
        st.success("No critical migration signal")

    st.markdown("### Recommended Action")

    if risk == "Danger":
        st.error("Immediate action: Stabilize food systems and economy")
    elif risk == "Warning":
        st.warning("Preventive action: Strengthen resilience systems")
    else:
        st.success("Maintain current policies")

# ----------------------------
# FOOTER
# ----------------------------
st.info("Entrepreneurial early warning system for societal collapse risk.")