# Credit Risk Data Generation — From Risk to Default

## Objective
Simulate realistic borrower behavior where features translate into probability of default and then into observed outcomes.

This mirrors how real-world credit data behaves.

---

## System Flow

features → risk score → probability → outcome

---

## Step 1 — Risk Score

We construct a risk score using borrower features such as:

- credit score  
- debt-to-income ratio  
- credit utilization  
- delinquencies  
- employment length  

The score represents overall borrower risk:

- higher score → higher risk  
- lower score → safer borrower  

---

## Step 2 — Probability of Default

The risk score is converted into probability using a sigmoid function:

P(default) = 1 / (1 + exp(-risk_score))

This ensures:

- values are between 0 and 1  
- outputs are interpretable as probabilities  
- higher risk → higher probability  

---

## Step 3 — Simulating Default

Default is generated using a binomial process:

default ~ Binomial(1, P(default))

This means:

- each borrower has a probability of default  
- the actual outcome is randomly sampled  

Examples:

- P = 0.8 → likely default, not guaranteed  
- P = 0.2 → unlikely default, but possible  

---

## Why Not Use a Threshold?

Avoid:

default = P(default) > 0.5

Because:

- it creates deterministic outcomes  
- removes real-world uncertainty  
- produces unrealistic data  

---

## Key Concept

Probability ≠ Outcome

- probability represents risk  
- outcome represents what actually happens  

---

## Feature Distribution Choices

Some features are generated using specific distributions:

### Beta Distribution
Used for:
- debt_to_income  
- credit_utilization  

Reason:
- values must be between 0 and 1  
- allows realistic skew (most borrowers are not extreme)

---

### Poisson Distribution
Used for:
- number of delinquencies  

Reason:
- models count of rare events  
- most borrowers have few delinquencies  

---

### Binomial Distribution
Used for:
- default outcome  

Reason:
- models binary events (default vs no default)  
- driven by probability  

---

## Business Interpretation

- default = 1 → borrower failed to repay  
- default = 0 → borrower repaid  

This assumes the loan has already been issued.

---

## Mental Model

Borrower Features  
→ Risk Score  
→ Probability of Default  
→ Observed Default  

---

## Interview Framing

“We simulate credit behavior by constructing a risk signal from borrower features, mapping it to probability using a sigmoid function, and sampling outcomes to reflect real-world uncertainty.”