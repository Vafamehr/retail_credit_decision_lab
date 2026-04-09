# Architecture: Retail Credit Decision System

## Overview

This repository implements a modular end-to-end credit decision system.

Each module represents a core banking function:

- Module 01 -> Credit Approval (Probability of Default)  
- Module 02 -> Response Modeling (Acceptance)  
- Module 03 -> Pricing Strategy (Expected Value)  
- Module 04 -> Decision Policy (Business Rules)  
- Module 05 -> Bayesian Decision Layer (Uncertainty Evaluation)  

Each module follows a consistent structure:

Data -> Features -> Model -> Decision Logic -> Evaluation -> Artifacts

---

## High-Level System Flow

Synthetic Data Generation  
-> Feature Engineering  
-> Credit Approval (Risk)  
-> Response Modeling (Acceptance)  
-> Pricing Strategy (Economics + Offer Selection)  
-> Decision Policy (Approve / Reject / Review)  
-> Bayesian Decision Layer (Uncertainty + Risk Evaluation)  
-> Final Output: Decisions + Risk Diagnostics

---

## End-to-End Decision Logic

The system converts predictions into actions in stages:

1. Risk Estimation -> probability of default  
2. Behavior Estimation -> probability of acceptance  
3. Economic Evaluation -> expected value per offer  
4. Policy Decision -> apply business rules  
5. Uncertainty Evaluation -> assess stability of decisions  

Final structure:

Decision = f(Risk, Response, Economics)  
Bayesian Layer -> evaluates how stable that decision is  

---

## Folder Structure

src/  
  credit_approval/  
  response_modeling/  
  pricing_strategy/  
  decision_policy/  
  bayesian_decision/  

  data/  
  features/  
  utils/  

---

## Data Layer

Shared data:

data/shared/  
  synthetic_loan_data.csv  
  processed/  
    loan_features.csv  

- single source of truth  
- consistent across modules  

Module-specific data:

data/response_modeling/  
  processed/  
    response_modeling_features.csv  

- isolated transformations  
- avoids leakage  

---

## Module Design Pattern

Each module is a self-contained pipeline.

Pipeline layer:

- load data  
- prepare features  
- run model  
- apply decision logic  
- evaluate outputs  
- save artifacts  

Modeling layer:

- outputs probabilities (not decisions)  

Decision logic layer:

- converts predictions into actions  

Evaluation layer:

- model metrics (AUC, calibration)  
- business metrics (approval rate, EV, risk)  

---

## Module Responsibilities

Module 01 — Credit Approval  
- estimates probability of default  
- outputs risk signal  

Module 02 — Response Modeling  
- predicts probability of acceptance  
- captures behavior  

Module 03 — Pricing Strategy  
- evaluates multiple offers  
- computes:  
  expected_revenue -> upside if loan performs  
  expected_loss -> downside if default occurs  
  expected_value -> risk-adjusted profit  
- selects best offer per customer  

Module 04 — Decision Policy  
- applies business constraints:  
  risk threshold  
  acceptance threshold  
  profitability threshold  
- supports strategies: conservative, balanced, aggressive, aggressive_with_risk_cap  
- outputs: approve / reject / review  

Important:  
This layer is deterministic and uses point estimates only  

Module 05 — Bayesian Decision Layer  
- models uncertainty in p_default and p_accept  
- simulates outcomes  
- evaluates downside risk  

Instead of:  
expected_value = fixed  

We evaluate:  
expected_value ~ distribution  

---

## Bayesian Outputs

- simulated_ev_mean -> average outcome  
- simulated_ev_p05 -> bad-case threshold (VaR-style)  
- prob_ev_negative -> frequency of losses  
- expected_shortfall -> average loss in worst cases (CVaR-style)  
- simulated_pd_p95 -> worst-case risk spike  

---

## Role of Bayesian Layer

- reads pricing output (best_offers.csv)  
- does not retrain models  
- does not replace policy  
- evaluates decision robustness  

---

## Artifacts

artifacts/  
  credit_approval/  
  response_modeling/  
  pricing_strategy/  
  decision_policy/  
  bayesian_decision/  

---

## Runner

runner.py executes:

1. data generation  
2. feature engineering  
3. credit approval  
4. response modeling  
5. pricing strategy  
6. decision policy  
7. Bayesian evaluation  

---

## Design Principles

Separation of concerns:  
- prediction != decision  
- decision != uncertainty  

Deterministic core + probabilistic layer:  
- base pipeline deterministic  
- Bayesian adds uncertainty  

Modular design:  
- modules isolated  
- Bayesian layer non-invasive  

Business alignment:  
- risk -> credit  
- response -> behavior  
- pricing -> economics  
- policy -> rules  
- Bayesian -> risk evaluation  

---

## System Behavior

Decisions are driven by:

- risk  
- acceptance  
- profitability  

Bayesian layer adds:

- uncertainty  
- downside risk  

---

## Extensions

- integrate Bayesian into policy  
- portfolio-level constraints  
- reinforcement learning  
- scenario stress testing  

---

## Final Takeaway

This system is a decision pipeline:

- models estimate probabilities  
- pricing converts predictions into money  
- policy enforces rules  
- Bayesian layer evaluates risk  

This mirrors real-world credit systems.