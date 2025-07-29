# 📰 News Article EDA: Interactive Plotly Analysis

## Dataset Overview

This project provides a **comprehensive, interactive EDA (Exploratory Data Analysis)** of a large company news dataset (~60,000 articles, ~180MB). All visualizations are built using Plotly for full interactivity.

- **Format:** JSON Lines (one article per line)
- **Example Record:**
  ```json
  {
    "Id": 1111111,
    "CreateDateString": "D.M.Y",
    "title": "...",
    "summary": "...",
    "Tags": "tag_1,tag_2",
    "Categories": [1,2],
    "full_text": "...",
    "title_norm": "...",
    "summary_norm": "...",
    "tags_norm": [],
    "full_text_norm": "...",
    "n_words_title": 111,
    "n_words_summary": 111,
    "n_words_full_text": 111
  }
  ```
- **Notable Columns:**
  - `Id`: Unique integer for each article.
  - `CreateDateString`: Date string (format: "DD.MM.YYYY").
  - `title`, `summary`, `full_text`: Raw news text fields.
  - `Tags`: Comma-separated string of tags/topics (sometimes repeated, not normalized).
  - `tags_norm`: Cleaned, lowercased list of unique tags.
  - `title_norm`, `summary_norm`, `full_text_norm`: Lowercased, normalized versions.
  - `n_words_*`: Word counts for respective text fields.

## Project Structure

This EDA consists of two main classes:
- **Analyzer** — Focuses on temporal, topical, and tag-based explorations.
- **TextAnalyzer** — Focuses on length and textual statistics.

## Analysis Functions

### 1. `plot_tag_counts(tags_col="Tags", top_n=20)`
**Purpose:** Visualize the most frequently occurring tags/topics in the dataset.

**Logic:**
- Aggregates all tags from the specified column (`tags_col`, typically `tags_norm` for deduped/lowercased tags).
- Uses a Counter to tally how many times each tag appears across all articles.
- Selects the top `top_n` tags by frequency.
- Plots a horizontal bar chart where:
  - **Y-axis**: Tag name.
  - **X-axis**: Count of articles that include the tag.
  - Bars are colored by count (using a continuous color scale for fast “hot topic” recognition).

**Parameters:**
- `tags_col`: The column to use for tags. Should be a list or string of tags per article.
- `top_n`: Number of top tags to display.

**Interpretation:**
- The longest bar shows the most dominant topic.
- Quickly reveals news coverage bias or focus (e.g., if “gaza” and “israel” dominate).

### 2. `plot_trend(freq="D")`
**Purpose:** Show the time-based distribution of article publication, revealing trends, bursts, or gaps.

**Logic:**
- Computes the number of articles published in each time interval (day, week, or month), using the `freq` parameter (“D” for day, “W” for week, “M” for month).
- Converts these counts into a DataFrame for plotting.
- Plots a line chart:
  - **X-axis**: Time (dates).
  - **Y-axis**: Article count per period.
  - Highlights the peak publication period with a special marker.

**Parameters:**
- `freq`: Aggregation period (“D”, “W”, or “M”).

**Interpretation:**
- Peaks represent bursts of activity (potential major news events).
- Gaps may indicate missing data, weekends, or holidays.
- Slope and variance help spot consistent coverage vs. news cycles.

### 3. `articles_per_month_around_date(selected_date, months_window=3, date_col="date")`
**Purpose:** Analyze article volume in a “window” around a key date (e.g., event, crisis, election).

**Logic:**
- Converts `selected_date` to a datetime object.
- Selects all articles where the `date_col` is within ±`months_window` months of `selected_date`.
- Groups these articles by month and counts the number per month.
- Plots a bar chart:
  - **X-axis**: Months within the window.
  - **Y-axis**: Article count.
  - Each bar represents one month.

**Parameters:**
- `selected_date`: Center date for the analysis.
- `months_window`: How many months before/after to include.
- `date_col`: The date column (should be standardized as datetime).

**Interpretation:**
- Shows how coverage “ramps up” and “winds down” before and after major events.
- Spikes may show pre-event speculation or post-event fallout.

### 4. `plot_tag_coverage_over_time(tag, date_col="date", tags_col="Tags", top_n_months=None, color="#009688")`
**Purpose:** Track how often a specific tag/topic appears over time.

