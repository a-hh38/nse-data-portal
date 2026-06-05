import streamlit as st
from auth import login, logout
from config import (
    INDEX_HIERARCHY,
    INDEX_OPTIONS,
    TRI_HIERARCHY,
    TRI_OPTIONS
)
from nse_api import get_index_data
from io import BytesIO
import pandas as pd

# ------------------------
# PAGE CONFIG
# ------------------------

st.set_page_config(
    page_title="NSE Historical Data Portal",
    page_icon="",
    layout="wide"
)

# ------------------------
# LOGIN
# ------------------------

if not login():
    st.stop()

# ------------------------
# HEADER
# ------------------------

header_col1, header_col2 = st.columns([1.5, 6])

with header_col1:
    st.image(
        "assets/yes_logo.png",
        width=200
    )

with header_col2:
    st.markdown(
        """
        <div style="padding-top:35px;">
            <h1 style="color:#003366;">
                NSE Historical Data Portal
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

st.caption("YES Securities | Internal Use Only")

st.divider()

# ------------------------
# USER BAR
# ------------------------

user_col1, user_col2 = st.columns([8, 1])

with user_col1:
    st.success(
        f"Logged in as: {st.session_state.username}"
    )

with user_col2:
    logout()

st.divider()
# ------------------------

# FILTERS

# ------------------------

data_type = st.selectbox(
"Data Type",
[
"Historical Index Data",
"Total Return Index Values"
]
)

if data_type == "Historical Index Data":


    index_type = st.selectbox(
        "Index Type",
        list(INDEX_HIERARCHY.keys())
    )

    sub_index_type = st.selectbox(
        "Sub Index Type",
        INDEX_HIERARCHY[index_type]
    )

    available_indices = sorted(
        INDEX_OPTIONS[index_type][sub_index_type].keys()
    )

    selected_index = st.selectbox(
        "Index",
        available_indices,
        key="historical_index"
    )

    index_data = (
        INDEX_OPTIONS[index_type]
        [sub_index_type]
        [selected_index]
    )


else:


    index_type = "Equity"

    sub_index_type = st.selectbox(
        "Sub Index Type",
        TRI_HIERARCHY["Equity"],
        key="tri_sub_index"
    )

    available_indices = sorted(
        TRI_OPTIONS[sub_index_type].keys()
    )

    selected_index = st.selectbox(
        "Index",
        available_indices,
        key="tri_index"
    )

    index_data = TRI_OPTIONS[sub_index_type][selected_index]


index_name = index_data["indexName"]
name_field = index_data["name"]
# ------------------------
# DATE PICKERS
# ------------------------

date_col1, date_col2 = st.columns(2)

with date_col1:

    start_date_obj = st.date_input(
        "Start Date"
    )

with date_col2:

    end_date_obj = st.date_input(
        "End Date"
    )

start_date = start_date_obj.strftime("%d-%b-%Y")
end_date = end_date_obj.strftime("%d-%b-%Y")

# ------------------------
# INDEX INFO
# ------------------------

with st.expander("Selected Index Details"):

    st.write(
        f"Index Name: {index_name}"
    )

    st.write(
        f"NSE Name Field: {name_field}"
    )


# ------------------------
# FETCH
# ------------------------

if st.button(
    "Fetch Historical Data",
    use_container_width=True):

    with st.spinner("Downloading..."):

        try:
            st.write("name_field =", name_field)
            st.write("index_name =", index_name)
            st.write("start_date =", start_date)
            st.write("end_date =", end_date)

            df = get_index_data(
            name_field,
            index_name,
            start_date,
            end_date,
            data_type
        )

            st.success(
                f"{len(df)} rows downloaded"
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            # ------------------------
            # DOWNLOADS
            # ------------------------

            download_col1, download_col2 = st.columns(2)

            # CSV

            csv = df.to_csv(
                index=False
            ).encode("utf-8")

            with download_col1:

                st.download_button(
                    "Download CSV",
                    csv,
                    file_name=f"{index_name}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            # EXCEL

            excel_buffer = BytesIO()

            with pd.ExcelWriter(
                excel_buffer,
                engine="openpyxl"
            ) as writer:

                df.to_excel(
                    writer,
                    sheet_name="Historical Data",
                    index=False
                )

            with download_col2:

                st.download_button(
                    "Download Excel",
                    excel_buffer.getvalue(),
                    file_name=f"{index_name}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

        except Exception as e:

            st.error(str(e))