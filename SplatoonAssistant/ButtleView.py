import random
import discord
from discord.ui import View, Button


# 勝利判定を定義する View クラス
class ButtleView(View):


    def __init__(self, start_time, count, embed, record, alpha, beta, spec):
        super().__init__(timeout=900)

        self.start_time = start_time
        self.count = count
        self.record = record
        self.alpha = alpha
        self.beta = beta
        self.spec = spec

        embed.title = "⚔️ 試合中..."
        embed.color = discord.Color.purple()
        embed.set_footer(text=f"勝利チームはどちらですか？")
        self.init_view = embed


    # 「アルファチーム」ボタンの定義
    @discord.ui.button(label="アルファチーム", style=discord.ButtonStyle.primary, emoji="🟨")
    async def alpha_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        caution_view = CautionView(
            self.start_time, 
            self.count, 
            self.init_view, 
            self.record, 
            self.alpha, 
            self.beta, 
            self.spec, 
            "alpha"
        )
        await interaction.edit_original_response(
            embed=caution_view.init_embed,
            view=caution_view
        )

        
    # 「ブラボーチーム」ボタンの定義
    @discord.ui.button(label="ブラボーチーム", style=discord.ButtonStyle.primary, emoji="🟦")
    async def beta_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        caution_view = CautionView(
            self.start_time, 
            self.count, 
            self.init_view, 
            self.record, 
            self.alpha, 
            self.beta, 
            self.spec, 
            "beta", 
        )
        await interaction.edit_original_response(
            embed=caution_view.init_embed,
            view=caution_view
        )


    # 「無効試合」ボタンの定義
    @discord.ui.button(label="無効試合", style=discord.ButtonStyle.secondary, emoji="❌")
    async def invalid_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        caution_view = CautionView(
            self.start_time, 
            self.count, 
            self.init_view, 
            self.record, 
            self.alpha, 
            self.beta, 
            self.spec
        )
        await interaction.edit_original_response(
            embed=caution_view.init_embed,
            view=caution_view
        )

        
# 最終確認を定義する View クラス
class CautionView(View):


    def __init__(self, start_time, count, embed, record, alpha, beta ,spec, win_team=None):
        super().__init__(timeout=900)

        self.start_time = start_time
        self.count = count
        self.embed = embed
        self.record = record
        self.alpha = alpha
        self.beta = beta
        self.spec = spec
        self.win_team = win_team

        info = ""
        if win_team == "alpha":
            info = "🟨 アルファチーム"
        elif win_team == "beta":
            info = "🟦 ブラボーチーム"
        else:
            info = "❌ 無効試合"
        self.init_embed = discord.Embed(
            title="⚠️ 確認",
            description=f"{info} で間違いないですか？",
            color=discord.Color.red()
        )


    # 「いいえ」ボタンの定義
    @discord.ui.button(label="いいえ", style=discord.ButtonStyle.danger)
    async def cancel_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        # 「試合中」に戻る
        buttle_view = ButtleView(
            self.start_time, 
            self.count, 
            self.embed, 
            self.record, 
            self.alpha, 
            self.beta, 
            self.spec
        )
        await interaction.edit_original_response(
            embed=buttle_view.init_view,
            view=buttle_view
        )


    # 「はい」ボタンの定義
    @discord.ui.button(label="はい", style=discord.ButtonStyle.success)
    async def confirm_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        # レコードを更新して「チーム編成」へ
        from TeamControlView import TeamControlView
        # カウント増加
        if self.win_team is not None:
            self.count += 1
        # 勝利チーム判定
        win_members = []
        lose_members = []
        if self.win_team == "alpha":
            win_members = self.alpha
            lose_members = self.beta
        elif self.win_team == "beta":
            win_members = self.beta
            lose_members = self.alpha
        # レコード更新
        for r in self.record:
            if r.name in win_members:
                r.record_win()
            if r.name in lose_members:
                r.record_lose()
        members = self.alpha + self.beta + self.spec
        team_view = TeamControlView(self.start_time, self.count, self.record, members)
        await interaction.edit_original_response(
            embed=team_view.current_embed,
            view=team_view
        )