import streamlit as st

# Set page layout
st.set_page_config(page_title="Salmonometer Dashboard", layout="wide")

# Navigation
st.sidebar.title("🔧 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📋 Data Entry", "📊 Analytics"])

# Session State for multiple fish entry
if 'fish_index' not in st.session_state:
    st.session_state.fish_index = 1
if 'fish_data' not in st.session_state:
    st.session_state.fish_data = []
if 'max_fish' not in st.session_state:
    st.session_state.max_fish = 0

# 📋 Data Entry
if page == "📋 Data Entry":
    st.title("📋 Data Entry - Fish by Fish")

    if st.session_state.fish_index == 1:
        with st.form("group_info_form"):
            group = st.text_input("Group Name")
            date = st.date_input("Date")
            num_fish = st.number_input("Number of Fish", min_value=1, max_value=50, step=1)
            data_types = st.multiselect("Select data types to record", 
                                        ["Welfare Indicators", "Production Data", "Water Quality"])
            welfare_indicators = []
            if "Welfare Indicators" in data_types:
                welfare_indicators = st.multiselect("Select Welfare Indicators", [
                    "Emaciation", "Scale Loss", "Fin Damage", "Wounds", "Eye Haemorrhaging",
                    "Exophthalmia", "Opercular Damage", "Snout Damage", "Upper Jaw Deformity",
                    "Lower Jaw Deformity", "Vertebral Deformity", "Skin Haemorrhages"
                ])
            start = st.form_submit_button("Start Recording")

        if start:
            st.session_state.group = group
            st.session_state.date = str(date)
            st.session_state.data_types = data_types
            st.session_state.welfare_indicators = welfare_indicators
            st.session_state.max_fish = num_fish
            st.rerun()

    else:
        st.subheader(f"🐟 Fish {st.session_state.fish_index} of {int(st.session_state.max_fish)}")

        with st.form(f"fish_form_{st.session_state.fish_index}"):
            entry = {"Fish": st.session_state.fish_index}

            if "Welfare Indicators" in st.session_state.data_types:
                for indicator in st.session_state.welfare_indicators:
                    with st.expander(f"🔍 {indicator} (click to view guideline)"):
                        st.image(f"images/{indicator.lower().replace(' ', '_')}.jpg", caption=f"{indicator} scoring guide")
                    entry[indicator] = st.selectbox(f"{indicator} Score (0–3)", [0, 1, 2, 3], key=f"{indicator}_{st.session_state.fish_index}")

            if "Production Data" in st.session_state.data_types:
                entry["Weight (g)"] = st.number_input("Weight (g)", min_value=0.0)
                entry["Length (cm)"] = st.number_input("Length (cm)", min_value=0.0)

            if "Water Quality" in st.session_state.data_types:
                entry["Temperature (°C)"] = st.number_input("Water Temp (°C)", min_value=0.0)
                entry["Oxygen (mg/L)"] = st.number_input("Oxygen (mg/L)", min_value=0.0)

            image = st.file_uploader("Upload image (optional)", type=["jpg", "jpeg", "png"])
            entry["Image"] = image.name if image else "None"

            submit = st.form_submit_button("Submit Fish Data")

        if submit:
            st.session_state.fish_data.append(entry)
            st.session_state.fish_index += 1

            if st.session_state.fish_index > st.session_state.max_fish:
                st.success("✅ All fish data recorded!")
                st.write("### Group Info")
                st.write(f"Group: {st.session_state.group}")
                st.write(f"Date: {st.session_state.date}")
                st.write("### Recorded Data")
                st.dataframe(st.session_state.fish_data)
            else:
                st.rerun()

# 🏠 Home Page
elif page == "🏠 Home":
    st.title("🐟 Welcome to Salmonometer")
    st.markdown("""
    This is a dashboard for collecting and analyzing fish farming data.
    Use the sidebar to submit new data or view analytics.
    """)

# 📊 Analytics Page
elif page == "📊 Analytics":
    st.title("📊 Analytics Page (coming soon)")
    st.info("After saving data, this page will show visualizations and comparisons.")
