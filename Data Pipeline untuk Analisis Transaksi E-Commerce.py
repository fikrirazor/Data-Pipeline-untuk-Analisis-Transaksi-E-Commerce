#!/usr/bin/env python
# coding: utf-8

# # Instalasi Package

# In[60]:


# Install package dasar
get_ipython().system('pip install pandas numpy matplotlib seaborn')

# Install Kaggle API (untuk download dataset dari Kaggle)
#!pip install kaggle

# Install library tambahan (jika diperlukan)
#!pip install openpyxl sqlalchemy kagglehub
get_ipython().system('pip install kagglehub')


# # Inisialisasi

# In[101]:


import kagglehub
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3


# # Input Data

# In[61]:


# Download latest version
path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")

print("Path to dataset files:", path)


# In[62]:


# List semua file di direktori dataset
files = os.listdir(path)
print("Daftar file yang tersedia:", files)


#  # Data Scheme
#  Schema data ini menunjukan relasi dari data yang ada untuk digunakan sebagai panduan untuk menggabungkan data.
#  <img src="https://i.imgur.com/HRhd2Y0.png" alt="data-scheme" width="1000"/>
# 

# In[63]:


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


# In[64]:


# List semua file CSV
csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]

# Baca semua CSV ke dictionary of DataFrames
dataframes = {}
for file in csv_files:
    df_name = file.replace("olist_", "").replace("_dataset.csv", "")
    dataframes[df_name] = pd.read_csv(os.path.join(path, file))


# # Mengetahui kata kunci data

# In[65]:


for key in dataframes:
    print(key)


# In[66]:


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


# Mengetahui seperti apa data dari order:

# In[67]:


orders.head()


# In[68]:


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


# In[69]:


merged_data.head()


# # Hitung Penjualan Bulanan dan Identifikasi Bulan Tertinggi/Rendah
# Menghitung penjualan bulanan bertujuan untuk mengetahui kapan penjualan paling tinggi dan paling rendah revenunya berdasarkan per bulannya

# In[102]:


# Melihat column apa saja yang ada pada order data
list(orders.columns)


# In[72]:


orders.head(5)


# In[73]:


def calculate_order(orders_data, orders_item_data, times='M'):
    # Menggabungkan (merge) dataset order_items dengan orders berdasarkan kolom "order_id".
    # Menggunakan inner join, sehingga hanya baris yang memiliki "order_id" yang sama di kedua dataset yang akan dipertahankan.
    merged_data = pd.merge(orders_item_data, orders_data, on="order_id", how="inner")
    
    # Mengonversi kolom 'order_purchase_timestamp' menjadi format datetime.
    # Parameter errors='coerce' akan mengubah nilai yang tidak bisa dikonversi menjadi NaT (Not a Time).
    merged_data['order_purchase_timestamp'] = pd.to_datetime(merged_data['order_purchase_timestamp'], errors='coerce')
    
    # Menghapus baris-baris yang memiliki nilai kosong (missing values) pada kolom 'order_purchase_timestamp' dan 'price'.
    # Hal ini penting agar perhitungan penjualan tidak terganggu oleh data yang tidak lengkap.
    merged_data = merged_data.dropna(subset=['order_purchase_timestamp', 'price'])
    
    # Mengonversi kolom 'price' menjadi tipe numerik agar operasi matematis (penjumlahan) dapat dilakukan.
    # Jika ada nilai yang tidak bisa dikonversi, akan diubah menjadi NaN.
    merged_data['price'] = pd.to_numeric(merged_data['price'], errors='coerce')
    
    # Menghapus baris yang memiliki nilai NaN pada kolom 'price' setelah konversi.
    merged_data = merged_data.dropna(subset=['price'])
    
    # Membuat kolom baru 'purchase_month' dengan mengekstrak periode bulanan dari kolom 'order_purchase_timestamp'.
    # Hasilnya adalah periode dalam format 'YYYY-MM', misalnya "2017-10".
    merged_data['purchase_month'] = merged_data['order_purchase_timestamp'].dt.to_period('M')
    
    # Mengelompokkan data berdasarkan 'purchase_month' dan menghitung total penjualan (sum) pada kolom 'price'
    # untuk setiap bulan.
    monthly_sales = merged_data.groupby('purchase_month')['price'].sum()
    
    # Mengembalikan hasil agregasi total penjualan per bulan.
    return monthly_sales



# In[74]:


monthly_sales_order = calaculate_order(orders, order_items)


# In[75]:


# Identifikasi bulan dengan penjualan maksimum dan minimum
max_month = monthly_sales_order.idxmax()
min_month = monthly_sales_order.idxmin()
print(f"Bulan penjualan tertinggi: {max_month}, penjualan: {monthly_sales[max_month]}")
print(f"Bulan penjualan terendah: {min_month}, penjualan: {monthly_sales[min_month]}")


# In[76]:


# Visualisasi grafik tren penjualan bulanan
plt.figure(figsize=(10, 5))
plt.plot(monthly_sales_order.index.astype(str), monthly_sales_order.values, marker='o')
plt.title('Tren Penjualan Bulanan')
plt.xlabel('Bulan')
plt.ylabel('Total Penjualan')
plt.xticks(rotation=45)
plt.axvline(x=str(max_month), color='g', linestyle='--', label='Penjualan Maksimum')
plt.axvline(x=str(min_month), color='r', linestyle='--', label='Penjualan Minimum')
plt.legend()
plt.tight_layout()
plt.show()


# #### Load Data

# In[77]:


