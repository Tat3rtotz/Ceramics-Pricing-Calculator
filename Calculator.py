import streamlit as st
import pandas as pd
import os
from Inventory import clays, glazes

# ---------------------------------
# PAGE SETTINGS
# ---------------------------------

st.set_page_config(
    page_title="Ceramics Pricing Calculator",
    page_icon=None,
    layout="wide"
)

# ---------------------------------
# FILE SETTINGS
# ---------------------------------

DATA_FILE = "ceramics.csv"

# ---------------------------------
# SESSION STATE
# ---------------------------------

if "production_calculated" not in st.session_state:
    st.session_state.production_calculated = False

if "revenue_calculated" not in st.session_state:
    st.session_state.revenue_calculated = False

# ---------------------------------
# TITLE
# ---------------------------------

st.title("Ceramics Pricing Calculator")

st.write(
    "Calculate the true production cost and profit of your ceramic pieces."
)

# ---------------------------------
# PRODUCT INFORMATION
# ---------------------------------

st.header("Product Information")

product_col1, product_col2, product_col3 = st.columns(3)

with product_col1:

    product_name = st.text_input(
        "Product Name",
        placeholder="Example: Small Bowl"
    )

with product_col2:

    sku = st.text_input(
        "SKU",
        placeholder="Example: BOWL-001"
    )

with product_col3:

    collection_name = st.text_input(
        "Collection Name",
        placeholder="Example: Forest Collection"
    )

# ---------------------------------
# PRODUCTION COSTS
# ---------------------------------

st.header("Production Costs")

col1, col2 = st.columns(2)

with col1:

    clay_type = st.selectbox(
        "Clay Type",
        list(clays.keys())
    )

    st.caption(
        f"Cost per 100g: ${clays[clay_type]:.2f}"
    )

    net_weight_kg = st.number_input(
        "Finished Weight (kg)",
        min_value=0.0,
        value=0.300,
        step=0.001,
        format="%.3f"
    )

with col2:

    glaze_type = st.selectbox(
        "Glaze Type",
        list(glazes.keys())
    )

    st.caption(
        f"Cost per 100g: ${glazes[glaze_type]:.2f}"
    )

    throwing_weight_kg = st.number_input(
        "Throwing Clay Weight (kg)",
        min_value=0.0,
        value=0.600,
        step=0.001,
        format="%.3f"
    )

# ---------------------------------
# CONVERT KG TO GRAMS
# ---------------------------------

net_weight = net_weight_kg * 1000
throwing_weight = throwing_weight_kg * 1000

# ---------------------------------
# FIRING COST
# ---------------------------------

# Firing cost:
# $16/kg = $1.60/100g

firing_cost_per_100g = 1.60

firing_cost = (
    net_weight / 100
) * firing_cost_per_100g

st.caption(
    f"Firing Cost: ${firing_cost:.2f} ($1.60 per 100g)"
)

# ---------------------------------
# CALCULATE PRODUCTION COST
# ---------------------------------

