import random
import datetime
import discord
from discord.ui import View, Button


# チーム振り分けを定義する View クラス
class TeamControlView(View):


    def __init__(self, start_time, count, record, members):
        super().__init__(timeout=900)

        self.start_time = start_time
        self.count = count
        self.record = record
        self.members = members

        # レコードに無いメンバーを追加
        for selected_name in members:
            if not any(r.name == selected_name for r in self.record):
                self.record.append(MemberRecord(selected_name))

        for r in self.record:
            print(r)
        self.current_embed = None
        self.update_teams()


    def update_teams(self):

        members_to_split = self.members[:]
        # ランダムにシャッフル
        random.shuffle(members_to_split)
        # チーム分け
        self.spectator = []
        if len(members_to_split) > 8:
            self.spectator = members_to_split[8:]
            members_to_split = members_to_split[:8]
        team_size = len(members_to_split) // 2
        self.team_alpha = members_to_split[team_size:]
        self.team_beta = members_to_split[:team_size]
        # メンションを作成して送信
        mentions_alpha = "\n".join(member.mention for member in self.team_alpha)
        mentions_beta = "\n".join(member.mention for member in self.team_beta)
        mentions_spectator = "\n".join(member.name.mention for member in self.spectator)
        # Embedの作成
        embed = discord.Embed(
            title="🔶 チーム編成",
            description=f"{self.count}試合目",
            color=discord.Color.dark_orange()
        )
        embed.add_field(name="🟨 アルファチーム", value=mentions_alpha, inline=False)
        embed.add_field(name="🟦 ブラボーチーム", value=mentions_beta, inline=False)
        embed.add_field(name="👀 観戦者", value=mentions_spectator, inline=False)
        now_time = datetime.datetime.now().strftime("%H:%M")
        embed.set_footer(text=f"最終更新: {now_time}")
        # embedセット
        self.current_embed = embed


    # 「再シャッフル」ボタンの定義
    @discord.ui.button(label="再シャッフル", style=discord.ButtonStyle.secondary, emoji="🔁")
    async def reshuffle_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer() # 処理中であることを表示
        self.update_teams() # チーム分けを更新
        # メッセージの編集 
        await interaction.edit_original_response(
            embed=self.current_embed
        )

        
    # 「メンバー再選択」ボタンの定義
    @discord.ui.button(label="メンバー再選択", style=discord.ButtonStyle.secondary, emoji="👥")
    async def reselection_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        from MemberSelectView import MemberSelectView
        member_view = MemberSelectView(self.start_time, self.count, self.record)
        await interaction.edit_original_response(
            embed=member_view.init_embed,
            view=member_view
        )


    # 「試合開始」ボタンの定義
    @discord.ui.button(label="試合開始", style=discord.ButtonStyle.primary, emoji="⚔️")
    async def buttle_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        from ButtleView import ButtleView
        buttle_view = ButtleView(
            self.start_time, 
            self.count, 
            self.current_embed, 
            self.record, 
            self.team_alpha, 
            self.team_beta, 
            self.spectator
        )
        await interaction.edit_original_response(
            embed=buttle_view.init_view,
            view=buttle_view
        )


    # # 「確定」ボタンの定義
    # @discord.ui.button(label="確定", style=discord.ButtonStyle.success, emoji="✅")
    # async def confirm_button(self, interaction: discord.Interaction, button: Button):
    #     await interaction.response.defer()  # 処理中であることを表示
    #     self.current_embed.title = "✅ チーム編成完了！"
    #     self.current_embed.color = discord.Color.green()
    #     self.current_embed.set_footer(text=f"チーム編成が確定しました。確定者: {interaction.user.display_name}")

    #     # View全体を無効化
    #     self.stop()
    #     for child in self.children:
    #         child.disabled = True

    #     # メッセージを更新し、ボタンを無効化
    #     await interaction.edit_original_response(
    #         embed=self.current_embed,
    #         view=self
    #     )


# メンバーの戦績を定義するクラス
class MemberRecord:
    def __init__(self, name):
        self.name = name
        self.win = 0
        self.num = 0

    def record_win(self):
        self.win += 1
        self.num += 1

    def record_lose(self):
        self.num += 1

    def __str__(self):
        rate = 0.0
        if self.win != 0:
            rate = self.win/self.num * 100
        return f"{self.name}: {self.win}勝/{self.num}試合 (勝率: {rate:.2f}%)"