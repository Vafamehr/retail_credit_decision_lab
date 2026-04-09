# Bayesian Uncertainty & Risk Evaluation — Knowledge Guide

## Overview

Up to this point, decisions are based on point estimates:

- p_default  
- p_accept  
- expected_value  

This assumes predictions are exact.

This module removes that assumption.

Instead of single values, we treat probabilities as uncertain and evaluate how decisions behave under variation.

---

## Core Idea

Replace:

p_default = 0.20  

with:

p_default ~ distribution

Same for:

p_accept

This allows us to simulate many possible realities instead of trusting one number.

---

## Why This Matters

Two customers can look identical:

- same expected value  
- same predicted probabilities  

But:

- one is stable  
- one is highly uncertain  

Point-estimate systems treat them equally.  
This layer separates them.

---

## Beta Distribution (Used for Uncertainty)

We model probabilities using Beta distributions.

Definition:

Beta(alpha, beta)

- alpha -> strength of "success" belief  
- beta -> strength of "failure" belief  

Mean:

mean = alpha / (alpha + beta)

---

## Interpretation

Think of:

alpha + beta -> confidence  
alpha / (alpha + beta) -> estimated probability  

Examples:

- alpha = beta = 1 -> uniform (maximum uncertainty)  
- alpha = beta = 0.5 -> U-shaped (extreme outcomes likely)  
- alpha = beta > 1 -> symmetric, centered around 0.5  
- alpha > beta -> skew toward 1 (higher probability)  
- beta > alpha -> skew toward 0  

---

## Important Clarification

alpha and beta are NOT actual observation counts.

They behave like pseudo-counts.

- higher values -> tighter distribution (more confidence)  
- lower values -> wider spread (more uncertainty)  

---

## How We Use It

Given a predicted probability:

p = 0.3  

We construct:

alpha = p × concentration  
beta  = (1 − p) × concentration  

Where:

concentration controls uncertainty

- high concentration -> narrow distribution  
- low concentration -> wide distribution  

---

## Simulation Process

For each customer:

1. sample p_default from Beta  
2. sample p_accept from Beta  
3. recompute expected value  

Repeat thousands of times.

Result:

a distribution of possible outcomes

---

## Expected Value Under Uncertainty

Each simulation produces:

EV = p_accept × [(1 − p_default) × revenue − p_default × loss]

Instead of one EV, we get many EVs.

---

## Key Metrics

### 1. Mean EV

Average outcome across simulations

Used as baseline profitability

---

### 2. Probability of Loss

Fraction of simulations where:

EV < 0

Measures:

how often the decision fails

---

### 3. p05 (Value at Risk)

5th percentile of EV

Interpretation:

"Typical bad-case outcome"

This is similar to VaR.

---

### 4. Expected Shortfall (CVaR)

Average of worst 5% outcomes

Interpretation:

"When things go wrong, how bad does it get?"

This is more informative than p05.

---

## VaR vs CVaR (Key Difference)

VaR (p05):

- gives a threshold  
- ignores severity beyond that point  

CVaR (Expected Shortfall):

- measures depth of losses  
- captures tail risk  

Example:

Two cases with same p05:

- Case A: [-50, -52, -55]  
- Case B: [-50, -200, -500]  

Same p05, very different risk.

CVaR distinguishes them.

---

## Tail Concept

Tail = extreme outcomes

Lower tail (left side):

- worst scenarios  
- losses  

Upper tail:

- best-case outcomes  

In credit systems, focus is on lower tail.

---

## How to Read a Row

For each decision:

1. simulated_ev_mean -> is it profitable?  
2. prob_ev_negative -> how often do we lose?  
3. simulated_ev_p05 -> what is a bad-case loss?  
4. expected_shortfall -> how severe are losses?  
5. simulated_pd_p95 -> how high can risk spike?  

---

## No Offer Case

no_offer is a baseline:

- no revenue  
- no loss  
- no uncertainty  

All values should be zero.

Used as comparison reference.

---

## What This Changes

Before:

- decisions based on average  

After:

- decisions based on risk distribution  

---

## Common Patterns

- high mean EV + high loss probability -> fragile decision  
- moderate EV + low downside -> stable decision  
- low EV + high uncertainty -> reject  

---

## Key Insight

Average outcome is not enough.

Risk is about what happens when things go wrong.

---

## Final Takeaway

This layer turns:

"Is this profitable?"

into:

"Is this safe enough to take?"

It introduces risk awareness into decision-making without changing the core system.