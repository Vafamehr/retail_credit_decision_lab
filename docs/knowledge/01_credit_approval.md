# Module 01 — Credit Approval (Risk Decision System)

## 1. Problem Definition

In lending systems, the core question is:

Should we approve this customer for a loan?

This is a risk decision problem where the objective is to control default risk while maintaining approval volume.

---

## 2. Business Context

Banks operate under a clear trade-off:

- higher approval rate → more revenue but higher risk  
- lower approval rate → safer portfolio but reduced volume  

The goal is to find a balance that satisfies risk constraints while maximizing approvals.

---

## 3. System Overview

This module implements a full credit decision pipeline:

Data → Features → Risk Model → Threshold Optimization → Decision Policy → Evaluation

---

## 4. Data Generation

A synthetic borrower population is created with realistic features:

- income  
- credit score  
- loan amount  
- debt-to-income ratio (DTI)  
- credit utilization  
- delinquencies  
- employment history  

### Risk Construction

Default risk is generated using:

- linear effects (credit score, DTI, utilization)  
- interaction effects (DTI × utilization)  
- threshold effects (low credit score penalty)  
- extreme risk spikes  

The final probability is produced using a sigmoid transformation and converted to a binary default outcome.

---

## 5. Feature Engineering

Engineered features include:

- loan-to-income ratio  
- high utilization indicator  
- delinquency indicator  
- employment stability  
- interaction terms  

These features reflect common patterns used in real credit risk modeling.

---

## 6. Risk Model

Model:

Logistic Regression

Purpose:

Estimate probability of default (PD)

Output:

predicted_risk ∈ [0,1]

---

## 7. Decision Layer

Predictions are converted into decisions using thresholding.

### Threshold Optimization

A threshold is selected such that:

Default Rate (Approved) ≤ 15%

While maximizing:

Approval Rate

This enforces a portfolio-level risk constraint rather than relying on arbitrary cutoffs.

---

## 8. Decision Policy

Customers are segmented into:

- Approve → low risk  
- Reject → high risk  
- Review → borderline cases  

This reflects standard underwriting workflows.

---

## 9. Evaluation

### Approval Metrics

- approval rate  
- default rate among approved customers  

---

### Calibration

Compare predicted risk vs actual default rate across bins to ensure probabilities are reliable.

---

## 10. Outputs

- customer-level decisions  
- predicted risk scores  
- calibration tables  
- trained model and preprocessing artifacts  

Stored in:

artifacts/credit_approval/

---

## 11. Key Insight

Prediction is not the end goal.

The system converts risk estimates into controlled decisions under business constraints.

---

## 12. Limitations

- synthetic data  
- simple model (logistic regression)  
- static threshold  
- no pricing or profitability layer  

---

## 13. Interview Summary

Built a credit approval system that estimates default probability and converts it into decisions using threshold optimization under a risk constraint, with evaluation focused on approval rate, default control, and calibration.

---

## Final Takeaway

This module focuses on turning risk predictions into controlled, constraint-driven decisions.