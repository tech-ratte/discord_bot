import random
import discord
from discord.ui import View, Button
from WeaponRandomSelectView import WeaponRandomSelectView


class WeaponScopeSelectView(View):

    def __init__(self, weapons):
        super().__init__(timeout=None)
        self.weapons = weapons
        self.current_embed = None
        self.type_select()

    def type_select(self):
        # Embedの作成
        embed = discord.Embed(
            title="🔀 ランダム選択",
            description="下のボタンからランダムに選択したいカテゴリを選んでください。",
            color=discord.Color.purple(),
        )
        embed.set_thumbnail(
            url="https://pbs.twimg.com/profile_images/938681212423454720/tgHfG8vm_400x400.jpg"
        )
        # embedセット
        self.current_embed = embed

    # 「ブキ」ボタンの定義
    @discord.ui.button(label="ブキ", style=discord.ButtonStyle.primary, emoji="⚔️")
    async def weapon_button(self, interaction: discord.Interaction, button: Button):
        next_view = WeaponRandomSelectView(weapons=self.weapons)
        await interaction.response.edit_message(
            embed=next_view.current_embed, view=next_view
        )

    # 「メイン」ボタンの定義
    @discord.ui.button(label="メイン", style=discord.ButtonStyle.secondary, emoji="🔫")
    async def main_button(self, interaction: discord.Interaction, button: Button):
        next_view = WeaponRandomSelectView(weapons=self.weapons, end="type")
        await interaction.response.edit_message(
            embed=next_view.current_embed, view=next_view
        )

    # 「サブ」ボタンの定義
    @discord.ui.button(label="サブ", style=discord.ButtonStyle.secondary, emoji="💣")
    async def sub_button(self, interaction: discord.Interaction, button: Button):
        next_view = WeaponRandomSelectView(weapons=self.weapons, end="sub")
        await interaction.response.edit_message(
            embed=next_view.current_embed, view=next_view
        )

    # 「スペシャル」ボタンの定義
    @discord.ui.button(
        label="スペシャル", style=discord.ButtonStyle.secondary, emoji="🚀"
    )
    async def special_button(self, interaction: discord.Interaction, button: Button):
        next_view = WeaponRandomSelectView(weapons=self.weapons, end="special")
        await interaction.response.edit_message(
            embed=next_view.current_embed, view=next_view
        )
