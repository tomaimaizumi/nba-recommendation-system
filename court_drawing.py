# court_drawing.py

import matplotlib.patches as patches
import matplotlib.pyplot as plt

def draw_court(ax=None):
    if ax is None:
        ax = plt.gca()

    elements = []

    elements.append(patches.Rectangle((-250, -47.5), 500, 440,linewidth=0,facecolor="#F5DEB3", zorder=0))

    elements.append(patches.Circle((0, -20), radius=7.5, linewidth=2, color="red", fill=False))  # ゴール
    elements.append(patches.Rectangle((-30, -27.5), 60, -1, linewidth=2, color="black"))          # バックボード
    elements.append(patches.Rectangle((-80, -47), 160, 180, linewidth=2, color="black", fill=False))  # ペイント
    elements.append(patches.Arc((0, 132.5), 100, 90, theta1=0, theta2=180, linewidth=2, color="black"))  # フリースロー
    elements.append(patches.Arc((0, 0), 430, 430, theta1=10, theta2=170, linewidth=2, color="black"))   # 3Pアーク
    elements.append(patches.Rectangle((-211.5, -47.5), 0, 90, linewidth=2, color="black"))              # コーナー
    elements.append(patches.Rectangle((211.5, -47.5), 0, 90, linewidth=2, color="black"))
    elements.append(patches.Rectangle((-250, -47.5), 500, 440, linewidth=2, color="black", fill=False)) # 外枠
    elements.append(patches.Arc((0, -23), 100, 100, theta1=0, theta2=180, linewidth=2, color="black"))      # ゴール下半円

    # センターサークルの半円（上部のみ）
    elements.append(patches.Arc((0, 392.5),120, 120,theta1=180, theta2=360,linewidth=2,color="black"))


    for e in elements:
        ax.add_patch(e)

    ax.set_xlim(-300, 300)
    ax.set_ylim(-50, 400)
    ax.axis('off')

    ax.set_aspect("equal")

    return ax
