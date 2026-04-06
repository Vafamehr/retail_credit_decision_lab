# Retail Credit Decision Lab

## Overview

This project builds an end-to-end decision system for retail banking.

It focuses on converting predictions into business decisions using risk, customer behavior, and economic logic.

Core flow:

Data, Risk, Response, Pricing, Decision

---

## What This Does

- estimates probability of default (PD) using a risk model  
- predicts customer acceptance using a response model  
- combines risk, response, and cost structure into expected value  
- selects the best offer or no-offer per customer  
- evaluates outcomes at both model and decision level  

---

## System Structure

### Module 01 — Credit Approval
- predicts default risk  
- optimizes threshold under a default constraint  
- produces approve / reject / review decisions  

### Module 02 — Response Modeling
- simulates offers and behavioral signals  
- predicts acceptance probability  
- evaluated using calibration and decile analysis  

### Module 03 — Pricing Strategy
- adjusts risk per offer  
- computes expected value using margin, loss, and cost  
- selects optimal offer or no-offer decision  

---

## Key Idea

This is not a collection of models.

It is a structured decision system:

- models estimate probabilities  
- logic combines signals  
- system produces actions  

Decision = f(Risk, Response, Economics)

---

## Example Results

- controlled default rate around 15% on approved population  
- response model AUC around 0.69 with good calibration  
- high interest offers produce strongest profitability  
- mid-level offers balance acceptance and margin  
- low-rate offers often fail economic viability  
- large portion of customers correctly filtered into no-offer  

---

## How to Run

```bash
python runner.py