import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

transaction=pd.read_csv('transaction.csv')
customer=pd.read_csv('customer.csv')

customer_transaction = transaction.merge(customer, left_on = 'id_customer', right_on = 'id_customer')
customer_transaction = customer_transaction[['id_customer', 'id_product', 'num_of_purchase']]

# table rata2 penjualan per product dan jumlah product telah dijual
purchase_mean_count = pd.DataFrame(customer_transaction.groupby('id_product')['num_of_purchase'].mean())
purchase_mean_count.rename(columns = {'num_of_purchase':'mean_of_purchase'}, inplace = True)
purchase_mean_count['num_of_purchase'] = pd.DataFrame(customer_transaction.groupby('id_product')['num_of_purchase'].sum())

sns.set_style('dark')
# visualisasi jumlah penjualan antar product
plt.figure(figsize=(8,6))
plt.rcParams['patch.force_edgecolor'] = True
purchase_mean_count['num_of_purchase'].hist(bins=50)
# visualisasi rata2 penjualan antar product
plt.figure(figsize=(8,6))
plt.rcParams['patch.force_edgecolor'] = True
purchase_mean_count['mean_of_purchase'].hist(bins=50)
# visualisasi rata2 penjualan terhadap jumlah penjualan
plt.figure(figsize=(8,6))
plt.rcParams['patch.force_edgecolor'] = True
sns.jointplot(x='mean_of_purchase', y='num_of_purchase', data=purchase_mean_count, alpha=0.4)
# membuat pivot table
purchase_detail = customer_transaction.pivot_table(index='id_customer', columns='id_product', values='num_of_purchase')
purchase_detail.columns=['Life Insurance','Health Insurance','Accident Insurance','Vehicle Insurance','Education Insurance','Social Insurance','Property Insurance','Travel Insurance']
purchase_detail=purchase_detail.fillna(0)
# mencari correlation
product_similarity_df = purchase_detail.corr(method='pearson')
def get_product_recommendation(product_name):
    similar_score = product_similarity_df[product_name]
    similar_score = similar_score.sort_values(ascending=False)
    return similar_score
print(get_product_recommendation('Health Insurance'))