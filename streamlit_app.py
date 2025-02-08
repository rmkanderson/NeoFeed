import streamlit as st

st.title("NeoFeed AI")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

def predict_safe_discharge(apnea_bradycardia_last_5_days, oxygen_requirement_lpm, weight_gain_g_per_kg,
                           oral_feed_percentage, feeding_tolerance_ml_per_kg, residuals_or_emesis,
                           parent_trained, caregiver_competent, home_nursing_available,
                           distance_from_hospital_hours):
    
    # Clinical Stability Check
    if apnea_bradycardia_last_5_days:
        return "Not safe for discharge: Recent apnea/bradycardia events."
    if oxygen_requirement_lpm > 0.1:
        return "Not safe for discharge: Oxygen requirement too high."
    if weight_gain_g_per_kg < 15:
        return "Caution: Weight gain below recommended threshold. Reassess."

    # Feeding Tolerance Check
    if oral_feed_percentage >= 80:
        feeding_risk = "Low risk for home NG needs."
    elif oral_feed_percentage < 50 and residuals_or_emesis:
        return "Not safe for discharge: Poor feeding tolerance."
    elif feeding_tolerance_ml_per_kg > 120 and not residuals_or_emesis:
        feeding_risk = "Stable on NG feeds, consider discharge with monitoring."
    else:
        return "Not safe for discharge: Feeding concerns present."

    # Parental Readiness Check
    if not parent_trained:
        return "Not safe for discharge: Parent not trained in NG care."
    if not caregiver_competent:
        return "Require supervised trial before discharge: Caregiver competency uncertain."

    # Social & Environmental Risk Stratification
    if home_nursing_available:
        social_risk = "Lower risk due to home nursing support."
    elif distance_from_hospital_hours > 2:
        return "High risk: Distance from hospital is too far for safe home NG management."
    else:
        social_risk = "Moderate risk: Ensure follow-up plan."

    return f"Safe for discharge with considerations. {feeding_risk} {social_risk}"

# Streamlit UI
st.title("NICU NG Tube Discharge Predictor")

apnea_bradycardia_last_5_days = st.radio("Has the baby had apnea/bradycardia in the last 5 days?", ["Yes", "No"]) == "Yes"
oxygen_requirement_lpm = st.number_input("Enter oxygen requirement in LPM", min_value=0.0, step=0.1)
weight_gain_g_per_kg = st.number_input("Enter weight gain in g/kg/day", min_value=0.0, step=0.1)
oral_feed_percentage = st.slider("Enter oral feeding percentage", 0, 100)
feeding_tolerance_ml_per_kg = st.number_input("Enter feeding tolerance in mL/kg/day", min_value=0.0, step=1.0)
residuals_or_emesis = st.radio("Is there significant residuals or emesis?", ["Yes", "No"]) == "Yes"
parent_trained = st.radio("Has the parent been trained in NG care?", ["Yes", "No"]) == "Yes"
caregiver_competent = st.radio("Is the caregiver competent in NG feeding?", ["Yes", "No"]) == "Yes"
home_nursing_available = st.radio("Is home nursing available?", ["Yes", "No"]) == "Yes"
distance_from_hospital_hours = st.number_input("Enter distance from hospital in hours", min_value=0.0, step=0.1)

if st.button("Predict Safe Discharge"):
    result = predict_safe_discharge(apnea_bradycardia_last_5_days, oxygen_requirement_lpm, weight_gain_g_per_kg,
                                    oral_feed_percentage, feeding_tolerance_ml_per_kg, residuals_or_emesis,
                                    parent_trained, caregiver_competent, home_nursing_available,
                                    distance_from_hospital_hours)
    st.subheader(result)
