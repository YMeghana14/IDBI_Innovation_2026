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

## App Walkthrough

This is not final app or final demo its just a mock interface on how the solution can be if developed like a prototype

## App Link - https://aihealthcard.streamlit.app/

CrediLens MSME is designed as an interactive bank officer workflow for evaluating New-to-Credit (NTC) and New-to-Bank (NTB) MSMEs using alternate data signals. The app demonstrates how a bank can move from consent-based data access to financial health scoring, risk explanation, and credit decisioning.

### 1. Bank Officer Console

The left sidebar acts as the main control panel for the bank officer.

From here, the officer can:

* Select an MSME applicant
* Enable or disable consent-based data sources
* Adjust the requested loan amount
* Change the loan tenure

The score and recommendation update dynamically whenever the officer changes the data availability or loan amount. This simulates a real-world scenario where not all MSMEs may provide every data source, and the bank must still make a reliable decision using available signals.

### 2. Consent-Based Data Access

The app includes toggles for different alternate data sources:

**AA Bank Transactions**
Simulates consent-based bank transaction data available through the Account Aggregator ecosystem. This helps evaluate cash-flow stability, balance behavior, repayment discipline, bounce history, and transaction patterns.

**GST Data**
Simulates GST sales and filing behavior. This helps understand business turnover, compliance consistency, and sales growth trends.

**UPI Data**
Simulates digital payment activity. This is useful for MSMEs that receive payments through UPI and other digital channels but may not have formal financial documents.

**EPFO / Payroll Data**
Simulates employee and payroll consistency. This gives an indication of business stability, operational continuity, and employment strength.

**Invoice Data**
Simulates invoice collection behavior. This helps identify whether the MSME receives payments on time from customers or business partners.

### 3. Officer Workflow Page

This page shows the complete journey from MSME application to credit recommendation.

The workflow is:

MSME applies → Consent is captured → Alternate data is fetched → AI health score is generated → Credit action is recommended

This page is useful for quickly understanding the end-to-end purpose of the solution. It also shows the selected MSME’s business details, overall score, adjusted loan score, risk category, and final recommendation.

### 4. Financial Health Card Page

This is the main page of the app.

It shows the MSME’s financial health in a report-card format.

The page includes:

* Overall Financial Health Score
* Credit Decision
* Risk Category
* Requested Loan Amount
* Score Breakdown
* Risk Radar
* Key Strengths
* Risks / Watchpoints
* Detailed risk drill-downs

The score breakdown shows how the MSME performs across dimensions such as cash-flow stability, repayment discipline, UPI strength, GST consistency, business growth, invoice reliability, and payroll stability.

The risk radar gives a visual view of the MSME’s strengths and weak areas.

### 5. Risks / Watchpoints Drill-Down

Each risk or watchpoint includes a “More info” section.

This allows the reviewer to see the actual evidence behind the risk instead of only seeing a generic warning.

Examples:

**GST / Compliance Risk**
Shows month-wise GST-like sales and filing status. If GST consistency is weak, the reviewer can see which months had late filing, irregularity, or mismatch.

**Repayment Discipline Risk**
Shows month-wise repayment behavior, bounce events, delay days, and observations. This helps the bank understand whether repayment issues are occasional or repeated.

**Business Growth Risk**
Shows monthly sales trend and month-on-month growth percentage. This helps identify whether the business is growing, flat, or declining.

**Cash-flow Stability Risk**
Shows average bank balance trend across months. This helps assess whether the MSME has enough liquidity to manage loan repayments.

**UPI Strength Risk**
Shows monthly UPI collection trend. This helps understand digital business activity and payment inflow consistency.

**Payroll Stability Risk**
Shows employee count, payroll regularity, and monthly obligation. This helps understand operational stability.

**Invoice Reliability Risk**
Shows invoice payment ratio and collection strength. This helps understand whether the MSME receives customer payments on time.

### 6. Alternate Data Explorer Page

This page provides a deeper view of the MSME’s alternate data trends.

It displays six-month trends for:

* GST-like sales
* UPI collections
* Average bank balance

It also shows metrics such as GST filing consistency, invoice paid ratio, and payroll regularity.

This page helps reviewers understand how the Financial Health Card is backed by data, not just a static score.

### 7. Loan Decision Simulator Page

This page shows how the credit decision changes when the requested loan amount changes.

For example, the same MSME may be safe for a ₹2 lakh loan but may require manual review for a ₹15 lakh loan.

The simulator displays:

* Loan amount
* Adjusted score
* Decision
* Risk category

This makes the app more realistic because creditworthiness depends not only on the MSME’s health score but also on the requested exposure amount and repayment capacity.

### 8. Ecosystem Flow Page

This page explains how the POC can fit into India’s digital lending ecosystem.

The POC does not connect to real APIs, but it is designed to be integration-ready for:

**Account Aggregator (AA)**
For consent-based financial data sharing.

**ULI**
For standardized borrower data access and lending-related data exchange.

**OCEN**
For enabling digital credit journeys between lenders, loan service providers, and MSME platforms.

The ecosystem flow is:

MSME Consent → AA / ULI Data Access → Alternate Data Aggregation → AI/ML Scoring Engine → Financial Health Card → Credit Decision API → Bank Officer / OCEN Lending Journey

### 9. Key Terms Used in the App

**MSME**
Micro, Small, and Medium Enterprise. These are small businesses such as traders, shops, manufacturers, service providers, and local enterprises.

**NTC — New-to-Credit**
A business that has not taken formal credit before and therefore may not have a strong credit history.

**NTB — New-to-Bank**
A business that is new to a specific bank and does not yet have an established relationship with that bank.

**Alternate Data**
Non-traditional financial data such as UPI transactions, GST activity, bank transaction behavior, invoice payments, payroll data, and digital payment activity.

**Financial Health Score**
A score from 0 to 100 that represents the overall financial strength of the MSME based on multiple alternate data signals.

**Risk Category**
A classification such as Low Risk, Medium Risk, or High Risk based on the financial health score and loan request.

**Credit Readiness**
An indication of whether the MSME appears suitable for credit approval, manual review, additional verification, or monitoring.

**Adjusted Loan Score**
A modified score that considers the requested loan amount, existing exposure, and monthly obligations.

**Risk Radar**
A visual chart that shows the MSME’s strength across different financial dimensions.

**Watchpoints**
Specific risk indicators that the bank should monitor before approving credit.

### 10. Why This POC Matters

This POC shows how banks can evaluate credit-invisible MSMEs more fairly and quickly by using alternate data instead of relying only on traditional documents.

The solution can help banks:

* Reduce rejection of viable MSMEs
* Improve financial inclusion
* Speed up digital lending decisions
* Support New-to-Credit and New-to-Bank borrowers
* Improve portfolio quality
* Make credit decisions more explainable
* Reduce manual evaluation effort
