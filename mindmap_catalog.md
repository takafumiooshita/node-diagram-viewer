# 機能カタログ（Flow × Layer, v0.04）

| Layer | ID | Name | Description |
|---|---|---|---|
| Data | N1 | Input | 外部データ/ファイル取り込み |
| Data | N2 | Stage1 | 前処理・整形 |
| Data | N3 | Stage2 | 特徴抽出・集計 |
| Data | N4 | DB | 永続化（RDB/湖） |
| Data | N5 | BI | 可視化/レポート |
| Logic | L1 | Control | 制御・スケジューラ |
| Logic | L2 | Action | 処理キック/実行 |
| Logic | L3 | Notify | 通知/監視 |

## Flows

**Data**
- N1→N2  (Input ====▶ Stage1)
- N2→N3  (Stage1 ====▶ Stage2)
- N3→N4  (Stage2 ====▶ DB)
- N4→N5  (DB ====▶ BI)

**Control**
- L1→L2  (Control ----▶ Action)
- L2→L3  (Action ----▶ Notify)
