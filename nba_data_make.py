from nba_api.stats.endpoints import shotchartdetail, commonplayerinfo
from nba_api.stats.static import players
import pandas as pd
from tqdm import tqdm
import time

SEASON = '2023-24'
MAX_VALID_PLAYERS = 231

all_players = players.get_active_players()
player_queue = all_players.copy()
valid_results = []
skipped = []

def calc_accuracy(df, condition):
    filtered = df[condition]
    if len(filtered) == 0:
        return None
    return round(filtered['SHOT_MADE_FLAG'].sum() / len(filtered), 3)

print(f"ショットデータを持つ選手を {MAX_VALID_PLAYERS} 人収集中...")

with tqdm(total=MAX_VALID_PLAYERS) as pbar:
    while len(valid_results) < MAX_VALID_PLAYERS and player_queue:
        player = player_queue.pop(0)
        name = player['full_name']
        player_id = player['id']

        try:
            # ポジション取得
            info = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_data_frames()[0]
            position = info.loc[0, 'POSITION'] if 'POSITION' in info.columns else None

            # ショットチャート取得
            chart = shotchartdetail.ShotChartDetail(
                team_id=0,
                player_id=player_id,
                season_type_all_star='Regular Season',
                season_nullable=SEASON,
                context_measure_simple='FGA'
            )
            df = chart.get_data_frames()[0]
            if df.empty:
                skipped.append(name + '（空）')
                continue

            total_shots = len(df)
            made_shots = df['SHOT_MADE_FLAG'].sum()

            acc = {
                'player_name': name,
                'position': position,
                'overall': round(made_shots / total_shots, 3),
                'total_shots': total_shots,
                'made_shots': made_shots,
                '3P': calc_accuracy(df, df['SHOT_TYPE'] == '3PT Field Goal'),
                '2P': calc_accuracy(df, df['SHOT_TYPE'] == '2PT Field Goal'),
                'restricted_area': calc_accuracy(df, df['SHOT_ZONE_BASIC'] == 'Restricted Area'),
                'in_paint': calc_accuracy(df, df['SHOT_ZONE_BASIC'] == 'In The Paint (Non-RA)'),
                'left_mid': calc_accuracy(df, (df['SHOT_ZONE_BASIC'] == 'Mid-Range') & (df['SHOT_ZONE_AREA'] == 'Left Side(L)')),
                'center_mid': calc_accuracy(df, (df['SHOT_ZONE_BASIC'] == 'Mid-Range') & (df['SHOT_ZONE_AREA'] == 'Center(C)')),
                'right_mid': calc_accuracy(df, (df['SHOT_ZONE_BASIC'] == 'Mid-Range') & (df['SHOT_ZONE_AREA'] == 'Right Side(R)')),
                'right_corner': calc_accuracy(df, df['SHOT_ZONE_BASIC'] == 'Right Corner 3'),
                'left_corner': calc_accuracy(df, df['SHOT_ZONE_BASIC'] == 'Left Corner 3'),
                'right_wing': calc_accuracy(df, (df['SHOT_ZONE_BASIC'] == 'Above the Break 3') & (df['LOC_X'] > 100)),
                'left_wing': calc_accuracy(df, (df['SHOT_ZONE_BASIC'] == 'Above the Break 3') & (df['LOC_X'] < -100)),
                'top_3': calc_accuracy(df, (df['SHOT_ZONE_BASIC'] == 'Above the Break 3') & (df['LOC_X'].between(-100, 100))),
                'deep_3': calc_accuracy(df, (df['SHOT_ZONE_BASIC'] == 'Above the Break 3') & (df['SHOT_ZONE_RANGE'] == '24+ ft.'))
            }

            valid_results.append(acc)
            pbar.update(1)
            time.sleep(0.6)

        except Exception as e:
            skipped.append(name + f'（エラー: {e}）')
            continue

# 保存
df_final = pd.DataFrame(valid_results)
df_final = df_final.fillna(0.0)
df_final.to_csv('nba_zone_accuracy_summary.csv', index=False, encoding='utf-8-sig')

print(f"\n完了！データ取得成功: {len(valid_results)}人")



