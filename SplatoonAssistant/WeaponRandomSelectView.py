import random
import discord
from discord.ui import View, Button


class WeaponRandomSelectView(View):

    def __init__(self, weapons, end=None):
        super().__init__(timeout=None)
        self.weapons = weapons
        self.end = end

        # カテゴリーキー
        self.category = ""
        if end is None:
            self.category = "weapon"
        elif end == "type":
            self.category = "main"
        else:
            self.category = end
        # カテゴリーごとの表示形式設定
        self.category_dict = {
            "weapon": {"name": "ブキ", "emoji": "⚔️"},
            "main": {"name": "メイン", "emoji": "🔫"},
            "sub": {"name": "サブ", "emoji": "💣"},
            "special": {"name": "スペシャル", "emoji": "🚀"},
        }
        self.name = self.category_dict[self.category]["name"]
        self.emoji = self.category_dict[self.category]["emoji"]

        # 画像パス生成用の辞書
        self.gamewith_image_dict = {
            "main": {
                "alias": "type",
                "shooter": 1,
                "charger": 2,
                "blaster": 3,
                "roller": 4,
                "brush": 5,
                "slosher": 6,
                "spinner": 7,
                "maneuver": 8,
                "brella": 9,
                "wiper": 10,
                "stringer": 11,
            },
            "sub": {
                "alias": "sub",
                "splashshield": 1,
                "curlingbomb": 2,
                "quickbomb": 3,
                "poisonmist": 4,
                "pointsensor": 5,
                "jumpbeacon": 6,
                "splashbomb": 7,
                "trap": 8,
                "robotbomb": 9,
                "sprinkler": 10,
                "tansanbomb": 11,
                "torpedo": 12,
                "kyubanbomb": 13,
                "linemarker": 14,
            },
            "special": {
                "alias": "sp",
                "missile": 1,
                "amefurashi": 2,
                "kanitank": 3,
                "nicedama": 4,
                "jetpack": 5,
                "megaphone51": 6,
                "greatbarrier": 7,
                "ultrahanko": 8,
                "kyuinki": 9,
                "energystand": 10,
                "hopsona": 11,
                "sameride": 12,
                "shokuwander": 13,
                "tripletornado": 14,
                "ultrashot": 15,
                "teioika": 16,
                "decoy": 17,
                "suminagasheet": 18,
                "ultra_chakuchi": 19,
            },
        }

        self.current_embed = None
        self.random_selection()

    # ブキに関する一覧を取得する関数
    def get_all(self):
        get_dict = {}
        for w in self.weapons:
            t = w.get(self.end) if self.end is not None else w
            key = t.get("key")
            name = t.get("name").get("ja_JP")
            if key and name:
                get_dict[key] = name
        if self.category == "main":
            get_dict.pop("reelgun")
        # print(get_dict)
        return get_dict

    # ブキ関連の画像URLを取得する関数
    def set_image_url(self, selected_key):
        image_url = ""
        if self.category == "weapon":
            return ""
        category = self.gamewith_image_dict.get(self.category).get("alias")
        num = self.gamewith_image_dict.get(self.category).get(selected_key)
        if self.category == "main":
            image_url = f"https://img.gamewith.jp/article_tools/splatoon3/gacha/{category}{num:02}.png"
        else:
            image_url = f"https://img.gamewith.jp/article_tools/splatoon3/gacha/{category}{num}.png"
        return image_url

    def random_selection(self):
        # ランダムに選択
        select_list = list(self.get_all().items())
        selected = random.choice(select_list)
        self.selected_key = selected[0]
        self.selected_value = selected[1]
        image_url = self.set_image_url(self.selected_key)

        # Embedの作成
        embed = discord.Embed(
            title=f"{self.emoji} ランダム {self.name}選択 (確認中)",
            color=discord.Color.orange(),
        )
        embed.add_field(
            name=f"選択された{self.name}", value=self.selected_value, inline=True
        )
        embed.set_thumbnail(url=image_url)
        # embedセット
        self.current_embed = embed

    # 「再選択」ボタンの定義
    @discord.ui.button(label="再選択", style=discord.ButtonStyle.secondary, emoji="🔁")
    async def reselect_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()  # 処理中であることを表示
        self.random_selection()
        # メッセージの編集
        await interaction.edit_original_response(embed=self.current_embed)

    # 「確定」ボタンの定義
    @discord.ui.button(label="確定", style=discord.ButtonStyle.success, emoji="✅")
    async def confirm_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()  # 処理中であることを表示
        self.current_embed.title = "✅ 決定！"
        self.current_embed.color = discord.Color.green()
        self.current_embed.set_footer(
            text=f"選択が確定しました。確定者: {interaction.user.display_name}"
        )

        # View全体を無効化
        self.stop()
        for child in self.children:
            child.disabled = True

        # メッセージを更新し、ボタンを無効化
        await interaction.edit_original_response(embed=self.current_embed, view=self)
