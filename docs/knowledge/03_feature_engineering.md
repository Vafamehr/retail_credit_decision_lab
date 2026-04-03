# Feature Engineering — From Raw Data to Risk Signals

## Objective

Transform raw borrower data into meaningful signals that help estimate credit risk.

Feature engineering is not about creating many features — it is about creating the right signals.


## Why Feature Engineering Matters

Models do not understand raw data.

They learn from:

- relationships  
- patterns  
- signals  

Good features make risk patterns easier to learn.


## Core Principle

We transform raw variables into representations that better capture risk behavior.


## Features Created

### 1. Loan to Income Ratio

Definition:

loan_to_income = loan_amount / annual_income

Purpose:

- measures financial burden  
- captures ability to repay  

Risk Insight:

Higher loan-to-income → higher probability of default


### 2. Credit Score Bucket

Definition:

- low (300–580)  
- medium (580–670)  
- high (670–850)  

Purpose:

- captures non-linear risk behavior  
- avoids assuming linear relationships  

Risk Insight:

- low score → high risk  
- high score → low risk  


### 3. High Utilization Flag

Definition:

credit_utilization > 0.7

Purpose:

- identifies borrowers using most of their available credit  

Risk Insight:

High utilization → financial stress → higher default risk


### 4. Delinquency Flag

Definition:

num_delinquencies > 0

Purpose:

- captures past missed payments  

Risk Insight:

Past delinquency is a strong predictor of default


### 5. Employment Stability

Definition:

employment_years < 2

Purpose:

- measures income stability  

Risk Insight:

Short employment history → higher uncertainty → higher risk


## Design Philosophy

- Keep features simple and interpretable  
- Focus on domain-relevant signals  
- Capture non-linear effects through transformations  
- Avoid unnecessary complexity  


## What We Avoided

- excessive feature creation  
- complex transformations with low interpretability  
- overfitting to synthetic data  


## Mental Model

Raw Data  
→ Derived Risk Signals  
→ Model Input  


## Interview Framing

“Feature engineering focuses on transforming borrower attributes into interpretable risk signals such as financial burden, credit behavior, and stability. We also capture non-linear effects using transformations like buckets and flags, making patterns easier for the model to learn.”