import pandas as pd
import mysql.connector
import warnings

warnings.filterwarnings("ignore")

# Step 1: Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='your_password',   # Replace with your MySQL password
    database='ip_project'
)

# Step 2: Read data into DataFrame
query = "SELECT * FROM compound_data;"
df = pd.read_sql(query, conn)

# Step 3: Close connection
conn.close()

# Step 4: Print the DataFrame
print("📄 DataFrame content:")
print(df)

# Step 5: Export DataFrame to CSV
df.to_csv('compound_data.csv', index=False)

print("\n✅ CSV file 'compound_data.csv' saved successfully.")