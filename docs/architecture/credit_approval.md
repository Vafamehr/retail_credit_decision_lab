# Credit Approval Module — Architecture

## Purpose

This module implements a simple end-to-end credit approval decision system.

It takes processed borrower features, predicts probability of default (PD), applies a business approval policy, and evaluates both model performance and decision outcomes.

The goal is to separate:

* prediction
* decision
* evaluation

so the system is easy to understand, extend, and explain in interviews.

---

## Current Module Scope

This module currently covers:

* processed input data loading
* model training with Logistic Regression
* probability of default prediction
* threshold-based approval policy
* business and calibration evaluation
* artifact saving for model and scaler

---

## High-Level Flow

Processed Feature Data
→ Train Model
→ Predict PD
→ Apply Approval Policy
→ Evaluate Decisions
→ Save Artifacts

---

## Current Folder Structure

```
src/
  credit_approval/
    pipeline.py
    policy.py
  data/
  features/
  modeling/
    train_model.py
  evaluation/
    calibration.py
    evaluate_model.py
  decision/
  utils/
  runner.py
```

---

## Component Responsibilities

### runner.py

Repository-level entry point.

* Calls the credit approval pipeline
* Will later route to other modules

---

### credit_approval/pipeline.py

Module orchestration layer.

* loads data
* calls model training and scoring
* builds results table
* applies approval policy
* runs evaluation
* saves artifacts
* prints structured outputs

This file owns the full workflow for this problem.

---

### credit_approval/policy.py

Business decision logic.

* converts predicted PD into:

  * approve
  * review
  * reject

Current thresholds:

* approve: PD < 0.18
* review: 0.18 ≤ PD < 0.32
* reject: PD ≥ 0.32

---

### modeling/train_model.py

Reusable modeling layer.

* prepares data
* performs train/test split
* scales features
* trains Logistic Regression
* predicts PD
* computes AUC

Returns model, scaler, and scored outputs.

---

### evaluation/

Reusable evaluation layer.

* decision distribution
* default rates by decision
* approval metrics
* calibration table

---

## Runtime Flow

### 1. Load Data

Reads processed feature file:

data/processed/loan_features.csv

---

### 2. Prepare Inputs

* X = features
* y = default
* customer_id retained

Categorical variables encoded using one-hot encoding.

---

### 3. Train and Score

* stratified split
* fit StandardScaler
* train Logistic Regression
* predict PD
* compute AUC

---

### 4. Build Results Table

Create:

* customer_id
* actual_default
* predicted_risk

---

### 5. Apply Decision Policy

Convert PD → decision:

* approve
* review
* reject

---

### 6. Evaluate

Evaluate:

* AUC
* decision distribution
* approval rate
* default rate (approved)
* calibration

---

### 7. Save Artifacts

Saved to artifacts/:

* model → logisticregression_model.pkl
* scaler → standardscaler_scaler.pkl

Names are derived from object types.

---

## Design Principles

### Separation of Prediction and Decision

Model predicts risk.
Policy makes decisions.

This separation makes the system:

* easier to explain
* easier to tune
* closer to real-world systems

---

### Shared vs Module-Specific Logic

Shared (reusable):

* modeling
* evaluation
* feature preparation

Module-specific:

* approval policy
* pipeline orchestration

---

### Modular Design

Each banking problem becomes its own module:

* credit approval (current)
* pricing strategy (next)
* limit assignment (future)

---

## Execution

Run full system:

python -m src.runner

Run module directly:

python -m src.credit_approval.pipeline

---

## Current Performance

* AUC ≈ 0.69
* Approval Rate ≈ 20%
* Default Rate (Approved) ≈ 14–15%

Policy:

* approve < 0.18
* review 0.18–0.32
* reject ≥ 0.32

---

## Key Insight

This is not just a model.

It is a decision system:

Prediction → Decision → Business Outcome
