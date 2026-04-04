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
* threshold optimization for approvals
* threshold-based approval policy
* business and calibration evaluation
* artifact saving for model and scaler

---

## High-Level Flow

Processed Feature Data  
→ Train Model  
→ Predict PD  
→ Optimize Approval Threshold  
→ Apply Approval Policy  
→ Evaluate Decisions  
→ Save Artifacts

---

## Current Folder Structure

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
    optimize_thresholds.py
  utils/
  runner.py

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
* computes optimized approval threshold
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

Current decision logic:

* approve: PD < optimized approval threshold
* review: optimized approval threshold ≤ PD < 0.32
* reject: PD ≥ 0.32

Key idea:

* approval threshold is data-driven
* reject threshold is currently a fixed business rule

---

### decision/optimize_thresholds.py

Threshold optimization layer.

* searches candidate approval thresholds
* evaluates approval population at each threshold
* selects the threshold that maximizes approval rate
* enforces a business constraint on approved default rate

Current constraint:

* approved default rate ≤ 15%

This layer separates threshold selection from hardcoded policy rules.

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

Includes:

* decision distribution
* default rates by decision
* approval metrics
* calibration table

This layer checks both:
* model usefulness
* decision quality

---

## Runtime Flow

### 1. Load Data

Reads processed feature file:

data/processed/loan_features.csv

---

### 2. Prepare Inputs

* X = features
* y = default
* customer_id retained separately

Categorical variables are encoded using one-hot encoding.

---

### 3. Train and Score

* stratified split
* fit StandardScaler
* train LogisticRegression
* predict PD
* compute AUC

---

### 4. Build Results Table

Create result dataset with:

* customer_id
* actual_default
* predicted_risk

---

### 5. Optimize Approval Threshold

Use scored results to find the approval cutoff that:

* maximizes approval rate
* while keeping approved default rate ≤ 15%

This produces a data-driven approval threshold.

---

### 6. Apply Decision Policy

Convert PD → decision:

* approve
* review
* reject

Current structure:

* approve below optimized threshold
* review between optimized threshold and 0.32
* reject at or above 0.32

---

### 7. Evaluate

Evaluate:

* AUC
* decision distribution
* default rate by decision
* approval rate
* default rate among approved customers
* calibration

---

### 8. Save Artifacts

Saved to artifacts/:

* model → logisticregression_model.pkl
* scaler → standardscaler_scaler.pkl

---

## Design Principles

### Separation of Prediction and Decision

Model predicts risk.  
Policy makes decisions.

---

### Separation of Threshold Optimization and Policy

Threshold selection is learned from data, not hardcoded.

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

## Current Performance Snapshot

* AUC ≈ 0.69
* Optimized approval threshold ≈ 0.1818
* Approval Rate ≈ 21%
* Default Rate (Approved) ≈ 14.9%

Decision distribution:

* approve ≈ 21%
* review ≈ 41%
* reject ≈ 38%

---

## Key Insight

This is a decision system:

Prediction → Threshold Optimization → Decision → Business Outcome