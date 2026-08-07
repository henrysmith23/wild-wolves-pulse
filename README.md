# Liverpool Pulse

Streamlit dashboard tracking Liverpool FC's cumulative goals scored and conceded across the Premier League season, compared against the previous season.

## Data Source

Match results from [football-data.org](https://www.football-data.org/) API (free tier).

## Setup

1. Get a free API key from football-data.org
2. Set the `FOOTBALL_DATA_API_KEY` environment variable
3. `pip install -r requirements.txt`
4. `python collector.py` to fetch data
5. `streamlit run app.py` to view the dashboard

## Automation

A GitHub Actions workflow runs weekly (Tuesdays) to fetch new match results and commit updated data. The API key is stored as a repository secret.
