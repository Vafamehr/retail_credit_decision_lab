# Retail Credit Decision Lab

## Overview

This project builds an end-to-end retail credit decision system.

The goal is not just predicting outcomes, but turning those predictions into real decisions using risk, customer behavior, and economics.

Pipeline flow:

Data -> Risk -> Response -> Pricing -> Decision -> Bayesian Evaluation

---

## What This Does

- estimate probability of default (PD) from a risk model  
- predict customer acceptance from a response model  
- evaluate multiple offers using expected value  
- select the best offer per customer  
- apply a decision policy (approve / reject / review)  
- check how stable those decisions are under uncertainty  

---

## System Structure

### Module 01 — Credit Approval

- predicts default probability  
- produces the core risk signal used across the system  

---

### Module 02 — Response Modeling

- predicts probability of accepting an offer  
- adds the behavioral component  

---

### Module 03 — Pricing Strategy

- evaluates multiple offers (APR levels)

- computes:

  - expected revenue -> upside if the loan performs  
  - expected loss -> downside if default happens  
  - expected value -> final risk-adjusted profit  

- selects the best offer per customer  

---

### Module 04 — Decision Policy

- applies business rules:

  - risk thresholds  
  - acceptance thresholds  
  - profitability requirements  

- supports multiple strategies:

  - conservative  
  - balanced  
  - aggressive  
  - aggressive_with_risk_cap  

- outputs:

  - approve  
  - reject  
  - review  

---

### Module 05 — Bayesian Decision Layer

- evaluates decisions under uncertainty  
- treats PD and acceptance as distributions, not fixed values  
- simulates outcomes and focuses on downside risk  

outputs include:

- simulated expected value  
- probability of loss  
- p05 -> bad-case outcome  
- expected shortfall -> average loss in worst cases  

this layer does not change the decision policy  
it checks how reliable the decisions are  

---

## Key Idea

this is not a set of independent models

it is a decision system:

- models -> estimate probabilities  
- pricing -> converts predictions into money  
- policy -> enforces business rules  
- Bayesian layer -> checks robustness  

Decision = f(Risk, Response, Economics)

---

## Example Insights

- acceptance is often the main bottleneck  
- high default risk quickly kills profitability  
- strong offers can offset moderate risk  
- some deals look profitable on average but fail under uncertainty  
- Bayesian layer helps detect fragile decisions  

---

## Policy Tradeoffs

- relaxing thresholds:

  - more approvals  
  - higher expected value  
  - higher risk  

- tightening thresholds:

  - fewer approvals  
  - better portfolio quality  
  - lower revenue  

---

## How to Run

run full pipeline:

python runner.py

this runs everything including:

- deterministic pipeline  
- Bayesian uncertainty + decision layer  

---

## Final Note

the system separates three things:

- prediction -> models  
- decision -> policy  
- uncertainty -> Bayesian evaluation  

this is how real credit systems are structured