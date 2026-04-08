# Decision Policy — Knowledge Guide

## Overview

The Decision Policy layer is responsible for converting model outputs into final business actions.

Upstream modules produce signals:
- p_default (risk)
- p_accept (behavior)
- expected_value (economics)

This layer determines:

approve / decline / manual_review

---

## Core Principle

This layer is:

- deterministic  
- interpretable  
- parameter-driven  

It does NOT learn from data.

It enforces business rules on top of model outputs.

---

## Why This Layer Exists

Models alone are not enough.

Example:

- high expected value but very risky → not acceptable  
- low risk but low acceptance → not useful  
- profitable but borderline → needs review  

Decision Policy ensures:

- risk control  
- business alignment  
- operational consistency  

---

## Inputs

From pricing layer (best_offers.csv):

- p_default  
- p_accept  
- expected_value  
- offer_name  

---

## Output

Final decision:

- approve  
- decline  
- manual_review  

Additional outputs:
- decision_reason  
- policy_segment  

---

## Core Decision Logic

The decision is governed by constraints:

### 1. Risk Constraint

Reject high-risk customers:

p_default > max_p_default → decline

---

### 2. Acceptance Constraint

Avoid unlikely conversions:

p_accept < min_p_accept → decline

---

### 3. Profitability Constraint

Avoid negative economics:

expected_value < min_expected_value → decline

---

### 4. Risk Cap (Hard Guardrail)

Even aggressive strategies respect:

p_default > risk_cap → force decline

---

### 5. Manual Review Logic

For borderline but valuable cases:

- moderate risk  
- positive expected value  
- flagged for review  

These are routed to:

manual_review

---

## Multi-Strategy Framework

Different parameter sets represent different business strategies:

### Conservative
- low risk tolerance  
- low approval rate  

### Balanced
- moderate thresholds  

### Aggressive
- higher approvals  
- higher risk  

### Aggressive with Risk Cap (Best Performing)
- pushes approvals  
- enforces strict upper risk bound  

---

## Why Multiple Strategies

Real systems do not operate with a single fixed rule.

They evaluate trade-offs between:
- growth  
- risk  
- profitability  

Strategy comparison enables:

- scenario analysis  
- policy tuning  
- portfolio optimization  

---

## Key Insight

Decision Policy is NOT about prediction.

It is about:

**control**

---

## Separation of Concerns

This is critical:

| Layer | Responsibility |
|------|--------|
| Risk Model | estimate default probability |
| Response Model | estimate acceptance |
| Pricing | optimize expected value |
| Decision Policy | enforce business rules |

---

## Limitations of Current Approach

All decisions rely on:

point estimates

Example:

p_default = 0.16  
expected_value = 1200  

This assumes:
- predictions are exact  
- no uncertainty  

This is unrealistic.

---

## Motivation for Next Layer (Bayesian)

The Decision Policy does NOT account for:

- uncertainty in predictions  
- downside risk  
- variability in outcomes  

Example issue:

Two customers:

- both EV = 1000  

But:

- one stable  
- one highly uncertain  

Current system treats them equally.

---

## What Bayesian Layer Will Add

The next module introduces:

uncertainty-aware evaluation

Instead of:

EV = fixed  

We move to:

EV ~ distribution  

This enables:

- downside risk measurement  
- probability of loss  
- tail risk analysis  

---

## Final Takeaway

Decision Policy is:

- rule-based  
- interpretable  
- business-aligned  

It converts predictions into actions.

But it assumes certainty.

The Bayesian layer extends this by evaluating how reliable those decisions actually are.