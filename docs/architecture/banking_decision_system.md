# Architecture : Banking Decision Systems Lab

## Overview

This repository is organized as a **modular decision system**, where each module represents a real banking capability:

* Module 01 → Credit Approval (Risk)
* Module 02 → Response Modeling (Behavior)

Each module follows the same pattern:

```text
Data → Module Logic → Model → Evaluation → Artifacts
```

---

## High-Level Flow

```text
Shared Data Layer
        ↓
+----------------------+
| Credit Approval      |
| (Risk / PD Model)    |
+----------------------+
        ↓
+----------------------+
| Response Modeling    |
| (Acceptance Model)   |
+----------------------+
        ↓
(Future)
Decision Optimization Layer
```

---

## Folder Structure

```text
src/
  credit_approval/
    pipeline.py
    policy.py
    optimize_thresholds.py

  response_modeling/
    pipeline.py
    train_response_model.py
    evaluate_response_model.py

  data/
    generate_data.py

  features/
    feature_engineering.py
```

---

## Data Layer

### Shared Data

```text
data/shared/
  synthetic_loan_data.csv
  processed/
    loan_features.csv
```

Used by all modules.

---

### Module-Specific Data

```text
data/response_modeling/
  processed/
    response_modeling_features.csv
```

Generated inside module pipeline.

---

## Module Design Pattern

Each module is designed as a **self-contained pipeline**.

### Responsibilities

#### Pipeline (Orchestrator)

* load data
* prepare inputs
* call modeling
* call evaluation
* save artifacts
* print summary

---

#### Modeling Layer

* train model
* return predictions

---

#### Evaluation Layer

* compute metrics
* return structured outputs

---

## Artifacts

Stored per module:

```text
artifacts/
  credit_approval/
  response_modeling/
```

Each contains:

* model
* scaler
* feature columns

---

## Design Principles

### 1. Separation of Concerns

* data generation ≠ modeling
* modeling ≠ decision
* prediction ≠ business logic

---

### 2. Deterministic Pipelines

* no hidden steps
* reproducible runs
* explicit data flow

---

### 3. Module Isolation

* each module owns its logic
* minimal cross-dependencies

---

### 4. Business Alignment

* models map to real banking problems
* outputs map to decisions

---

## Current System Capability

* Risk prediction (default probability)
* Threshold-based approval decisions
* Acceptance prediction (response probability)
* Calibration and decile analysis

---

## Next Extension (Planned)

Add a **Decision Optimization Layer**:

```text
Decision = f(Risk, Response, Economics)
```

This will introduce:

* expected value modeling
* pricing strategies
* policy optimization

---

## Final Takeaway

This architecture is not model-centric.

It is:

> a modular system that transforms data into structured business decisions
