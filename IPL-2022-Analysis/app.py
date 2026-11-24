from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "IPL.csv"
st.set_page_config(page_title="IPL 2022 Match Insights", page_icon="🏏", layout="wide")

@st.cache_data
def load_matches():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")
    matches = pd.read_csv(DATA_FILE)
    required = {
        "team1", "team2", "stage", "venue", "toss_winner", "toss_decision",
        "match_winner", "won_by", "first_ings_score", "second_ings_score",
        "player_of_the_match", "best_bowling", "best_bowling_figure",
    }
    missing = required.difference(matches.columns)
    if missing:
        raise ValueError(f"IPL.csv is missing columns: {', '.join(sorted(missing))}")
    for column in ["team1", "team2", "toss_winner", "match_winner"]:
        matches[column] = matches[column].replace({"Banglore": "Bangalore"})
    matches["best_figure_wickets"] = pd.to_numeric(
        matches["best_bowling_figure"].astype("string").str.extract(r"^\s*(\d+)")[0],
        errors="coerce",
    )
    return matches

df = load_matches()
st.title("IPL 2022 Match Insights")
st.caption("Explore team results, player performances, match patterns and venues.")

st.sidebar.header("Filters")
stages = sorted(df["stage"].dropna().unique().tolist())
venues = sorted(df["venue"].dropna().unique().tolist())
teams = sorted(set(df["team1"].dropna()) | set(df["team2"].dropna()))
selected_stages = st.sidebar.multiselect("Stage", stages, default=stages)
selected_teams = st.sidebar.multiselect("Team", teams, default=teams)
selected_venues = st.sidebar.multiselect("Venue", venues, default=venues)

team_mask = df["team1"].isin(selected_teams) | df["team2"].isin(selected_teams)
filtered = df[
    df["stage"].isin(selected_stages)
    & team_mask
    & df["venue"].isin(selected_venues)
].copy()

if filtered.empty:
    st.warning("No matches match the selected filters. Change the filters to continue.")
    st.stop()

winner_counts = filtered["match_winner"].value_counts()
top_winner = winner_counts.index[0] if not winner_counts.empty else "—"
toss_match_rate = filtered["toss_winner"].eq(filtered["match_winner"]).mean() * 100
highest_score = int(filtered[["first_ings_score", "second_ings_score"]].max().max())

metric_cols = st.columns(4)
metric_cols[0].metric("Matches", f"{len(filtered)}")
metric_cols[1].metric("Teams", f"{len(set(filtered['team1']) | set(filtered['team2']))}")
metric_cols[2].metric("Most wins", top_winner)
metric_cols[3].metric("Toss winner also won", f"{toss_match_rate:.1f}%")
st.caption(f"Highest innings score in the selected matches: {highest_score} runs")

team_tab, player_tab, match_tab, venue_tab = st.tabs(
    ["Team performance", "Player performance", "Match patterns", "Venues"]
)

with team_tab:
    left, right = st.columns(2)
    wins = winner_counts.rename_axis("Team").reset_index(name="Wins")
    wins_fig = px.bar(
        wins, x="Wins", y="Team", orientation="h", text="Wins",
        title="Matches won by team", color="Wins", color_continuous_scale="Blues",
    )
    wins_fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    left.plotly_chart(wins_fig, use_container_width=True)

    results = filtered["won_by"].value_counts().rename_axis("Result").reset_index(name="Matches")
    result_fig = px.pie(results, names="Result", values="Matches", title="Wins by runs or wickets", hole=0.45)
    right.plotly_chart(result_fig, use_container_width=True)

with player_tab:
    left, right = st.columns(2)
    player_awards = (
        filtered["player_of_the_match"].value_counts().head(10)
        .rename_axis("Player").reset_index(name="Awards")
    )
    awards_fig = px.bar(
        player_awards, x="Awards", y="Player", orientation="h", text="Awards",
        title="Most Player of the Match awards", color="Awards", color_continuous_scale="Teal",
    )
    awards_fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    left.plotly_chart(awards_fig, use_container_width=True)

    bowling = (
        filtered.groupby("best_bowling", as_index=False)["best_figure_wickets"]
        .sum().sort_values("best_figure_wickets", ascending=False).head(10)
        .rename(columns={"best_bowling": "Bowler", "best_figure_wickets": "Wickets"})
    )
    bowling_fig = px.bar(
        bowling, x="Wickets", y="Bowler", orientation="h", text="Wickets",
        title="Wickets in recorded best bowling figures", color="Wickets",
        color_continuous_scale="Purples",
    )
    bowling_fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    right.plotly_chart(bowling_fig, use_container_width=True)
    st.caption("These wickets are summed from each match's recorded best bowling figure, not full-season player totals.")

with match_tab:
    left, right = st.columns(2)
    toss_counts = filtered["toss_decision"].value_counts().rename_axis("Decision").reset_index(name="Matches")
    toss_fig = px.bar(toss_counts, x="Decision", y="Matches", text="Matches", title="Toss decisions", color="Decision")
    left.plotly_chart(toss_fig, use_container_width=True)

    score_fig = px.scatter(
        filtered, x="first_ings_score", y="second_ings_score", color="won_by",
        hover_data=["match_id", "match_winner", "venue"],
        labels={"first_ings_score": "First innings score", "second_ings_score": "Second innings score", "won_by": "Result"},
        title="First innings vs second innings scores",
    )
    right.plotly_chart(score_fig, use_container_width=True)

with venue_tab:
    venue_counts = filtered["venue"].value_counts().rename_axis("Venue").reset_index(name="Matches")
    venue_fig = px.bar(
        venue_counts, x="Matches", y="Venue", orientation="h", text="Matches",
        title="Matches by venue", color="Matches", color_continuous_scale="Viridis",
    )
    venue_fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    st.plotly_chart(venue_fig, use_container_width=True)

st.divider()
st.caption("Dataset: IPL.csv · 2022 season · Match-level records")
