import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set page layout
st.set_page_config(page_title="Salmonometer Dashboard", layout="wide")

# Navigation
st.sidebar.title("🔧 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📋 Data Entry", "📊 Analytics"])

# Session State Initialization
if 'fish_index' not in st.session_state:
    st.session_state.fish_index = 1
if 'fish_data' not in st.session_state:
    st.session_state.fish_data = []
if 'max_fish' not in st.session_state:
    st.session_state.max_fish = 0
if 'recording_started' not in st.session_state:
    st.session_state.recording_started = False
if 'selected_data_types' not in st.session_state:
    st.session_state.selected_data_types = []
if 'welfare_indicators' not in st.session_state:
    st.session_state.welfare_indicators = []

# 📋 Data Entry
if page == "📋 Data Entry":
    st.title("📋 Data Entry - Fish by Fish")

    if not st.session_state.recording_started:
        group = st.text_input("Group Name")
        date = st.date_input("Date")
        num_fish = st.number_input("Number of Fish", min_value=1, max_value=50, step=1)

        st.markdown("**Select Data Types to Record:**")
        all_data_types = ["Welfare Indicators", "Production Data", "Water Quality", "Lice Count", "Product Quality"]
        selected_data_types = []
        for dtype in all_data_types:
            if st.checkbox(dtype, value=dtype in st.session_state.selected_data_types):
                selected_data_types.append(dtype)
        st.session_state.selected_data_types = selected_data_types

        if "Welfare Indicators" in selected_data_types:
            st.markdown("**Select Welfare Indicators:**")
            indicator_options = [
                "Emaciation", "Scale Loss", "Fin Damage", "Wounds", "Eye Haemorrhaging",
                "Exophthalmia", "Opercular Damage", "Snout Damage", "Upper Jaw Deformity",
                "Lower Jaw Deformity", "Vertebral Deformity", "Skin Haemorrhages"
            ]
            selected = []
            for ind in indicator_options:
                if st.checkbox(ind, value=ind in st.session_state.welfare_indicators):
                    selected.append(ind)
            st.session_state.welfare_indicators = selected

        col1, col2 = st.columns(2)
        if col1.button("Start Recording"):
            st.session_state.group = group
            st.session_state.date = str(date)
            st.session_state.data_types = selected_data_types
            st.session_state.max_fish = num_fish
            st.session_state.fish_data = []
            st.session_state.fish_index = 1
            st.session_state.recording_started = True
            st.rerun()

    else:
        st.subheader(f"📋 Score Table for {st.session_state.max_fish} Fish")

        if st.button("🔙 Go Back to Selection"):
            st.session_state.recording_started = False
            st.rerun()

        form = st.form("bulk_entry_form")
        entries = []

        cols = ["Fish"] + st.session_state.welfare_indicators
        if "Lice Count" in st.session_state.data_types:
            cols.append("Lice Count")

        data = pd.DataFrame(columns=cols)
        for i in range(1, int(st.session_state.max_fish) + 1):
            row = {"Fish": i}
            cols_display = st.columns(len(cols))
            cols_display[0].write(f"{i}")

            for j, ind in enumerate(st.session_state.welfare_indicators):
                row[ind] = cols_display[j+1].selectbox(f"{ind} (Fish {i})", [0, 1, 2, 3], key=f"{ind}_{i}")

            if "Lice Count" in st.session_state.data_types:
                row["Lice Count"] = cols_display[len(cols_display)-1].number_input(f"Lice Count (Fish {i})", min_value=0, step=1, key=f"lice_{i}")

            entries.append(row)

        submit = form.form_submit_button("Submit All Data")
        if submit:
            df = pd.DataFrame(entries)
            df.insert(0, "Group", st.session_state.group)
            df.insert(1, "Date", st.session_state.date)
            st.session_state.fish_data = df
            st.success("✅ All fish data recorded!")
            st.dataframe(df)

            # Download buttons
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download CSV", data=csv, file_name=f"{st.session_state.group}_fish_data.csv", mime='text/csv')

            xlsx_buffer = BytesIO()
            with pd.ExcelWriter(xlsx_buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Fish Data')
            st.download_button("⬇️ Download Excel", data=xlsx_buffer.getvalue(), file_name=f"{st.session_state.group}_fish_data.xlsx", mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            st.session_state.recording_started = False

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
