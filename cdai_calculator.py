import streamlit as st

# Set app title and header
st.set_page_config(page_title="CDAI Calculator", page_icon=":pill:", layout="wide")
st.title("Crohn's Disease Activity Index (CDAI) Score")

# Get input values from user
liquid_stools = st.number_input("Cumulative number of liquid or soft stools for the past 7 days", value=0)
abdominal_pain = st.selectbox(
    "Daily assessment of abdominal pain for the past 7 days",
    options=["None", "Mild", "Moderate", "Severe"]
)
general_well_being = st.selectbox(
    "Daily assessment of general well-being for the past 7 days",
    options=["Generally well", "Slightly under par", "Poor", "Very poor", "Terrible"]
)
complications = st.multiselect(
    "Extra-intestinal complications",
    options=["Arthritis/arthralgia", "Iritis/uveitis", "Skin/mouth lesions", "Peri-anal disease", "Other fistula", "Fever >37.8 °C, >100 °F (in the last week)"]
)
diarrhea_treatment = st.selectbox("Diarrhea Treatment",
                                 options=["None", "Lomotil, Loperamide or Opiates"])
abdominal_mass = st.selectbox("Presence of abdominal mass",
                              options=["None", "Questionable", "Definite"])

hematocrit_score = st.number_input("Hematocrit Score in %", value=0)
weight_lb = st.number_input("Weight (Current body weight in lb)", value=0)
standard_weight_lb = st.number_input("Standard Body Weight (in lb)", value=0)
gender = st.radio("Gender", options=["Male", "Female"])

# Define the CDAI classifications
classifications = {
    "Remission": "CDAI < 150",
    "Mild": "150 ≤ CDAI < 220",
    "Moderate": "220 ≤ CDAI < 450",
    "Severe": "CDAI ≥ 450"
}

# Function to calculate CDAI score
def calculate_cdai_score(liquid_stools, abdominal_pain, general_well_being, complications, diarrhea_treatment,
                         abdominal_mass, hematocrit_score, weight_lb, standard_weight_lb, gender):
    # Convert weight from lb to kg
    weight_kg = weight_lb * 0.45359237
    standard_weight_kg = standard_weight_lb * 0.45359237

    # Calculate scores for each component
    liquid_stools_score = liquid_stools * 2
    abdominal_pain_score = {
        "None": 0,
        "Mild": 7,
        "Moderate": 14,
        "Severe": 21
    }[abdominal_pain] * 5    
    general_well_being_score = {
        "Generally well": 0,
        "Slightly under par": 7,
        "Poor": 14,
        "Very poor": 21,
        "Terrible": 28
    }[general_well_being] * 7    
    complications_score = len(complications) * 20
    diarrhea_treatment_score = 30 if diarrhea_treatment != "None" else 0
    abdominal_mass_score = {
        "None": 0,
        "Questionable": 2,
        "Definite": 5
    }[abdominal_mass] * 10

    if gender == "Female" and hematocrit_score >= 0:
        hematocrit_score = (42 - hematocrit_score) * 6
    else:
        hematocrit_score = 0

    # Calculate percentage deviation from standard weight
    if standard_weight_kg != 0:
        weight_deviation_score = 100 * (1 - weight_kg / standard_weight_kg)
    else:
        weight_deviation_score = 0

    # Calculate total CDAI score
    total_score = (
        liquid_stools_score + abdominal_pain_score + general_well_being_score + complications_score +
        diarrhea_treatment_score + abdominal_mass_score + hematocrit_score + weight_deviation_score
    )

    return total_score

# Display information in the sidebar
st.sidebar.markdown("---")

st.sidebar.markdown("#### About CDAI")


st.sidebar.markdown("The Crohn's Disease Activity Index (CDAI) is a tool used to assess the severity of Crohn's disease. It takes into account various symptoms and factors to calculate a numerical score.")

st.sidebar.markdown("---")

# Initialize classification variable
classification = ""

# Call the calculate_cdai_score function
total_score = calculate_cdai_score(
    liquid_stools, abdominal_pain, general_well_being, complications,
    diarrhea_treatment, abdominal_mass, hematocrit_score,
    weight_lb, standard_weight_lb, gender
)

# Add the "Calculate" button
if st.button("Calculate"):
    # Call the calculate_cdai_score function
    # ...

    # Calculate CDAI classification based on total score
    if total_score < 150:
        classification = "Remission"
    elif total_score < 220:
        classification = "Mild"
    elif total_score < 450:
        classification = "Moderate"
    else:
        classification = "Severe"

    # Display the calculated CDAI score
    st.subheader("CDAI Score Calculation Result")
    st.markdown(f"**CDAI Score:** {total_score}")
    
    # Display the CDAI classification
    st.markdown(f"**CDAI Classification:** {classification}")

# Display the CDAI classification in the sidebar
st.sidebar.markdown("#### CDAI Classifications")
for classification, criteria in classifications.items():
    st.sidebar.markdown(f"**{classification}:** {criteria}")
st.sidebar.markdown("---")


