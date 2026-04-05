# Banking Decision Systems — Big Picture

## 1. Core Idea

Modern banking systems are not just predictive models.

They are **decision systems**.

> Data Science in banking = turning data into decisions under constraints

---

## 2. The Three-Layer Structure

Every real system follows this structure:

```text
Data → Prediction → Decision
```

---

## 3. Layer 1 — Data

Raw customer and loan information:

* income
* credit score
* debt-to-income (DTI)
* utilization
* delinquencies

Plus engineered features.

This layer answers:

> “What do we know about the customer?”

---

## 4. Layer 2 — Prediction

We build models to estimate probabilities:

### Risk Model (PD)

> Probability customer will default

### Response Model

> Probability customer will accept the offer

Outputs:

```text
P(default), P(accept)
```

---

## 5. Layer 3 — Decision (Most Important)

Predictions are NOT decisions.

We combine them to make business choices.

Example:

```text
Approve if:
- Risk is low
- AND expected acceptance is high
```

Or more generally:

```text
Decision = f(Risk, Response, Business Constraints)
```

---

## 6. What You Built

### Module 01 — Credit Approval

* Predict default risk (PD)
* Optimize threshold under constraint
* Make approve/reject decisions

---

### Module 02 — Response Modeling

* Simulate offers
* Predict acceptance probability
* Evaluate using calibration and deciles

---

## 7. Why This Matters

Without this structure:

* Models are disconnected
* Decisions are inconsistent
* Business impact is unclear

With this structure:

* Decisions are explainable
* Trade-offs are controlled
* Systems are scalable

---

## 8. Where This Goes Next

The next step is combining both models:

```text
Expected Value = f(Risk, Response, Revenue)
```

This leads to:

* pricing optimization
* targeting strategies
* policy optimization
* reinforcement learning

---

## 9. Interview Framing

You are not presenting:

> “I trained models”

You are presenting:

> “I built a structured decision system that separates risk, behavior, and decision logic to align with real banking workflows.”

---

## Final Takeaway

The key shift is:

> From predicting outcomes → to making decisions
