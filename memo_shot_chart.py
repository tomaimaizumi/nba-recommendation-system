# shot_chart.py

from court_drawing import draw_court

# 各ゾーンの描画位置（3Pはライン外に表示）
zone_coords = {
    "restricted_area": (0, 20),
    "in_paint": (0, 100),
    "mid_range": (0, 195),
    "right_corner": (260, 0),      # ライン外
    "left_corner": (-260, 0),      # ライン外
    "right_wing": (200, 150),       # ライン外
    "left_wing": (-200, 150),       # ライン外
    "top_3": (0, 250),              # アーチ上
}

def draw_shot_chart(player_name, player_data, ax, title=""):
    draw_court(ax)
    stats = player_data.loc[player_name]

    for zone, (x, y) in zone_coords.items():
        if zone in stats:
            value = stats[zone]
            ax.text(x, y, f"{value:.1f}%", ha='center', va='center', fontsize=11, weight='bold')

    ax.set_title(title, fontsize=14)
#-------------------------------------------------------------------------------------------------------
# shot_chart.py

from court_drawing import draw_court

zone_coords = {
    "restricted_area": (0, 20),
    "in_paint": (0, 100),
    "mid_range": (0, 195),
    "right_corner": (260, 0),
    "left_corner": (-260, 0),
    "right_wing": (200, 150),
    "left_wing": (-200, 150),
    "top_3": (0, 250),
}

def draw_shot_chart(player_name, player_data, ax, title=""):
    draw_court(ax)
    stats = player_data.loc[player_name] if isinstance(player_data, dict) == False else player_data

    for zone, (x, y) in zone_coords.items():
        if zone in stats:
            value = stats[zone]
            color = "red" if value < 30 else ("orange" if value < 40 else "green")
            ax.text(x, y, f"{value:.1f}%", ha='center', va='center', fontsize=11, weight='bold', color=color)

    ax.set_title(title, fontsize=14)
#----------------------------------------------------------------------------
# shot_chart.py

from court_drawing import draw_court

zone_coords = {
    "restricted_area": (0, 20),
    "in_paint": (0, 100),
    "mid_range": (0, 195),
    "right_corner": (260, 0),
    "left_corner": (-260, 0),
    "right_wing": (200, 150),
    "left_wing": (-200, 150),
    "top_3": (0, 250),
}

def draw_shot_chart(player_name, player_data, ax, title=""):
    draw_court(ax)
    stats = player_data.loc[player_name] if hasattr(player_data, "loc") else player_data

    for zone, (x, y) in zone_coords.items():
        if zone in stats:
            value = stats[zone]
            color = "green" if value >= 40 else ("orange" if value >= 30 else "red")
            ax.text(x, y, f"{value:.1f}%", ha='center', va='center', fontsize=11, weight='bold', color=color)

    ax.set_title(title, fontsize=14)
#------------------------------------------------------------------------------------------------------------------
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
    "mid_range": (0, 195),
    "right_corner": (260, 0),
    "left_corner": (-260, 0),
    "right_wing": (200, 150),
    "left_wing": (-200, 150),
    "top_3": (0, 250),
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
            value = stats[zone]
            color = cmap(norm(value))

            # ゾーンを色付き円で可視化
            circle = patches.Circle((x, y), radius=28, color=color, alpha=0.85)
            ax.add_patch(circle)

            # 成功率の数値表示
            ax.text(x, y, f"{value:.1f}%", ha='center', va='center',
                    fontsize=10, color='black', weight='bold')

    ax.set_title(title, fontsize=14)
#-------------------------------------------------------------------------------------------------
# shot_chart.py

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from court_drawing import draw_court
import numpy as np

norm = mcolors.Normalize(vmin=20, vmax=60)
cmap = cm.get_cmap("RdYlGn")

def draw_shot_chart(player_name, player_data, ax, title=""):
    draw_court(ax)
    stats = player_data.loc[player_name] if hasattr(player_data, "loc") else player_data

    # 1. ゴール下（restricted_area）
    if "restricted_area" in stats:
        val = stats["restricted_area"]
        color = cmap(norm(val))
        arc = patches.Wedge((0, -25), 50, 0, 180, facecolor=color, alpha=0.8)
        ax.add_patch(arc)
        ax.text(0, -5, f"{val:.1f}%", ha='center', va='center', fontsize=10, weight='bold')

    # 2. ペイント内（in_paint）→ そのまま
    if "in_paint" in stats:
        val = stats["in_paint"]
        color = cmap(norm(val))
        rect = patches.Rectangle((-80, -48), 160, 180, facecolor=color, alpha=0.7)
        ax.add_patch(rect)
        ax.text(0, 70, f"{val:.1f}%", ha='center', va='center', fontsize=10, weight='bold')

    # 3. ミドルレンジ（mid_range）→ ペイント外かつ3Pライン内
    if "mid_range" in stats:
        val = stats["mid_range"]
        color = cmap(norm(val))
        arc = patches.Wedge((0, 0), 200, 0, 180, width=95, facecolor=color, alpha=0.5)
        ax.add_patch(arc)
        ax.text(0, 160, f"{val:.1f}%", ha='center', va='center', fontsize=10, weight='bold')

    # 4. コーナー3P（直線部分）
    if "left_corner" in stats:
        val = stats["left_corner"]
        color = cmap(norm(val))
        rect = patches.Rectangle((-250, -48), 38.5, 95, facecolor=color, alpha=0.8)
        ax.add_patch(rect)
        ax.text(-235, 5, f"{val:.1f}%", ha='center', va='center', fontsize=9, weight='bold')

    if "right_corner" in stats:
        val = stats["right_corner"]
        color = cmap(norm(val))
        rect = patches.Rectangle((211.5, -48), 38.5, 95, facecolor=color, alpha=0.8)
        ax.add_patch(rect)
        ax.text(235, 5, f"{val:.1f}%", ha='center', va='center', fontsize=9, weight='bold')

    # 5. ウイング（30°〜60° 弧状部分）
    if "left_wing" in stats:
        val = stats["left_wing"]
        color = cmap(norm(val))
        arc = patches.Wedge((0, 0), 255, 110, 170, width=40, facecolor=color, alpha=0.6)
        ax.add_patch(arc)
        ax.text(-180, 150, f"{val:.1f}%", ha='center', va='center', fontsize=9, weight='bold')

    if "right_wing" in stats:
        val = stats["right_wing"]
        color = cmap(norm(val))
        arc = patches.Wedge((0, 0), 255, 10, 70, width=40, facecolor=color, alpha=0.6)
        ax.add_patch(arc)
        ax.text(180, 150, f"{val:.1f}%", ha='center', va='center', fontsize=9, weight='bold')

    # 6. トップ（60°〜120° 弧状部分）
    if "top_3" in stats:
        val = stats["top_3"]
        color = cmap(norm(val))
        arc = patches.Wedge((0, 0), 255, 70, 110, width=40, facecolor=color, alpha=0.6)
        ax.add_patch(arc)
        ax.text(0, 230, f"{val:.1f}%", ha='center', va='center', fontsize=9, weight='bold')

    ax.set_title(title, fontsize=14)
