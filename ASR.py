import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv('F:/Internship inobyte/Amazon Sale Report.csv',encoding='unicode_escape')
df.isnull().sum()
# Dropping below columns due to null values exceeding 80%
df=df.drop(columns=['New','PendingS','fulfilled-by'])
# replacing currency na values using mode
mode_value = df['currency'].mode()[0]
df['currency'].fillna(mode_value,inplace=True)
#replacing amount na alues with 0 because delivey is cancelled or on the way
df['Amount'].fillna(0,inplace=True)
df=df.dropna()
df.isnull().sum()
df['Date']=pd.to_datetime(df['Date'])

df['year']=df['Date'].dt.year
df['month']=df['Date'].dt.month
summary_stats=df.describe()


# Aggregate sales data by year and month
monthly_sales = df.groupby(['year', 'month']).agg({'Amount': 'sum', 'Order ID': 'count'}).reset_index()
monthly_sales['date'] = pd.to_datetime(monthly_sales[['year', 'month']].assign(day=1))

# Plot monthly sales trends
plt.figure(figsize=(12, 6))
sns.lineplot(x='date', y='Amount', data=monthly_sales)
plt.title('Monthly Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Sales Amount')
plt.show()


# Category Distribution
category_sales = df.groupby('Category').agg({'Amount': 'sum', 'Order ID': 'count'}).reset_index()

plt.figure(figsize=(12, 6))
sns.barplot(x='Amount', y='Category', data=category_sales)
plt.title('Sales by Product Category')
plt.xlabel('Sales Amount')
plt.ylabel('Product Category')
plt.show()

# Fulfillment Methods
fulfillment_methods = df.groupby('Fulfilment').agg({'Order ID': 'count'}).reset_index()

plt.figure(figsize=(12, 6))
sns.barplot(x='Order ID', y='Fulfilment', data=fulfillment_methods)
plt.title('Orders by Fulfillment Method')
plt.xlabel('Number of Orders')
plt.ylabel('Fulfillment Method')
plt.show()

# Aggregate data to find total amount spent and total orders per customer
customer_behavior = df.groupby('Order ID').agg({
    'Amount': 'sum',
    'Order ID': 'count'
}).rename(columns={'Order ID': 'total_orders'}).reset_index()



# Customer Segmentation based on geographical location
geographical_sales = df.groupby(['ship-state', 'ship-city']).agg({'Amount': 'sum', 'Order ID': 'count'}).reset_index()

plt.figure(figsize=(12, 6))
sns.barplot(x='Amount', y='ship-state', data=geographical_sales)
plt.title('Sales by State')
plt.xlabel('Sales Amount')
plt.ylabel('State')
plt.show()

# Analyze sales distribution across different regions
plt.figure(figsize=(12, 6))
sns.barplot(x='Amount', y='ship-city', data=geographical_sales.sort_values(by='Amount', ascending=False).head(10))
plt.title('Top 10 Cities by Sales Amount')
plt.xlabel('Sales Amount')
plt.ylabel('City')
plt.show()


state_sales = df.groupby('ship-state').agg({'Amount': 'sum', 'Order ID': 'count'}).reset_index()
state_sales = state_sales.rename(columns={'Amount': 'Total Sales', 'Order ID': 'Total Orders'})

# Sort by Total Sales and get the top 10 states
top_10_states = state_sales.sort_values(by='Total Sales', ascending=False).head(10)

# Plot top 10 states by sales amount
plt.figure(figsize=(12, 6))
sns.barplot(x='Total Sales', y='ship-state', data=top_10_states)
plt.title('Top 10 States by Sales Amount')
plt.xlabel('Total Sales Amount')
plt.ylabel('State')
plt.show()

# finally exporting clean data to csv for visualization

df.to_csv('cleaned_sales_report.csv', index=False)