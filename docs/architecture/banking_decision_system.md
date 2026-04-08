# Architecture: Retail Credit Decision System

## Overview

This repository implements a modular end-to-end credit decision system.

Each module represents a core banking capability:

- Module 01 → Credit Approval (Risk / Probability of Default)
- Module 02 → Response Modeling (Customer Acceptance)
- Module 03 → Pricing Strategy (Expected Value Optimization)
- Module 04 → Decision Policy (Final Business Decisions)
- Module 05 → Bayesian Decision Layer (Uncertainty-Aware Evaluation)

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
Bayesian Decision Layer (Uncertainty Simulation + Risk Evaluation)  
↓  
Final Output: Portfolio Decisions + Risk Diagnostics

---

## End-to-End Decision Logic

The system transforms predictions into actions in multiple stages:

1. Risk Estimation  
   Estimate probability of default for each customer  

2. Behavior Estimation  
   Estimate probability of accepting an offer  

3. Economic Evaluation  
   Compute expected value for each offer  

4. Policy Decision  
   Apply business constraints and assign actions  

5. Uncertainty Evaluation (Bayesian Layer)  
   Evaluate robustness of decisions under uncertainty  

Final decision structure:

Decision = f(Risk, Acceptance, Expected Value)  
Bayesian Layer = evaluates stability of that decision  

---

## Folder Structure

src/
  credit_approval/
  response_modeling/
  pricing_strategy/
  decision_policy/
  bayesian_decision/          ← NEW

  data/
  features/
  utils/

---

## Data Layer

### Shared Data

data/shared/
  synthetic_loan_data.csv
  processed/
    loan_features.csv

- Single source of truth  
- Ensures consistency across modules  

---

### Module-Specific Data

data/response_modeling/
  processed/
    response_modeling_features.csv

- Encapsulated transformations per module  

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

- outputs probabilities (NOT decisions)  
- independent from business constraints  

---

### Decision Logic Layer

- converts predictions into actions  

Examples:
- approval thresholds  
- expected value computation  
- offer selection  
- policy rules  

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
- outputs core risk signal  

---

### Module 02 — Response Modeling

- predicts probability of acceptance  
- captures customer behavior  

---

### Module 03 — Pricing Strategy

- evaluates multiple offers  
- computes:
  - expected revenue  
  - expected loss  
  - expected value  

- selects optimal offer per customer  

---

### Module 04 — Decision Policy

- applies business constraints:
  - max risk threshold  
  - minimum acceptance threshold  
  - minimum profitability  

- supports multi-strategy decisioning:
  - conservative  
  - balanced  
  - aggressive  
  - aggressive_with_risk_cap  

- includes:
  - hard risk caps  
  - manual review routing for borderline cases  

- outputs:
  - approve  
  - decline  
  - manual_review  

IMPORTANT:
This layer uses **point estimates only** and is fully deterministic.

---

### Module 05 — Bayesian Decision Layer (NEW)

This module introduces uncertainty-aware evaluation.

Purpose:
- model uncertainty around predictions (p_default, p_accept)  
- propagate uncertainty into expected value  
- evaluate downside risk and decision robustness  

Key characteristics:
- reads from pricing outputs (best_offers.csv)  
- does NOT retrain models  
- does NOT replace decision policy (initially)  
- operates as a downstream evaluation layer  

Core idea:

Instead of:
EV = fixed value  

We model:
EV ~ distribution  

Outputs include:
- expected value distribution  
- downside risk metrics  
- tail loss metrics  
- probability of negative outcomes  

This layer enables:
- risk-aware decision analysis  
- stress testing of portfolio decisions  
- improved interpretability of uncertainty  

---

## Artifacts

artifacts/
  credit_approval/
  response_modeling/
  pricing_strategy/
  decision_policy/
  bayesian_decision/   ← NEW

---

## Runner

`runner.py` executes the main pipeline:

1. Data generation  
2. Feature engineering  
3. Credit approval  
4. Response modeling  
5. Pricing strategy  
6. Decision policy  

Bayesian layer is executed separately (for now).

---

## Design Principles

### Separation of Concerns

- modeling ≠ decision making  
- point estimates ≠ uncertainty evaluation  

---

### Deterministic Core

- base pipeline remains deterministic  
- Bayesian layer adds probabilistic analysis on top  

---

### Modular Isolation

- each module owns its logic  
- Bayesian layer does not break existing modules  

---

### Business Alignment

- each module maps to real-world banking functions  
- decision policy reflects operational constraints  
- Bayesian layer reflects risk management / stress testing  

---

## Current System Capability

The system supports:

- risk estimation  
- customer behavior modeling  
- multi-offer pricing optimization  
- policy-based decisioning  
- strategy comparison  
- sensitivity analysis  

NEW capability:
- uncertainty-aware decision evaluation  

---

## System Behavior

The portfolio is governed by three forces:

- risk  
- acceptance  
- profitability  

The Bayesian layer adds a fourth dimension:

- uncertainty / downside risk  

---

## Next possible Extensions

- Bayesian-informed decision policy integration  
- portfolio-level risk constraints  
- reinforcement learning for decision policies  
- scenario-based stress testing  

---

## Final Takeaway

This system is not just a collection of models.

It is a structured decision pipeline that:

- separates prediction from decision  
- separates decision from uncertainty evaluation  

This mirrors real-world credit systems where:
- models generate signals  
- policies enforce constraints  
- risk layers evaluate uncertainty