import streamlit as st
import pandas as pd
import os

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Movie Survey 📝")
st.write("Tell me about your movie habits! Your answers get added to the dataset.")

CSV_FILE = "data.csv"

# DATA INPUT FORM
with st.form("survey_form", clear_on_submit=True):
    genre_input = st.selectbox(
        "What's your favorite movie genre?",
        ["Action", "Animation", "Comedy", "Drama", "Horror", "Mystery", "Romance", "Sci-Fi", "Thriller", "Other"],
    )
    recommendation_input = st.text_input("What's one movie you'd recommend?")
    per_month_input = st.number_input(
        "How many movies do you watch per month?", min_value=0, max_value=100, value=4, step=1
    )
    watch_input = st.radio("Where do you mostly watch?", ["Theater", "Streaming", "Both"])
    rating_input = st.slider("How would you rate the last movie you watched? (1-10)", 1, 10, 7)

    submitted = st.form_submit_button("Submit Data")

    if submitted:
        if recommendation_input.strip() == "":
            st.error("Please enter a movie recommendation before submitting.")
        else:
            # 1. Build one row of data as a dictionary (keys become CSV columns)
            new_row = {
                "genre": genre_input,
                "recommendation": recommendation_input.strip(),
                "movies_per_month": per_month_input,
                "watch_method": watch_input,
                "last_rating": rating_input,
            }

            # 2. Write the header only if the file is missing or empty
            write_header = (not os.path.exists(CSV_FILE)) or os.path.getsize(CSV_FILE) == 0

            # 3. Append the row in 'a' mode
            pd.DataFrame([new_row]).to_csv(CSV_FILE, mode="a", header=write_header, index=False)

            st.success("Your data has been submitted!")
            st.write(f"You entered: **{genre_input}**, **{recommendation_input.strip()}**, "
                     f"**{per_month_input}**, **{watch_input}**, **{rating_input}**")

# DATA DISPLAY
st.divider()
st.header("Current Data in CSV")

if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
    current_data_df = pd.read_csv(CSV_FILE)
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
