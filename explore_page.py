import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Function to group less frequent categories as 'Other'
def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

# Clean experience data
def clean_experience(x):
    if x == 'Less than 1 year': 
        return 0.5
    if x == 'More than 50 years':
        return 50
    return float(x)

# Clean education level data
def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Associate degree' in x:
        return 'Post grad'
    return 'Less than a Bachelor'

# Load and clean the data
@st.cache_data  # Updated caching method
def load_data():
    df = pd.read_csv("stack-overflow-developer-survey-2024/survey_results_public.csv")
    
    # Select relevant columns and clean data
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df[df["ConvertedCompYearly"].notnull()]  # Filter rows where salary data exists
    df = df.dropna()  # Drop rows with any missing values
    df = df[df["Employment"] == "Employed, full-time"]  # Filter full-time employed
    df = df.drop("Employment", axis=1)  # Drop the employment column as it's not needed

    # Group less frequent countries as 'Other'
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)

    # Apply salary filters
    df = df[df["ConvertedCompYearly"] <= 250000]
    df = df[df["ConvertedCompYearly"] >= 10000]
    df = df[df["Country"] != 'Other']  # Exclude 'Other' countries

    # Clean YearsCodePro and EdLevel columns
    df['YearsCodePro'] = df["YearsCodePro"].apply(clean_experience)
    df['EdLevel'] = df["EdLevel"].apply(clean_education)

    # Rename the salary column
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    
    return df

# Load data
df = load_data()

# Function to display the exploration page
def show_explore_page():
    st.title("Explore Software Engineer Salaries")
    st.write("""
        ### Stack Overflow Developer Survey 2024
        This visualization shows salary data of software engineers across various countries.
    """)

    # Display country distribution
    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.write("""#### Number of Data Points from Different Countries""")
    st.pyplot(fig1)

    st.write(
        """
    #### Mean Salary Based On Country
    """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)

    # Create a bar chart with Plotly and custom color
    fig = px.bar(
        data,
        x=data.index,
        y=data.values,
        labels={'x': 'Country', 'y': 'Mean Salary'},
        color_discrete_sequence=["#A5C9CA"]  # Custom color for the bars
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig)

    #st.bar_chart(data)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)

# Run the explore page
show_explore_page()

