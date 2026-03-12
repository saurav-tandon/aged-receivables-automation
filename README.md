# Aged Receivables Automation (Chargebee + Xero)

## Overview

This project automates the analysis of aged receivables for a SaaS
company by processing invoice data and identifying overdue balances. The
script helps finance teams quickly identify outstanding invoices and
categorize them into aging buckets (0--30, 31--60, 61--90, 90+ days).

The automation reduces manual effort previously required to check
hundreds of invoices across billing and accounting systems.

------------------------------------------------------------------------

## Business Problem

In SaaS finance operations, reviewing aged receivables manually can be
time‑consuming.\
Finance teams often need to:

-   Check hundreds of invoices individually
-   Identify overdue balances
-   Track credit notes affecting invoice balances
-   Prepare aging reports for finance leadership

Manual processes increase the risk of: - Missed overdue invoices -
Incorrect outstanding balances - Time lost on repetitive checks

------------------------------------------------------------------------

## Solution

This automation script processes invoice data and generates an aged
receivables report automatically.

The workflow:

1.  Load invoice data
2.  Adjust balances based on credit notes
3.  Calculate overdue days
4.  Classify invoices into aging buckets
5.  Generate a structured AR report

------------------------------------------------------------------------

## Key Features

-   Automated aging bucket classification
-   Outstanding balance calculation
-   Credit note adjustment support
-   Bulk invoice processing
-   Structured report generation

------------------------------------------------------------------------

## Aging Buckets

  Days Overdue   Category
  -------------- ---------------
  0--30 days     Current
  31--60 days    Moderate Risk
  61--90 days    High Risk
  90+ days       Critical

------------------------------------------------------------------------

## Example Output

  Invoice ID   Customer    Amount   Days Overdue   Aging Bucket
  ------------ ----------- -------- -------------- --------------
  INV001       ABC Ltd     €1200    15             0‑30
  INV002       XYZ Ltd     €980     45             31‑60
  INV003       Demo Corp   €450     95             90+

------------------------------------------------------------------------

## Tech Stack

-   Python
-   Pandas
-   REST API integration
-   CSV / Excel reporting

------------------------------------------------------------------------

## Project Structure

    aged-receivables-automation
    │
    ├── main.py
    ├── config.py
    ├── calculate_aging.py
    │
    ├── sample_data
    │   └── invoices_sample.csv
    │
    ├── output
    │   └── aged_receivables_report.csv
    │
    ├── README.md
    └── requirements.txt

------------------------------------------------------------------------

## Impact

-   Reduced manual AR analysis time significantly
-   Automated processing of hundreds of invoices
-   Improved visibility of overdue receivables

------------------------------------------------------------------------

## Author

Saurav Tandon\
Accounts Receivable & Revenue Operations Specialist\
10+ years experience in SaaS finance operations

Note:
All company names, identifiers, and billing data used in this repository have been anonymized.
This project demonstrates automation techniques for SaaS finance workflows.
