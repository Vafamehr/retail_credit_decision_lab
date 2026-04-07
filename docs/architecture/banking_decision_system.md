# Architecture: Retail Credit Decision System

## Overview

This repository implements a modular end-to-end credit decision system.

Each module represents a core banking capability:

- Module 01 → Credit Approval (Risk / Probability of Default)
- Module 02 → Response Modeling (Customer Acceptance)
- Module 03 → Pricing Strategy (Expected Value Optimization)
- Module 04 → Decision Policy (Final Business Decisions)

Each module follows a consistent pattern:

Data → Features → Model → Decision Logic → Evaluation → Artifacts

---

## High-Level System Flow

Synthetic Data Generation  
↓  
Feature Engineering  
↓  
Credit Approval (Risk Model)  
↓  
Response Modeling (Acceptance Model)  
↓  
Pricing Strategy (Expected Value + Offer Selection)  
↓  
Decision Policy (Approve / Decline / Review)  
↓  
Final Output: Portfolio Decisions

---

## End-to-End Decision Logic

The system transforms predictions into actions in four stages:

1. Risk Estimation  
   Estimate probability of default for each customer  

2. Behavior Estimation  
   Estimate probability of accepting an offer  

3. Economic Evaluation  
   Compute expected value for each offer  

4. Policy Decision  
   Apply business constraints and select final action  

Final decision is governed by:

Decision = f(Risk, Acceptance, Expected Value)

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

  decision_policy/
    pipeline.py
    decision_engine.py
    reporting.py
    sensitivity.py

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

Each module is a self-contained pipeline.

### Pipeline (Orchestrator)

Responsible for:
- loading data  
- preparing features  
- running models  
- applying decision logic  
- evaluating outputs  
- saving artifacts  

---

### Modeling Layer

- trains predictive models  
- outputs probabilities (not decisions)  
- independent of business rules  

---

### Decision Logic Layer

- converts predictions into actions  

Examples:
- approval thresholding  
- risk adjustment  
- expected value computation  
- offer selection  
- final decision policy  

---

### Evaluation Layer

- model metrics (AUC, calibration)  
- business metrics:
  - approval rate  
  - expected value  
  - risk profile  

---

## Module Responsibilities

### Module 01 — Credit Approval

- estimates probability of default  
- applies approval threshold  
- outputs base risk signal  

---

### Module 02 — Response Modeling

- predicts probability of customer acceptance  
- introduces behavioral dimension  

---

### Module 03 — Pricing Strategy

- evaluates multiple APR offers  
- computes:
  - expected revenue  
  - expected loss  
  - expected value  

- selects best offer per customer  

---

### Module 04 — Decision Policy

- applies business constraints:
  - risk threshold  
  - acceptance threshold  
  - economic viability  

- assigns:
  - approve (with offer)  
  - decline  
  - manual review  

- produces portfolio-level outputs  

---

## Artifacts

artifacts/
  credit_approval/
  response_modeling/
  pricing_strategy/

Outputs include:
- trained models  
- scalers  
- feature columns  
- scored datasets  
- final decision outputs  

---

## Runner

`runner.py` executes the full pipeline:

1. Data generation  
2. Feature engineering  
3. Credit approval  
4. Response modeling  
5. Pricing strategy  
6. Decision policy  

This enables reproducible, end-to-end execution.

---

## Design Principles

### Separation of Concerns

- modeling ≠ decision making  
- predictions ≠ actions  

---

### Deterministic Pipelines

- reproducible runs  
- explicit transformations  
- no hidden logic  

---

### Modular Isolation

- each module owns its logic  
- clean interfaces between modules  

---

### Business Alignment

- each module maps to a real banking function  
- outputs are decision-ready  

---

## Current System Capability

The system supports:

- risk estimation (default probability)  
- customer behavior modeling  
- multi-offer pricing evaluation  
- expected value optimization  
- policy-based decisioning  
- portfolio-level diagnostics  
- sensitivity analysis of policy thresholds  

---

## System Behavior

The final portfolio is governed by three competing forces:

- risk control  
- customer acceptance  
- profitability  

The system produces decisions through tradeoffs between these constraints rather than optimizing a single objective.

---

## Next possible Extensions

Planned enhancements:

- threshold optimization  
- constrained portfolio optimization  
- Bayesian uncertainty modeling  
- reinforcement learning for policy selection  

---

## Final Takeaway

This system is not a collection of independent models.

It is a structured decision pipeline that integrates risk, behavior, and economics to produce actionable business decisions.