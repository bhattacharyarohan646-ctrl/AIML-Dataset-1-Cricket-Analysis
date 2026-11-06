
# =====================================================
# AIML DATASET 1 - CRICKET MATCH ANALYSIS
# Question 1: Top 10 Batsmen Based on Total Runs
# =====================================================

import pandas as pd

# Load Dataset
try:
    try:
        df = pd.read_csv("dataset.csv")
    except FileNotFoundError:
        df = pd.read_csv("dataset.csv.csv")

    print("Dataset loaded successfully!")
    print("Total Records:", len(df))

except FileNotFoundError:
    print("Error: CSV file not found. Check the file name.")

    raise SystemExit


# Check required columns
required_columns = ["Player", "R"]

if not all(col in df.columns for col in required_columns):
    print("Required columns are missing!")
    raise SystemExit


# Convert runs into numeric values
df["R"] = pd.to_numeric(df["R"], errors="coerce").fillna(0)


# Calculate total runs scored by each player
top_batsmen = (
    df.groupby("Player")["R"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

top_batsmen.columns = ["Player Name", "Total Runs"]

# Display Results
print("\n========================================")
print(" QUESTION 1: TOP 10 BATSMEN")
print("========================================")

print(top_batsmen.to_string(index=False))


# Save results
top_batsmen.to_csv("Q1_Top_10_Batsmen.csv", index=False)

print("\nResults saved to Q1_Top_10_Batsmen.csv")




# =====================================================
# QUESTION 2: TOP 10 PLAYERS BY STRIKE RATE
# Minimum 50 Balls Faced
# =====================================================

# Convert Runs and Balls into numeric values
df["R"] = pd.to_numeric(df["R"], errors="coerce").fillna(0)
df["B"] = pd.to_numeric(df["B"], errors="coerce").fillna(0)

# Calculate total runs and balls for each player
player_stats = df.groupby("Player").agg(
    Total_Runs=("R", "sum"),
    Total_Balls=("B", "sum")
).reset_index()

# Filter players who faced at least 50 balls
qualified_players = player_stats[
    player_stats["Total_Balls"] >= 50
].copy()

# Calculate overall strike rate
qualified_players["Strike_Rate"] = (
    qualified_players["Total_Runs"] /
    qualified_players["Total_Balls"]
) * 100

# Sort and select Top 10 players
top_strike_rate = qualified_players.sort_values(
    by="Strike_Rate",
    ascending=False
).head(10)

# Display Results
print("\n========================================")
print(" QUESTION 2: TOP 10 STRIKE RATE")
print("========================================")

print(
    top_strike_rate[
        ["Player", "Total_Runs", "Total_Balls", "Strike_Rate"]
    ].round(2).to_string(index=False)
)

# Save results
top_strike_rate.to_csv(
    "Q2_Top_10_Strike_Rate.csv",
    index=False
)

print("\nResults saved to Q2_Top_10_Strike_Rate.csv")



# =====================================================
# QUESTION 3: MOST FOURS AND SIXES
# =====================================================

# Convert boundary columns into numeric values
df["4s"] = pd.to_numeric(df["4s"], errors="coerce").fillna(0)
df["6s"] = pd.to_numeric(df["6s"], errors="coerce").fillna(0)

# Calculate total fours and sixes for each player
boundary_stats = df.groupby("Player").agg(
    Total_Fours=("4s", "sum"),
    Total_Sixes=("6s", "sum")
).reset_index()

# Find maximum fours and sixes
max_fours = boundary_stats["Total_Fours"].max()
max_sixes = boundary_stats["Total_Sixes"].max()

# Find player(s) with most fours
most_fours = boundary_stats[
    boundary_stats["Total_Fours"] == max_fours
]

# Find player(s) with most sixes
most_sixes = boundary_stats[
    boundary_stats["Total_Sixes"] == max_sixes
]

# Display Results
print("\n========================================")
print(" QUESTION 3: MOST FOURS AND SIXES")
print("========================================")

print("\nPlayer(s) with Most Fours:")
print(most_fours[["Player", "Total_Fours"]].to_string(index=False))

print("\nPlayer(s) with Most Sixes:")
print(most_sixes[["Player", "Total_Sixes"]].to_string(index=False))

# Save complete boundary statistics
boundary_stats = boundary_stats.sort_values(
    by=["Total_Fours", "Total_Sixes"],
    ascending=False
)

boundary_stats.to_csv(
    "Q3_Boundary_Statistics.csv",
    index=False
)

print("\nResults saved to Q3_Boundary_Statistics.csv")




# =====================================================
# QUESTION 4: TEAM WITH HIGHEST NUMBER OF WINS
# =====================================================

# Group match records to avoid counting every player row
match_results = df.groupby(
    ["Date", "Team", "Vs"],
    as_index=False
)["Win"].first()

# Select only winning teams
winning_matches = match_results[
    match_results["Win"] == 1
]

# Count total wins for each team
team_wins = winning_matches.groupby(
    "Team"
).size().reset_index(name="Total Wins")

# Sort teams by total wins
team_wins = team_wins.sort_values(
    by="Total Wins",
    ascending=False
)

# Find the team with maximum wins
highest_wins = team_wins["Total Wins"].max()

top_teams = team_wins[
    team_wins["Total Wins"] == highest_wins
]

# Display Results
print("\n========================================")
print(" QUESTION 4: MOST MATCHES WON")
print("========================================")

print("\nTeam(s) with Highest Number of Wins:")
print(top_teams.to_string(index=False))

print("\nComplete Team Wins Ranking:")
print(team_wins.to_string(index=False))

# Save results
team_wins.to_csv("Q4_Team_Wins.csv", index=False)

print("\nResults saved to Q4_Team_Wins.csv")




# =====================================================
# QUESTION 5: HIGHEST RUN SCORER IN EACH MATCH
# =====================================================

# Create a unique match identifier using date and both teams
df["Match_ID"] = df.apply(
    lambda row: (
        str(row["Date"]) + "_" +
        "_".join(sorted([
            str(row["Team"]).strip(),
            str(row["Vs"]).strip()
        ]))
    ),
    axis=1
)

# Convert runs into numeric values
df["R"] = pd.to_numeric(df["R"], errors="coerce").fillna(0)

# Find the highest run scorer in each match
top_scorers = df.loc[
    df.groupby("Match_ID")["R"].idxmax()
].copy()

# Select required columns
match_top_scorers = top_scorers[
    ["Date", "Player", "Team", "Vs", "R"]
].copy()

# Rename columns
match_top_scorers.columns = [
    "Match Date",
    "Player Name",
    "Team",
    "Opponent",
    "Runs Scored"
]

# Sort by match date
match_top_scorers = match_top_scorers.sort_values(
    by="Match Date"
)

# Display Results
print("\n========================================")
print(" QUESTION 5: TOP SCORER IN EACH MATCH")
print("========================================")

print(match_top_scorers.to_string(index=False))

# Save results
match_top_scorers.to_csv(
    "Q5_Highest_Run_Scorer.csv",
    index=False
)

print("\nTotal Matches Analyzed:", len(match_top_scorers))

print("\nResults saved to Q5_Highest_Run_Scorer.csv")



# =====================================================
# QUESTION 6: CHASING VS BATTING FIRST
# =====================================================

# Create unique match identifier
df["Match_ID"] = df.apply(
    lambda row: (
        str(row["Date"]) + "_" +
        "_".join(sorted([
            str(row["Team"]).strip(),
            str(row["Vs"]).strip()
        ]))
    ),
    axis=1
)

# Calculate total runs scored by each team in each match
match_team_runs = df.groupby(
    ["Match_ID", "Date", "Team", "Vs"],
    as_index=False
).agg(
    Total_Runs=("R", "sum"),
    Win=("Win", "first")
)

# Determine batting order from dataset row order
# The first team listed in each match is treated as batting first
match_team_runs["Batting_Order"] = (
    match_team_runs.groupby("Match_ID").cumcount()
)

match_team_runs["Situation"] = (
    match_team_runs["Batting_Order"].map({
        0: "Batting First",
        1: "Chasing"
    })
)

# Calculate average runs and wins
performance = match_team_runs.groupby(
    "Situation"
).agg(
    Average_Runs=("Total_Runs", "mean"),
    Matches=("Match_ID", "count"),
    Total_Wins=("Win", "sum")
).reset_index()

# Calculate win percentage
performance["Win_Percentage"] = (
    performance["Total_Wins"] /
    performance["Matches"]
) * 100

# Display Results
print("\n========================================")
print(" QUESTION 6: CHASING VS BATTING FIRST")
print("========================================")

print(performance.round(2).to_string(index=False))

# Save results
performance.to_csv(
    "Q6_Chasing_vs_Batting_First.csv",
    index=False
)

print("\nResults saved to Q6_Chasing_vs_Batting_First.csv")



# =====================================================
# QUESTION 7: TOP 10 BOWLERS BY WICKETS
# =====================================================

# Extract bowler names from Dismissal column
# The bowler name appears after 'b'

bowling_data = df[
    df["Dismissal"].notna()
].copy()

bowling_data["Bowler"] = bowling_data[
    "Dismissal"
].str.extract(r'\bb\s+(.+)$', expand=False)

# Remove missing bowler names
bowling_data = bowling_data.dropna(
    subset=["Bowler"]
)

# Clean bowler names
bowling_data["Bowler"] = (
    bowling_data["Bowler"].str.strip()
)

# Count wickets taken by each bowler
bowler_stats = bowling_data.groupby(
    "Bowler"
).size().reset_index(name="Total_Wickets")

# Sort by wickets
top_bowlers = bowler_stats.sort_values(
    by="Total_Wickets",
    ascending=False
).head(10)

# Display Results
print("\n========================================")
print(" QUESTION 7: TOP 10 BOWLERS")
print("========================================")

print(top_bowlers.to_string(index=False))

print("\nNote: Economy Rate is unavailable in this dataset.")

# Save results
top_bowlers.to_csv(
    "Q7_Top_10_Bowlers.csv",
    index=False
)

print("\nResults saved to Q7_Top_10_Bowlers.csv")



# =====================================================
# QUESTION 8: MOST RUNS THROUGH BOUNDARIES
# =====================================================

# Convert columns into numeric values
for col in ["R", "B", "4s", "6s"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Calculate player performance
boundary_analysis = df.groupby("Player").agg(
    Total_Runs=("R", "sum"),
    Total_Balls=("B", "sum"),
    Total_Fours=("4s", "sum"),
    Total_Sixes=("6s", "sum")
).reset_index()

# Calculate runs scored through boundaries
boundary_analysis["Boundary_Runs"] = (
    boundary_analysis["Total_Fours"] * 4 +
    boundary_analysis["Total_Sixes"] * 6
)

# Calculate strike rate
boundary_analysis["Strike_Rate"] = (
    boundary_analysis["Total_Runs"] /
    boundary_analysis["Total_Balls"].replace(0, float("nan"))
) * 100

# Calculate overall average strike rate
overall_average_sr = (
    boundary_analysis["Total_Runs"].sum() /
    boundary_analysis["Total_Balls"].sum()
) * 100

# Sort players by boundary runs
top_boundary_players = boundary_analysis.sort_values(
    by="Boundary_Runs",
    ascending=False
).head(10).copy()

# Compare strike rate with overall average
top_boundary_players["SR_Comparison"] = (
    top_boundary_players["Strike_Rate"] - overall_average_sr
)

# Display Results
print("\n========================================")
print(" QUESTION 8: TOP BOUNDARY SCORERS")
print("========================================")

print("\nOverall Average Strike Rate:",
      round(overall_average_sr, 2))

print("\nTop 10 Players by Boundary Runs:")

print(
    top_boundary_players[
        ["Player", "Total_Fours", "Total_Sixes",
         "Boundary_Runs", "Total_Runs",
         "Strike_Rate", "SR_Comparison"]
    ].round(2).to_string(index=False)
)

# Save results
top_boundary_players.to_csv(
    "Q8_Top_Boundary_Scorers.csv",
    index=False
)

print("\nResults saved to Q8_Top_Boundary_Scorers.csv")


# =====================================================
# QUESTION 9: PLAYER PERFORMANCE SCORE (TOP 20)
# =====================================================

# Calculate player statistics
player_performance = df.groupby("Player").agg(
    Total_Runs=("R", "sum"),
    Total_Balls=("B", "sum"),
    Total_Fours=("4s", "sum"),
    Total_Sixes=("6s", "sum")
).reset_index()

# Calculate Strike Rate
player_performance["Strike_Rate"] = (
    player_performance["Total_Runs"] /
    player_performance["Total_Balls"].replace(0, float("nan"))
) * 100

# Min-Max Normalization
features = [
    "Total_Runs",
    "Strike_Rate",
    "Total_Fours",
    "Total_Sixes",
    "Total_Balls"
]

for feature in features:
    min_value = player_performance[feature].min()
    max_value = player_performance[feature].max()

    if max_value == min_value:
        player_performance[feature + "_Score"] = 0
    else:
        player_performance[feature + "_Score"] = (
            (player_performance[feature] - min_value) /
            (max_value - min_value)
        )

# Calculate Weighted Player Performance Score
player_performance["Performance_Score"] = (
    0.40 * player_performance["Total_Runs_Score"] +
    0.25 * player_performance["Strike_Rate_Score"] +
    0.15 * player_performance["Total_Fours_Score"] +
    0.10 * player_performance["Total_Sixes_Score"] +
    0.10 * player_performance["Total_Balls_Score"]
) * 100

# Rank Top 20 Batsmen
top_20_batsmen = player_performance.sort_values(
    by="Performance_Score",
    ascending=False
).head(20).copy()

top_20_batsmen.insert(
    0,
    "Rank",
    range(1, len(top_20_batsmen) + 1)
)

# Display Results
print("\n========================================")
print(" QUESTION 9: TOP 20 BATSMEN")
print("========================================")

print(
    top_20_batsmen[
        ["Rank", "Player", "Total_Runs",
         "Strike_Rate", "Total_Fours",
         "Total_Sixes", "Total_Balls",
         "Performance_Score"]
    ].round(2).to_string(index=False)
)

# Save Results
top_20_batsmen.to_csv(
    "Q9_Top_20_Performance_Score.csv",
    index=False
)

print("\nResults saved to Q9_Top_20_Performance_Score.csv")




# =====================================================
# QUESTION 10: TOP 10 ALL-ROUND PERFORMERS
# =====================================================

# 1. Calculate batting performance
batting_stats = df.groupby("Player").agg(
    Total_Runs=("R", "sum"),
    Total_Balls=("B", "sum"),
    Total_Fours=("4s", "sum"),
    Total_Sixes=("6s", "sum")
).reset_index()

# Calculate Strike Rate
batting_stats["Strike_Rate"] = (
    batting_stats["Total_Runs"] /
    batting_stats["Total_Balls"].replace(0, float("nan"))
) * 100

# Calculate Boundary Runs
batting_stats["Boundary_Runs"] = (
    batting_stats["Total_Fours"] * 4 +
    batting_stats["Total_Sixes"] * 6
)

# 2. Extract wickets credited to bowlers
bowling_data = df.copy()

bowling_data["Bowler"] = bowling_data[
    "Dismissal"
].str.extract(r'\bb\s+(.+)$', expand=False)

bowling_data = bowling_data.dropna(
    subset=["Bowler"]
)

bowling_data["Bowler"] = (
    bowling_data["Bowler"].str.strip()
)

bowling_stats = bowling_data.groupby(
    "Bowler"
).size().reset_index(name="Total_Wickets")

bowling_stats = bowling_stats.rename(
    columns={"Bowler": "Player"}
)

# 3. Calculate match wins for each player
player_wins = df.groupby("Player")["Win"].sum().reset_index()

player_wins.columns = ["Player", "Match_Wins"]

# 4. Combine batting and bowling statistics
all_rounders = batting_stats.merge(
    bowling_stats,
    on="Player",
    how="outer"
)

all_rounders = all_rounders.merge(
    player_wins,
    on="Player",
    how="left"
)

# Fill missing values
numeric_columns = [
    "Total_Runs",
    "Total_Balls",
    "Total_Fours",
    "Total_Sixes",
    "Boundary_Runs",
    "Total_Wickets",
    "Match_Wins"
]

all_rounders[numeric_columns] = (
    all_rounders[numeric_columns].fillna(0)
)

# 5. Fill missing strike rates
all_rounders["Strike_Rate"] = (
    all_rounders["Strike_Rate"].fillna(0)
)

# 6. Normalize performance metrics
features = [
    "Total_Runs",
    "Total_Wickets",
    "Strike_Rate",
    "Boundary_Runs",
    "Match_Wins"
]

for feature in features:
    minimum = all_rounders[feature].min()
    maximum = all_rounders[feature].max()

    if maximum == minimum:
        all_rounders[feature + "_Score"] = 0
    else:
        all_rounders[feature + "_Score"] = (
            (all_rounders[feature] - minimum) /
            (maximum - minimum)
        )

# 7. Calculate Match Impact Score
all_rounders["Match_Impact_Score"] = (
    0.25 * all_rounders["Total_Runs_Score"] +
    0.30 * all_rounders["Total_Wickets_Score"] +
    0.20 * all_rounders["Strike_Rate_Score"] +
    0.15 * all_rounders["Boundary_Runs_Score"] +
    0.10 * all_rounders["Match_Wins_Score"]
) * 100

# 8. Rank Top 10 All-Round Performers
top_10_all_rounders = all_rounders.sort_values(
    by="Match_Impact_Score",
    ascending=False
).head(10).copy()

top_10_all_rounders.insert(
    0,
    "Rank",
    range(1, len(top_10_all_rounders) + 1)
)

# 9. Display Results
print("\n========================================")
print(" QUESTION 10: TOP 10 ALL-ROUND PERFORMERS")
print("========================================")

print(
    top_10_all_rounders[
        ["Rank", "Player", "Total_Runs",
         "Total_Wickets", "Strike_Rate",
         "Boundary_Runs", "Match_Wins",
         "Match_Impact_Score"]
    ].round(2).to_string(index=False)
)

# 10. Save Results
top_10_all_rounders.to_csv(
    "Q10_Top_10_All_Rounders.csv",
    index=False
)

print("\nNote: Economy Rate is unavailable in this dataset.")
print("Match Impact Score is calculated using 5 available metrics.")

print("\nResults saved to Q10_Top_10_All_Rounders.csv")

