# 04 - Modeling and Decision System

## Overview

This module builds a simple credit risk decision system:

data → features → model → probability of default (PD) → decision → evaluation

---

## Model

A Logistic Regression model is trained to predict probability of default (PD).

- Input: engineered features
- Output: probability of default per customer

The model is trained using a stratified train/test split.

---

## Predicted Risk (PD)

The model outputs:

PD = probability that a customer defaults

This is used as the core risk signal for decision making.

---

## Decision Policy

A simple threshold-based policy is applied:

- Approve: PD < 0.18
- Review: 0.18 ≤ PD < 0.32
- Reject: PD ≥ 0.32

This simulates a real-world credit decision strategy.

---

## Evaluation

### 1. AUC

Measures ranking quality of the model.

---

### 2. Decision Metrics

- Decision distribution (approve / review / reject)
- Default rate per decision bucket

---

### 3. Approval Metrics

- Approval Rate = % of customers approved
- Default Rate (Approved Only) = risk of approved population

This represents the business tradeoff between growth and risk.

---

### 4. Calibration

Calibration checks whether predicted probabilities match reality.

A calibration table compares:

- average predicted PD
- actual default rate

across risk buckets.

Good calibration means:

predicted ≈ actual

---

## Key Learnings

- Model performance depends on data signal, not just model choice
- Feature engineering can encode non-linear risk patterns
- Decision thresholds control business tradeoffs
- Calibration is critical for using probabilities in decisions
- Small threshold changes can significantly impact approval volume

---

## Next Steps

- Threshold optimization (grid search)
- Model comparison (tree-based models)
- Cost-based decision optimization
- Stability testing across multiple data samples