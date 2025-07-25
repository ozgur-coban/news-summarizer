import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import tempfile

from eda.metadata_analysis import Analyzer
from eda.text_analysis import TextAnalyzer

# Page configuration
st.set_page_config(page_title="News EDA Dashboard", layout="wide")
st.title("📰 News Article EDA Dashboard")

# File uploader
uploaded_file = st.file_uploader(
    "Upload your news data (JSONL/JSON)", type=["jsonl", "json"]
)


# ---------- Caching ----------
@st.cache_data
def save_and_get_path(uploaded_file):
    suffix = ".jsonl" if uploaded_file.name.lower().endswith(".jsonl") else ".json"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name
    return tmp_file_path


@st.cache_resource
def get_analyzers(tmp_file_path):
    analyzer = Analyzer(tmp_file_path)
    text_analyzer = TextAnalyzer(
        source_file=tmp_file_path, id_col="Id", title_col="title"
    )
    return analyzer, text_analyzer


if uploaded_file is not None:
    # Save uploaded file to a temporary path
    tmp_file_path = save_and_get_path(uploaded_file)
    analyzer, text_analyzer = get_analyzers(tmp_file_path)

    st.success(f"Loaded {uploaded_file.name} ({os.path.getsize(tmp_file_path)} bytes)")

    # Instantiate analyzer with file path
    # analyzer = Analyzer(tmp_file_path)
    # text_analyzer = TextAnalyzer(
    #     source_file=tmp_file_path, id_col="Id", title_col="title"
    # )
    # Sidebar: analysis selection
    st.sidebar.header("EDA Options")
    plot_type = st.sidebar.selectbox(
        "Select analysis",
        [
            "Tag Counts",
            "Article Trend",
            "Monthly Around Date",
            "Tag Coverage Over Time",
            "Tag Co-occurrence",
            "Tag Temporal Shifts",
            "Topic Emergence/Decay",
            "Article Velocity",
            "Event Lifespan",
            "Length Distribution",
            "Most Common N-grams",
        ],
    )

    # Render selected analysis
    if plot_type == "Tag Counts":
        top_n = st.sidebar.slider("Top N tags", 5, 50, 20)
        fig = analyzer.plot_tag_counts(tags_col="tags_norm", top_n=top_n)
        st.plotly_chart(fig, use_container_width=True)

    elif plot_type == "Article Trend":
        freq = st.sidebar.selectbox("Frequency", ["D", "W", "M"])
        fig = analyzer.plot_trend(freq=freq)
        st.plotly_chart(fig, use_container_width=True)

    elif plot_type == "Monthly Around Date":
        date = st.sidebar.date_input("Center date", pd.to_datetime("2025-01-01"))
        window = st.sidebar.slider("Months window", 1, 12, 3)
        df_mon = analyzer.articles_per_month_around_date(date, months_window=window)
        st.plotly_chart(df_mon)

    elif plot_type == "Tag Coverage Over Time":
        tag = st.sidebar.text_input("Tag (case-insensitive)", "Gaza")
        top_n_months = st.sidebar.slider("Show top N months", 1, 12, 6)
        fig = analyzer.plot_tag_coverage_over_time(
            tag, tags_col="tags_norm", top_n_months=top_n_months
        )
        st.plotly_chart(fig, use_container_width=True)
    elif plot_type == "Tag Co-occurrence":
        top_n = st.sidebar.slider("Top N tags for matrix", 5, 50, 20)
        fig = analyzer.tag_cooccurrence_matrix(tag_col="tags_norm", top_n=top_n)
        st.plotly_chart(fig, use_container_width=True)
    elif plot_type == "Tag Temporal Shifts":
        top_n = st.sidebar.slider("Top N tags to track", 5, 20, 10)
        matrix = analyzer.get_tag_month_matrix(tag_col="tags_norm", top_n=top_n)
        fig = analyzer.plot_tag_temporal_shifts(matrix)
        st.plotly_chart(fig, use_container_width=True)
    elif plot_type == "Topic Emergence/Decay":
        freq = st.sidebar.selectbox("Window frequency", ["W", "M"], index=1)
        min_count = st.sidebar.slider("Min occurrences per window", 1, 5, 2)
        df_em = analyzer.topic_emergence_decay(
            tag_col="tags_norm", freq=freq, min_window_count=min_count
        )
        print(df_em)
        fig = Analyzer.plot_topic_emergence_decay(emergence_df=df_em)
        st.plotly_chart(fig, use_container_width=True)
    elif plot_type == "Article Velocity":
        tag = st.sidebar.text_input("Tag for velocity", "Gaza")
        freq = st.sidebar.selectbox("Velocity freq", ["W", "M"], index=1)
        agg = st.sidebar.selectbox("Aggregate", ["mean", "max"], index=0)
        unit = "days"
        fig = analyzer.plot_article_velocity_agg(
            tag, tag_col="tags_norm", freq=freq, agg=agg, time_unit=unit
        )
        st.plotly_chart(fig, use_container_width=True)

    elif plot_type == "Event Lifespan":
        tag = st.sidebar.text_input("Tag for lifespan", "Gaza")
        freq = st.sidebar.selectbox("Lifespan freq", ["D", "W", "M"], index=2)
        grouped, first, peak, last = analyzer.event_coverage_lifespan(
            tag, tag_col="tags_norm", freq=freq
        )
        fig = analyzer.plot_event_lifespan(
            grouped, first, peak, last, freq=freq, tag=tag
        )
        st.plotly_chart(fig, use_container_width=True)
    # TODO add other text columns as selection
    elif plot_type == "Length Distribution":
        text_col = st.sidebar.selectbox(
            "Column for length hist",
            text_analyzer.df.columns,
            index=text_analyzer.df.columns.get_loc("full_text_norm"),
        )
        bins = st.sidebar.slider("Bins", 10, 100, 30)
        fig = text_analyzer.length_hist(text_col, bins=bins)
        st.plotly_chart(fig, use_container_width=True)
    elif plot_type == "Most Common N-grams":
        text_col = st.sidebar.selectbox(
            "Column for n-grams",
            text_analyzer.df.columns,
            index=text_analyzer.df.columns.get_loc("full_text_norm"),
        )
        n = st.sidebar.slider("Top N n-grams", 5, 50, 20)
        ngram = st.sidebar.slider("N-gram size", 1, 3, 1)
        fig = text_analyzer.most_common_words(text_col=text_col, n=n, ngram=ngram)
        st.plotly_chart(fig, use_container_width=True)

    # Optional cleanup
    # os.remove(tmp_file_path)

else:
    st.info("Please upload your news data file.")

# Sidebar footer
st.sidebar.markdown("---")
st.sidebar.info("Developed with ❤️ using Streamlit and Plotly.")
