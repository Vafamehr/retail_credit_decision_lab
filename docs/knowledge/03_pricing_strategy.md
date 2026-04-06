# Module 03 — Pricing Strategy (Economic Decision System)

## 1. Problem Definition

After estimating risk and response, the key question becomes:

Which offer should we give to each customer to maximize business value?

This is a decision problem under uncertainty.

---

## 2. Business Context

A bank makes money only if:

- the customer accepts the offer  
- the loan performs (does not default)  

This creates a three-way trade-off:

- higher interest rate → higher margin but lower acceptance  
- lower interest rate → higher acceptance but lower margin  
- higher risk → higher losses  

The goal is to choose offers that maximize expected profit, not just approval or acceptance.

---

## 3. Core Concept

This module combines:

- Risk → P(default)  
- Response → P(accept)  
- Economics → revenue, cost, loss  

Into a single decision:

Decision = f(Risk, Response, Economics)

---

## 4. System Design

Pipeline:

Response Data → Base Risk → Risk Adjustment → Value Scoring → Offer Selection

---

## 5. Inputs

From previous modules:

- predicted default probability  
- predicted acceptance probability  
- customer and loan features  

Plus offer definitions:

- interest rate  
- loan amount  
- derived payment metrics  

---

## 6. Risk Adjustment

Risk is adjusted per offer to reflect pricing effects.

Higher interest rates slightly increase default probability.

This introduces:

adjusted_p_default

which is used for economic calculations.

---

## 7. Value Scoring (Core Engine)

For each customer-offer pair, compute expected value.

### Step 1 — Expected Credit Cost

expected_credit_cost_rate = adjusted_p_default × LGD

---

### Step 2 — Unit Margin

unit_margin = interest_rate − expected_credit_cost − funding_cost − servicing_cost

---

### Step 3 — Expected Value

expected_value = P(accept) × loan_amount × unit_margin

This captures:

- probability of booking  
- profitability of the loan  
- risk-adjusted loss  

Negative values are allowed.

---

## 8. Offer Selection

For each customer:

- filter offers with:
  - expected_value > 0  
  - P(accept) ≥ threshold  

- choose the offer with highest expected value  

If no offer meets criteria:

no_offer

---

## 9. Outputs

- selected offer per customer  
- expected value per decision  
- selection reason (positive, low acceptance, negative value)  

Stored in:

artifacts/pricing_strategy/

---

## 10. Key Observations

- high_apr → highest margin, lower acceptance, strongest profitability  
- mid_apr → balanced trade-off  
- low_apr → high acceptance but often unprofitable  

The system naturally filters:

- profitable customers → receive offers  
- unprofitable customers → no_offer  

---

## 11. Why This Matters

This is where models become decisions.

Instead of:

- predicting risk  
- predicting behavior  

The system now:

- selects actions  
- controls profitability  
- enforces constraints  

---

## 12. Limitations

- simplified cost structure  
- static parameters (LGD, costs)  
- no uncertainty modeling  
- no dynamic optimization  

---

## 13. Interview Summary

Built a pricing decision system that combines risk, response, and economic assumptions to compute expected value for each offer and select the optimal action, including a no-offer option when no profitable opportunity exists.

---

## 14. What Comes Next

Next step is adding uncertainty:

Expected Value = f(Risk, Response, Economics, Uncertainty)

This enables:

- Bayesian decisioning  
- confidence-aware policies  
- exploration vs exploitation (RL)  

---

## Final Takeaway

This module transforms predictions into economic decisions.

It is the point where data science directly drives business value.