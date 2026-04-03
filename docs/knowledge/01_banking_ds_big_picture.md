# Banking Decision Systems — Big Picture

## Objective

This project builds end-to-end banking decision systems that translate data into business decisions.

Primary goal:

Approve loans while balancing risk and growth.


## Core Problem

Given a loan applicant:

- What is their risk of default?
- Should we approve, review, or reject?

This is not just a modeling problem — it is a decision system.


## End-to-End System

Applicant Data  
→ Feature Engineering  
→ Risk Model (PD)  
→ Decision Policy  
→ Business Outcome  


## System Layers

### 1. Prediction Layer (Model)

- Estimate probability of default (PD)
- Example: Logistic Regression

Output:
Probability between 0 and 1


### 2. Decision Layer (Policy)

Convert prediction into action:

- Approve  
- Review  
- Reject  

Based on risk thresholds


### 3. Evaluation Layer

Measure both model and business impact:

- AUC (model quality)
- Approval rate (growth)
- Default rate (risk)
- Calibration (probability reliability)


## Example: Credit Approval

Input → borrower features  

→ Model predicts:
PD = 0.12  

→ Decision:
Approve  

→ Outcome:
Loan issued → profit or loss depending on repayment  


## Core Tradeoff

Risk vs Growth

- Too strict → lose customers  
- Too lenient → increase defaults  


## Key Insight

Machine learning does not create value by itself.

Value is created when predictions are translated into decisions.


## What This Project Builds

- Simulated borrower data  
- Risk estimation (PD)  
- Decision policies  
- Business evaluation metrics  


## Interview Framing

“We separate prediction, decision, and evaluation. The model estimates probability of default, and business rules convert that into actionable decisions while controlling risk and growth.”