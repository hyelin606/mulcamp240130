# -*- coding:utf-8 -*-
import pandas as pd
import streamlit as st 
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    orders_file_path = r"./data/random_sample_orders.csv"
    orders_data = pd.read_csv(orders_file_path)
    return orders_data

@st.cache_data
def load_product_data():
    product_file_path = r"./data/random_sample_product.csv"
    product_data = pd.read_csv(product_file_path)
    return product_data

def display_product_name_by_id(product_data, product_id):
    product_info = product_data[product_data['product_id'] == product_id]

    if not product_info.empty:
        product_name = product_info['product_name'].values[0]
        st.success(f"Product Name for Product ID {product_id}: {product_name}")
    else:
        st.error(f"No product found for Product ID {product_id}.")


def display_user_orders(user_id, orders_data):
    user_orders = orders_data[orders_data['user_id'] == user_id]
    if not user_orders.empty:
        st.write(f"User {user_id}'s Orders:")
        st.table(user_orders[['order_id', 'order_number', 'order_dow', 'order_hour_of_day', 'days_since_prior_order']])

    else:
        st.write(f"No orders found for User {user_id}.")

def display_days_since_prior_order(orders_data):
    st.subheader("Distribution of Days Since Prior Order")

    plt.figure(figsize=(10, 6))
    sns.histplot(orders_data['days_since_prior_order'].dropna(), bins=30, kde=True, color='green')
    plt.title('Distribution of Days Since Prior Order')
    plt.xlabel('Days Since Prior Order')
    plt.ylabel('Frequency')

    st.pyplot(plt.gcf())

def display_order_dow_distribution(orders_data):
    st.subheader("Order Day of Week Distribution")
 
    order_dow_distribution = orders_data['order_dow'].value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    sns.barplot(x=order_dow_distribution.index, y=order_dow_distribution.values, color='green')
    plt.title('Order Day of Week Distribution')
    plt.xlabel('Day of Week')
    plt.ylabel('Order Count')

    st.pyplot(plt.gcf())


def main():
    orders_data = load_data()

    order_frequency_by_hour = orders_data['order_hour_of_day'].value_counts().sort_index()

    st.title("Instacart Order Analysis")
    st.subheader("Order Frequency by Hour of Day")

    plt.figure(figsize=(10, 6))
    sns.barplot(x=order_frequency_by_hour.index, y=order_frequency_by_hour.values, color='blue')
    plt.title('Order Frequency by Hour of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Order Frequency')

    st.pyplot(plt.gcf())

    display_days_since_prior_order(orders_data)
    display_order_dow_distribution(orders_data)

    st.title("Instacart")

    st.write("Please login using your User ID")
    user_id = st.text_input("User ID:", "00000")

    if st.button("Login"):
        if user_id.isdigit() and int(user_id) in orders_data['user_id'].unique():
            st.success("Valid User ID")
            st.write("Now search for Product")
            display_user_orders(int(user_id), orders_data)
        else:
            st.error("Invalid User ID. Please enter a valid User ID.")

    st.title("Product Lookup Dashboard")

    product_data = load_product_data()

    # Product ID를 입력 받기
    product_id = st.text_input("Enter Product ID:")

    if st.button("Lookup"):
        if product_id.isdigit() and int(product_id) in product_data['product_id'].unique():
            display_product_name_by_id(product_data, int(product_id))
        else:
            st.error("Invalid Product ID. Please enter a valid Product ID.")

if __name__ == "__main__":
    main()