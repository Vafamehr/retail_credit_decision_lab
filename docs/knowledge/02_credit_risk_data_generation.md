# Credit Risk Data Generation — From Features to Outcomes

## Objective

Simulate realistic credit data where borrower features generate:

features → risk signal → probability of default → observed outcome

This mirrors real-world credit behavior.


## System Flow

Borrower Features  
→ Risk Score  
→ Probability of Default (PD)  
→ Default Outcome  


## Step 1 — Risk Score

We construct a risk signal using borrower attributes and their interactions:

- credit score  
- debt-to-income ratio  
- credit utilization  
- delinquencies  
- employment length  

The risk score is not purely linear. It includes:

- feature interactions (e.g., high utilization + low credit score)  
- non-linear effects (e.g., sharp risk increase beyond certain thresholds)  

This better reflects real-world credit behavior, where risk is rarely linear.


## Step 2 — Probability Mapping

The risk score is transformed into probability using a sigmoid function:

P(default) = 1 / (1 + exp(-risk_score))

This ensures:

- output is between 0 and 1  
- interpretable as probability  
- higher risk → higher PD  


## Step 3 — Outcome Simulation

Default is generated using a binomial process:

default ~ Binomial(1, PD)

This introduces real-world uncertainty:

- high PD → more likely to default  
- low PD → less likely, but still possible  


## Why Not Use a Threshold?

Avoid deterministic rules like:

default = PD > 0.5

Because:

- removes randomness  
- produces unrealistic data  
- eliminates overlap between good and bad borrowers  


## Key Concept

Probability ≠ Outcome

- PD = risk estimate  
- default = realized event  


## Feature Distribution Design

### Beta Distribution
Used for:
- debt_to_income  
- credit_utilization  

Reason:
- bounded between 0 and 1  
- flexible skew for realistic populations  


### Poisson Distribution
Used for:
- number of delinquencies  

Reason:
- models count of rare events  


### Binomial Distribution
Used for:
- default outcome  

Reason:
- models binary event driven by probability  


## Business Interpretation

- default = 1 → borrower failed to repay  
- default = 0 → borrower repaid  

Assumes loan has already been issued.


## Mental Model

Features  
→ Risk Signal  
→ Probability  
→ Outcome  


## Interview Framing

“We simulate credit behavior by generating a risk signal from borrower features, incorporating non-linear effects and interactions, converting it into probability using a sigmoid function, and sampling outcomes to reflect real-world uncertainty.”