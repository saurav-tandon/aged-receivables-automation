# 🚀 Aged Receivables Automation (Chargebee + Xero)

## 💼 Business Problem

In SaaS finance operations, analyzing aged receivables is often a **manual and time-consuming task**.

Finance teams typically:

* Review hundreds of invoices manually
* Identify overdue balances across systems
* Track credit notes affecting invoice amounts
* Cross-check subscription status from billing tools
* Prepare AR reports for leadership

This leads to:

* ❌ Missed overdue invoices
* ❌ Inaccurate outstanding balances
* ❌ Delayed reporting
* ❌ High manual effort (3–4+ hours daily)

---

## ✅ Solution

This project automates the **Aged Receivables Analysis** by combining:

* **Xero AR Aging Reports**
* **Chargebee Billing Data**
* **Python-based processing**

It generates a **clean, structured AR report** with:

* Aging buckets
* Subscription status
* Payment insights

---

## ⚙️ How It Works

```text
Xero AR Aging Report
        │
        ▼
Python Processing Script
        │
        ▼
Chargebee API (Invoice + Subscription Data)
        │
        ▼
Data Enrichment + Classification
        │
        ▼
Automated AR Aging Report
```

---

## 🔑 Key Features

* Automated aging bucket classification
* Chargebee API integration
* Invoice + credit note handling
* Subscription status enrichment
* Parallel API calls for faster processing
* Retry logic for API failures
* Clean structured output (Excel/CSV)

---

## 📊 Aging Buckets Logic

| Days Overdue | Category      |
| ------------ | ------------- |
| 0–30         | Current       |
| 31–60        | Moderate Risk |
| 61–90        | High Risk     |
| 90+          | Critical      |

---

## 📄 Sample Output

| Invoice ID | Customer  | Amount | Days Overdue | Aging Bucket  |
| ---------- | --------- | ------ | ------------ | ------------- |
| INV001     | ABC Ltd   | €1200  | 15           | Current       |
| INV002     | XYZ Ltd   | €980   | 45           | Moderate Risk |
| INV003     | Demo Corp | €450   | 95           | Critical      |

---

## 🛠 Tech Stack

* Python
* Pandas
* Chargebee API
* Excel / CSV Processing
* Multithreading (ThreadPoolExecutor)

---

## 📁 Project Structure

```text
aged-receivables-automation/
│── main.py
│── config.py
│── chargebee_client.py
│
├── sample_data/
│   └── invoices_sample.csv
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ▶️ How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create `.env` file

```env
ENTITY1_CB_SITE=your_site
ENTITY1_CB_API_KEY=your_api_key

ENTITY2_CB_SITE=your_site
ENTITY2_CB_API_KEY=your_api_key
```

### 3. Run script

```bash
python main.py
```

---

## 📈 Impact

* ⏱ Reduced manual AR analysis from **3–4 hours → ~10 minutes**
* 📊 Processes **hundreds of invoices automatically**
* 🎯 Improves accuracy and visibility of overdue receivables
* ⚡ Enables faster decision-making for finance teams

---

## 🔐 Security & Confidentiality

All data in this project is **anonymized**.

This repository demonstrates **real-world SaaS finance automation workflows** without exposing sensitive business data.

---

## 👨‍💼 About Me

**Saurav Tandon**
SaaS Finance Automation Specialist (Chargebee | Xero | AR Reconciliation)

* 10+ years in SaaS finance (Chargebee, Xero)
* Expertise in invoice reconciliation & AR automation
* Built real-world automation handling 300+ invoices/day

📫 Email: [Lect.Saurav@gmail.com](mailto:Lect.Saurav@gmail.com)
