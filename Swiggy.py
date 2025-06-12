import streamlit as st
import pandas as pd

# Load Data
df = pd.read_csv("cleaned_data.csv")
df['cuisine'] = df['cuisine'].astype(str).apply(lambda x: [i.strip() for i in x.split(',')])

# Page Setup
st.set_page_config("Swiggy Restaurant Recommender", page_icon="🍽️", layout="wide")

with st.sidebar:
        st.image("E:\APythonSoftware_2025\MP4\SYMBOL.jpeg",width=300)

# Sidebar Filters
with st.sidebar:
    st.markdown("### 🌟 Customize Your Search")
    selected_city = st.selectbox("📍 City", sorted(df['city'].dropna().unique()))
    cuisines = sorted(set(c for sublist in df['cuisine'] for c in sublist))
    selected_cuisines = st.multiselect("🍽️ Cuisine", cuisines, default=["Biryani"])
    selected_rating = st.slider("⭐ Minimum Rating", 0.0, 5.0, 3.5, 0.1) #minimum , maximum , default , step
    selected_cost = st.slider("💰 Max Cost for Two", 100, 2000, 500, 50)  #minimum , maximum , default , step

# Global Custom CSS with animation and sidebar color
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
        font-size: 18px;  /* Increase text size */
        color: #fbf9f9;  /* Change text color to white */
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

# Title
st.markdown("<h1 style='text-align:center;'>🍴 Swiggy Restaurant Recommender 🍝</h1>", unsafe_allow_html=True)

# Filter Data
filtered_df = df[
    (df['city'].str.lower() == selected_city.lower()) &
    (df['rating'] >= selected_rating) &
    (df['cost'] <= selected_cost) &
    (df['cuisine'].apply(lambda x: any(c in x for c in selected_cuisines)))
]

# Show results
if not filtered_df.empty:
    st.success(f"🎯 {len(filtered_df)} restaurants found")

    for _, row in filtered_df.iterrows():
        rating = row['rating']
        rating_color = "#0b0708"

        st.markdown(f"""
        <div class="restaurant-card">
            <h3 style="color:#89327f; margin-bottom:0.3rem;">{row['name']}</h3>
            <h4>📍 <strong>City:</strong> {row['city']} &nbsp;&nbsp; 🍽️ {' , '.join(row['cuisine'])}</h4>
            <h4>⭐ <strong style="color:{rating_color};">Rating:</strong> <span style="color:{rating_color};">{rating} ({row['rating_count']} ratings)</span></h4>
            <h4>💸 <strong>Cost for two:</strong> ₹{row['cost']}</h4>
          
        """, unsafe_allow_html=True)
else:
    st.warning("😕 No restaurants match your filters. Try adjusting your preferences.")
