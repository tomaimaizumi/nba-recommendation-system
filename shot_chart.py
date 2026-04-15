# shot_chart.py

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from court_drawing import draw_court

# 各ゾーンの描画中心座標（バスケットコート上）
zone_coords = {
    "restricted_area": (0, 20),
    "in_paint": (0, 100),
    "center_mid": (0, 180),
    "left_mid": (-150, 20),
    "right_mid": (150, 20),
    "right_corner": (260, 0),
    "left_corner": (-260, 0),
    "right_wing": (200, 150),
    "left_wing": (-200, 150),
    "top_3": (0, 250),
    "deep_3": (0, 350)
}

# ヒートマップの色スケーリング：成功率が 20〜60% の範囲を想定
norm = mcolors.Normalize(vmin=15, vmax=60)
cmap = cm.get_cmap("RdYlGn")  # 赤→黄→緑のカラーマップ

def draw_shot_chart(player_name, player_data, ax, title=""):
    """
    指定した選手のシュートゾーン成功率をヒートマップ風に描画する。
    
    Parameters:
        player_name (str): 選手名（インデックス）
        player_data (DataFrame): 各ゾーンの成功率を持つ DataFrame
        ax (matplotlib.axes): 描画対象の Axes オブジェクト
        title (str): グラフタイトル
    """
    draw_court(ax)
    
    stats = player_data.loc[player_name] if hasattr(player_data, "loc") else player_data

    for zone, (x, y) in zone_coords.items():
        if zone in stats:
            value = stats[zone] * 100
            color = cmap(norm(value))

            # ゾーンを色付き円で可視化
            circle = patches.Circle((x, y), radius=35, color=color, alpha=0.85)
            ax.add_patch(circle)

            # 成功率の数値表示
            ax.text(x, y, f"{value:.1f}%", ha='center', va='center', fontsize=10, color='black', weight='bold')

    ax.set_title(title, fontsize=14)
    ax.set_aspect("equal")