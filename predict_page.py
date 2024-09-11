import streamlit as st
import numpy as np
import pickle

# Function to load the model and encoders
def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

# Load the model and label encoders
data = load_model()
regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

# Function to show the prediction page
def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict the salary""")

    # Countries and education levels used for the dropdowns
    countries = (
        "United States of America",
        "Germany",
        "United Kingdom of Great Britain and Northern Ireland",
        "Ukraine",
        "India",
        "France",
        "Canada",
        "Brazil",
        "Spain",
        "Italy",
        "Netherlands",
        "Australia"
    )

    education = (
        "Less than a Bachelor",  
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad"
    )

    # Widgets to take inputs from the user
    country = st.selectbox("Country", countries, key="country_unique_1")
    education_level = st.selectbox("Education Level", education, key="education_unique_2")
    experience = st.slider("Years of Experience", 0, 50, 3, key="experience_slider_unique_3")

    # When the user clicks "Calculate Salary"
    if st.button("Calculate Salary"):
        try:
            # Prepare input data for the model
            X = np.array([[country, education_level, experience]])
            X[:, 0] = le_country.transform(X[:, 0])
            X[:, 1] = le_education.transform(X[:, 1])
            X = X.astype(float)

            # Predict the salary using the trained model
            salary = regressor.predict(X)
            st.subheader(f"The estimated salary is ${salary[0]:,.2f}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Display the prediction page
show_predict_page()
