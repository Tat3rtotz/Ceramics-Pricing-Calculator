import streamlit as st


# -----------------------------
# PAGE SETTINGS
# -----------------------------

st.set_page_config(
    page_title="Material Inventory",
    layout="wide"
)


st.title("Material Inventory")

st.write(
    "Manage your clay and glaze costs here."
)


# -----------------------------
# CLAY INVENTORY
# -----------------------------

st.header("🪨 Clay Library")


clays = {
    "Walker's 10 Stoneware Clay": 0.23,
    "Keane's No.7 Stoneware Speckled Clay": 0.31,
    "Blackwattle Buff Speckled Stoneware Clay": 0.27,
    "Blackwattle Natural Speckled Stoneware Clay": 0.30,
    "Lesmurdie Natural Stoneware Clay": 0.47,
    "Kim Lyon's Dark Buff Stoneware Clay": 0.27

}


clay_table = []

for name, price in clays.items():

    clay_table.append(
        {
            "Clay Type": name,
            "Cost per 100g ($)": price
        }
    )


st.dataframe(
    clay_table,
    use_container_width=True
)


# -----------------------------
# ADD NEW CLAY
# -----------------------------

st.subheader("➕ Add New Clay")


new_clay = st.text_input(
    "Clay Name"
)


new_clay_price = st.number_input(
    "Cost per 100g",
    min_value=0.0,
    step=0.01
)


if st.button("Add Clay"):

    if new_clay:

        clays[new_clay] = new_clay_price

        st.success(
            f"{new_clay} added!"
        )

    else:

        st.warning(
            "Please enter a clay name."
        )



# -----------------------------
# GLAZE INVENTORY
# -----------------------------

st.divider()

st.header("Glaze Library")


glazes = {

    "Crazy Crackle": 1.00,
    "Speckled White": 1.13,
    "Tenmoku": 1.22,
    "Sand Castle": 1.85,
    "Apple Pie": 1.67,
    "Emerald Moss": 2.55,
    "Winter Blue": 2.36,
    "Muddy Lapis": 1.65,

}


glaze_table = []


for name, price in glazes.items():

    glaze_table.append(
        {
            "Glaze": name,
            "Cost per 100g ($)": price
        }
    )


st.dataframe(
    glaze_table,
    use_container_width=True
)