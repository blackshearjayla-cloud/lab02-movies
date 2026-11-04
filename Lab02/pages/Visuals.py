
# This creates the page for displaying data visualizations.

import streamlit as st

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
import json
import pandas as pd
import streamlit as st

with open("data.json") as f:
    data = json.load(f)

st.title(data["chart_title"])

df = pd.DataFrame(data["movies"])
st.dataframe(df)

import altair as alt

# STATIC CHART: movies per genre
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

bar_chart = (
    alt.Chart(genre_counts)
    .mark_bar()
    .encode(
        x=alt.X("genre:N", title="Genre", sort="-y"),
        y=alt.Y("count:Q", title="Number of Movies"),
        tooltip=["genre", "count"],
    )
    .properties(title="Movies per Genre")
)

st.altair_chart(bar_chart)
# DYNAMIC CHART: runtime vs. year, filtered by a slider
st.subheader("Explore Movies by Release Year")

min_year = int(df["year"].min())
max_year = int(df["year"].max())

# Session state: set the default only once
if "year_range" not in st.session_state:
    st.session_state["year_range"] = (min_year, max_year)

def reset_slider():
    st.session_state["year_range"] = (min_year, max_year)

st.slider(
    "Select a range of release years",
    min_value=min_year,
    max_value=max_year,
    key="year_range",
)
st.button("Reset", on_click=reset_slider)

start, end = st.session_state["year_range"]
filtered = df[(df["year"] >= start) & (df["year"] <= end)]

if filtered.empty:
    st.write("No movies in this range.")
else:
    scatter = (
        alt.Chart(filtered)
        .mark_circle(size=120)
        .encode(
            x=alt.X("year:Q", title="Release Year", scale=alt.Scale(zero=False)),
            y=alt.Y("runtime:Q", title="Runtime (minutes)", scale=alt.Scale(zero=False)),
            color=alt.Color("genre:N", title="Genre"),
            tooltip=["title", "genre", "year", "runtime"],
        )
        .properties(title=f"Runtime vs. Year ({start} to {end})")
    )
    st.altair_chart(scatter)
# PART 2: GRAPHS FROM data.csv
# PART 2: GRAPHS FROM data.csv
st.divider()
st.header("Survey Results")

survey_df = pd.read_csv("data.csv")

survey_df.columns = survey_df.columns.str.strip()

# STATIC CHART: share of each watching method (donut chart)
watch_counts = survey_df["watch_method"].value_counts().reset_index()
watch_counts.columns = ["watch_method", "count"]

donut = (
    alt.Chart(watch_counts)
    .mark_arc(innerRadius=60)
    .encode(
        theta=alt.Theta("count:Q", title="Responses"),
        color=alt.Color("watch_method:N", title="Where People Watch"),
        tooltip=["watch_method", "count"],
    )
    .properties(title="Where Do People Watch Movies?")
)
st.altair_chart(donut)

# DYNAMIC CHART: movies per month vs. last rating, filtered by watch method
st.subheader("Explore Survey Responses")

options = ["All"] + sorted(survey_df["watch_method"].unique().tolist())

if "watch_filter" not in st.session_state:
    st.session_state["watch_filter"] = "All"

st.radio("Filter by where people watch:", options, key="watch_filter", horizontal=True)

selected = st.session_state["watch_filter"]
if selected == "All":
    filtered_survey = survey_df
else:
    filtered_survey = survey_df[survey_df["watch_method"] == selected]


survey_scatter = (
    alt.Chart(filtered_survey)
    .mark_circle(size=150, opacity=0.6)
    .encode(
        x=alt.X("movies_per_month:Q", title="Movies Watched per Month"),
        y=alt.Y("last_rating:Q", title="Rating of Last Movie (1-10)", scale=alt.Scale(domain=[0, 10])),
        color=alt.Color("genre:N", title="Favorite Genre"),
        tooltip=[
            alt.Tooltip("genre:N", title="Genre"),
            alt.Tooltip("recommendation:N", title="Recommended"),
            alt.Tooltip("movies_per_month:Q", title="Movies/Month"),
            alt.Tooltip("last_rating:Q", title="Rating"),
            alt.Tooltip("watch_method:N", title="Watches"),
        ],
    )
    .properties(title=f"Viewing Habits vs. Rating ({selected})")
)
st.altair_chart(survey_scatter)
