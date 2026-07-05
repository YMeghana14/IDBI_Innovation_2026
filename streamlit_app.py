import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="CrediLens MSME",
    page_icon="💳",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #0f172a 0%, #1e3a8a 55%, #2563eb 100%);
        padding: 1.4rem 1.6rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 1rem;
    }
    .main-header h1 {
        margin-bottom: 0.2rem;
    }
    .decision-approve {
        padding: 1rem;
        border-radius: 14px;
        background: #ecfdf5;
        border: 1px solid #10b981;
        color: #065f46;
        font-weight: 700;
    }
    .decision-review {
        padding: 1rem;
        border-radius: 14px;
        background: #fffbeb;
        border: 1px solid #f59e0b;
        color: #92400e;
        font-weight: 700;
    }
    .decision-reject {
        padding: 1rem;
        border-radius: 14px;
        background: #fef2f2;
        border: 1px solid #ef4444;
        color: #991b1b;
        font-weight: 700;
    }
    .risk-tag {
        padding: 0.5rem 0.8rem;
        border-radius: 12px;
        background: #fff7ed;
        border: 1px solid #fdba74;
        margin-bottom: 0.6rem;
        font-weight: 600;
        color: #9a3412;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("data/synthetic_msme_data.csv")

    # Compatibility fix:
    # If your GitHub CSV is older and does not contain these new columns,
    # the app will create them automatically instead of crashing.

    if "existing_credit_exposure" not in df.columns:
        df["existing_credit_exposure"] = (
            df.get("gst_monthly_sales", pd.Series([500000] * len(df))) * 0.35
        ).fillna(250000).astype(int)

    if "monthly_obligation" not in df.columns:
        df["monthly_obligation"] = (
            df.get("gst_monthly_sales", pd.Series([500000] * len(df))) * 0.06
        ).fillna(25000).astype(int)

    if "city" not in df.columns:
        df["city"] = "Not Available"

    if "sales_series" not in df.columns:
        df["sales_series"] = df["gst_monthly_sales"].apply(
            lambda x: "|".join([
                str(int(x * factor))
                for factor in [0.82, 0.88, 0.93, 1.0, 1.04, 1.08]
            ])
        )

    if "upi_series" not in df.columns:
        df["upi_series"] = df["upi_monthly_value"].apply(
            lambda x: "|".join([
                str(int(x * factor))
                for factor in [0.78, 0.84, 0.91, 0.96, 1.02, 1.08]
            ])
        )

    if "balance_series" not in df.columns:
        df["balance_series"] = df["avg_bank_balance"].apply(
            lambda x: "|".join([
                str(int(x * factor))
                for factor in [0.75, 0.82, 0.9, 0.95, 1.0, 1.05]
            ])
        )

    return df


def calculate_scores(row, use_gst, use_upi, use_aa, use_epfo, use_invoice):
    scores = {}

    if use_aa:
        cashflow_score = max(
            0,
            min(
                100,
                96
                - row["cashflow_volatility"] * 125
                + min(18, row["avg_bank_balance"] / 25000),
            ),
        )

        repayment_score = max(
            0,
            min(
                100,
                100
                - row["bounce_count_6m"] * 7.5
                - row["repayment_delay_days"] * 1.7,
            ),
        )

        scores["Cash-flow Stability"] = round(cashflow_score, 1)
        scores["Repayment Discipline"] = round(repayment_score, 1)

    if use_upi:
        upi_score = max(
            0,
            min(
                100,
                52
                + row["upi_growth_rate"] * 170
                + min(32, row["upi_monthly_value"] / 45000),
            ),
        )
        scores["UPI Strength"] = round(upi_score, 1)

    if use_gst:
        gst_score = max(
            0,
            min(
                100,
                row["gst_filing_consistency"] * 100
                + min(10, row["revenue_growth_rate"] * 20),
            ),
        )

        growth_score = max(
            0,
            min(
                100,
                55 + row["revenue_growth_rate"] * 180,
            ),
        )

        scores["GST Consistency"] = round(gst_score, 1)
        scores["Business Growth"] = round(growth_score, 1)

    if use_invoice:
        invoice_score = max(
            0,
            min(
                100,
                row["invoice_paid_ratio"] * 100,
            ),
        )
        scores["Invoice Reliability"] = round(invoice_score, 1)

    if use_epfo:
        payroll_score = max(
            0,
            min(
                100,
                row["payroll_regularity"] * 100
                + min(10, row["employee_count"] / 2),
            ),
        )
        scores["Payroll Stability"] = round(payroll_score, 1)

    if not scores:
        return {}, 0

    weights = {
        "Cash-flow Stability": 0.20,
        "Repayment Discipline": 0.20,
        "UPI Strength": 0.15,
        "GST Consistency": 0.15,
        "Business Growth": 0.10,
        "Invoice Reliability": 0.10,
        "Payroll Stability": 0.10,
    }

    active_weight = sum(weights[k] for k in scores)

    overall = sum(scores[k] * weights[k] for k in scores) / active_weight

    data_coverage_bonus = (len(scores) / 7) * 4
    overall = min(100, overall + data_coverage_bonus)

    return scores, round(overall, 1)


def decision_from_score(score, loan_amount, row):
    estimated_monthly_cash = max(1, row["gst_monthly_sales"] * 0.18)

    exposure_ratio = (
        loan_amount + row["existing_credit_exposure"]
    ) / max(1, row["gst_monthly_sales"] * 6)

    obligation_ratio = row["monthly_obligation"] / estimated_monthly_cash

    risk_penalty = 0

    if exposure_ratio > 0.55:
        risk_penalty += 8

    if obligation_ratio > 0.45:
        risk_penalty += 7

    adjusted_score = max(0, score - risk_penalty)

    if adjusted_score >= 76:
        return (
            "Approve",
            "Low Risk",
            adjusted_score,
            "Approve working capital loan with monthly portfolio monitoring.",
        )

    elif adjusted_score >= 58:
        return (
            "Manual Review",
            "Medium Risk",
            adjusted_score,
            "Request additional verification or offer a lower-ticket credit line.",
        )

    else:
        return (
            "Do Not Auto-Approve",
            "High Risk",
            adjusted_score,
            "Do not approve instantly. Monitor alternate data signals and reassess.",
        )


def parse_series(value):
    return [int(x) for x in str(value).split("|")]


def generate_repayment_details(row):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

    bounce_count = int(row["bounce_count_6m"])
    delay_days = int(row["repayment_delay_days"])

    events = []

    if bounce_count == 0 and delay_days == 0:
        return pd.DataFrame(
            [
                {
                    "Month": "All Months",
                    "Bounce Event": "No",
                    "Delay Days": 0,
                    "Observation": "Clean repayment behavior",
                }
            ]
        )

    flagged_months = months[-min(6, max(1, bounce_count + (1 if delay_days > 0 else 0))):]

    remaining_bounces = bounce_count
    remaining_delay = delay_days

    for m in months:
        if m in flagged_months:
            bounce = "Yes" if remaining_bounces > 0 else "No"

            if remaining_bounces > 0:
                remaining_bounces -= 1

            delay = min(remaining_delay, 7) if remaining_delay > 0 else 0
            remaining_delay = max(0, remaining_delay - delay)

            observations = []

            if bounce == "Yes":
                observations.append("EMI/repayment bounce recorded")

            if delay > 0:
                observations.append(f"Payment delayed by {delay} days")

            if not observations:
                observations.append("Minor repayment variation")

            events.append(
                {
                    "Month": m,
                    "Bounce Event": bounce,
                    "Delay Days": delay,
                    "Observation": "; ".join(observations),
                }
            )

        else:
            events.append(
                {
                    "Month": m,
                    "Bounce Event": "No",
                    "Delay Days": 0,
                    "Observation": "No adverse repayment event",
                }
            )

    return pd.DataFrame(events)


def generate_gst_details(row):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

    filing_score = float(row["gst_filing_consistency"])
    sales = parse_series(row["sales_series"])

    missed_or_late = max(0, round((1 - filing_score) * 6))
    flagged = months[-missed_or_late:] if missed_or_late > 0 else []

    output = []

    for i, m in enumerate(months):
        status = "Filed On Time"

        if m in flagged:
            status = "Filed Late" if i % 2 == 0 else "Return mismatch / irregularity"

        output.append(
            {
                "Month": m,
                "GST-like Sales": sales[i],
                "Filing Status": status,
            }
        )

    return pd.DataFrame(output)


def generate_growth_details(row):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

    sales = parse_series(row["sales_series"])

    data = []
    previous = None

    for m, sales_value in zip(months, sales):
        if previous is None:
            mom_growth = 0.0
        else:
            mom_growth = ((sales_value - previous) / previous) * 100 if previous else 0.0

        data.append(
            {
                "Month": m,
                "GST-like Sales": sales_value,
                "MoM Growth %": round(mom_growth, 1),
            }
        )

        previous = sales_value

    return pd.DataFrame(data)


df = load_data()

st.markdown(
    """
<div class="main-header">
    <h1>CrediLens MSME</h1>
    <p>Interactive AI Financial Health Card for NTC/NTB MSME Credit Decisioning</p>
</div>
""",
    unsafe_allow_html=True,
)

st.caption(
    "POC uses synthetic data to simulate GST, UPI, AA, EPFO, invoice and repayment signals."
)

tabs = st.tabs(
    [
        "1. Officer Workflow",
        "2. Financial Health Card",
        "3. Alternate Data Explorer",
        "4. Loan Decision Simulator",
        "5. Ecosystem Flow",
    ]
)

with st.sidebar:
    st.header("Bank Officer Console")

    selected_business = st.selectbox(
        "Select MSME Applicant",
        df["business_name"].tolist(),
    )

    row = df[df["business_name"] == selected_business].iloc[0]

    st.markdown("### Consent-Based Data Access")

    use_aa = st.toggle("AA Bank Transactions", value=True)
    use_gst = st.toggle("GST Data", value=True)
    use_upi = st.toggle("UPI Data", value=True)
    use_epfo = st.toggle("EPFO / Payroll", value=True)
    use_invoice = st.toggle("Invoice Data", value=True)

    st.markdown("### Loan Request")

    loan_amount = st.slider(
        "Requested Loan Amount",
        50000,
        2000000,
        500000,
        step=50000,
    )

    tenure = st.slider(
        "Tenure in Months",
        3,
        36,
        12,
        step=3,
    )


scores, overall_score = calculate_scores(
    row,
    use_gst,
    use_upi,
    use_aa,
    use_epfo,
    use_invoice,
)

decision, risk_category, adjusted_score, recommendation = decision_from_score(
    overall_score,
    loan_amount,
    row,
)


with tabs[0]:
    st.subheader("End-to-End Reviewer-Friendly Workflow")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.info("1. MSME applies")
    c2.info("2. Consent captured")
    c3.info("3. Alternate data fetched")
    c4.info("4. AI health score generated")
    c5.info("5. Credit action recommended")

    st.markdown("### Applicant Snapshot")

    a, b, c, d = st.columns(4)

    a.metric("Business", row["business_name"])
    b.metric("Sector", row["sector"])
    c.metric("City", row["city"])
    d.metric("Vintage", f"{row['business_vintage_years']} yrs")

    st.markdown("### Live Decision Summary")

    k1, k2, k3 = st.columns(3)

    k1.metric("Financial Health Score", f"{overall_score}/100")
    k2.metric("Adjusted Loan Score", f"{round(adjusted_score, 1)}/100")
    k3.metric("Risk Category", risk_category)

    if decision == "Approve":
        st.markdown(
            f'<div class="decision-approve">Decision: {decision} — {recommendation}</div>',
            unsafe_allow_html=True,
        )

    elif decision == "Manual Review":
        st.markdown(
            f'<div class="decision-review">Decision: {decision} — {recommendation}</div>',
            unsafe_allow_html=True,
        )

    else:
        st.markdown(
            f'<div class="decision-reject">Decision: {decision} — {recommendation}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("### How reviewers should test this")

    st.write(
        """
        Use the left sidebar to select different MSMEs, toggle available consent-based data sources,
        and change the requested loan amount. The score, risk category, and decision will update instantly.
        """
    )


with tabs[1]:
    st.subheader("MSME Financial Health Card")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Overall Score", f"{overall_score}/100")
    m2.metric("Credit Decision", decision)
    m3.metric("Risk", risk_category)
    m4.metric("Requested Loan", f"₹{loan_amount:,.0f}")

    if scores:
        score_df = pd.DataFrame(
            {
                "Dimension": list(scores.keys()),
                "Score": [round(v, 1) for v in scores.values()],
            }
        )

        col_a, col_b = st.columns([1, 1])

        with col_a:
            fig = px.bar(
                score_df,
                x="Score",
                y="Dimension",
                orientation="h",
                range_x=[0, 100],
                title="Score Breakdown",
            )

            st.plotly_chart(fig, use_container_width=True)

        with col_b:
            fig_radar = go.Figure()

            fig_radar.add_trace(
                go.Scatterpolar(
                    r=score_df["Score"].tolist(),
                    theta=score_df["Dimension"].tolist(),
                    fill="toself",
                    name="MSME Score",
                )
            )

            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                title="Risk Radar",
            )

            st.plotly_chart(fig_radar, use_container_width=True)

        strengths = []
        risks = []

        for dim, score in scores.items():
            if score >= 75:
                strengths.append((dim, "strong signal supports credit confidence."))

            elif score >= 55:
                risks.append((dim, "moderate signal; may need monitoring."))

            else:
                risks.append((dim, "weak signal; requires verification."))

        s1, s2 = st.columns(2)

        with s1:
            st.success("Key Strengths")

            if strengths:
                for dim, message in strengths:
                    st.write(f"✅ **{dim}**: {message}")

            else:
                st.write("No strong signals available based on selected consent sources.")

        with s2:
            st.warning("Risks / Watchpoints")

            if risks:
                for dim, message in risks:
                    st.markdown(
                        f'<div class="risk-tag">⚠️ {dim}: {message}</div>',
                        unsafe_allow_html=True,
                    )

                    if dim == "GST Consistency":
                        with st.expander("More info: GST / compliance details"):
                            gst_df = generate_gst_details(row)

                            st.dataframe(gst_df, use_container_width=True)

                            fig_gst = px.bar(
                                gst_df,
                                x="Month",
                                y="GST-like Sales",
                                color="Filing Status",
                                title="Monthly GST-like Sales and Filing Status",
                            )

                            st.plotly_chart(fig_gst, use_container_width=True)

                    elif dim == "Repayment Discipline":
                        with st.expander("More info: repayment bounce / delay details"):
                            repayment_df = generate_repayment_details(row)

                            st.dataframe(repayment_df, use_container_width=True)

                    elif dim == "Business Growth":
                        with st.expander("More info: monthly growth details"):
                            growth_df = generate_growth_details(row)

                            st.dataframe(growth_df, use_container_width=True)

                            fig_growth = px.line(
                                growth_df,
                                x="Month",
                                y="GST-like Sales",
                                markers=True,
                                title="Monthly Business Sales Trend",
                            )

                            st.plotly_chart(fig_growth, use_container_width=True)

                    elif dim == "Cash-flow Stability":
                        with st.expander("More info: bank balance trend"):
                            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

                            balance_df = pd.DataFrame(
                                {
                                    "Month": months,
                                    "Average Balance": parse_series(row["balance_series"]),
                                }
                            )

                            st.dataframe(balance_df, use_container_width=True)

                            fig_balance = px.line(
                                balance_df,
                                x="Month",
                                y="Average Balance",
                                markers=True,
                                title="Average Balance Trend",
                            )

                            st.plotly_chart(fig_balance, use_container_width=True)

                    elif dim == "UPI Strength":
                        with st.expander("More info: UPI collection trend"):
                            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

                            upi_df = pd.DataFrame(
                                {
                                    "Month": months,
                                    "UPI Collections": parse_series(row["upi_series"]),
                                }
                            )

                            st.dataframe(upi_df, use_container_width=True)

                            fig_upi = px.line(
                                upi_df,
                                x="Month",
                                y="UPI Collections",
                                markers=True,
                                title="UPI Collection Trend",
                            )

                            st.plotly_chart(fig_upi, use_container_width=True)

                    elif dim == "Payroll Stability":
                        with st.expander("More info: payroll details"):
                            payroll_df = pd.DataFrame(
                                [
                                    {
                                        "Employee Count": int(row["employee_count"]),
                                        "Payroll Regularity %": round(
                                            row["payroll_regularity"] * 100,
                                            1,
                                        ),
                                        "Estimated Monthly Obligation": int(
                                            row["monthly_obligation"]
                                        ),
                                    }
                                ]
                            )

                            st.dataframe(payroll_df, use_container_width=True)

                    elif dim == "Invoice Reliability":
                        with st.expander("More info: invoice payment details"):
                            invoice_df = pd.DataFrame(
                                [
                                    {
                                        "Invoice Paid Ratio %": round(
                                            row["invoice_paid_ratio"] * 100,
                                            1,
                                        ),
                                        "Collection Strength": "Good"
                                        if row["invoice_paid_ratio"] >= 0.75
                                        else "Moderate / Weak",
                                    }
                                ]
                            )

                            st.dataframe(invoice_df, use_container_width=True)

            else:
                st.write("No major risk watchpoints identified.")

    else:
        st.error("No data source selected. Enable at least one consent source from the sidebar.")


with tabs[2]:
    st.subheader("Alternate Data Explorer")

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

    sales = parse_series(row["sales_series"])
    upi = parse_series(row["upi_series"])
    balances = parse_series(row["balance_series"])

    trend_df = pd.DataFrame(
        {
            "Month": months,
            "GST-like Sales": sales,
            "UPI Collections": upi,
            "Average Bank Balance": balances,
        }
    )

    fig_line = px.line(
        trend_df,
        x="Month",
        y=["GST-like Sales", "UPI Collections", "Average Bank Balance"],
        markers=True,
        title="Six-Month Alternate Data Trend",
    )

    st.plotly_chart(fig_line, use_container_width=True)

    c1, c2, c3 = st.columns(3)

    c1.metric("GST Filing Consistency", f"{row['gst_filing_consistency'] * 100:.1f}%")
    c2.metric("Invoice Paid Ratio", f"{row['invoice_paid_ratio'] * 100:.1f}%")
    c3.metric("Payroll Regularity", f"{row['payroll_regularity'] * 100:.1f}%")

    st.dataframe(trend_df, use_container_width=True)


with tabs[3]:
    st.subheader("Loan Decision Simulator")

    st.write(
        """
        This screen shows how the same MSME score changes based on loan amount,
        existing exposure, obligations, and available alternate data.
        """
    )

    simulator_df = []

    for amount in [100000, 250000, 500000, 750000, 1000000, 1500000, 2000000]:
        d, r, adj, rec = decision_from_score(overall_score, amount, row)

        simulator_df.append(
            {
                "Loan Amount": amount,
                "Adjusted Score": round(adj, 1),
                "Decision": d,
                "Risk": r,
            }
        )

    simulator_df = pd.DataFrame(simulator_df)

    fig = px.line(
        simulator_df,
        x="Loan Amount",
        y="Adjusted Score",
        markers=True,
        title="Loan Amount vs Adjusted Score",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(simulator_df, use_container_width=True)

    st.markdown("### Current Recommended Action")
    st.info(recommendation)


with tabs[4]:
    st.subheader("Integration-Ready Ecosystem Flow")

    st.markdown(
        """
        This POC does not connect to real banking APIs. It simulates how the production solution
        would fit into India's digital lending ecosystem.
        """
    )

    f1, f2, f3, f4 = st.columns(4)

    f1.success("AA Consent")
    f2.success("GST / UPI / EPFO Signals")
    f3.success("AI Health Score")
    f4.success("OCEN / ULI Credit Flow")

    st.markdown(
        """
        **Production integration concept:**

        1. MSME gives consent through Account Aggregator.
        2. Data is fetched from bank statements, GST, UPI, invoice and payroll systems.
        3. CrediLens scoring engine computes a multidimensional health score.
        4. Explainability module shows strengths and risks.
        5. Bank officer or digital lending journey receives approve/manual review/monitor recommendation.
        6. OCEN/ULI-ready APIs can support digital credit journeys at scale.
        """
    )

    st.code(
        """
MSME Consent → AA / ULI Data Access → Alternate Data Aggregation
→ AI/ML Scoring Engine → Financial Health Card
→ Credit Decision API → Bank Officer / OCEN Lending Journey
"""
    )
