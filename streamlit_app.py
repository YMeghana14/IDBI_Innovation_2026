import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="CrediLens MSME",
    page_icon="💳",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/synthetic_msme_data.csv")

df = load_data()

st.title("CrediLens MSME")
st.subheader("AI-Powered Financial Health Card for Credit-Invisible MSMEs")

st.markdown("""
This Proof of Concept demonstrates how alternate MSME data such as UPI activity, GST-like sales,
Account Aggregator-style bank transaction signals, EPFO-like payroll stability, invoice behavior,
and repayment patterns can be converted into an explainable Financial Health Card for digital lending.
""")

selected_business = st.sidebar.selectbox(
    "Select MSME Profile",
    df["business_name"].tolist()
)

row = df[df["business_name"] == selected_business].iloc[0]

st.sidebar.markdown("### Data Sources Simulated")
st.sidebar.write("GST-like data")
st.sidebar.write("UPI transaction data")
st.sidebar.write("AA-style bank statement data")
st.sidebar.write("EPFO-like payroll data")
st.sidebar.write("Invoice and repayment signals")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Financial Health Score", f"{row['overall_score']}/100")
col2.metric("Risk Category", row["risk_category"])
col3.metric("Credit Readiness", row["credit_readiness"])
col4.metric("Business Vintage", f"{row['business_vintage_years']} yrs")

st.markdown("---")

left, right = st.columns([1.2, 1])

with left:
    st.markdown("## MSME Financial Health Card")
    st.write(f"**Business Name:** {row['business_name']}")
    st.write(f"**Sector:** {row['sector']}")
    st.write(f"**Monthly UPI Value:** ₹{row['upi_monthly_value']:,.0f}")
    st.write(f"**GST-like Monthly Sales:** ₹{row['gst_monthly_sales']:,.0f}")
    st.write(f"**Average Bank Balance:** ₹{row['avg_bank_balance']:,.0f}")
    st.write(f"**Employee Count:** {int(row['employee_count'])}")

with right:
    score_df = pd.DataFrame({
        "Dimension": [
            "Cash-flow Stability",
            "UPI Strength",
            "GST Consistency",
            "Repayment Discipline",
            "Invoice Reliability",
            "Payroll Stability",
            "Business Growth"
        ],
        "Score": [
            row["cashflow_score"],
            row["upi_score"],
            row["gst_score"],
            row["repayment_score"],
            row["invoice_score"],
            row["payroll_score"],
            row["growth_score"]
        ]
    })

    fig = px.bar(
        score_df,
        x="Score",
        y="Dimension",
        orientation="h",
        range_x=[0, 100],
        title="Score Breakdown"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.markdown("## Explainable AI Insights")

strengths = []
risks = []

if row["upi_score"] >= 75:
    strengths.append("Strong UPI transaction activity indicates healthy digital business movement.")
else:
    risks.append("UPI transaction strength is moderate and may need additional validation.")

if row["gst_score"] >= 75:
    strengths.append("Consistent GST-like sales and filing behavior improves confidence.")
else:
    risks.append("GST/compliance consistency is weak or irregular.")

if row["repayment_score"] >= 75:
    strengths.append("Good repayment discipline with low bounce or delay indicators.")
else:
    risks.append("Repayment behavior shows bounce/delay risk.")

if row["cashflow_score"] >= 75:
    strengths.append("Stable cash-flow pattern and healthy average bank balance.")
else:
    risks.append("Cash-flow volatility or low balance pattern may affect repayment ability.")

if row["growth_score"] >= 70:
    strengths.append("Positive business growth trend supports credit readiness.")
else:
    risks.append("Growth trend is flat or declining and requires monitoring.")

scol1, scol2 = st.columns(2)

with scol1:
    st.success("Strengths")
    for item in strengths:
        st.write(f"✅ {item}")

with scol2:
    st.warning("Risks / Watchpoints")
    for item in risks:
        st.write(f"⚠️ {item}")

st.markdown("## Recommended Credit Action")
st.info(row["recommendation"])

st.markdown("---")
st.markdown("## Ecosystem Readiness")
st.write("""
In a real implementation, this architecture can integrate with:
- Account Aggregator for consent-based bank transaction data
- ULI for standardized borrower data access
- OCEN for digital credit journey enablement
- GST, UPI, EPFO and invoice systems as alternate data providers
""")

st.caption("POC uses synthetic data for demonstration only.")