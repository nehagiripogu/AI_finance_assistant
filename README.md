# AI-Powered Personal Finance Assistant

An AI-powered personal finance assistant built using **Flask** that helps users manage their expenses, analyze spending patterns, generate budgets, and receive financial insights. The system also includes a chatbot for financial queries and supports exporting reports in PDF and Excel formats.

---

## Features

- User authentication (Register / Login / Logout)
- Expense tracking and management
- Automatic expense categorization
- Spending analysis using visual charts
- Budget recommendations based on spending habits
- Financial health score calculation
- AI-based financial insights
- Interactive chatbot for financial queries
- Downloadable financial reports (PDF & Excel)

---

## Tech Stack

**Backend**
- Python
- Flask
- Flask-SQLAlchemy

**Frontend**
- HTML
- Bootstrap
- Chart.js

**Database**
- SQLite

**Reporting Tools**
- ReportLab (PDF generation)
- OpenPyXL (Excel reports)

---
## Functional Modules

### 1. User Authentication
Users can register, log in, and securely access their financial dashboard.

### 2. Expense Tracking
Users can add and manage daily expenses with details such as:
- Category
- Amount
- Date
- Description

### 3. Automated Expense Categorization
The system automatically classifies expenses into categories based on keywords.

### 4. Financial Insights
The system analyzes spending patterns and generates helpful financial suggestions.

### 5. Budget Recommendation
Based on spending behavior, the assistant suggests recommended budgets for each category.

### 6. Financial Health Score
A score out of **100** is calculated to represent how balanced the user's spending habits are.

### 7. Chatbot Assistant
Users can ask questions like:
- Total spending
- Highest spending category
- Expense categories

### 8. Financial Reports
Users can download their financial data as:
- PDF reports
- Excel reports

---

## Future Improvements

- Integration with banking APIs  
- Advanced AI-based financial recommendations  
- Monthly and weekly spending trend analysis  
- Mobile application version  
- Secure password hashing and encryption

## Project Structure

```AI_finance_assistant/
│
├── app.py
├── models.py
├── chatbot.py
├── budget.py
│
├── templates/
│ ├── dashboard.html
│ ├── login.html
│ ├── register.html
│ ├── add_transaction.html
│ └── reports.html
│
├── static/
│
├── requirements.txt
└── SRS.md
---

  
