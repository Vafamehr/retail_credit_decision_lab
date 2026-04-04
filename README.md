# Retail Credit Decision Lab

## Overview

This project builds end-to-end decision systems for retail banking, starting with a credit approval system.

It converts data into business actions:

data → model → risk (PD) → decision → evaluation

---

## What This Does

- Predicts probability of default (PD) using Logistic Regression  
- Converts PD into decisions: approve / review / reject  
- Optimizes approval threshold based on a risk constraint  
- Evaluates outcomes at both model and decision level  

---

## Key Idea

This is not just a model.

It is a decision system:

- model estimates risk  
- policy makes decisions  
- evaluation measures business impact  

---

## Example Output

- AUC ≈ 0.69  
- Approval Rate ≈ 21%  
- Default Rate (Approved) ≈ 14–15%  

Clear risk separation across:
- approve (low risk)
- review (medium risk)
- reject (high risk)

---

## How to Run

python -m src.runner

---

## Why This Matters

- avoids arbitrary thresholds  
- introduces data-driven decisioning  
- separates prediction vs policy vs evaluation  
- reflects how real credit systems are structured  

---

## Next Steps

- optimize reject threshold  
- add profit / loss simulation  
- extend to pricing and credit limit decisions  