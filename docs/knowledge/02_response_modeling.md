# Module 02 — Response Modeling (Offer Acceptance)

## 1. Problem Definition

Once a customer is approved for credit, the next question is:

Will the customer accept the offer?

This is a behavioral prediction problem focused on conversion.

---

## 2. Business Context

Banks do not make money by approving customers.

They make money when:

- customers accept offers  
- loans are booked  

Without response modeling:

- approved customers may reject offers  
- marketing spend is wasted  
- pricing decisions are blind  

With response modeling:

- target customers likely to accept  
- improve conversion rates  
- support pricing and targeting strategies  

---

## 3. Core Concept

Risk and behavior are different.

Credit Risk Model:  
P(default | customer)

Response Model:  
P(accept | customer, offer, relationship)

A customer can be:

- low risk but not interested  
- high risk but highly responsive  

Both signals must be modeled separately.

---

## 4. System Design

Pipeline:

Shared Features → Offer Simulation → Relationship Features → Behavior Simulation → Model → Evaluation

---

## 5. Data Construction

Response modeling depends on both the customer and the offer.

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

Derived from:

- loan characteristics  
- pricing assumptions  

---

### Relationship Features

- existing_customer  
- relationship_tenure  
- product_count  

Capture customer engagement and loyalty.

---

### Acceptance Simulation

A behavioral score is constructed using:

- affordability (payment_to_income)  
- pricing (interest rate)  
- risk signals  
- relationship strength  
- randomness (noise)  

Then transformed:

sigmoid(score) → response_probability

Then sampled:

accepted_offer ∈ {0,1}

---

## 6. Modeling Approach

Model:

Logistic Regression

Purpose:

Estimate probability of acceptance

Focus is on:

- clean structure  
- interpretable behavior  
- stable baseline  

---

## 7. Evaluation

### AUC

Measures ranking quality:

Ability to distinguish high vs low responders

Result:

~0.69 → realistic for behavioral modeling

---

### Calibration

Compare:

- predicted probability  
- actual acceptance rate  

Result:

Predicted ≈ Actual

This is critical for:

- campaign planning  
- expected conversion forecasting  

---

### Decile Analysis

Customers grouped into buckets by predicted probability.

Used for:

- targeting strategies  
- campaign prioritization  

Top deciles show significantly higher acceptance rates.

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

Module 01 provides:

P(default)

Module 02 provides:

P(accept)

Together they enable:

Decision = f(Risk, Response)

---

## 10. Limitations

- synthetic data  
- no causal inference  
- no optimization layer  
- simple model  

These are intentional to keep the system interpretable and modular.

---

## 11. Interview Summary

Built a response modeling system that incorporates customer, offer, and relationship features to predict acceptance probability, validated through calibration and decile analysis to support targeting and pricing decisions.

---

## 12. What Comes Next

Next step:

Combine Risk + Response + Economics

To compute:

Which offers maximize expected value

---

## Final Takeaway

This module captures how customers respond to offers.

It complements risk modeling and enables decision-making based on both behavior and economics.