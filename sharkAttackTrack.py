import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('attacks.csv')

print("Column Names:")
for column in data.columns:
    print(column)

for index, value in data[~data['Fatal (Y/N)'].isin(['Y', 'N', 'UNKNOWN']) & data['Fatal (Y/N)'].notnull()].iterrows():
    print("Row:", index, "Value:", value['Fatal (Y/N)'])
numeric_years = data['Year'][pd.notnull(data['Year'])]
fatal_values = data['Fatal (Y/N)'][pd.notnull(data['Year'])]
fatal_values = fatal_values.astype(str)
year_counts = data['Year'].value_counts().sort_index()
year_counts.index = year_counts.index.astype(int)
year_counts.plot(kind='bar')
plt.title('Fatal Attacks by Year')
plt.xlabel('Year')
plt.ylabel('Number of Fatal Attacks')
n = 10
plt.xticks(range(0, len(year_counts), n), year_counts.index[::n], rotation=45)
plt.tight_layout()
plt.show()


data['Date'] = data['Date'].str.replace('Reported ', '')
data = data[data['Date'].str.match(r'\d{2}-\w{3}-\d{4}$', na=False)]
data['Month'] = pd.to_datetime(data['Date'], errors='coerce').dt.month
month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
               7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
attacks_per_month = data['Month'].map(month_names).value_counts().sort_index()
attacks_per_month = attacks_per_month.reindex(month_names.values())
attacks_per_month.plot(kind='bar')
plt.title('Shark Attacks per Month')
plt.xlabel('Month')
plt.ylabel('Number of Attacks')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


filtered_data = data[data['Year'].notnull() & data['Activity'].notnull()]
filtered_data.loc[filtered_data['Activity'].isin(['Bathing', 'Wading', 'Standing']), 'Activity'] = 'Swimming'
filtered_data = filtered_data[filtered_data['Year'] >= 1850]
activity_counts = filtered_data['Activity'].value_counts()
top_activities = activity_counts.head(5).index
filtered_data = filtered_data[filtered_data['Activity'].isin(top_activities)]
activity_counts = filtered_data.groupby(['Year', 'Activity']).size().unstack(fill_value=0)
activity_counts.plot(kind='line', figsize=(12, 6))
plt.title('Trend of Shark Attacks by Top 5 Activities Over the Years (After 1850)')
plt.xlabel('Year')
plt.ylabel('Number of Shark Attacks')
plt.legend(title='Activity')
plt.grid(True)
plt.show()


# Filter out rows where age is available and 'Fatal (Y/N)' is either 'Y' or 'N'
filtered_data = data[data['Age'].notnull() & data['Fatal (Y/N)'].isin(['Y', 'N'])]
# Convert 'Age' column to numeric (assuming it's stored as strings)
filtered_data.loc[:, 'Age'] = pd.to_numeric(filtered_data['Age'], errors='coerce')
# Group the data by age and count the occurrences of 'Y' and 'N' in 'Fatal (Y/N)'
fatal_counts = filtered_data.groupby(['Age', 'Fatal (Y/N)']).size().unstack(fill_value=0)
# Plot the bar plot
fatal_counts.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title('Fatal and Non-fatal Shark Attacks by Age')
plt.xlabel('Age of Victim')
plt.ylabel('Number of Attacks')
plt.xticks(rotation=90)
# Remove the .0 after ages in the x-axis
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0f}'.format(x)))
plt.legend(title='Fatal Outcome')
plt.grid(axis='y')
plt.show()