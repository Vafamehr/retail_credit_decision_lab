# Module 04 — Decision Policy

## 1. Objective

Translate model outputs into actionable business decisions.

Inputs:
- default risk (adjusted_p_default)
- acceptance probability (p_accept)
- expected value (expected_value)
- selected offer (APR)

Output:
- final decision (approve / decline / review)
- decision reason
- policy segment


---

## 2. Decision Framework

The system applies a sequential decision policy:

1. Risk filter  
   Reject customers outside risk appetite

2. Economic filter  
   Reject customers with non-positive expected value

3. Acceptance filter  
   Reject customers with low probability of accepting the offer

4. Manual review  
   Route flagged cases for human evaluation

5. Final approval  
   Assign offer based on pricing output


---

## 3. Policy Segmentation

Customers are segmented based on adjusted default probability:

- low_risk
- medium_risk
- high_risk
- outside_risk_appetite

This enables analysis of decision behavior across risk tiers.


---

## 4. Key Findings

### Risk as a hard gate

A large portion of customers are rejected immediately due to risk.

Insight:
Risk acts as a strict eligibility constraint, removing nearly half of the population before other factors are considered.


---

### Acceptance probability as a major bottleneck

Among eligible customers, many are rejected due to low acceptance probability.

Insight:
Customer behavior (conversion likelihood) is a dominant constraint, even for otherwise viable customers.


---

### Expected value as a secondary filter

Expected value removes some customers but less than acceptance probability.

Insight:
Profitability matters, but most filtering occurs earlier in the pipeline.


---

### High APR dominance

Most approved customers receive high APR offers.

Insight:
The system prioritizes profitability, concentrating approvals in high-margin segments.


---

## 5. Sensitivity Analysis (Policy Tradeoffs)

Policy thresholds were varied across:

- acceptance threshold
- default threshold

### Acceptance threshold (primary driver)

Lower threshold:
- approval rate increases significantly (~2% → ~25%)
- total expected value increases substantially
- average risk increases
- acceptance quality decreases

Higher threshold:
- approval collapses
- portfolio becomes highly selective
- expected value drops sharply

Insight:
Acceptance threshold is the dominant control lever for portfolio size and revenue.


---

### Default threshold (secondary driver)

Higher threshold:
- gradual increase in approvals
- gradual increase in portfolio risk

Lower threshold:
- tighter risk control
- reduced approval volume

Insight:
Risk threshold acts as a fine-tuning mechanism rather than a primary driver.


---

## 6. System Interpretation

The final portfolio is governed by three competing forces:

- risk control (stability)
- acceptance probability (customer behavior)
- expected value (profitability)

Insight:
The system is more sensitive to acceptance constraints than to risk thresholds, indicating that customer behavior is a key limiting factor in portfolio growth.


---

## 7. Key Takeaway

The decision policy transforms predictive models into a constrained optimization system, where final outcomes emerge from tradeoffs between risk, conversion, and economic value.


---

## 8. Extensions

Natural next steps:

- threshold optimization
- constrained portfolio optimization
- reinforcement learning for policy selection