**Logic:**
- Filters articles to only those that contain the specified `tag`.
- Groups these by month and counts occurrences.
- If `top_n_months` is set, only the months with the highest counts are plotted.
- Plots a vertical bar chart:
  - **X-axis**: Month.
  - **Y-axis**: Article count for that tag.
  - The peak month is highlighted with a special marker.

**Parameters:**
- `tag`: The topic to track.
- `date_col`: Date field to use.
- `tags_col`: Tag field.
- `top_n_months`: Optionally, just the busiest months.
- `color`: Bar color (optional).

**Interpretation:**
- Shows the “media pulse” of a topic—when it became hot, how long it stayed relevant.
- Useful for mapping news cycles for recurring topics.

### 5. `tag_cooccurrence_matrix(tag_col="Tags", top_n=20, plot_heatmap=True)`
**Purpose:** Visualize which topics/tags frequently appear together in articles.

**Logic:**
- Counts co-occurrences: for each article, finds all unique pairs of tags and increments their count.
- Tallies up the total occurrence of each tag, selects `top_n` most frequent tags.
- Builds a square matrix where the rows and columns are tags, and each cell is the number of articles where both tags co-occurred.
- Plots this as a heatmap:
  - **X/Y-axes**: Tag names.
  - **Color**: Intensity of co-occurrence (the more intense, the more often those two tags appeared together).

**Parameters:**
- `tag_col`: Column to use for tags.
- `top_n`: How many top tags to include.
- `plot_heatmap`: If `True`, return the Plotly heatmap; if `False`, just the matrix.

**Interpretation:**
- Bright (hot) cells mean two topics are often linked in the news (e.g., “gaza” and “israel”).
- Blocks or clusters in the matrix suggest sub-themes or “news clusters”.

### 6. `plot_tag_temporal_shifts(matrix)`
**Purpose:** Show how the prevalence of top tags changes over time.

**Logic:**
- Takes a matrix of counts (from `get_tag_month_matrix`): rows=months, columns=tags.
- Converts it to “long” format for Plotly.
- Plots a stacked area chart:
  - **X-axis**: Month.
  - **Y-axis**: Number of articles.
  - Each colored area represents one tag.

**Parameters:**
- `matrix`: Output from `get_tag_month_matrix`.

**Interpretation:**
- Shows topic “takeovers” (when one topic rises and others fall).
- Helps visualize shifts in public/media attention.
- Plateaus or drops can be interpreted as topic “fatigue” or saturation.

### 7. `plot_topic_emergence_decay(emergence_df, window_col="window")`
**Purpose:** Analyze and visualize the birth and death of topics over time.

**Logic:**
- Calculates for each time window (e.g., month):
  - **Emergent tags**: Tags appearing for the first time.
  - **Decayed tags**: Tags present now, but gone in the next window.
- Plots a dual-line chart:
  - **X-axis**: Time window (e.g., months).
  - **Y-axis**: Number of emergent/decayed tags.
  - Two lines: one for new, one for disappearing topics.

**Parameters:**
- `emergence_df`: Output from `topic_emergence_decay`.
- `window_col`: Column to use for the x-axis.

**Interpretation:**
- Spikes in emergent tags signal new news cycles, crises, or sudden global attention shifts.
- Spikes in decayed tags mean many topics “died off” at once (media focus shift).

### 8. `plot_article_velocity_agg(tag, tag_col="Tags", date_col="date", freq="M", agg="mean", time_unit="days")`
**Purpose:** Measure how rapidly articles on a given topic appear over time.

**Logic:**
- Filters all articles with the specified `tag`.
- Sorts their publication dates and calculates time gaps (deltas) between each article.
- Computes the velocity: `Velocity = 1 / (gap in units)`, so more frequent articles = higher velocity.
- Aggregates these velocities by the chosen time window (`freq`), and either takes the mean or max per window.
- Plots a line chart:
  - **X-axis**: Time window.
  - **Y-axis**: Velocity.
  - Peak velocity is highlighted.

