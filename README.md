# IPL 2022 Data Visualisation

A Python project for exploring IPL 2022 match results and learning data visualisation. It includes an IPL analysis notebook, visualisation practice notebooks, and an interactive Streamlit dashboard.

## About the dataset

The project uses the \`IPL.csv\` file included in this repository. It contains **74 match-level records and 20 columns**, covering the Group stage, Playoffs and Final.

| Dataset detail | Value |
|---|---:|
| Matches | 74 |
| Teams represented | 10 |
| Venues represented | 6 |
| Group-stage matches | 70 |
| Playoff matches | 3 |
| Final | 1 |

Each row represents one match. The dataset includes match information, participating teams, toss details, innings scores, match result, Player of the Match, top scorer and the best bowling figure recorded for that match.

### Important columns

| Column | What it represents |
|---|---|
| \`match_id\`, \`date\` | Match identifier and date |
| \`venue\`, \`stage\` | Ground and tournament stage |
| \`team1\`, \`team2\` | Teams playing the match |
| \`toss_winner\`, \`toss_decision\` | Toss winner and decision to bat or field |
| \`first_ings_score\`, \`first_ings_wkts\` | First-innings score and wickets lost |
| \`second_ings_score\`, \`second_ings_wkts\` | Second-innings score and wickets lost |
| \`match_winner\`, \`won_by\`, \`margin\` | Winning team, result type and winning margin |
| \`player_of_the_match\` | Player receiving the match award |
| \`top_scorer\`, \`highscore\` | Top scorer recorded for the match and their score |
| \`best_bowling\`, \`best_bowling_figure\` | Bowler and best bowling figures recorded for the match |

The CSV uses the team spelling \`Banglore\` in some rows. The dashboard standardises this label to \`Bangalore\` for display and filtering; the source CSV is kept unchanged.

## What we analyse

The analysis uses Pandas to load and inspect the match records, group related values, calculate summary statistics and prepare data for visualisation. Matplotlib and Seaborn are used in the notebooks, while the dashboard uses Plotly charts.

| Analysis | How it is analysed | Question it answers |
|---|---|---|
| Team performance | Count records by \`match_winner\` | Which teams won the most matches? |
| Result type | Count wins by \`won_by\` | How many matches were won by runs and by wickets? |
| Toss decisions | Count \`toss_decision\` values | Did teams generally choose to bat or field? |
| Toss and match result | Compare \`toss_winner\` with \`match_winner\` | How often did the toss winner also win the match? |
| Player awards | Count \`player_of_the_match\` values | Which players received the most awards? |
| Batting performance | Review \`top_scorer\` and \`highscore\` | Which high individual scores appear in the dataset? |
| Bowling performance | Extract the wicket count from \`best_bowling_figure\` and group by bowler | Which bowlers most often appear with strong match-level figures? |
| Venue analysis | Count matches by \`venue\` | Which venues hosted the most matches? |
| Innings comparison | Compare first- and second-innings scores | How do the two innings relate across matches? |

### Analysis workflow

1. **Load the data:** Read \`IPL.csv\` into a Pandas DataFrame.
2. **Inspect the records:** Check the dimensions, columns, data types and missing values.
3. **Prepare fields:** Standardise the Bangalore team label in the dashboard and extract the wicket count from bowling figures such as \`3--20\`.
4. **Aggregate:** Use value counts and group-by operations to summarise team wins, awards, venues and bowling figures.
5. **Visualise:** Use bar charts, pie charts, scatter plots, histograms, box plots, heatmaps and regression plots to make patterns easier to interpret.
6. **Explore:** Apply dashboard filters for stage, team and venue to inspect a selected subset of matches.

## Findings from the 74 match records

These are descriptive results calculated directly from the included CSV:

- **Gujarat** recorded the most wins with **12**, followed by Rajasthan with **10**. Bangalore and Lucknow recorded 9 each.
- Matches were evenly split by result type: **37 wins by runs** and **37 wins by wickets**.
- Teams chose to **field first in 59 matches** and bat first in 15.
- The toss winner also won the match in **36 of 74 matches (48.6%)**. In this dataset, winning the toss did not automatically translate into a match win.
- **Kuldeep Yadav** received the most Player of the Match awards (**4**), followed by Jos Buttler (**3**).
- **Wankhede Stadium, Mumbai** hosted the most matches (**21**), followed by Dr DY Patil Sports Academy (**20**) and Brabourne Stadium (**16**).
- The highest individual score recorded in the \`highscore\` column is **140**, by **Quinton de Kock**.
- The largest victory by runs in the records was **Chennai's 91-run win**.

These observations describe this dataset only. They do not establish why a team won or prove that a toss decision caused a result.

## Interactive dashboard

The Streamlit dashboard provides four sections:

- **Team performance:** Match wins by team and the split between wins by runs and wickets.
- **Player performance:** Player of the Match awards and a comparison of recorded best bowling figures.
- **Match patterns:** Toss decisions and first-innings versus second-innings scores.
- **Venues:** Number of matches hosted at each venue.

Use the sidebar to filter matches by tournament stage, team and venue. The summary metrics and charts update based on the selected matches.

### Visualisations

The charts below are generated from the IPL analysis notebook and are included as quick previews.

| Team wins | Player of the Match awards |
|---|---|
| ![Team wins](images/team-wins.png) | ![Player awards](images/player-awards.png) |

| Recorded bowling figures | Matches by venue |
|---|---|
| ![Bowling figures](images/bowling-figures.png) | ![Matches by venue](images/venue-matches.png) |

## Run locally

### 1. Clone the repository

~~~bash
git clone https://github.com/abhishekkp00/Data-Visualisation.git
cd Data-Visualisation
~~~

### 2. Create and activate a virtual environment

**Linux / macOS**

~~~bash
python3 -m venv .venv
source .venv/bin/activate
~~~

**Windows PowerShell**

~~~powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
~~~

### 3. Install dependencies

~~~bash
pip install -r requirements.txt
~~~

### 4. Start the dashboard

~~~bash
streamlit run app.py
~~~

Open the local address printed in the terminal by Streamlit.

### Open the notebooks

To work through the visualisation examples and IPL analysis:

~~~bash
jupyter lab
~~~

Open \`IPL_PROJECT.ipynb\` for the IPL analysis. The other notebooks cover the individual plotting libraries and chart types.

## Repository structure

~~~text
Data-Visualisation/
├── app.py
├── IPL.csv
├── IPL_PROJECT.ipynb
├── 1.Matplotlib.ipynb
├── 2.1DistributionPlot.ipynb
├── 2.2-CategoricalPlot.ipynb
├── 3.MatrixPlot.ipynb
├── 4. RegressionPlot.ipynb
├── 5. Plotly.ipynb
├── images/
│   ├── team-wins.png
│   ├── player-awards.png
│   ├── bowling-figures.png
│   └── venue-matches.png
├── requirements.txt
└── README.md
~~~

## Tools and libraries

- **Python** — project language
- **Pandas, NumPy** — data loading, cleaning and analysis
- **Matplotlib, Seaborn** — static data visualisation
- **Plotly** — interactive charts
- **Streamlit** — interactive dashboard
- **Jupyter Notebook** — analysis and practice

## Notes and limitations

- The dataset contains match-level summaries, not ball-by-ball records or complete player season statistics.
- The bowling comparison is derived from the wicket count in each match's recorded best bowling figure. It is **not** a player's total wickets for the season.
- The \`highscore\` field is the top scorer's score recorded for each match; summing it should not be interpreted as a player's official season run total.
- The repository contains the CSV used by this project. Further external dataset provenance is not documented here.
