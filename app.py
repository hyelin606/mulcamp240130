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


def display_user_orders(user_id, orders_data):
    user_orders = orders_data[orders_data['user_id'] == user_id]
    if not user_orders.empty:
        st.write(f"User {user_id}'s Orders:")
        st.table(user_orders[['order_id', 'order_number', 'order_dow', 'order_hour_of_day', 'days_since_prior_order']])

    else:
        st.write(f"No orders found for User {user_id}.")

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

if __name__ == "__main__":
    main()