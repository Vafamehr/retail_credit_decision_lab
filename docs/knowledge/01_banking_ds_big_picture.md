# Banking Data Science: Big Picture

## Objective
Understand how data science is used in retail credit decisioning.

At a high level, the goal is:

Decide whether to approve a loan while balancing risk and growth.

---

## Core Problem

Given a loan applicant:

- Should we approve the loan?
- What is the risk of default?
- How do we control losses while enabling business growth?

---

## End-to-End System

A simplified credit decision system follows this flow:

Applicant Data → Risk Model → Probability of Default → Decision Policy → Business Outcome

---

## Key Components

### 1. Applicant Data (Features)

Information about the borrower:

- income  
- credit score  
- debt-to-income ratio  
- credit utilization  
- delinquencies  
- employment history  

---

### 2. Risk Model

A model estimates:

Probability of Default (PD)

---

### 3. Decision Policy

Business rules convert probability into decisions:

- low risk → APPROVE  
- medium risk → REVIEW  
- high risk → REJECT  

---

### 4. Business Outcome

Each decision has consequences:

- Approved + good borrower → profit  
- Approved + bad borrower → loss  
- Rejected + good borrower → missed opportunity  

---

## Core Tradeoff

Risk vs Growth

- Being too strict → lose customers  
- Being too lenient → increase defaults  

---

## Key Concepts

### Default
- borrower fails to repay the loan  
- represents a loss event  

### Probability of Default (PD)
- likelihood that borrower will default  
- output of the model  

### Decision vs Prediction

- Model → predicts risk  
- Policy → makes decision  

These are NOT the same.

---

## Mental Model

We do NOT predict decisions.  
We predict risk, then apply business rules.

---

## What This Project Builds

This project simulates:

- realistic borrower data  
- risk estimation (PD)  
- decision policy  
- evaluation of outcomes  

---

## Interview Framing

“This system separates prediction from decision. We estimate probability of default using borrower features, then apply policy thresholds to control risk while maintaining business growth.”