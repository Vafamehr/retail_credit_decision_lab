# Feature Engineering — From Raw Data to Risk Signals

## Objective
Transform raw borrower data into meaningful signals that help estimate credit risk.

Feature engineering is not about creating many features — it is about creating the right signals.

---

## Why Feature Engineering Matters

Models do not understand raw data.

They learn from:

- relationships  
- patterns  
- signals  

Good features make risk patterns easier to learn.

---

## Core Principle

We transform raw variables into representations that better capture risk.

---

## Features Created

### 1. Loan to Income Ratio

Definition:

loan_to_income = loan_amount / annual_income

Purpose:

- measures how large the loan is relative to income  
- higher values indicate higher financial burden  

Risk Insight:

Higher loan-to-income → higher probability of default

---

### 2. Credit Score Bucket

Definition:

- low (300–580)  
- medium (580–670)  
- high (670–850)  

Purpose:

- captures non-linear risk behavior  
- avoids assuming linear relationship  

Risk Insight:

- low score → high risk  
- high score → low risk  

---

### 3. High Utilization Flag

Definition:

credit_utilization > 0.7

Purpose:

- identifies borrowers using most of their credit  

Risk Insight:

High utilization → financial stress → higher default risk

---

### 4. Delinquency Flag

Definition:

num_delinquencies > 0

Purpose:

- captures history of missed payments  

Risk Insight:

Past delinquency is one of the strongest predictors of default

---

### 5. Employment Stability

Definition:

employment_years < 2

Purpose:

- measures stability of income  

Risk Insight:

Short employment history → higher uncertainty → higher risk

---

## Design Philosophy

- Keep features simple and interpretable  
- Focus on domain-relevant signals  
- Avoid unnecessary complexity  

---

## What We Avoided

- complex transformations  
- scaling and normalization (not needed for trees)  
- excessive feature creation  

---

## Mental Model

Raw Data  
→ Derived Signals  
→ Risk Estimation  

---

## Interview Framing

“Feature engineering focuses on transforming raw borrower attributes into risk-relevant signals such as loan burden, credit behavior, and financial stability. The goal is to make patterns easier for the model to learn while keeping features interpretable.”