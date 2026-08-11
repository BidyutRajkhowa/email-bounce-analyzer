# Email Bounce Rate Analyzer

## Project Overview
Analyzed 6 months of SMTP response data to identify the root cause of increased email bounce rates for a global support client. This project demonstrates data analysis, technical investigation, and problem-solving skills applied to a real customer support scenario.

## Problem Statement
A client reported a significant increase in email bounce rates during May 2018. Using SMTP response data spanning February to August 2018, this investigation identifies the root cause and proposes actionable solutions.

## Tools Used
- Python 3 (pandas, matplotlib)
- Data Analysis and Visualization
- SMTP Protocol Knowledge
- Root Cause Analysis Methodology

## Key Findings
- May 2018 bounce rate: **4.56%** vs normal range of **0.78% - 1.60%**
- Dominant error: **SMTP Code 554** (Transaction Failed)
- Primary affected domain: **centrum.sk**
- centrum.sk error 554 count: **1,884 in May** vs **53 in April** (35x spike)
- Error completely disappeared in June 2018

## Investigation Steps
1. Loaded and parsed SMTP response dataset (167 rows, 6 months)
2. Converted UNIX timestamps to readable dates
3. Separated success (200) and bounce error codes
4. Calculated monthly bounce rates
5. Identified May 2018 as spike month
6. Drilled into error codes — found code 554 dominant
7. Analyzed by domain — centrum.sk identified as root cause
8. Formed hypothesis and proposed solutions

## Root Cause
centrum.sk email domain experienced a temporary server-side policy or configuration change in May 2018 causing it to reject emails with SMTP 554 errors. The issue resolved itself in June suggesting a temporary change.

## Proposed Solutions
- Contact centrum.sk domain administrator
- Check if sending IP was blacklisted
- Implement email list hygiene
- Set up real-time SMTP bounce monitoring
- Use domain-level bounce rate alerts

## Files
- `analysis.py` — Python script for full investigation
- `bounce_analysis.png` — Visualization charts

## How To Run
```bash
pip install pandas matplotlib
python analysis.py
```

## Skills Demonstrated
- Data Analysis
- Python Programming
- SMTP Protocol Understanding
- Root Cause Analysis
- Data Visualization
- Technical Report Writing
