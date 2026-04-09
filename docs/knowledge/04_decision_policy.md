# Decision Policy — Knowledge Guide

## Overview

The Decision Policy layer converts model outputs into final actions.

Inputs from upstream:

- p_default -> risk  
- p_accept -> behavior  
- expected_value -> economics  

Output:

approve / reject / review

---

## Core Principle

This layer is:

- deterministic  
- interpretable  
- parameter-driven  

It does not learn.

It applies business rules on top of model outputs.

---

## Why This Layer Exists

Model outputs are not decisions.

Examples:

- high expected value but too risky -> reject  
- low risk but very low acceptance -> not useful  
- profitable but borderline -> review  

This layer ensures:

- risk control  
- consistency  
- alignment with business constraints  

---

## Inputs

From pricing layer (best_offers.csv):

- p_default  
- p_accept  
- expected_value  
- offer_name  

---

## Outputs

- decision -> approve / reject / review  
- decision_reason  
- policy_segment  

---

## Core Decision Logic

Decisions are based on constraints.

### 1. Risk Constraint

p_default > threshold -> reject

---

### 2. Acceptance Constraint

p_accept < threshold -> reject

---

### 3. Profitability Constraint

expected_value < threshold -> reject

---

### 4. Risk Cap (Hard Guardrail)

p_default > risk_cap -> force reject

---

### 5. Review Zone

Borderline cases:

- moderate risk  
- positive value  

-> review

---

## Strategy Framework

Different parameter sets define different behaviors.

### Conservative
- low risk tolerance  
- lower approvals  

### Balanced
- moderate thresholds  

### Aggressive
- higher approvals  
- higher risk  

### Aggressive with Risk Cap
- allows growth  
- enforces strict upper risk limit  

---

## Why Multiple Strategies

There is no single correct policy.

Trade-offs exist between:

- growth  
- risk  
- profitability  

Multiple strategies allow:

- comparison  
- tuning  
- scenario analysis  

---

## Key Insight

This layer is about control, not prediction.

---

## Separation of Roles

| Layer | Role |
|------|------|
| Risk Model | estimate default probability |
| Response Model | estimate acceptance |
| Pricing | compute expected value |
| Decision Policy | apply rules |

---

## Limitation

All decisions are based on point estimates.

Example:

p_default = 0.16  
expected_value = 1200  

Assumes predictions are exact.

---

## Why This Is Not Enough

Two customers can have the same expected value:

- one stable  
- one highly uncertain  

Policy treats them the same.

---

## What Comes Next

Introduce uncertainty.

Instead of:

expected_value -> single number  

We move to:

expected_value -> distribution  

This allows:

- probability of loss  
- downside scenarios  
- tail risk evaluation  

---

## Final Takeaway

Decision Policy turns model outputs into actions using rules.

It is simple, interpretable, and controllable.

But it assumes certainty.

The next layer evaluates how reliable those decisions actually are.