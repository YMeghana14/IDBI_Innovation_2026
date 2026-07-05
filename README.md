# CrediLens MSME

## AI-Powered Financial Health Card for Credit-Invisible MSMEs

CrediLens MSME is a Proof of Concept built for Track 03: Financial Inclusion, Digital Lending, and Credit Decisioning.

The solution creates an AI-powered Financial Health Card for New-to-Credit and New-to-Bank MSMEs using alternate data signals such as GST-like sales, UPI transactions, Account Aggregator-style bank statement signals, EPFO-like payroll consistency, invoice behavior, repayment discipline, and cash-flow trends.

## Problem

Many viable MSMEs are rejected by banks because they lack traditional credit documents such as audited financial statements, detailed balance sheets, or strong credit history. However, these MSMEs may still show strong business activity through digital transactions, GST activity, UPI payments, payroll patterns, and invoice behavior.

## Solution

CrediLens MSME converts alternate business signals into a unified, explainable Financial Health Card.

The dashboard provides:

- Overall Financial Health Score
- Risk Category
- Credit Readiness
- Score Breakdown
- Strengths and Risks
- Recommended Credit Action
- Ecosystem readiness for AA, ULI, and OCEN flows

## POC Features

- Synthetic MSME alternate data
- Financial health scoring engine
- Multidimensional score breakdown
- Explainable AI-style insights
- Interactive Streamlit dashboard
- Bank-officer style decision view

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- Synthetic MSME dataset

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Data Sources Simulated

- GST-like data
- UPI transaction data
- Account Aggregator-style bank statement data
- EPFO-like payroll data
- Invoice and repayment behavior

## Future Scope

- Real AA integration with consent-based financial data
- ULI API integration for standardized borrower information access
- OCEN-based digital credit flow integration
- Advanced ML models with SHAP explainability
- Portfolio-level MSME risk analytics