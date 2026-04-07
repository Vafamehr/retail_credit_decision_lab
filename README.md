# Retail Credit Decision Lab

## Overview

This project implements an end-to-end retail credit decision system.

The goal is not just prediction, but **decision-making** — combining risk, customer behavior, and economics into actionable outcomes.

Core flow:

Data → Risk → Response → Pricing → Decision

---

## What This Does

- estimates probability of default (PD) using a risk model  
- predicts customer acceptance using a response model  
- evaluates multiple offers using expected value  
- selects the optimal offer (or no-offer) per customer  
- applies a final decision policy (approve / decline / review)  
- analyzes portfolio outcomes and policy tradeoffs  

---

## System Structure

### Module 01 — Credit Approval
- predicts default risk  
- applies approval threshold under risk constraints  
- produces base risk signal  

---

### Module 02 — Response Modeling
- simulates offers and behavioral features  
- predicts acceptance probability  
- evaluated using calibration and decile analysis  

---

### Module 03 — Pricing Strategy
- adjusts risk per offer  
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

- produces final decisions:
  - approve (with offer)  
  - decline  
  - manual review  

- generates portfolio diagnostics and decision reasoning  

---

## Key Idea

This is not a collection of models.

It is a structured decision system:

- models estimate probabilities  
- logic combines signals  
- policy enforces constraints  
- system produces actions  

Decision = f(Risk, Response, Economics)

---

## Example Insights

- risk filtering removes a large portion of the population upfront  
- acceptance probability is a major bottleneck even for viable customers  
- expected value acts as a secondary filter  
- high-APR offers dominate approvals due to profitability pressure  

---

## Policy Tradeoffs

Sensitivity analysis shows:

- acceptance threshold is the primary driver of approval volume  
- risk threshold acts as a secondary control on portfolio quality  

Key behavior:

- relaxing acceptance threshold:
  - increases approval rate significantly  
  - increases total expected value  
  - increases portfolio risk  

- tightening acceptance threshold:
  - sharply reduces approvals  
  - improves portfolio quality  
  - reduces revenue  

---

## Example Results

- approval rate ranges from near 0% to ~25% depending on policy  
- expected value scales significantly with approval volume  
- average risk increases gradually with relaxed risk thresholds  
- portfolio outcomes emerge from tradeoffs, not a single objective  

---

## How to Run

```bash
python runner.py