if st.button(
    "Calculate Production Cost",
    type="primary"
):

    # ---------------------------------
    # INVENTORY PRICES
    # ---------------------------------

    clay_price = clays[clay_type]
    glaze_price = glazes[glaze_type]

    # ---------------------------------
    # CLAY COST
    # ---------------------------------

    throwing_cost = (
        throwing_weight / 100
    ) * clay_price

    finished_clay_cost = (
        net_weight / 100
    ) * clay_price

    total_clay_cost = (
        throwing_cost +
        finished_clay_cost
    )

    # ---------------------------------
    # GLAZE COST
    # ---------------------------------

    # Glaze amount = finished weight x 0.1

    glaze_amount = (
        net_weight * 0.1
    )

    glaze_cost = (
        glaze_amount / 100
    ) * glaze_price

    # ---------------------------------
    # MATERIAL COST
    # ---------------------------------

    material_cost = (
        total_clay_cost +
        glaze_cost
    )

    # ---------------------------------
    # PRODUCTION COST
    # ---------------------------------

    production_cost = (
        material_cost +
        firing_cost
    )

    # ---------------------------------
    # ADDITIONAL COSTS
    # ---------------------------------

    # Packaging
    packaging_cost = 1.00

    # Waste allowance = 15% of throwing weight
    waste_weight = (
        throwing_weight * 0.15
    )

    waste_cost = (
        waste_weight / 100
    ) * clay_price

    # Equipment allowance
    equipment_cost = 1.00

    # Labour allowance
    labour_cost = 2.00

    # ---------------------------------
    # TOTAL PRODUCTION COST
    # ---------------------------------

    total_production_cost = (
        production_cost +
        packaging_cost +
        waste_cost +
        equipment_cost +
        labour_cost
    )

    # ---------------------------------
    # SAVE PRODUCTION CALCULATIONS
    # ---------------------------------

    st.session_state.production_calculated = True
    st.session_state.revenue_calculated = False

    st.session_state.total_clay_cost = total_clay_cost
    st.session_state.glaze_cost = glaze_cost
    st.session_state.material_cost = material_cost
    st.session_state.firing_cost = firing_cost
    st.session_state.production_cost = production_cost

    st.session_state.packaging_cost = packaging_cost
    st.session_state.waste_cost = waste_cost
    st.session_state.equipment_cost = equipment_cost
    st.session_state.labour_cost = labour_cost
    st.session_state.waste_weight = waste_weight

    st.session_state.total_production_cost = (
        total_production_cost
    )

# ---------------------------------
# PRODUCTION COST BREAKDOWN
# ---------------------------------

