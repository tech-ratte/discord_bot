# Splaassist (SplatoonAssistant)

Splatoon 3 のプライベートマッチ向け Discord Bot。  
チーム分け、武器ランダム選択、対戦結果の記録と集計をサポートします。

## 主な機能
- `/game-start`  
  参加メンバーを選択し、チーム分けを作成。再シャッフルや再選択が可能。
- 対戦結果の記録  
  勝利チーム（アルファ/ブラボー/無効試合）を登録し、メンバーごとの成績を集計。
- `/weapon`  
  武器/メイン/サブ/スペシャルのいずれかをランダムに選択。

## セットアップ
1. Python 環境を用意（3.10 以上推奨）
2. 依存関係をインストール
   ```bash
   pip install discord.py requests python-dotenv
   ```
3. `.env` を作成してトークンを設定
   ```
   SPLATOON_ASSISTANT_TOKEN=YOUR_DISCORD_BOT_TOKEN
   ```

## 使い方
```bash
python SplatoonAssistant/main.py
```
Bot が起動したら Discord で以下のスラッシュコマンドを利用できます。
- `/game-start` チーム分け開始
- `/weapon` 武器ランダム選択

## 依存 API / 参照先
- 武器データ: stat.ink API（`https://stat.ink/api/v3/weapon`）
- 画像参照: GameWith の画像 URL を使用

## ディレクトリ構成（主要）
- `SplatoonAssistant/main.py` Bot エントリポイント
- `SplatoonAssistant/MemberSelectView.py` メンバー選択 UI
- `SplatoonAssistant/TeamControlView.py` チーム分け・集計 UI
- `SplatoonAssistant/ButtleView.py` 勝敗登録 UI
- `SplatoonAssistant/WeaponScopeSelectView.py` 武器種別選択 UI
- `SplatoonAssistant/WeaponRandomSelectView.py` 武器ランダム選択 UI