**Parameters:**
- `tag`: Topic to analyze.
- `tag_col`: Column with tags.
- `date_col`: Publication date.
- `freq`: Time window (“W”/“M”).
- `agg`: “mean” or “max” velocity per window.
- `time_unit`: “days”, “hours”, “minutes”.

**Interpretation:**
- Higher velocity = faster, more intense coverage (e.g., breaking news).
- Can be used to distinguish between viral news and long-tail stories.

### 9. `plot_event_lifespan(grouped, first_appearance, peak_window, last_appearance, freq="D", tag="")`
**Purpose:** Visualize the full “life-cycle” of news coverage for a given event/topic.

**Logic:**
- Takes the grouped time series (articles per window for the given `tag`).
- Plots a bar chart:
  - **X-axis**: Time windows (e.g., months).
  - **Y-axis**: Article count.
  - Special bar colors for:
    - First appearance (green).
    - Peak coverage (gold).
    - Last appearance (blue).
- Adds a custom legend so interpretation is clear.

**Parameters:**
- `grouped`: Time series of article counts for the tag.
- `first_appearance`, `peak_window`, `last_appearance`: Timestamps to highlight.
- `freq`: Window size for aggregation (“D”, “W”, “M”).
- `tag`: Tag/event being visualized.

**Interpretation:**
- Shows exactly when a story broke, peaked, and faded away.
- Compare different events’ coverage lifespan or see which get “forgotten” quickly.

### 10. `length_hist(text_col, bins=30)` (TextAnalyzer)
**Purpose:** Understand the distribution of article lengths.

**Logic:**
- Calculates the number of words per article for the chosen `text_col`.
- Plots a histogram:
  - **X-axis**: Number of words.
  - **Y-axis**: Number of articles with that length.
  - Uses `bins` to control granularity.

**Parameters:**
- `text_col`: Which column to analyze (e.g., “full_text_norm”).
- `bins`: Number of histogram bins.

**Interpretation:**
- Outliers on either side may indicate malformed data (extremely short/long articles).
- Mode of the histogram shows the “typical” article length.

### 11. `most_common_words(text_col, n=30, ngram=1)` (TextAnalyzer)
**Purpose:** Reveal the most common words/phrases in the dataset.

**Logic:**
- Extracts unigrams, bigrams, or trigrams from the text of all articles in the column.
- Tallies their frequencies using a Counter.
- Selects the top `n`.
- Plots a vertical bar chart:
  - **X-axis**: Word or phrase.
  - **Y-axis**: Number of occurrences.

**Parameters:**
- `text_col`: Which text column to use (e.g., “full_text_norm”).
- `n`: How many top words/phrases to plot.
- `ngram`: 1 = word, 2 = bigram, 3 = trigram.

**Interpretation:**
- High-frequency ngrams are often stopwords, named entities, or recurring themes.
- Useful for quickly understanding the vocabulary and focus of the news corpus.

## Summary Table

| Function                           | Chart Type         | Main Insight                          | Key Parameters                              |
|------------------------------------|--------------------|---------------------------------------|---------------------------------------------|
| `plot_tag_counts`                  | Bar (horizontal)   | Top topics                            | `tags_col`, `top_n`                         |
| `plot_trend`                       | Line               | Article trend over time               | `freq`                                      |
| `articles_per_month_around_date`   | Bar                | Articles around event date            | `selected_date`, `months_window`            |
| `plot_tag_coverage_over_time`      | Bar                | Tag/topic trend                       | `tag`, `top_n_months`                       |
| `tag_cooccurrence_matrix`          | Heatmap            | Tag pairings                          | `tag_col`, `top_n`                          |
| `plot_tag_temporal_shifts`         | Area               | Topic shifts over time                | `matrix`                                    |
| `plot_topic_emergence_decay`       | Line               | New/disappeared tags                  | `emergence_df`, `window_col`                |
| `plot_article_velocity_agg`        | Line               | Coverage tempo                        | `tag`, `agg`, `freq`, `time_unit`           |
| `plot_event_lifespan`              | Bar                | Event news lifecycle                  | `grouped`, `first/peak/last`                |
| `length_hist`                      | Histogram          | Article length                        | `text_col`, `bins`                          |
| `most_common_words`                | Bar                | Frequent words/phrases                | `text_col`, `n`, `ngram`                    |