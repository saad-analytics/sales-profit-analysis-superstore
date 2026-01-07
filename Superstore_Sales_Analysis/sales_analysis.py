"""
Project: Superstore Sales & Revenue Analysis
Author: Saad
Tools: Python, Pandas, NumPy, Matplotlib
"""
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
df = pd.read_csv('raw_superstore.csv',encoding='latin1')
#standardizing column names 
df.columns = df.columns.str.strip().str.lower()
#checking columns
print(df.columns.tolist())
#checking data types of columns 
print('dtypes before converting to category: ',df.dtypes)
# fixing data types of columns 
cols = df.select_dtypes(include=['object']).columns
df[cols] = df[cols].astype('category') #converting every object dtype column to category for more efficiency and speed 
print('\n dtypes after converting to category: ',df.dtypes) 
#converting order id column to string as it has unique values and no math needed 
df['order id'] = df['order id'].astype('string')
print(df['order id'].dtypes)
#converting columns: order date & ship date  into datetime format 
df = df.astype({
    'order date': 'object',
    'ship date': 'object' 
}) # converting these columns back to object type to avoid errors while converting them into datetime
date_cols = ['order date', 'ship date']
df[date_cols] = df[date_cols].apply(pd.to_datetime, errors='coerce')
print('\n',df.dtypes) #testing changes 
# Handling null values 
print(df.isnull().sum()) #there are not any null or empty values in the data 
#calculating shipping time 
df['sub_ship'] = df['ship date'] - df['order date']
print(df['sub_ship'])
#identifing which ship mode ships faster
shipping_report = df.groupby('ship mode', observed=True)['sub_ship'].mean().reset_index()
print('\n',shipping_report)
# Identifing duplicates 
# Find exact duplicate rows
duplicates = df[df.duplicated()]
print(f"Total exact duplicates: {len(duplicates)}")
#checking if row ID is truly unique z
row_id_duplicate = df['row id'].duplicated().any()
print(row_id_duplicate)
#Making a function for saving file 
def save_file(df):
    df.to_csv('cleaned_superstore.csv',index=False, float_format='%.2f')
    print('File Updated')
save_file(df)
#calculating monthly how much we earned, what's our profit and how many units we sold 
df['order month'] = df['order date'].dt.month
monthly_metrics = df.groupby('order month').agg(
    total_sales = ('sales', 'sum'),
    total_profit = ('profit', 'sum'),
    total_quantity = ('quantity', 'sum'),
    order_count = ('order id', 'nunique'),
    discounts_count = ('discount','sum')
    ).reset_index().round(2) #round(2) is used to keep the float format upto 2 decimals 
print('\n',monthly_metrics)
#calculating which product got more sales 
product_cal = df.groupby('sub-category', observed=True)['sales'].sum().sort_values(ascending=False)
print('\n')
print(product_cal)
#calculating which category got more sales 
category_cal = df.groupby('category', observed=True)['sales'].sum().sort_values(ascending=False)
print('\n')
print(category_cal)
# Adding AOV( Average Order Value ) column to justify marketing decisions more precisely 
monthly_metrics['aov'] = monthly_metrics['total_sales'] / monthly_metrics['order_count']
# Round it to 2 decimal places for a cleaner look
monthly_metrics['aov'] = monthly_metrics['aov'].round(2)
print('\n')
print(monthly_metrics[['order month', 'total_sales', 'order_count', 'aov']])
#checking which category got more orders to analize which cateogry is driving our sales with high prices 
category_an = df.groupby('category')['order id'].count()
print(category_an)
# Performing category level insights to see which product is good and which is bad for our business 
# Category insights 
category_insights = df.groupby('category',observed=True).agg(
    total_sales = ('sales', 'sum'),
    total_profit = ('profit','sum'),
    quantity_sold = ('quantity', 'sum'),
    discounts_count = ('discount','sum')
).reset_index().sort_values(ascending=False,by='total_sales')
category_insights['profit_margin'] = category_insights['total_profit'] / category_insights['total_sales']
print('\n',category_insights)
# sub-Category insights 
sub_category_insights = df.groupby('sub-category',observed=True).agg(
    total_sales = ('sales', 'sum'),
    total_profit = ('profit','sum'),
    quantity_sold = ('quantity', 'sum'),
    discounts_count = ('discount','sum')
).reset_index().sort_values(ascending=False,by='total_sales')
sub_category_insights['profit_margin'] = sub_category_insights['total_profit'] / sub_category_insights['total_sales']
print('\n',sub_category_insights)
# Customer Analysis to find VIP customer's and to understand customer's behaviour 
customers_analysis = df.groupby('customer id',observed=True).agg(
    total_sales = ('sales', 'sum'),
    total_profit = ('profit','sum'),
    quantity_sold = ('quantity', 'sum'),
    order_count = ('order id', 'nunique')
).reset_index().sort_values(ascending=False,by='total_profit')
customers_analysis['aov'] = customers_analysis['total_sales'] / customers_analysis['order_count']
customers_analysis['profit_margin'] = customers_analysis['total_profit'] / customers_analysis['total_sales']
print('\n',customers_analysis.head(10))
# updating file
save_file(df)
#Data Visualization & insights
#Order month and total sales graph
plt.figure(figsize=(8,5))
plt.plot(monthly_metrics['order month'], monthly_metrics['total_sales'])
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total sales")
plt.savefig("monthly_sales.png", bbox_inches='tight')
plt.show()
#order month and total profit chart
plt.figure(figsize=(10,7))
plt.plot(monthly_metrics['order month'], monthly_metrics['total_profit'])
plt.title("Montly Profit")
plt.xlabel("Month")
plt.ylabel("Total Profit")
plt.savefig("Monthly_Profit.png", bbox_inches='tight')
plt.show()
# Sub_Category Sales Comparison (bar chart)
plt.figure(figsize=(17,9))
plt.bar(sub_category_insights['sub-category'], sub_category_insights['total_sales'])
plt.title("Sub-Category Sales Comparison")
plt.xlabel("Sub-Category")
plt.ylabel("Total Sales")
plt.xticks(rotation=45, ha='right')
plt.savefig("sub_category_sales.png", bbox_inches='tight')
plt.show()