#-------------------------------------------------------------------------------------------
# shot_chart.py

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from shapely.geometry import Polygon as SPolygon
from court_drawing import draw_court
import numpy as np

norm = mcolors.Normalize(vmin=20, vmax=60)
cmap = cm.get_cmap("RdYlGn")

def draw_shot_chart(player_name, player_data, ax, title=""):
    draw_court(ax)
    stats = player_data.loc[player_name] if hasattr(player_data, "loc") else player_data

    # 6. トップ（60°〜120° 弧状部分）
    if "top_3" in stats:
        val = stats["top_3"]
        color = cmap(norm(val))
        arc = patches.Wedge((0, 0), 255, 70, 110, width=40, facecolor=color, alpha=0.5,zorder=2)
        ax.add_patch(arc)
        ax.text(0, 230, f"{val:.1f}%", ha='center', va='center', fontsize=9, weight='bold',zorder=100)

    # 5. ウイング（30°〜60° 弧状部分）
    if "left_wing" in stats:
        val = stats["left_wing"]
        color = cmap(norm(val))
        arc = patches.Wedge((0, 0), 255, 110, 168, width=40, facecolor=color, alpha=0.5,zorder=3)
        ax.add_patch(arc)
        ax.text(-180, 150, f"{val:.1f}%", ha='center', va='center', fontsize=9, weight='bold',zorder=100)

    if "right_wing" in stats:
        val = stats["right_wing"]
        color = cmap(norm(val))
        arc = patches.Wedge((0, 0), 255, 12, 70, width=40, facecolor=color, alpha=0.5,zorder=4)
        ax.add_patch(arc)
        ax.text(180, 150, f"{val:.1f}%", ha='center', va='center', fontsize=9, weight='bold',zorder=100)


    # 4. コーナー3P（直線部分）
    if "left_corner" in stats:
        val = stats["left_corner"]
        color = cmap(norm(val))
        rect = patches.Rectangle((-250, -48), 38.5, 95, facecolor=color, alpha=0.5,zorder=5)
        ax.add_patch(rect)
        ax.text(-235, 5, f"{val:.1f}%", ha='center', va='center', fontsize=9, weight='bold',zorder=100)

    if "right_corner" in stats:
        val = stats["right_corner"]
        color = cmap(norm(val))
        rect = patches.Rectangle((211.5, -48), 38.5, 95, facecolor=color, alpha=0.5,zorder=6)
        ax.add_patch(rect)
        ax.text(235, 5, f"{val:.1f}%", ha='center', va='center', fontsize=9, weight='bold',zorder=100)


    # 2. ペイント内（in_paint）→ そのまま
    if "in_paint" in stats:
        val = stats["in_paint"]
        color = cmap(norm(val))
        rect = patches.Rectangle((-80, -48), 160, 180, facecolor=color, alpha=0.5,zorder=7)
        ax.add_patch(rect)
        ax.text(0, 70, f"{val:.1f}%", ha='center', va='center', fontsize=10, weight='bold',zorder=100)

    # 1. ゴール下（restricted_area）
    if "restricted_area" in stats:
        val = stats["restricted_area"]
        color = cmap(norm(val))
        arc = patches.Wedge((0, -25), 50, 0, 180, facecolor=color, alpha=0.5,zorder=8)
        ax.add_patch(arc)
        ax.text(0, -5, f"{val:.1f}%", ha='center', va='center', fontsize=10, weight='bold',zorder=100)

     # 3. ミドルレンジ（mid_range）→ ペイント外かつ3Pライン内
    if "mid_range" in stats:
        val = stats["mid_range"]
        color = cmap(norm(val))
        arc = patches.Wedge((0, 0), 215, 10, 170, facecolor=color, alpha=0.5,zorder=1)
        
        #rect1 = patches.Rectangle((-80, 132.5), 160, 25, facecolor=color, alpha=0.5,zorder=2)
        ax.add_patch(arc)
        #ax.add_patch(rect1)

        ax.text(0, 160, f"{val:.1f}%", ha='center', va='center', fontsize=10, weight='bold',zorder=100)


    ax.set_title(title, fontsize=14)
