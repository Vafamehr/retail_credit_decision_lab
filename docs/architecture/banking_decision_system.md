# Architecture: Banking Decision Systems Lab

## Overview

This repository is structured as a modular decision system, where each module represents a core banking capability:

- Module 01 → Credit Approval (Risk / PD)
- Module 02 → Response Modeling (Customer Behavior)
- Module 03 → Pricing Strategy (Decision / Economics)

Each module follows a consistent pattern:

Data → Features → Model → Decision Logic → Evaluation → Artifacts

---

## High-Level Flow

Shared Data Layer  
↓  
Credit Approval (PD / Risk Model)  
↓  
Response Modeling (Acceptance Model)  
↓  
Pricing Strategy (Expected Value Decisioning)  
↓  
Final Output: Offer Selection or No Offer

---

## Folder Structure

src/
  credit_approval/
    pipeline.py
    policy.py
    optimize_thresholds.py
    inference.py

  response_modeling/
    pipeline.py
    train_response_model.py
    evaluate_response_model.py

  pricing_strategy/
    pipeline.py
    risk_adjustment.py
    value_scoring.py

  data/
    generate_data.py

  features/
    feature_engineering.py

  utils/
    config.py
    schema.py

---

## Data Layer

### Shared Data

data/shared/
  synthetic_loan_data.csv
  processed/
    loan_features.csv

- Single source of truth for all modules  
- Ensures consistency across risk, response, and pricing  

---

### Module-Specific Data

data/response_modeling/
  processed/
    response_modeling_features.csv

- Generated within module pipelines  
- Encapsulates module-specific transformations  

---

## Module Design Pattern

Each module is a self-contained pipeline with clear responsibilities.

### Pipeline (Orchestrator)

- load data  
- prepare features  
- call modeling  
- apply decision logic  
- evaluate results  
- save artifacts  
- print summary  

---

### Modeling Layer

- train model  
- generate predictions  
- independent of business rules  

---

### Decision Logic Layer

- converts predictions into actions  
- examples:
  - approval thresholding  
  - risk adjustment  
  - expected value computation  
  - offer selection  

---

### Evaluation Layer

- compute performance metrics  
- calibration and deciles  
- business KPIs (approval rate, default rate, expected value)  

---

## Artifacts

artifacts/
  credit_approval/
  response_modeling/
  pricing_strategy/

Each contains:

- model  
- scaler  
- feature columns  
- scored outputs (for pricing)  

---

## Design Principles

### Separation of Concerns

- data generation is separate from modeling  
- modeling is separate from decision logic  
- predictions are separate from business actions  

---

### Deterministic Pipelines

- reproducible runs  
- no hidden transformations  
- explicit data flow  

---

### Modular Isolation

- each module owns its logic  
- minimal coupling  
- clean interfaces between modules  

---

### Business Alignment

- each module maps to a real banking function  
- outputs are decision-ready, not just predictions  

---

## Current System Capability

- probability of default modeling  
- risk-based approval decisions  
- customer acceptance prediction  
- offer-level expected value computation  
- offer selection with no-offer fallback  
- portfolio-level economic view  

---

## Next Extension

Decision system will be extended to include uncertainty-aware decisioning:

Decision = f(Risk, Response, Economics, Uncertainty)

- introduce probabilistic priors  
- model uncertainty in default and response  
- propagate uncertainty into expected value  
- support risk-aware decision policies  

---

## Final Takeaway

This is not a collection of models.

It is a structured decision system that combines risk, behavior, and economics to drive business actions.