import streamlit as st

# Page setup
st.set_page_config(page_title="Salmonometer Dashboard", layout="wide")

# Sidebar navigation
st.sidebar.title("🔧 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📋 Data Entry", "📊 Analytics"])

# 🏠 Home Page
if page == "🏠 Home":
    st.title("🐟 Welcome to Salmonometer")
    st.markdown("""
    **Salmonometer** is a data collection and analytics dashboard for:
    - Monitoring fish welfare
    - Tracking lice count
    - Recording water quality
    - Logging production parameters

    💡 Used by student groups, farms, and researchers to visualize and compare results in real-time.
    """)

    st.success("Use the sidebar to start submitting or viewing data.")

# 📋 Data Entry Page
elif page == "📋 Data Entry":
    st.title("📋 Data Entry Form")

    with st.form(key='data_form'):
        group_name = st.text_input("Enter Group Name", placeholder="Group A")
        date = st.date_input("Select Date")
        num_fish = st.number_input("Number of Fish", min_value=1, max_value=100, step=1)

        data_options = st.multiselect(
            "Select the data you want to record",
            ["Welfare Indicators", "Production Data", "Water Quality", "Lice Count"]
        )

        submitted = st.form_submit_button("Start Recording")
        
        if submitted:
            st.success(f"Data entry initiated for {group_name} on {date} with {num_fish} fish.")
            st.info(f"Selected categories: {', '.join(data_options)}")
            st.warning("This is a placeholder — form for individual fish will be added next.")

# 📊 Analytics Page
elif page == "📊 Analytics":
    st.title("📊 Analytics Dashboard")

    st.markdown("""
    In future updates, this page will:
    - Show group-wise and farm-wise comparisons
    - Generate graphs and summary statistics
    - Display uploaded image previews (optional)
    """)

    st.info("Analytics will be displayed here once data is collected.")
