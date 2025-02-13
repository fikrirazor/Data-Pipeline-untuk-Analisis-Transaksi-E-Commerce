#!/usr/bin/env python
# coding: utf-8

# # Instalasi Package

# In[1]:


# Install package dasar
get_ipython().system('pip install pandas numpy matplotlib seaborn')

# Install Kaggle API (untuk download dataset dari Kaggle)
#!pip install kaggle

# Install library tambahan (jika diperlukan)
#!pip install openpyxl sqlalchemy kagglehub
get_ipython().system('pip install kagglehub')


# # Input Data

# In[7]:


import kagglehub
import os
import pandas as pd

# Download latest version
path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")

print("Path to dataset files:", path)


# In[8]:


# List semua file di direktori dataset
files = os.listdir(path)
print("Daftar file yang tersedia:", files)


#  # Data Scheme
#  <img src="https://i.imgur.com/HRhd2Y0.png" alt="data-scheme" width="1000"/>
# 

# In[64]:


"""
# Contoh: Baca file orders
orders_path = os.path.join(path, "olist_orders_dataset.csv")
orders_df = pd.read_csv(orders_path)

# Contoh: Baca file products
products_path = os.path.join(path, "olist_products_dataset.csv")
products_df = pd.read_csv(products_path)

print("Orders Data:")
print(orders_df.head())
"""


# In[10]:


# List semua file CSV
csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]

# Baca semua CSV ke dictionary of DataFrames
dataframes = {}
for file in csv_files:
    df_name = file.replace("olist_", "").replace("_dataset.csv", "")
    dataframes[df_name] = pd.read_csv(os.path.join(path, file))


# # Mengetahui kata kunci data

# In[12]:


for key in dataframes:
    print(key)


# In[16]:


# Contoh: Ambil data orders dan customers
customers = dataframes['customers']
geolocation = dataframes['geolocation']
orders = dataframes['orders']
order_items = dataframes['order_items']
order_payments = dataframes['order_payments']
order_reviews = dataframes['order_reviews']
products = dataframes['products']
sellers = dataframes['sellers']
product_category_name = dataframes['product_category_name_translation.csv']
# Gabungkan data orders dan customers
#merged_data = pd.merge(orders, customers, on='customer_id', how='left')
#print(merged_data.head())


# In[35]:


orders.head()


# In[36]:


# Menggabungkan dataset order dengan customer
merged_data = pd.merge(orders, customers, on="customer_id", how="left")

# Menggabungkan dataset order dengan items
merged_data = pd.merge(merged_data, orders, on="order_id", how="inner")

merged_data = pd.merge(merged_data, order_items, on="order_id", how="inner")

# Menggabungkan dataset items dengan products
merged_data = pd.merge(merged_data, products, on="product_id", how="left")

# Menggabungkan dataset items dengan sellers
merged_data = pd.merge(merged_data, sellers, on="seller_id", how="left")

# Menggabungkan dataset orders dengan payments
merged_data = pd.merge(merged_data, order_payments, on="order_id", how="left")

# Menggabungkan dataset orders dengan reviews
merged_data = pd.merge(merged_data, order_reviews, on="order_id", how="left")


# In[37]:


merged_data.head()


# In[38]:


# Contoh: Membersihkan data orders
# Handle missing values
orders.dropna(subset=['order_status'], inplace=True)

# Konversi tipe data
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

# Filter data yang relevan (contoh: hanya pesanan yang sudah terkirim)
completed_orders = orders[orders['order_status'] == 'delivered']


# In[40]:


# Contoh KPI:
# - Total penjualan per bulan
merged_data['order_purchase_timestamp_x'] = pd.to_datetime(merged_data['order_purchase_timestamp_x'])
merged_data['purchase_month_x'] = merged_data['order_purchase_timestamp_x'].dt.to_period('M')
monthly_sales = merged_data.groupby('purchase_month_x')['price'].sum()


# In[41]:


monthly_sales


# In[42]:


top_products = product_category_name.value_counts().head(10)


# In[43]:


import matplotlib.pyplot as plt
import seaborn as sns

# Contoh visualisasi tren penjualan bulanan
plt.figure(figsize=(12, 6))
sns.lineplot(x=monthly_sales.index.astype(str), y=monthly_sales.values)
plt.title('Tren Penjualan Bulanan')
plt.xlabel('Bulan')
plt.ylabel('Total Penjualan (R$)')
plt.xticks(rotation=45)
plt.show()


# In[ ]:




