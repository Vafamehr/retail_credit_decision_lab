# Module 03 — Pricing Strategy (Economic Decision System)

## 1. Problem Definition

After estimating risk and response, the key question becomes:

Which offer should we give to each customer to maximize business value?

This is a decision problem, not a modeling problem.

---

## 2. Business Context

A bank makes money only if:

- the customer accepts the offer  
- the loan performs (no default)  

This creates a trade-off:

- higher interest rate -> higher margin, lower acceptance  
- lower interest rate -> higher acceptance, lower margin  
- higher risk -> higher expected loss  

The goal is not to maximize approvals or acceptance.

The goal is to maximize expected profit.

---

## 3. Core Concept

This module combines:

- Risk -> P(default)  
- Response -> P(accept)  
- Economics -> revenue and loss  

Into one decision signal:

Decision = f(Risk, Response, Economics)

---

## 4. System Design

Pipeline:

Response Data -> Base Risk -> Risk Adjustment -> Value Scoring -> Offer Selection

---

## 5. Inputs

From previous modules:

- predicted default probability  
- predicted acceptance probability  
- customer and loan features  

From offer setup:

- interest rate  
- loan amount  
- payment-related features  

---

## 6. Risk Adjustment

Risk is adjusted per offer.

Higher interest rates slightly increase default probability.

Output:

adjusted_p_default

This reflects that pricing affects behavior and risk.

---

## 7. Value Scoring (Core Engine)

For each customer-offer pair, compute economic value.

### Step 1 — Expected Revenue

expected_revenue -> upside if loan performs

Based on:

loan_amount × (interest_rate − costs)

---

### Step 2 — Expected Loss

expected_loss -> downside if default occurs

Based on:

loan_amount × LGD

---

### Step 3 — Expected Value

expected_value = P(accept) × [(1 − P(default)) × revenue − P(default) × loss]

This captures:

- probability of booking  
- profit if successful  
- loss if default  

Negative values are allowed.

---

## 8. Offer Selection

For each customer:

- filter offers:

  - expected_value > 0  
  - P(accept) above threshold  

- select the offer with highest expected value  

If no offer qualifies:

no_offer

---

## 9. Outputs

- selected offer per customer  
- expected value  
- selection reason  

Stored in:

artifacts/pricing_strategy/

---

## 10. Key Observations

- high_apr -> higher margin, lower acceptance, often strong EV  
- mid_apr -> balanced option  
- low_apr -> higher acceptance but often weak economics  

The system naturally filters:

- profitable customers -> receive offers  
- unprofitable customers -> no_offer  

---

## 11. Why This Matters

This is where predictions turn into actions.

Before this:

- models estimate probabilities  

Here:

- the system chooses what to do  

---

## 12. Limitations

- simplified cost structure  
- fixed LGD and cost assumptions  
- no uncertainty modeling  
- no dynamic pricing  

---

## 13. Interview Summary

Built a pricing system that combines risk, response, and economics to compute expected value for each offer and select the best action per customer, including a no-offer option when no profitable opportunity exists.

---

## 14. What Comes Next

Next step:

Add uncertainty to evaluate how stable these decisions are.

Expected Value -> becomes distribution-aware

---

## Final Takeaway

This module converts predictions into economic decisions.

It is the point where data science directly impacts business outcomes.