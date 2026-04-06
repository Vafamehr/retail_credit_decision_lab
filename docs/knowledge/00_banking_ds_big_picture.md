# Banking Decision Systems — Big Picture

## 1. Core Idea

Modern banking systems are not just predictive models.

They are decision systems.

Data science in banking means turning data into decisions under constraints.

---

## 2. The Three-Layer Structure

Every real system follows this structure:

Data → Prediction → Decision

---

## 3. Layer 1 — Data

Raw customer and loan information:

- income  
- credit score  
- debt-to-income (DTI)  
- utilization  
- delinquencies  

Plus engineered features.

This layer answers:

“What do we know about the customer?”

---

## 4. Layer 2 — Prediction

Models estimate key probabilities:

Risk Model (PD)  
Probability that the customer will default  

Response Model  
Probability that the customer will accept an offer  

Outputs:

P(default), P(accept)

---

## 5. Layer 3 — Decision (Most Important)

Predictions are not decisions.

They must be combined with business logic and constraints.

Examples:

Approve if:
- risk is below threshold  
- and portfolio constraints are satisfied  

Offer selection based on economics:

Decision = f(Risk, Response, Economics, Constraints)

---

## 6. What Is Implemented

### Module 01 — Credit Approval

- predict default probability (PD)  
- optimize approval threshold under default constraint  
- produce approve / reject / review decisions  

---

### Module 02 — Response Modeling

- simulate multiple loan offers  
- predict acceptance probability  
- evaluate using calibration and decile analysis  

---

### Module 03 — Pricing Strategy

- adjust risk per offer  
- compute expected value using margin and loss  
- select best offer or no-offer option  

---

## 7. Why This Structure Matters

Without this structure:

- models are disconnected  
- decisions are inconsistent  
- business impact is unclear  

With this structure:

- decisions are consistent and explainable  
- trade-offs are explicit  
- system is extensible  

---

## 8. What the System Is Doing

The system combines:

- risk (probability of default)  
- behavior (probability of acceptance)  
- economics (margin, loss, cost)  

to produce:

- approval decisions  
- offer selection  
- expected value-based targeting  

---

## 9. Where This Goes Next

Next step is adding uncertainty-aware decisioning:

Expected Value = f(Risk, Response, Economics, Uncertainty)

This enables:

- probabilistic decision policies  
- better risk control  
- Bayesian updates  
- reinforcement learning integration  

---

## 10. Interview Framing

You are not presenting:

“I trained models”

You are presenting:

“I built a structured decision system that separates risk, behavior, and economics to produce consistent, decision-ready outputs aligned with real banking workflows.”

---

## Final Takeaway

The key shift is:

From predicting outcomes → to making decisions