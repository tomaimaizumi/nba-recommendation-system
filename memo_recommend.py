import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def load_vectors(csv_path):
    df = pd.read_csv(csv_path)
    df = df.set_index("player_name")
    exclude = ["overall", "total_shots", "made_shots"]
    zone_cols = [col for col in df.columns if col not in exclude]
    return df[zone_cols]

def recommend_similar(player_name, vectors, top_n=1):
    similarity = cosine_similarity(vectors)
    sim_df = pd.DataFrame(similarity, index=vectors.index, columns=vectors.index)
    return sim_df[player_name].sort_values(ascending=False).iloc[1:top_n+1]
#-----------------------------------------------------------------------------------------------------------
# court_drawing.py

import matplotlib.patches as patches
import matplotlib.pyplot as plt

def draw_court(ax=None):
    if ax is None:
        ax = plt.gca()

    elements = []

    # リング
    elements.append(patches.Circle((0, 0), radius=7.5, linewidth=2, color="black", fill=False))
    # バックボード
    elements.append(patches.Rectangle((-30, -7.5), 60, -1, linewidth=2, color="black"))
    # ペイントエリア（細長く）
    elements.append(patches.Rectangle((-80, -47.5), 160, 180, linewidth=2, color="black", fill=False))
    # フリースローサークル
    elements.append(patches.Arc((0, 132.5), 100, 90, theta1=0, theta2=180, linewidth=2, color="black"))
    # 3Pアーク
    elements.append(patches.Arc((0, 0), 430, 430, theta1=10, theta2=170, linewidth=2, color="black"))
    # コーナー3Pライン
    elements.append(patches.Rectangle((-211.5, -47.5), 0, 90, linewidth=2, color="black"))
    elements.append(patches.Rectangle((211.5, -47.5), 0, 90, linewidth=2, color="black"))
    # 外枠
    elements.append(patches.Rectangle((-250, -47.5), 500, 440, linewidth=2, color="black", fill=False))
    # ゴール下半円
    elements.append(patches.Arc((0, 7), 100, 90, theta1=0, theta2=180, linewidth=2, color="black"))

    for e in elements:
        ax.add_patch(e)

    ax.set_xlim(-270, 270)
    ax.set_ylim(-50, 400)
    ax.axis('off')

    return ax
