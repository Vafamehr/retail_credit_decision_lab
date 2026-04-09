# Module 01 — Credit Approval (Risk Decision System)

## 1. Problem Definition

In lending systems, the core question is:

Should we approve this customer for a loan?

This is a risk decision problem where the goal is to control default risk while maintaining approval volume.

---

## 2. Business Context

Banks operate under a trade-off:

- higher approval rate -> more revenue, higher risk  
- lower approval rate -> safer portfolio, lower volume  

The objective is not to eliminate risk, but to control it within acceptable limits.

---

## 3. System Overview

This module builds the risk layer of the system:

Data -> Features -> Risk Model -> Threshold Optimization -> Decision

This is the foundation for everything downstream.

---

## 4. Data Generation

A synthetic borrower population is created with realistic attributes:

- income  
- credit score  
- loan amount  
- debt-to-income ratio (DTI)  
- credit utilization  
- delinquencies  
- employment history  

### Risk Construction

Default probability is generated using:

- linear effects -> credit score, DTI, utilization  
- interaction effects -> DTI × utilization  
- threshold effects -> penalties for low credit score  
- extreme risk spikes -> high-risk segments  

The final probability is passed through a sigmoid and converted into a binary default outcome.

---

## 5. Feature Engineering

Derived features include:

- loan-to-income ratio  
- high utilization indicator  
- delinquency indicator  
- employment stability  
- interaction terms  

These reflect common signals used in real underwriting systems.

---

## 6. Risk Model

Model:

Logistic Regression

Purpose:

Estimate probability of default (PD)

Output:

predicted_risk ∈ [0, 1]

This output is not a decision — it is an input to the decision layer.

---

## 7. Decision Layer

Predictions are converted into actions using thresholding.

### Threshold Optimization

The threshold is chosen such that:

Default Rate (Approved) ≤ 15%

While maximizing:

Approval Rate

This enforces a portfolio-level constraint instead of relying on arbitrary cutoffs.

---

## 8. Decision Policy

Customers are segmented into:

- Approve -> low risk  
- Reject -> high risk  
- Review -> borderline cases  

This mirrors real underwriting workflows.

---

## 9. Evaluation

### Approval Metrics

- approval rate  
- default rate among approved customers  

---

### Calibration

Predicted risk is compared with actual default rates across bins.

This ensures the model’s probabilities are usable for downstream decisions.

---

## 10. Outputs

- customer-level decisions  
- predicted risk scores  
- calibration tables  
- trained model artifacts  

Stored in:

artifacts/credit_approval/

---

## 11. Key Insight

This module does not maximize accuracy.

It converts risk estimates into controlled decisions under a business constraint.

---

## 12. Limitations

- synthetic data  
- simple model (logistic regression)  
- static threshold  
- no pricing or profitability integration  

---

## 13. Interview Summary

Built a credit approval system that estimates default probability and converts it into decisions using threshold optimization under a risk constraint, balancing approval rate and portfolio risk while ensuring calibration.

---

## Final Takeaway

This module establishes the risk backbone of the system. All downstream decisions depend on the quality and calibration of this signal.