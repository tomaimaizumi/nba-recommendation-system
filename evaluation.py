import pandas as pd
from recommend import recommend_similar

# Precision@K
def precision_at_k(recommended, relevant, k=3):
    hits = sum(1 for p in recommended[:k] if p in relevant)
    return hits / k

# Recall@K
def recall_at_k(recommended, relevant, k=3):
    hits = sum(1 for p in recommended[:k] if p in relevant)
    return hits / len(relevant) if relevant else 0.0

# 手動で作成した正解リスト（例）
manual_test_cases = {
    "LeBron James": {
        "Jimmy Butler", "Scottie Barnes", "Ben Simmons",
        "Kawhi Leonard", "Paul George", "Jayson Tatum",
        "Brandon Ingram", "Khris Middleton", "Zach LaVine", "Jaylen Brown"
    },
    "Stephen Curry": {
        "Klay Thompson", "Damian Lillard", "Trae Young",
        "CJ McCollum", "Kyrie Irving", "Devin Booker",
        "Malcolm Brogdon", "Derrick Rose", "Tyrese Haliburton", "Dante Exum"
    },
    "Kevin Durant": {
        "Jayson Tatum", "Brandon Ingram", "Michael Porter Jr.",
        "Kawhi Leonard", "Paul George", "Jaylen Brown",
        "Harrison Barnes", "Gordon Hayward", "RJ Barrett", "Andrew Wiggins"
    },
    "Desmond Bane": {
        "Buddy Hield", "Duncan Robinson", "Kevin Durant",
        "Gary Trent Jr.", "Bogdan Bogdanović", "Dorian Finney-Smith",
        "Joe Harris", "Norman Powell", "Seth Curry", "Tim Hardaway Jr."
    },
    "Anthony Edwards": {
        "Donovan Mitchell", "Shai Gilgeous-Alexander", "Kevin Durant",
        "Jordan Clarkson", "Caris LeVert", "Malik Beasley",
        "Devin Booker", "Zach LaVine", "Jaylen Brown", "Terry Rozier"
    },
    "Jarrett Allen": {
        "Clint Capela", "Mitchell Robinson", "Deandre Ayton",
        "Richaun Holmes", "Nerlens Noel", "Montrezl Harrell",
        "Mason Plumlee", "Jakob Poeltl", "Bismack Biyombo", "Steven Adams"
    },
    "De'Aaron Fox": {
        "Ja Morant", "Tyrese Haliburton", "Fred VanVleet",
        "Lonzo Ball", "Dennis Smith Jr.", "Derrick Rose",
        "Russell Westbrook", "Jamal Murray", "Shai Gilgeous-Alexander", "Kemba Walker"
    },
    "Darius Garland": {
        "Trae Young", "Collin Sexton", "Jamal Murray",
        "Fred VanVleet", "Tyrese Haliburton", "CJ McCollum",
        "Mike Conley", "Derrick Rose", "De'Aaron Fox", "Lonzo Ball"
    },
    "Josh Giddey": {
        "LaMelo Ball", "Cade Cunningham", "Jalen Green",
        "Tyrese Haliburton", "Desmond Bane", "Darius Garland",
        "De'Aaron Fox", "Shai Gilgeous-Alexander", "Jalen Suggs", "Franz Wagner"
    },
    "John Collins": {
        "Pascal Siakam", "Aaron Gordon", "Kevin Durant",
        "Jaren Jackson Jr.", "Miles Bridges", "PJ Washington",
        "Bam Adebayo", "John Wall", "Harrison Barnes", "Julius Randle"
    },
    "Seth Curry": {
        "Danny Green", "J.J. Redick", "Joe Harris",
        "Tim Hardaway Jr.", "Norman Powell", "JJ Redick",
        "Patty Mills", "Dorian Finney-Smith", "Gary Trent Jr.", "RJ Barrett"
    },
    "Malcolm Brogdon": {
        "George Hill", "Mike Conley", "Fred VanVleet",
        "Patty Mills", "Tyrese Haliburton", "Darren Collison",
        "Jeff Teague", "Ish Smith", "J.J. Barea", "Derrick Rose"
    },
    "Kyle Kuzma": {
        "Doug McDermott", "Norman Powell", "Michael Porter Jr.",
        "Will Barton", "Torrey Craig", "Jae Crowder",
        "Robby Hummel", "Troy Daniels", "Bojan Bogdanović", "Kelly Olynyk"
    }
}


# 評価処理
def evaluate_manual(full_df, vectors, test_cases, k=3):
    results = []

    for player, relevant in test_cases.items():
        recommended_df = recommend_similar(
            player_name=player,
            vectors=vectors,
            full_df=full_df,
            top_n=k,
            same_position=False,
            min_shots=0
        )
        recommended = recommended_df["player_name"].tolist()

        prec = precision_at_k(recommended, relevant, k)
        rec = recall_at_k(recommended, relevant, k)

        results.append({
            "player": player,
            "precision@{}".format(k): round(prec, 3),
            "recall@{}".format(k): round(rec, 3),
            "relevant": list(relevant),
            "recommended": recommended
        })

    df_results = pd.DataFrame(results)
    avg_prec = df_results[f"precision@{k}"].mean()
    avg_rec = df_results[f"recall@{k}"].mean()

    summary = {
        "avg_precision": round(avg_prec, 3),
        "avg_recall": round(avg_rec, 3),
        "num_test_cases": len(test_cases),
        "details": df_results
    }
    return summary
