# 05 — Decision Policy & Threshold Optimization

## Overview

In a credit risk system, a model alone is not sufficient. The model outputs a **probability of default (PD)**, but business decisions require **clear actions** such as approve, review, or reject.

This module converts model outputs into actionable decisions using:
- threshold-based policy rules
- data-driven threshold optimization
- decision-level evaluation

---

## From Model to Decision

The modeling step produces:

- Input: customer features
- Output: predicted probability of default (PD)

However, PD is not directly actionable.

We introduce a **decision policy layer**:

| PD Range | Decision |
|----------|--------|
| low PD   | approve |
| mid PD   | review |
| high PD  | reject |

---

## Static vs Data-Driven Thresholds

### Static Thresholds (Initial Version)

Originally, thresholds were fixed:

- approve: PD < 0.18  
- review: 0.18 ≤ PD < 0.32  
- reject: PD ≥ 0.32  

This approach is simple but arbitrary.

---

### Optimized Threshold (Current Approach)

We replace the approval threshold with a **data-driven value**.

Objective:

> Maximize approval rate subject to a constraint on default risk

Constraint:

- approved default rate ≤ 15%

Procedure:

1. Iterate over possible PD thresholds
2. For each threshold:
   - define approved population (PD < threshold)
   - compute:
     - approval rate
     - default rate
3. Select threshold that:
   - satisfies risk constraint
   - maximizes approval rate

This produces an **optimal approval cutoff** grounded in data.

---

## Final Decision Policy

The system now uses:

- approve: PD < optimized_threshold  
- review: optimized_threshold ≤ PD < 0.32  
- reject: PD ≥ 0.32  

Key idea:

- approval boundary is learned from data
- reject boundary remains a conservative business rule

---

## Why This Matters

This transforms the system from:

> “a model with a random threshold”

to:

> “a decision system optimized under business constraints”

This is critical in real-world credit systems, where:
- risk must be controlled
- approvals drive revenue
- thresholds cannot be arbitrary

---

## Evaluation at Decision Level

The system evaluates decisions using:

### 1. Decision Distribution
- % approved / review / rejected

### 2. Default Rate by Decision
- verifies risk separation across segments

### 3. Business Metrics
- approval rate
- default rate among approved customers

---

## Example Outcome

- Approve: ~21%
- Review: ~41%
- Reject: ~38%

Default rates:

- Approve: ~15% (within constraint)
- Review: higher risk
- Reject: highest risk

This confirms effective segmentation.

---

## Key Takeaways

- Models estimate risk; policies make decisions
- Thresholds should be derived, not guessed
- Business constraints must guide optimization
- Evaluation must happen at the **decision level**, not just model level

---

## Interview Framing

This module can be explained as:

> “We built a credit decision system where model outputs are converted into actions using a policy layer. Instead of choosing thresholds arbitrarily, we optimized approval thresholds under a default-rate constraint, then evaluated decisions across segments to ensure proper risk separation.”