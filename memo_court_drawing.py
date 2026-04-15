# court_drawing.py

import matplotlib.patches as patches
import matplotlib.pyplot as plt

def draw_court(ax=None):
    if ax is None:
        ax = plt.gca()

    # フリースロー、ペイント、リング、3Pアークなど
    elements = []

    # ゴール（リング）
    elements.append(patches.Circle((0, 0), radius=7.5, linewidth=2, color="black", fill=False))

    # バックボード
    elements.append(patches.Rectangle((-30, -7.5), 60, -1, linewidth=2, color="black"))

    # ペイントエリア（細長く）
    elements.append(patches.Rectangle((-80, -47.5), 160, 180, linewidth=2, color="black", fill=False))

    # フリースローサークル（上のみ）
    elements.append(patches.Arc((0, 132.5), 100, 90, theta1=0, theta2=180, linewidth=2, color="black"))

    # 3Pラインアーク（正面）
    elements.append(patches.Arc((0, 0), 430, 430, theta1=10, theta2=170, linewidth=2, color="black"))

    # コーナーの3Pライン（縦線）
    elements.append(patches.Rectangle((-211.5, -47.5), 0, 90, linewidth=2, color="black"))
    elements.append(patches.Rectangle((211.5, -47.5), 0, 90, linewidth=2, color="black"))

    # コートの線
    elements.append(patches.Rectangle((-250, -47.5), 500, 440, linewidth=2, color="black", fill=False))

    # ゴール下の半円
    elements.append(patches.Arc((0, 7), 100, 90, theta1=0, theta2=180, linewidth=2, color="black"))

    # 描画
    for element in elements:
        ax.add_patch(element)

    # 軸の設定
    ax.set_xlim(-270, 270)
    ax.set_ylim(-50, 400)
    ax.axis('off')

    return ax
#------------------------------------------------------------------------------------------------------------------------
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
