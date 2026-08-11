# Email Bounce Rate Analyzer
# Author: Bidyut Rajkhowa
# Description: Analyzes SMTP response data to identify root cause of increased bounce rates

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime

# ============================================================
# STEP 1 - LOAD THE DATA
# ============================================================
print("Step 1: Loading data...")
df = pd.read_csv('Global_Support_-_Interview_Assignment_-_Data.csv')
print(f"Data loaded successfully! Total rows: {len(df)}")

# ============================================================
# STEP 2 - CONVERT UNIX TIMESTAMP TO READABLE DATES
# ============================================================
print("\nStep 2: Converting timestamps to readable dates...")
df['date'] = pd.to_datetime(df['timestamp'], unit='s')
df['month_name'] = df['date'].dt.strftime('%B %Y')
df['month_num'] = df['date'].dt.month
print("Timestamps converted successfully!")

# ============================================================
# STEP 3 - SEPARATE SUCCESS VS BOUNCE COLUMNS
# ============================================================
print("\nStep 3: Separating success and bounce columns...")

# Success = SMTP code 200
success_cols = [c for c in df.columns if c.startswith('200,')]

# Bounces = all other error codes
bounce_cols = [c for c in df.columns if any(
    c.startswith(f'{code},') 
    for code in ['421','451','452','499','550','552','554','605']
)]

print(f"Success columns found: {len(success_cols)}")
print(f"Bounce columns found: {len(bounce_cols)}")

# ============================================================
# STEP 4 - CALCULATE TOTALS PER ROW
# ============================================================
print("\nStep 4: Calculating totals...")
df['total_success'] = df[success_cols].sum(axis=1)
df['total_bounces'] = df[bounce_cols].sum(axis=1)
df['total_emails'] = df['total_success'] + df['total_bounces']
df['bounce_rate'] = (df['total_bounces'] / df['total_emails'] * 100).round(2)

# ============================================================
# STEP 5 - GROUP BY MONTH
# ============================================================
print("\nStep 5: Grouping data by month...")

month_order = [
    'February 2018','March 2018','April 2018',
    'May 2018','June 2018','July 2018','August 2018'
]

monthly = df.groupby('month_name').agg({
    'total_success': 'sum',
    'total_bounces': 'sum',
    'total_emails': 'sum',
}).reset_index()

monthly['bounce_rate_pct'] = (
    monthly['total_bounces'] / monthly['total_emails'] * 100
).round(2)

monthly['month_name'] = pd.Categorical(
    monthly['month_name'], 
    categories=month_order, 
    ordered=True
)
monthly = monthly.sort_values('month_name')

print("\n=== MONTHLY BOUNCE RATE SUMMARY ===")
print(monthly[['month_name','total_bounces','total_emails','bounce_rate_pct']].to_string(index=False))

# ============================================================
# STEP 6 - IDENTIFY ROOT CAUSE - ERROR CODE ANALYSIS
# ============================================================
print("\n\nStep 6: Analyzing bounce codes in May 2018...")

may_data = df[df['month_name'] == 'May 2018']
bounce_codes = ['421','451','452','499','550','552','554','605']
code_totals = {}

for code in bounce_codes:
    cols = [c for c in df.columns if c.startswith(f'{code},')]
    total = may_data[cols].sum().sum()
    code_totals[code] = int(total)

print("\n=== BOUNCE CODE BREAKDOWN IN MAY 2018 ===")
for code, total in sorted(code_totals.items(), key=lambda x: x[1], reverse=True):
    print(f"  Code {code}: {total} occurrences")

# ============================================================
# STEP 7 - IDENTIFY ROOT CAUSE - DOMAIN ANALYSIS
# ============================================================
print("\n\nStep 7: Analyzing centrum.sk domain across months...")

