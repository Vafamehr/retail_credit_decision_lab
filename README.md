# Retail Credit Decision Lab

## Overview

This project implements an end-to-end retail credit decision system.

The focus is not just on prediction, but on turning model outputs into actual business decisions by combining risk, customer behavior, and economics.

Pipeline flow: Data -> Risk -> Response -> Pricing -> Decision, with an additional uncertainty (Bayesian) evaluation layer.

---

## What This Does

* estimates probability of default (PD) using a risk model
* predicts customer acceptance using a response model
* evaluates multiple offers using expected value
* selects the optimal offer per customer
* applies a final decision policy (approve / decline / review)
* evaluates how stable those decisions are under uncertainty

---

## System Structure

### Module 01 — Credit Approval

* predicts default risk
* produces the base risk signal used throughout the system

---

### Module 02 — Response Modeling

* predicts probability of accepting an offer
* introduces the behavioral component

---

### Module 03 — Pricing Strategy

* evaluates multiple offers (e.g., APR levels)

* computes:

  * expected revenue
  * expected loss
  * expected value

* selects the best offer per customer

---

### Module 04 — Decision Policy

* applies business constraints:

  * risk thresholds
  * acceptance thresholds
  * profitability requirements

* supports multiple strategies:

  * conservative
  * balanced
  * aggressive
  * aggressive_with_risk_cap

* produces final decisions:

  * approve (with offer)
  * decline
  * manual review

* includes rule-based reasoning and portfolio diagnostics

---

### Module 05 — Bayesian Decision Layer

* evaluates decisions under uncertainty
* treats model outputs (PD, acceptance, EV) as uncertain rather than fixed
* simulates possible outcomes and measures downside risk

This layer answers:

"How reliable is this decision if our estimates are slightly wrong?"

Outputs include:

* expected value distribution
* probability of loss
* lower-tail outcomes
* risk-aware evaluation of decisions

This layer is implemented separately and does not modify the core decision policy.

---

## Key Idea

This is not a collection of independent models.

It is a structured decision system:

* models estimate probabilities
* pricing converts predictions into economic value
* policy enforces business rules
* Bayesian layer evaluates uncertainty and risk

Decision = f(Risk, Response, Economics)

---

## Example Insights

* risk filtering removes a large portion of customers upfront
* acceptance probability is often the main bottleneck
* expected value acts as a secondary filter
* high-return offers tend to dominate approvals
* some decisions look profitable but are fragile under uncertainty

---

## Policy Tradeoffs

Sensitivity analysis shows:

* acceptance threshold strongly affects approval volume
* risk threshold controls portfolio quality

Typical behavior:

* relaxing acceptance thresholds:

  * increases approvals
  * increases total expected value
  * increases risk

* tightening acceptance thresholds:

  * reduces approvals
  * improves portfolio quality
  * reduces revenue

---

## Example Results

* approval rate ranges from near 0% to ~25% depending on policy
* expected value increases with approval volume
* average risk rises as thresholds are relaxed
* outcomes reflect tradeoffs, not a single objective

---

## How to Run

python runner.py

Bayesian layer (run separately):

python -m src.bayesian_decision.pipeline

---

## Final Note

The system separates three concerns:

* prediction (models)
* decision (policy)
* uncertainty (Bayesian evaluation)

This mirrors how real-world credit systems are designed.
