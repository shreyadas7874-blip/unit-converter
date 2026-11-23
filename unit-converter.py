import streamlit as st

st.set_page_config(
    page_title="Smart Unit Converter",
    page_icon="🔄",
    layout="centered"
)

st.title("🔄 Smart Unit Converter")
st.write("Convert units quickly and easily!")

categories = {
    "Length": {
        "Metres": 1,
        "Kilometres": 1000,
        "Centimetres": 0.01,
        "Millimetres": 0.001,
        "Miles": 1609.344,
        "Feet": 0.3048,
        "Inches": 0.0254
    },
    "Weight": {
        "Kilograms": 1,
        "Grams": 0.001,
        "Milligrams": 0.000001,
        "Pounds": 0.45359237,
        "Ounces": 0.0283495
    },
    "Time": {
        "Seconds": 1,
        "Minutes": 60,
        "Hours": 3600,
        "Days": 86400
    },
    "Speed": {
        "Metres/second": 1,
        "Kilometres/hour": 1 / 3.6,
        "Miles/hour": 0.44704
    },
    "Area": {
        "Square metres": 1,
        "Square kilometres": 1000000,
        "Square feet": 0.092903,
        "Acres": 4046.856
    },
    "Volume": {
        "Litres": 1,
        "Millilitres": 0.001,
        "Cubic metres": 1000,
        "Gallons (US)": 3.78541
    },
    "Digital Storage": {
        "Bytes": 1,
        "Kilobytes": 1000,
        "Megabytes": 1000000,
        "Gigabytes": 1000000000
    }
}

category = st.selectbox(
    "Choose conversion category",
    list(categories.keys()) + ["Temperature"]
)

if category == "Temperature":
    units = ["Celsius", "Fahrenheit", "Kelvin"]
else:
    units = list(categories[category].keys())

col1, col2 = st.columns(2)

with col1:
    from_unit = st.selectbox("From", units)

with col2:
    to_unit = st.selectbox("To", units, index=1 if len(units) > 1 else 0)

amount = st.number_input(
    "Enter value",
    value=1.0,
    step=1.0
)

def convert_temperature(value, source, target):
    if source == "Celsius":
        celsius = value
    elif source == "Fahrenheit":
        celsius = (value - 32) * 5 / 9
    else:
        celsius = value - 273.15

    if target == "Celsius":
        return celsius
    elif target == "Fahrenheit":
        return (celsius * 9 / 5) + 32
    return celsius + 273.15

if st.button("Convert", type="primary"):
    if category == "Temperature":
        result = convert_temperature(
            amount, from_unit, to_unit
        )
    else:
        factors = categories[category]
        result = amount * factors[from_unit] / factors[to_unit]

    st.success(f"{amount:g} {from_unit} = {result:,.6g} {to_unit}")

    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history.append(
        f"{amount:g} {from_unit} = {result:,.6g} {to_unit}"
    )

if "history" in st.session_state:
    st.subheader("📜 Conversion History")
    for item in reversed(st.session_state.history):
        st.write("•", item)

    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()