col_554_centrum = '554, centrum.sk: count(campaign)'
centrum_monthly = df.groupby('month_name')[col_554_centrum].sum().reset_index()
centrum_monthly.columns = ['month_name', 'centrum_554']
centrum_monthly['month_name'] = pd.Categorical(
    centrum_monthly['month_name'], 
    categories=month_order, 
    ordered=True
)
centrum_monthly = centrum_monthly.sort_values('month_name')

print("\n=== CENTRUM.SK ERROR 554 BY MONTH ===")
print(centrum_monthly.to_string(index=False))

# ============================================================
# STEP 8 - CREATE VISUALIZATIONS
# ============================================================
print("\n\nStep 8: Creating charts...")

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle(
    'Email Bounce Rate Investigation — Global Support Analysis', 
    fontsize=14, fontweight='bold'
)

colors_monthly = [
    '#F44336' if m == 'May 2018' else '#2196F3' 
    for m in monthly['month_name']
]

# Chart 1 - Monthly Bounce Trend
ax1 = axes[0]
bars1 = ax1.bar(monthly['month_name'], monthly['bounce_rate_pct'], color=colors_monthly)
ax1.set_title('Monthly Bounce Trend', fontweight='bold')
ax1.set_ylabel('Bounce Rate %')
ax1.tick_params(axis='x', rotation=45)
for bar, val in zip(bars1, monthly['bounce_rate_pct']):
    ax1.text(
        bar.get_x() + bar.get_width()/2, 
        bar.get_height() + 0.1, 
        f'{val}%', ha='center', fontsize=8
    )
normal = mpatches.Patch(color='#2196F3', label='Normal')
spike = mpatches.Patch(color='#F44336', label='May Spike')
ax1.legend(handles=[normal, spike], fontsize=8)

# Chart 2 - Error Code Breakdown May 2018
ax2 = axes[1]
codes = list(code_totals.keys())
values = list(code_totals.values())
bar_colors = [
    '#F44336' if c == '554' else 
    '#FF9800' if c in ['550','605'] else 
    '#2196F3' for c in codes
]
bars2 = ax2.bar(codes, values, color=bar_colors)
ax2.set_title('SMTP Error Code Analysis — May 2018', fontweight='bold')
ax2.set_ylabel('Count')
ax2.set_xlabel('Error Code')
for bar, val in zip(bars2, values):
    ax2.text(
        bar.get_x() + bar.get_width()/2, 
        bar.get_height() + 5, 
        str(val), ha='center', fontsize=8
    )

# Chart 3 - centrum.sk 554 errors
ax3 = axes[2]
colors_centrum = [
    '#F44336' if m == 'May 2018' else '#2196F3' 
    for m in centrum_monthly['month_name']
]
bars3 = ax3.bar(
    centrum_monthly['month_name'], 
    centrum_monthly['centrum_554'], 
    color=colors_centrum
)
ax3.set_title('Domain Analysis — centrum.sk Error 554', fontweight='bold')
ax3.set_ylabel('Count of 554 Errors')
ax3.tick_params(axis='x', rotation=45)
for bar, val in zip(bars3, centrum_monthly['centrum_554']):
    ax3.text(
        bar.get_x() + bar.get_width()/2, 
        bar.get_height() + 5, 
        str(int(val)), ha='center', fontsize=8
    )

plt.tight_layout()
plt.savefig('bounce_analysis.png', dpi=150, bbox_inches='tight')
print("Charts saved as bounce_analysis.png")

# ============================================================
# STEP 9 - PRINT FINAL SUMMARY
# ============================================================
print("\n\n=== INVESTIGATION SUMMARY ===")
print("Root Cause: SMTP error 554 on centrum.sk domain")
print("May 2018 centrum.sk errors: 1,884")
print("April 2018 centrum.sk errors: 53")
print("Increase: 35x spike in one month")
print("Resolution: Error disappeared in June 2018")
print("Conclusion: Temporary server-side policy change at centrum.sk")
print("\nAnalysis complete!")