def load_data(monthly_sales_df):
    conn = sqlite3.connect('ecommerce_analysis.db')
    monthly_sales_df.to_sql('monthly_sales', conn, if_exists='replace', index=False)
    conn.close()

# Misalnya, jika monthly_sales_df sudah disiapkan:
load_data(monthly_sales_order)


# # Analisis Penjualan Berdasarkan Kategori Produk

# In[79]:


products.head()


# In[80]:


order_items.head()


# #### Reveneu

# In[83]:


# Menggabungkan dataset orders dengan order items
merged_data_order = pd.merge(orders, order_items, on="order_id", how="inner")

# Menggabungkan dataset items dengan products
merged_data_products = pd.merge(merged_data_order, products, on="product_id", how="left")


# In[92]:


merged_data_products.columns


# In[93]:


# Agregasi total penjualan berdasarkan kategori produk
category_sales = merged_data_products.groupby('product_category_name')['price'].sum().reset_index()

# Tampilkan hasil
print(category_sales)


# In[96]:


# Asumsi 'category_sales' sudah berisi kolom:
# 1) 'product_category_name' 
# 2) 'price' (total penjualan per kategori)

# (Opsional) Sorting kategori dari penjualan terbesar ke terkecil
category_sales = category_sales.sort_values('price', ascending=True)

# Mengatur tema dan ukuran figure
sns.set_theme(style='whitegrid')
plt.figure(figsize=(8, 12))

# Membuat horizontal bar plot
ax = sns.barplot(
    x='price',
    y='product_category_name',
    data=category_sales,
    palette='viridis'
)

# Menambahkan judul dan label sumbu
plt.title('Total Penjualan per Kategori Produk')
plt.xlabel('Total Penjualan')
plt.ylabel('Kategori Produk')

# Menyesuaikan layout agar tidak terpotong
plt.tight_layout()
plt.show()


# #### Total Penjualan

# In[103]:


# Setiap baris mewakili 1 item, jadi kita cukup count
items_sold = merged_data_products.groupby('product_category_name')['order_item_id'].count().reset_index()
items_sold.rename(columns={'order_item_id': 'items_count'}, inplace=True)
items_sold = items_sold.sort_values('items_count', ascending=False)

print(items_sold.head())  # Melihat 5 kategori dengan jumlah item terbanyak

plt.figure(figsize=(8, 10))
# Gunakan 'product_category_name' juga sebagai hue dan matikan dodge agar bar tidak terpisah
ax = sns.barplot(
    x='items_count',
    y='product_category_name',
    hue='product_category_name',
    data=items_sold.head(10),
    palette='viridis',
    dodge=False
)

# Hilangkan legend agar tampilannya seperti sebelum ada hue
if ax.get_legend() is not None:
    ax.get_legend().remove()

plt.title('Jumlah Barang Terjual per Kategori')
plt.xlabel('Jumlah Terjual')
plt.ylabel('Kategori Produk')
plt.tight_layout()
plt.show()


# # Hitung Laba Bulanan dan Identifikasi Bulan dengan Laba Tertinggi

# In[106]:


merged_data.columns


# In[110]:


# Misal merged_data sudah memiliki kolom 'price' dan 'freight_value'
merged_data['order_purchase_timestamp_x'] = pd.to_datetime(merged_data['order_purchase_timestamp_x'], errors='coerce')
merged_data['purchase_month'] = merged_data['order_purchase_timestamp_x'].dt.to_period('M')

# Asumsi: payment_value mencakup biaya operasional atau total pembayaran yang diterima
monthly_revenue = merged_data.groupby('purchase_month')['price'].sum()
monthly_payment = merged_data.groupby('purchase_month')['payment_value'].sum()

# Definisikan laba (misalnya, margin = revenue - (payment_value - revenue) jika payment_value sudah mencakup markup)
monthly_profit = monthly_revenue - (monthly_payment - monthly_revenue)

# Identifikasi bulan dengan laba tertinggi dan terendah
max_profit_month = monthly_profit.idxmax()
min_profit_month = monthly_profit.idxmin()

print("Bulan laba tertinggi:", max_profit_month, "dengan laba:", monthly_profit[max_profit_month])
print("Bulan laba terendah:", min_profit_month, "dengan laba:", monthly_profit[min_profit_month])


# In[111]:


# Misalnya, merged_data sudah merupakan hasil merge dari berbagai dataset,
# dan kita menggunakan kolom 'order_purchase_timestamp_x' dan 'payment_value'.

# Konversi kolom timestamp ke datetime
merged_data['order_purchase_timestamp'] = pd.to_datetime(merged_data['order_purchase_timestamp_x'], errors='coerce')

# Hapus baris dengan nilai kosong pada kolom yang penting
merged_data = merged_data.dropna(subset=['order_purchase_timestamp', 'payment_value'])

# Pastikan kolom payment_value berupa numerik
merged_data['payment_value'] = pd.to_numeric(merged_data['payment_value'], errors='coerce')
merged_data = merged_data.dropna(subset=['payment_value'])

# Buat kolom periode bulanan
merged_data['purchase_month'] = merged_data['order_purchase_timestamp'].dt.to_period('M')

# Agregasi total payment_value per bulan (asumsi ini mewakili laba)
monthly_profit = merged_data.groupby('purchase_month')['payment_value'].sum()

# Plot grafik garis untuk menampilkan tren laba bulanan
plt.figure(figsize=(12, 6))
plt.plot(monthly_profit.index.astype(str), monthly_profit.values, marker='o', linestyle='-')
plt.title('Laba Bulanan (Profit = Total Payment Value)')
plt.xlabel('Bulan')
plt.ylabel('Laba')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[ ]:




