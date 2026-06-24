# Data Dictionary

## Dataset Overview
This document describes all variables in the customer purchase behavior dataset.

---

## Features

### 1. **Customer_ID** (Integer)
- **Type**: Identifier
- **Description**: Unique identifier for each customer
- **Range**: 1001-1500
- **Missing Values**: None
- **Notes**: Primary key

### 2. **Age** (Numeric)
- **Type**: Integer
- **Description**: Age of the customer in years
- **Range**: 22-65 years
- **Mean**: 41.2 years
- **Std Dev**: 12.5 years
- **Missing Values**: None
- **Interpretation**: Represents customer lifecycle stage

### 3. **Gender** (Categorical)
- **Type**: String
- **Description**: Gender of the customer
- **Categories**: Male, Female, Other
- **Distribution**: 52% Male, 46% Female, 2% Other
- **Missing Values**: None

### 4. **Monthly_Spending** (Numeric)
- **Type**: Float
- **Description**: Average monthly spending in USD
- **Range**: $50-$2,500
- **Mean**: $450.75
- **Std Dev**: $380.25
- **Missing Values**: None
- **Interpretation**: Primary metric for customer value

### 5. **Annual_Income** (Numeric)
- **Type**: Float
- **Description**: Annual household income in USD
- **Range**: $20,000-$250,000
- **Mean**: $85,500
- **Std Dev**: $52,300
- **Missing Values**: None
- **Interpretation**: Socioeconomic indicator

### 6. **Email_Frequency** (Numeric)
- **Type**: Integer
- **Description**: Number of marketing emails received per month
- **Range**: 0-20
- **Mean**: 8.3
- **Std Dev**: 4.1
- **Missing Values**: None
- **Interpretation**: Engagement metric

### 7. **Purchase_Frequency** (Numeric)
- **Type**: Integer
- **Description**: Number of purchases made per year
- **Range**: 1-24
- **Mean**: 8.5
- **Std Dev**: 5.2
- **Missing Values**: None
- **Interpretation**: Customer loyalty indicator

### 8. **Customer_Since** (Date)
- **Type**: Date
- **Description**: Date when customer account was created
- **Range**: 2015-2024
- **Format**: YYYY-MM-DD
- **Missing Values**: None
- **Interpretation**: Customer tenure (used to calculate days as customer)

### 9. **Region** (Categorical)
- **Type**: String
- **Description**: Geographic region of customer
- **Categories**: North, South, East, West, Central
- **Distribution**: North (25%), South (22%), East (20%), West (18%), Central (15%)
- **Missing Values**: None

### 10. **Churn_Status** (Binary)
- **Type**: Boolean/Integer
- **Description**: Whether customer has churned
- **Values**: 0 (Active), 1 (Churned)
- **Distribution**: 72% Active, 28% Churned
- **Missing Values**: None
- **Interpretation**: Retention metric

---

## Data Quality Notes

### Completeness
- **Overall**: 100% complete
- No missing values detected
- All required fields populated

### Accuracy
- Age ranges validated (18-99)
- Income values checked for outliers
- Spending amounts verified as positive values
- Dates validated within reasonable range

### Consistency
- All categorical values standardized
- Numeric values within expected ranges
- No duplicate Customer_IDs
- Date formats uniform

---

## Summary Statistics

| Feature | Count | Mean | Std Dev | Min | 25% | 50% | 75% | Max |
|---------|-------|------|---------|-----|-----|-----|-----|-----|
| Age | 500 | 41.2 | 12.5 | 22 | 32 | 41 | 51 | 65 |
| Monthly_Spending | 500 | 450.75 | 380.25 | 50 | 200 | 350 | 650 | 2500 |
| Annual_Income | 500 | 85500 | 52300 | 20000 | 45000 | 75000 | 120000 | 250000 |
| Email_Frequency | 500 | 8.3 | 4.1 | 0 | 5 | 8 | 11 | 20 |
| Purchase_Frequency | 500 | 8.5 | 5.2 | 1 | 4 | 8 | 12 | 24 |

---

## Feature Relationships

### Strong Correlations
- Monthly_Spending ↔ Annual_Income (r = 0.72)
- Purchase_Frequency ↔ Email_Frequency (r = 0.78)
- Age ↔ Monthly_Spending (r = 0.65)

### Weak Correlations
- Gender ↔ Monthly_Spending (r = 0.12)
- Region ↔ Churn_Status (r = -0.18)

---

## Data Entry Rules
- Age: Integers only, range 18-99
- Income: Positive floats, divisible by 100
- Spending: Positive floats, max $3,000/month
- Frequency: Non-negative integers
- Dates: ISO format (YYYY-MM-DD)
- Categories: Predefined values only

---

## Update Frequency
Dataset is updated monthly with new transaction data and customer information.

**Last Updated**: June 2026  
**Next Update**: July 2026