if st.session_state.production_calculated:

    total_clay_cost = st.session_state.total_clay_cost
    glaze_cost = st.session_state.glaze_cost
    material_cost = st.session_state.material_cost
    firing_cost = st.session_state.firing_cost
    production_cost = st.session_state.production_cost

    packaging_cost = st.session_state.packaging_cost
    waste_cost = st.session_state.waste_cost
    equipment_cost = st.session_state.equipment_cost
    labour_cost = st.session_state.labour_cost
    waste_weight = st.session_state.waste_weight

    total_production_cost = (
        st.session_state.total_production_cost
    )

    st.divider()

    st.header("Production Cost Breakdown")

    # ---------------------------------
    # MATERIAL / PRODUCTION COSTS
    # ---------------------------------

    result1, result2 = st.columns(2)

    with result1:

        st.metric(
            "Clay Cost",
            f"${total_clay_cost:.2f}"
        )

        st.metric(
            "Glaze Cost",
            f"${glaze_cost:.2f}"
        )

        st.metric(
            "Material Cost",
            f"${material_cost:.2f}"
        )

    with result2:

        st.metric(
            "Firing Cost",
            f"${firing_cost:.2f}"
        )

        st.metric(
            "Production Cost",
            f"${production_cost:.2f}"
        )

    # ---------------------------------
    # ADDITIONAL COSTS
    # ---------------------------------

    st.subheader("Additional Costs")

    additional_col1, additional_col2, additional_col3 = st.columns(3)

    with additional_col1:

        st.metric(
            "Packaging",
            f"${packaging_cost:.2f}"
        )

        st.metric(
            "Waste Allowance (15%)",
            f"${waste_cost:.2f}"
        )

    with additional_col2:

        st.metric(
            "Equipment Allowance",
            f"${equipment_cost:.2f}"
        )

        st.metric(
            "Labour",
            f"${labour_cost:.2f}"
        )

    with additional_col3:

        st.metric(
            "Waste Weight",
            f"{waste_weight:.1f} g"
        )

        st.caption(
            "Waste allowance is calculated as 15% "
            "of throwing clay weight."
        )

    # ---------------------------------
    # TOTAL PRODUCTION COST
    # ---------------------------------

    st.divider()

    st.markdown(
        f"### **Total Production Cost: ${total_production_cost:.2f}**"
    )

    st.caption(
        "Includes materials, firing, packaging, waste, "
        "equipment and labour."
    )

    # ---------------------------------
    # MARKUP
    # ---------------------------------

    st.divider()

    st.header("Markup")

    markup_percentage = st.number_input(
        "Markup (%)",
        min_value=0.0,
        value=100.0,
        step=5.0
    )

    # ---------------------------------
    # MARKUP CALCULATION
    # ---------------------------------

    markup_amount = (
        total_production_cost *
        (markup_percentage / 100)
    )

    suggested_selling_price = (
        total_production_cost +
        markup_amount
    )

    # ---------------------------------
    # MARKUP RESULTS
    # ---------------------------------

    markup_col1, markup_col2 = st.columns(2)

    with markup_col1:

        st.metric(
            "Markup Amount",
            f"${markup_amount:.2f}"
        )

    with markup_col2:

        st.metric(
            "Suggested Selling Price",
            f"${suggested_selling_price:.2f}"
        )

    # ---------------------------------
    # SELLING PRICE
    # ---------------------------------

    st.divider()

    st.header("Selling Price")

    selling_price = st.number_input(
        "Actual Selling Price ($)",
        min_value=0.0,
        value=float(round(suggested_selling_price, 2)),
        step=0.50,
        key="selling_price"
    )

    st.caption(
        "Enter the actual price you intend to sell the ceramic for."
    )

    # ---------------------------------
    # CALCULATE REVENUE & PROFIT
    # ---------------------------------

    if st.button(
        "Calculate Revenue & Profit",
        type="primary"
    ):

        # ---------------------------------
        # SQUARE FEE
        # ---------------------------------

        square_fee_rate = 0.016

        square_fee = (
            selling_price *
            square_fee_rate
        )

        # ---------------------------------
        # TOTAL EXPENSES
        # ---------------------------------

        total_expenses = (
            total_production_cost +
            square_fee
        )

        # ---------------------------------
        # REVENUE
        # ---------------------------------

        revenue = selling_price

        # ---------------------------------
        # PROFIT
        # ---------------------------------

        profit = (
            revenue -
            total_expenses
        )

        # ---------------------------------
        # PROFIT MARGIN
        # ---------------------------------

        if revenue > 0:

            profit_margin = (
                profit /
                revenue
            ) * 100

        else:

            profit_margin = 0

        # ---------------------------------
        # ACTUAL MARKUP
        # ---------------------------------

        actual_markup_amount = (
            selling_price -
            total_production_cost
        )

        if total_production_cost > 0:

            actual_markup_percentage = (
                actual_markup_amount /
                total_production_cost
            ) * 100

        else:

            actual_markup_percentage = 0

        # ---------------------------------
        # SAVE RESULTS
        # ---------------------------------

        st.session_state.revenue_calculated = True

        st.session_state.square_fee = square_fee

        st.session_state.total_expenses = (
            total_expenses
        )

        st.session_state.revenue = revenue

        st.session_state.profit = profit

        st.session_state.profit_margin = (
            profit_margin
        )

        st.session_state.actual_markup_amount = (
            actual_markup_amount
        )

        st.session_state.actual_markup_percentage = (
            actual_markup_percentage
        )

    # ---------------------------------
    # REVENUE & PROFIT
    # ---------------------------------

    if st.session_state.revenue_calculated:

        selling_price = st.session_state.get(
            "selling_price",
            0.0
        )

        square_fee = st.session_state.square_fee
        total_expenses = st.session_state.total_expenses
        revenue = st.session_state.revenue
        profit = st.session_state.profit
        profit_margin = st.session_state.profit_margin

        actual_markup_amount = (
            st.session_state.actual_markup_amount
        )

        actual_markup_percentage = (
            st.session_state.actual_markup_percentage
        )

        # ---------------------------------
        # EXPENSE BREAKDOWN
        # ---------------------------------

        st.divider()

        st.header("Expenses")

        expense_col1, expense_col2 = st.columns(2)

        with expense_col1:

            st.metric(
                "Total Production Cost",
                f"${total_production_cost:.2f}"
            )

        with expense_col2:

            st.metric(
                "Square Fee (1.6%)",
                f"${square_fee:.2f}"
            )

        st.markdown(
            f"### **Total Expenses: ${total_expenses:.2f}**"
        )

        # ---------------------------------
        # REVENUE & PROFIT
        # ---------------------------------

        st.divider()

        st.header("Revenue & Profit")

        revenue_col, profit_col, margin_col = st.columns(3)

        with revenue_col:

            st.metric(
                "Revenue",
                f"${revenue:.2f}"
            )

        with profit_col:

            st.metric(
                "Profit",
                f"${profit:.2f}"
            )

        with margin_col:

            st.metric(
                "Profit Margin",
                f"{profit_margin:.1f}%"
            )

        # ---------------------------------
        # ACTUAL MARKUP
        # ---------------------------------

        st.subheader("Actual Selling Price Results")

        actual_col1, actual_col2 = st.columns(2)

        with actual_col1:

            st.metric(
                "Actual Markup",
                f"{actual_markup_percentage:.1f}%"
            )

        with actual_col2:

            st.metric(
                "Markup Amount",
                f"${actual_markup_amount:.2f}"
            )

        # ---------------------------------
        # SAVE CERAMIC
        # ---------------------------------

        st.divider()

        st.header("Save Ceramic")

        if not product_name.strip():

            st.warning(
                "Please enter a Product Name before saving."
            )

        elif not sku.strip():

            st.warning(
                "Please enter an SKU before saving."
            )

        elif not collection_name.strip():

            st.warning(
                "Please enter a Collection Name before saving."
            )

        else:

            if st.button("Save Ceramic"):

                # ---------------------------------
                # NEW CERAMIC RECORD
                # ---------------------------------

                new_ceramic = {
                    "Product Name": product_name.strip(),
                    "SKU": sku.strip(),
                    "Collection Name": collection_name.strip(),
                    "Production Cost": round(
                        total_expenses,
                        2
                    ),
                    "Revenue": round(
                        revenue,
                        2
                    ),
                    "Profit": round(
                        profit,
                        2
                    )
                }

                # ---------------------------------
                # LOAD EXISTING DATA
                # ---------------------------------

                if os.path.exists(DATA_FILE):

                    existing_data = pd.read_csv(
                        DATA_FILE
                    )

                else:

                    existing_data = pd.DataFrame()

                # ---------------------------------
                # REQUIRED COLUMNS
                # ---------------------------------

                required_columns = [
                    "Product Name",
                    "SKU",
                    "Collection Name",
                    "Production Cost",
                    "Revenue",
                    "Profit"
                ]

                for column in required_columns:

                    if column not in existing_data.columns:

                        existing_data[column] = ""

                existing_data = existing_data[
                    required_columns
                ]

                # ---------------------------------
                # CHECK DUPLICATE SKU
                # ---------------------------------

                if sku.strip() in existing_data[
                    "SKU"
                ].astype(str).values:

                    st.error(
                        f"SKU '{sku.strip()}' already exists. "
                        "Please use a unique SKU."
                    )

                else:

                    # ---------------------------------
                    # ADD CERAMIC
                    # ---------------------------------

                    updated_data = pd.concat(
                        [
                            existing_data,
                            pd.DataFrame([new_ceramic])
                        ],
                        ignore_index=True
                    )

                    # ---------------------------------
                    # SAVE DATA
                    # ---------------------------------

                    updated_data.to_csv(
                        DATA_FILE,
                        index=False
                    )

                    st.success(
                        f"'{product_name.strip()}' saved successfully "
                        f"to '{collection_name.strip()}'."
                    )