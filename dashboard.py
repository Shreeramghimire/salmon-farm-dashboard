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
        all_data_types = ["Welfare Indicators", "Production Data", "Water Quality", "Lice Count"]
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
        if "Welfare Indicators" in st.session_state.data_types:
            st.subheader("💫 Welfare Indicators Data Entry")

            if st.button("🔙 Go Back to Selection"):
                st.session_state.recording_started = False
                st.rerun()

            entries = []
            form = st.form("welfare_form")
            with form:
                for i in range(1, int(st.session_state.max_fish) + 1):
                    row = {"Fish": i}
                    cols = st.columns(len(st.session_state.welfare_indicators) + 1)
                    cols[0].write(f"Fish {i}")
                    for j, ind in enumerate(st.session_state.welfare_indicators):
                        row[ind] = cols[j + 1].selectbox(f"{ind} (Fish {i})", [0, 1, 2, 3], key=f"{ind}_{i}")
                    entries.append(row)
                submit_welfare = form.form_submit_button("Submit Welfare Data")

            if submit_welfare:
                df = pd.DataFrame(entries)
                df.insert(0, "Group", st.session_state.group)
                df.insert(1, "Date", st.session_state.date)
                st.success("✅ Welfare data recorded!")
                st.dataframe(df)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("⬇️ Download CSV", data=csv, file_name=f"{st.session_state.group}_welfare.csv", mime='text/csv')
                xlsx_buffer = BytesIO()
                with pd.ExcelWriter(xlsx_buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Welfare Indicators')
                st.download_button("⬇️ Download Excel", data=xlsx_buffer.getvalue(), file_name=f"{st.session_state.group}_welfare.xlsx", mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                st.session_state.recording_started = False
                st.stop()

        if "Production Data" in st.session_state.data_types:
            st.subheader("📏 Production Data Entry")

            if st.button("🔙 Go Back to Selection"):
                st.session_state.recording_started = False
                st.rerun()

            entries = []
            form = st.form("production_form")
            with form:
                for i in range(1, int(st.session_state.max_fish) + 1):
                    col1, col2, col3 = st.columns(3)
                    length = col1.number_input(f"Length (cm) - Fish {i}", min_value=0.0, step=0.1, key=f"len_{i}")
                    weight = col2.number_input(f"Weight (g) - Fish {i}", min_value=0.0, step=0.1, key=f"wt_{i}")
                    cf = round((100 * weight) / (length ** 3), 2) if length > 0 else 0
                    col3.write(f"CF: {cf}")
                    entries.append({"Fish": i, "Length (cm)": length, "Weight (g)": weight, "Condition Factor": cf})
                submit = form.form_submit_button("Submit Production Data")

            if submit:
                df = pd.DataFrame(entries)
                df.insert(0, "Group", st.session_state.group)
                df.insert(1, "Date", st.session_state.date)
                st.success("✅ Production data recorded!")
                st.dataframe(df)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("⬇️ Download CSV", data=csv, file_name=f"{st.session_state.group}_production.csv", mime='text/csv')
                xlsx_buffer = BytesIO()
                with pd.ExcelWriter(xlsx_buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Production Data')
                st.download_button("⬇️ Download Excel", data=xlsx_buffer.getvalue(), file_name=f"{st.session_state.group}_production.xlsx", mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                st.session_state.recording_started = False
                st.stop()

        if "Water Quality" in st.session_state.data_types:
            st.subheader("🌊 Water Quality Data Entry")

            if st.button("🔙 Go Back to Selection"):
                st.session_state.recording_started = False
                st.rerun()

            num_locations = st.number_input("Number of Locations / Cages", min_value=1, max_value=20, step=1)
            entries = []
            with st.form("water_quality_form"):
                for i in range(1, int(num_locations) + 1):
                    col1, col2, col3, col4, col5 = st.columns(5)
                    location = col1.text_input(f"Location/Cage {i}", key=f"loc_{i}")
                    do = col2.number_input("DO (mg/L)", min_value=0.0, step=0.1, key=f"do_{i}")
                    ph = col3.number_input("pH", min_value=0.0, step=0.1, key=f"ph_{i}")
                    temp = col4.number_input("Temp (°C)", min_value=-2.0, step=0.1, key=f"temp_{i}")
                    sal = col5.number_input("Salinity (ppt)", min_value=0.0, step=0.1, key=f"sal_{i}")
                    entries.append({"Location": location, "Dissolved Oxygen (mg/L)": do, "pH": ph, "Temperature (°C)": temp, "Salinity (ppt)": sal})
                submit = st.form_submit_button("Submit Water Quality Data")

            if submit:
                df = pd.DataFrame(entries)
                df.insert(0, "Group", st.session_state.group)
                df.insert(1, "Date", st.session_state.date)
                st.success("✅ Water quality data recorded!")
                st.dataframe(df)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("⬇️ Download CSV", data=csv, file_name=f"{st.session_state.group}_water_quality.csv", mime='text/csv')
                xlsx_buffer = BytesIO()
                with pd.ExcelWriter(xlsx_buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Water Quality')
                st.download_button("⬇️ Download Excel", data=xlsx_buffer.getvalue(), file_name=f"{st.session_state.group}_water_quality.xlsx", mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                st.session_state.recording_started = False
                st.stop()

        if "Lice Count" in st.session_state.data_types:
            st.subheader("🪱 Lice Count Data Entry")

            if st.button("🔙 Go Back to Selection"):
                st.session_state.recording_started = False
                st.rerun()

            lice_stages = ["Sessile", "Pre-Adult I", "Pre-Adult II", "Adult Male", "Adult Female"]
            entries = []
            form = st.form("lice_form")
            with form:
                for i in range(1, int(st.session_state.max_fish) + 1):
                    row = {"Fish": i}
                    cols = st.columns(len(lice_stages) + 1)
                    cols[0].write(f"Fish {i}")
                    for j, stage in enumerate(lice_stages):
                        row[stage] = cols[j + 1].number_input(f"{stage} (Fish {i})", min_value=0, step=1, key=f"{stage}_{i}")
                    entries.append(row)
                submit = form.form_submit_button("Submit Lice Count Data")

            if submit:
                df = pd.DataFrame(entries)
                df.insert(0, "Group", st.session_state.group)
                df.insert(1, "Date", st.session_state.date)
                st.success("✅ Lice count data recorded!")
                st.dataframe(df)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("⬇️ Download CSV", data=csv, file_name=f"{st.session_state.group}_lice.csv", mime='text/csv')
                xlsx_buffer = BytesIO()
                with pd.ExcelWriter(xlsx_buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Lice Count')
                st.download_button("⬇️ Download Excel", data=xlsx_buffer.getvalue(), file_name=f"{st.session_state.group}_lice.xlsx", mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                st.session_state.recording_started = False
                st.stop()

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
