# Module 02 — Response Modeling (Offer Acceptance)

## 1. Problem Definition

Once a customer is approved for credit, the next question is:

Will the customer accept the offer?

This is a behavioral prediction problem focused on conversion.

---

## 2. Business Context

Banks do not make money by approvals alone.

They make money when:

- customers accept offers  
- loans are booked  

Without response modeling:

- approved customers may reject offers  
- marketing spend is inefficient  
- pricing decisions lack feedback  

With response modeling:

- focus on customers likely to convert  
- improve acceptance rates  
- support pricing and targeting decisions  

---

## 3. Core Concept

Risk and behavior are separate signals.

Credit Risk Model:  
P(default | customer)

Response Model:  
P(accept | customer, offer, relationship)

A customer can be:

- low risk but not interested  
- higher risk but highly responsive  

Both must be modeled independently.

---

## 4. System Design

Pipeline:

Shared Features -> Offer Simulation -> Relationship Features -> Behavior Simulation -> Model -> Evaluation

---

## 5. Data Construction

Response depends on both the customer and the offer.

### Customer Features

- credit score  
- income  
- DTI  
- utilization  
- delinquencies  

---

### Offer Features

- offered_interest_rate  
- estimated_monthly_payment  
- payment_to_income_ratio  

These reflect pricing and affordability.

---

### Relationship Features

- existing_customer  
- relationship_tenure  
- product_count  

These capture engagement and familiarity.

---

### Acceptance Simulation

Behavior is constructed using:

- affordability -> payment-to-income  
- pricing -> interest rate  
- risk signals  
- relationship strength  
- randomness  

Then transformed:

sigmoid(score) -> response_probability  

Then sampled:

accepted_offer ∈ {0, 1}

---

## 6. Modeling Approach

Model:

Logistic Regression

Purpose:

Estimate probability of acceptance

Focus:

- interpretability  
- stable baseline behavior  
- clean separation from risk model  

---

## 7. Evaluation

### AUC

Measures ranking ability:

How well the model separates high vs low responders

Result:

~0.69 -> realistic for this type of problem

---

### Calibration

Compare:

- predicted probability  
- actual acceptance rate  

Result:

Predicted ≈ Actual

This is important for forecasting conversion.

---

### Decile Analysis

Customers grouped by predicted probability.

Used for:

- targeting campaigns  
- prioritizing outreach  

Top deciles show higher acceptance rates.

---

## 8. Outputs

- acceptance probability per customer  
- calibrated predictions  
- decile segmentation  
- trained model artifacts  

Stored in:

artifacts/response_modeling/

---

## 9. Role in System

Module 01:

P(default)

Module 02:

P(accept)

Together:

Decision = f(Risk, Response)

---

## 10. Limitations

- synthetic data  
- no causal modeling  
- no optimization layer  
- simple model  

These keep the system interpretable and modular.

---

## 11. Interview Summary

Built a response model using customer, offer, and relationship features to estimate acceptance probability, validated through calibration and decile analysis, and used to support targeting and pricing decisions.

---

## 12. What Comes Next

Next step:

Combine Risk + Response + Economics

to determine which offers are worth making.

---

## Final Takeaway

This module captures customer behavior.

It complements risk modeling and enables decisions based on both likelihood of default and likelihood of acceptance.