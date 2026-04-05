# Module 01 — Credit Approval (Risk Decision System)

## 1. Problem Definition

In lending systems, the core decision is:

> **Should we approve this customer for a loan?**

This is a **risk decision problem**, where the goal is to control default risk while maintaining business volume.

---

## 2. Business Context

Banks must balance:

* **Approval Rate** → more customers, more revenue
* **Default Risk** → losses from bad loans

This creates a trade-off:

> Approve more → higher risk
> Approve less → lower revenue

The system must find the **optimal balance**.

---

## 3. System Overview

This module builds a complete **credit decision pipeline**:

```text
Data → Features → Risk Model → Threshold Optimization → Decision Policy → Evaluation
```

---

## 4. Data Generation (Synthetic Population)

We simulate a realistic borrower dataset:

Features include:

* income
* credit score
* loan amount
* debt-to-income ratio (DTI)
* credit utilization
* delinquencies
* employment history

### Risk Construction

A risk score is built using:

* linear effects (credit score, DTI, utilization)
* interaction effects (DTI × utilization)
* threshold effects (low credit score penalty)
* extreme risk spikes

Then transformed via:

```text
sigmoid → probability of default
```

Finally:

```text
default ∈ {0,1}
```

---

## 5. Feature Engineering

We create signals that improve model performance:

* loan-to-income ratio
* high utilization flag
* delinquency flag
* employment stability
* interaction features

These reflect real-world credit modeling practices.

---

## 6. Risk Model

Model used:

```text
Logistic Regression
```

Purpose:

> Estimate probability of default (PD)

Output:

```text
predicted_risk ∈ [0,1]
```

---

## 7. Decision Layer (Critical)

Prediction is NOT the final step.

We convert predictions into decisions using thresholds.

### Threshold Optimization

We search for a threshold such that:

```text
Default Rate (Approved) ≤ 15%
```

While maximizing:

```text
Approval Rate
```

---

## 8. Decision Policy

Customers are segmented into:

* **Approve** → low risk
* **Reject** → high risk
* **Review** → borderline

This mimics real underwriting systems.

---

## 9. Evaluation (Business-Focused)

### 9.1 Approval Metrics

* Approval Rate
* Default Rate (Approved)

---

### 9.2 Calibration

We compare:

* predicted risk
* actual default rate

Across bins to ensure reliability.

---

## 10. Outputs

* customer-level decisions
* risk scores
* calibration tables
* trained model artifacts

Saved in:

```text
artifacts/credit_approval/
```

---

## 11. Key Insight

> **Prediction ≠ Decision**

A model predicts risk.

A system makes decisions.

---

## 12. Limitations

* synthetic data
* simple model
* static threshold
* no pricing optimization

---

## 13. Interview Summary

> “I built a credit approval system that predicts default risk and converts it into decisions using threshold optimization under business constraints, with evaluation focused on approval rate, default control, and calibration.”

---

## Final Takeaway

This module is about:

> turning risk predictions into **controlled business decisions**
