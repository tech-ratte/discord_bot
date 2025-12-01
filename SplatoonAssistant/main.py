import os
import requests
from datetime import datetime

from dotenv import load_dotenv
import discord
from discord.ext import commands

from MemberSelectView import MemberSelectView
from WeaponScopeSelectView import WeaponScopeSelectView

# トークンの読み込み
load_dotenv()
token = os.getenv("SPLATOON_ASSISTANT_TOKEN")

# Botオブジェクト
intents = discord.Intents.default()
intents.members = True          # ユーザー選択に必要
bot = commands.Bot(command_prefix='!', intents=intents) 

# ブキデータを保存するためのグローバル変数
weapon_data = {}

# Stat.ink APIからブキデータを取得する関数
def get_weapon_data():
    url = "https://stat.ink/api/v3/weapon"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

@bot.event
async def on_ready():
    print(f'{bot.user} がログインしました！')

    # ブキデータの取得
    global weapon_data
    weapon_data = get_weapon_data()

    # Botが参加しているサーバー全てにコマンドを登録
    try:
        synced = await bot.tree.sync()
        print(f"✅ スラッシュコマンドを {len(synced)} 件同期しました。")
    except Exception as e:
        print(f"スラッシュコマンドの同期中にエラーが発生しました: {e}")


@bot.tree.command(name='team', description="ランダムにチーム分けを行います")
async def random_assign_command(interaction: discord.Interaction):
    start_time = datetime.now().strftime("%Y/%m/%d %H:%M")
    member_view = MemberSelectView(start_time=start_time)
    await interaction.response.send_message(
        embed=member_view.init_embed,
        view=member_view
    )


@bot.tree.command(name='weapon', description="ブキをランダムに選択します")
async def random_weapon_command(interaction: discord.Interaction):
    global weapon_data
    # ランダム選択 & 成形
    weapon_view = WeaponScopeSelectView(weapon_data)
    # Viewと、Viewが生成したEmbedをメッセージに付与して送信
    await interaction.response.send_message(
        embed=weapon_view.current_embed,
        view=weapon_view
    )


# Botの起動
bot.run(token)