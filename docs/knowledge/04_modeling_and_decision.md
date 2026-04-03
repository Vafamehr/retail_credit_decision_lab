# Modeling and Decision System

## Overview

This module builds a complete credit decision system:

Data → Features → Model → Probability of Default (PD) → Decision → Evaluation

The goal is not just prediction, but translating predictions into business decisions.


## Model

We use Logistic Regression to estimate probability of default.

- Input: engineered features  
- Output: PD for each customer  

Training setup:

- stratified train/test split  
- scaling applied before modeling  

The model focuses on producing a well-ranked and interpretable risk signal.


## Predicted Risk (PD)

The model outputs:

PD = probability that a borrower defaults

This serves as the core input to the decision system.

Important:

PD is not a decision — it is a risk estimate.


## Decision Policy

A threshold-based policy converts PD into actions:

- Approve: PD < 0.18  
- Review: 0.18 ≤ PD < 0.32  
- Reject: PD ≥ 0.32  

This reflects how real credit systems translate risk into operational decisions.


## Evaluation Framework

We evaluate both model performance and business outcomes.


### 1. Model Performance

**AUC (Area Under ROC Curve)**

- measures ranking ability  
- evaluates how well the model separates good vs bad borrowers  


### 2. Decision Distribution

- % approved  
- % reviewed  
- % rejected  

Shows how strict or lenient the policy is.


### 3. Business Metrics

- Approval Rate = % of customers approved  
- Default Rate (Approved Only) = risk of accepted population  

This captures the key business tradeoff:

growth vs risk


### 4. Calibration

Calibration checks whether predicted probabilities match observed outcomes.

We compare:

- average predicted PD  
- actual default rate  

across risk buckets.

Good calibration means:

predicted ≈ actual

This is critical for using probabilities in decision systems.


## Key Learnings

- Model performance depends on data signal and features  
- Decision thresholds directly control business outcomes  
- Small threshold changes can significantly impact approval volume  
- Calibration is essential when using probabilities for decisions  
- Prediction and decision must be separated in system design  


## Next Steps

- threshold optimization  
- model comparison (tree-based models)  
- cost-based decision optimization  
- stability testing across multiple datasets  


## Interview Framing

“This system separates prediction from decision. The model estimates probability of default, and a policy layer converts that into actions while controlling the tradeoff between growth and risk.”