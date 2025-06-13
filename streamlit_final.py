import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.cluster import KMeans

# Load Data
cleaned_data = pd.read_csv('cleaned_data.csv')
encoded_data = pd.read_csv('encoded_data.csv')

# Load KMeans model
with open('kmeans_model.pkl', 'rb') as f:
    kmeans = pickle.load(f)

with st.sidebar:
        st.image("E:\APythonSoftware_2025\MP4\SYMBOL.jpeg", width=300)

# Sidebar Navigation
st.sidebar.title('🍴 Restaurant Recommender')

choice = st.sidebar.selectbox('Navigation', ['Home', 'Recommendations'])

# Home Page
if choice == 'Home':
    st.title('🍽️ Restaurant Recommendation App')
    st.write("Use the sidebar to navigate to the Recommendations section.")

# Recommendation Page
if choice == 'Recommendations':
    with st.sidebar:
        st.markdown("### 🌟 Customize Your Search")
        #st.title('🔍 Find Your Restaurant')

    # User Input
        city = st.selectbox('Select City', cleaned_data['city_cleaned'].unique())
        cuisine = st.selectbox('Preferred Cuisine', cleaned_data['cuisine'].unique())
        min_rating = st.slider('Minimum Rating', 0.0, 5.0, 3.5)
        max_cost = st.slider('Maximum Cost (₹)', 100, 1000, 500)

    # Filter for initial match
    filtered = cleaned_data[
        (cleaned_data['city_cleaned'] == city) &
        (cleaned_data['cuisine'] == cuisine) &
        (cleaned_data['rating'] >= min_rating) &
        (cleaned_data['cost'] <= max_cost)
    ]
    st.markdown("""
    <style>    
    @keyframes fadeSlide {
        from { opacity: 1; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    section[data-testid="stSidebar"] {
        background-color: #17685d;
        padding: 1rem;
        border-right: 2px solid #ddd;
        animation: fadeSlide 0.8s ease-in-out;
    }
    section[data-testid="stSidebar"] * {  
        font-size: 18px;
        color: #fbf9f9;
    }      
    .restaurant-card {
        background-color: #12f6d7;
        color: #000;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        animation: fadeSlide 0.8s ease-in-out;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }                  
    </style>
""", unsafe_allow_html=True)


    if not filtered.empty:
        st.success(f"Found {len(filtered)} matching restaurants. Generating recommendations...")

        # Get the index of the first match
        idx = filtered.index[0]

        # Get the encoded feature vector of that restaurant
        encoded_vector = encoded_data.loc[idx].values.reshape(1, -1)

        # Predict the cluster of the selected restaurant
        cluster_label = kmeans.predict(encoded_vector)[0]

        # Get all restaurants in the same cluster
        cluster_indices = np.where(kmeans.labels_ == cluster_label)[0]

        # Remove the original input restaurant and select top 5
        recommended_indices = [i for i in cluster_indices if i != idx][:5]

        st.subheader('🍽️ Top Recommended Restaurants')
        for i in recommended_indices:
            row = cleaned_data.loc[i]
            st.markdown(f"### {row['name']}")
            st.write(f"📍 City: {row['city_cleaned']}")
            st.write(f"🍽️ Cuisine: {row['cuisine']}")
            st.write(f"⭐ Rating: {row['rating']} ({row['rating_count']} reviews)")
            st.write(f"💰 Cost: ₹{row['cost']}")
            st.markdown("---")
    else:
        st.warning("No restaurants match your filters. Please adjust your input.")