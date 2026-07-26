import streamlit as st
import pandas as pd
import os

# ---------------------------------
# PAGE SETTINGS
# ---------------------------------

st.set_page_config(
    page_title="Ceramic Inventory",
    page_icon=None,
    layout="wide"
)

# ---------------------------------
# FILE SETTINGS
# ---------------------------------

DATA_FILE = "ceramics.csv"

# ---------------------------------
# TITLE
# ---------------------------------

st.title("Ceramic Inventory")

st.write(
    "View and manage your saved ceramic pieces."
)

# ---------------------------------
# CHECK FOR DATA
# ---------------------------------

if not os.path.exists(DATA_FILE):

    st.info(
        "No ceramics have been saved yet. "
        "Use the Pricing Calculator to add your first piece."
    )

else:

    # ---------------------------------
    # LOAD DATA
    # ---------------------------------

    ceramics = pd.read_csv(DATA_FILE)

    # ---------------------------------
    # HANDLE OLD DATA
    # ---------------------------------

    if "Collection Name" not in ceramics.columns:

        ceramics["Collection Name"] = "Unsorted"

    ceramics["Collection Name"] = (
        ceramics["Collection Name"]
        .fillna("Unsorted")
        .replace("", "Unsorted")
    )

    # ---------------------------------
    # CHECK FOR EMPTY INVENTORY
    # ---------------------------------

    if ceramics.empty:

        st.info(
            "No ceramics have been saved yet."
        )

    else:

        # ---------------------------------
        # INVENTORY SUMMARY
        # ---------------------------------

        st.header("Inventory Summary")

        total_pieces = len(ceramics)

        total_collections = (
            ceramics["Collection Name"]
            .nunique()
        )

        total_revenue = (
            ceramics["Revenue"]
            .sum()
        )

        total_profit = (
            ceramics["Profit"]
            .sum()
        )

        summary1, summary2, summary3, summary4 = st.columns(4)

        with summary1:

            st.metric(
                "Total Ceramics",
                total_pieces
            )

        with summary2:

            st.metric(
                "Collections",
                total_collections
            )

        with summary3:

            st.metric(
                "Total Revenue",
                f"${total_revenue:.2f}"
            )

        with summary4:

            st.metric(
                "Total Profit",
                f"${total_profit:.2f}"
            )

        # ---------------------------------
        # COLLECTIONS
        # ---------------------------------

        st.divider()

        st.header("Collections")

        collections = sorted(
            ceramics["Collection Name"]
            .unique()
        )

        # ---------------------------------
        # DISPLAY EACH COLLECTION
        # ---------------------------------

        for collection in collections:

            st.subheader(collection)

            collection_data = ceramics[
                ceramics["Collection Name"] == collection
            ].copy()

            # ---------------------------------
            # COLLECTION SUMMARY
            # ---------------------------------

            collection_revenue = (
                collection_data["Revenue"]
                .sum()
            )

            collection_profit = (
                collection_data["Profit"]
                .sum()
            )

            collection_col1, collection_col2, collection_col3 = st.columns(3)

            with collection_col1:

                st.metric(
                    "Ceramics",
                    len(collection_data)
                )

            with collection_col2:

                st.metric(
                    "Revenue",
                    f"${collection_revenue:.2f}"
                )

            with collection_col3:

                st.metric(
                    "Profit",
                    f"${collection_profit:.2f}"
                )

            # ---------------------------------
            # COLLECTION TABLE
            # ---------------------------------

            display_columns = [
                "Product Name",
                "SKU",
                "Production Cost",
                "Revenue",
                "Profit"
            ]

            st.dataframe(
                collection_data[display_columns],
                use_container_width=True,
                hide_index=True
            )

            st.divider()

        # ---------------------------------
        # DELETE CERAMIC
        # ---------------------------------

        st.header("Delete Ceramic")

        sku_to_delete = st.selectbox(
            "Select SKU to delete",
            ceramics["SKU"].astype(str).tolist()
        )

        if st.button(
            "Delete Selected Ceramic",
            type="secondary"
        ):

            updated_data = ceramics[
                ceramics["SKU"].astype(str) != sku_to_delete
            ]

            updated_data.to_csv(
                DATA_FILE,
                index=False
            )

            st.success(
                f"SKU '{sku_to_delete}' has been deleted."
            )

            st.rerun()