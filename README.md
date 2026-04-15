# NBA Recommendation System

## 概要
NBA選手のスタッツデータを用いて、類似選手を推薦するシステムです。

## 背景
データに基づいて似たプレースタイルの選手を発見するために開発しました。

## 技術スタック
- Python
- pandas
- numpy
- scikit-learn
- Streamlit

## 実行方法
pip install -r requirements.txt
streamlit run app.py

## 工夫した点
- スケーリングによる特徴量の正規化
- 類似度計算の比較（複数手法）

## 今後の課題
- 評価指標の導入
- 精度改善
