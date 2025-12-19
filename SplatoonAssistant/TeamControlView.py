import random
import datetime
import discord
from discord.ui import View, Button


# チーム振り分けを定義する View クラス
class TeamControlView(View):

    def __init__(self, weapons, start_time, count, record, members):
        super().__init__(timeout=None)

        self.weapons = weapons
        self.start_time = start_time
        self.count = count
        self.record = record
        self.members = members

        # レコードに無いメンバーを追加
        for selected_name in members:
            if not any(r.name == selected_name for r in self.record):
                self.record.append(MemberRecord(selected_name))
        self.current_embed = None
        self.update_teams()

    def update_teams(self):

        members_to_split = self.members[:]
        # 人数ハンデ
        handicap = len(members_to_split) % 2 != 0
        handicap_text = "（人数ハンデあり）" if handicap else ""
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
        # 人数ハンデありの場合
        mentions_alpha_list = []
        if handicap:
            # ランダムに武器選択
            from WeaponRandomSelectView import WeaponRandomSelectView

            for member in self.team_alpha:
                weapon_view = WeaponRandomSelectView(weapons=self.weapons)
                weapon = ""
                for field in weapon_view.current_embed.fields:
                    weapon = field.value
                mentions_alpha_list.append(member.mention + f"\n（ブキ候補：{weapon}）")
        else:
            for member in self.team_alpha:
                mentions_alpha_list.append(member.mention)
        # メンションを作成して送信
        mentions_alpha = "\n".join(mentions_alpha_list)
        mentions_beta = "\n".join(member.mention for member in self.team_beta)
        mentions_spectator = "\n".join(member.name.mention for member in self.spectator)
        # Embedの作成
        embed = discord.Embed(
            title=f"🔶 チーム編成{handicap_text}",
            description=f"{self.count}試合目",
            color=discord.Color.orange(),
        )
        embed.add_field(name="🟨 アルファチーム", value=mentions_alpha, inline=False)
        embed.add_field(name="🟦 ブラボーチーム", value=mentions_beta, inline=False)
        embed.add_field(name="👀 観戦者", value=mentions_spectator, inline=False)
        now_time = datetime.datetime.now().strftime("%H:%M")
        embed.set_footer(text=f"最終更新: {now_time}")
        # embedセット
        self.current_embed = embed

    # 「再シャッフル」ボタンの定義
    @discord.ui.button(
        label="再シャッフル", style=discord.ButtonStyle.secondary, emoji="🔁"
    )
    async def reshuffle_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()  # 処理中であることを表示
        self.update_teams()  # チーム分けを更新
        # メッセージの編集
        await interaction.edit_original_response(embed=self.current_embed)

    # 「メンバー再選択」ボタンの定義
    @discord.ui.button(
        label="メンバー再選択", style=discord.ButtonStyle.secondary, emoji="👥"
    )
    async def reselection_button(
        self, interaction: discord.Interaction, button: Button
    ):
        await interaction.response.defer()
        from MemberSelectView import MemberSelectView

        member_view = MemberSelectView(
            self.weapons, self.start_time, self.count, self.record
        )
        await interaction.edit_original_response(
            embed=member_view.init_embed, view=member_view
        )

    # 「試合開始」ボタンの定義
    @discord.ui.button(label="試合開始", style=discord.ButtonStyle.primary, emoji="⚔️")
    async def buttle_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        from ButtleView import ButtleView

        buttle_view = ButtleView(
            self.weapons,
            self.start_time,
            self.count,
            self.current_embed,
            self.record,
            self.team_alpha,
            self.team_beta,
            self.spectator,
        )
        await interaction.edit_original_response(
            embed=buttle_view.init_view, view=buttle_view
        )

    # 「終了」ボタンの定義
    @discord.ui.button(label="終了", style=discord.ButtonStyle.danger, emoji="🔚")
    async def confirm_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        # 試合数が多い順、勝利数が多い順
        sorted_record = sorted(self.record, key=lambda r: (-r.total_num(), -r.total_win()))
        self.current_embed.title = f"🏆 {self.start_time.split()[0]}の戦績"
        self.current_embed.description = f"計{self.count-1}試合"
        self.current_embed.color = discord.Color.green()
        self.current_embed.set_footer(
            text=f"{self.start_time} - {datetime.datetime.now().strftime('%H:%M')}"
        )

        self.current_embed.clear_fields()
        for sorted_r in sorted_record:
            # 各モード別の集計と勝率を表示
            adv_win = sorted_r.win_adv
            adv_num = sorted_r.num_adv
            dis_win = sorted_r.win_dis
            dis_num = sorted_r.num_dis
            even_win = sorted_r.win_even
            even_num = sorted_r.num_even

            def rate_str(w, n):
                return f"{(w / n * 100):.2f}%" if n > 0 else "0.00%"

            total_win = sorted_r.total_win()
            total_num = sorted_r.total_num()
            total_rate = sorted_r.total_rate()

            value = (
                f"人数有利：{adv_win}勝/{adv_num}試合 (勝率: {rate_str(adv_win, adv_num)})\n"
                f"人数不利：{dis_win}勝/{dis_num}試合 (勝率: {rate_str(dis_win, dis_num)})\n"
                f"同人数　：{even_win}勝/{even_num}試合 (勝率: {rate_str(even_win, even_num)})\n"
                f"合計　　：{total_win}勝/{total_num}試合 (勝率: {total_rate:.2f}%)"
            )

            self.current_embed.add_field(
                name=sorted_r.name.mention,
                value=value,
                inline=False,
            )

        # View全体を無効化
        self.stop()
        for child in self.children:
            child.disabled = True

        # メッセージを更新し、ボタンを無効化
        await interaction.edit_original_response(embed=self.current_embed, view=self)


# メンバーの戦績を定義するクラス
class MemberRecord:
    def __init__(self, name):
        self.name = name
        # 人数有利時の成績
        self.win_adv = 0
        self.num_adv = 0
        # 人数不利時の成績
        self.win_dis = 0
        self.num_dis = 0
        # ハンデ無し時の成績
        self.win_even = 0
        self.num_even = 0

    def record_win(self, mode):
        """
        mode: 'adv'（人数有利）, 'dis'（人数不利）, その他はハンデ無し
        """
        if mode == "adv":
            self.win_adv += 1
            self.num_adv += 1
        elif mode == "dis":
            self.win_dis += 1
            self.num_dis += 1
        else:
            self.win_even += 1
            self.num_even += 1

    def record_lose(self, mode):
        if mode == "adv":
            self.num_adv += 1
        elif mode == "dis":
            self.num_dis += 1
        else:
            self.num_even += 1

    def total_win(self):
        return self.win_adv + self.win_dis + self.win_even

    def total_num(self):
        return self.num_adv + self.num_dis + self.num_even

    def total_rate(self):
        tn = self.total_num()
        return (self.total_win() / tn * 100) if tn > 0 else 0.0

    def __str__(self):
        return (
            f"{self.name}: {self.total_win()}勝/{self.total_num()}試合 (勝率: {self.total_rate():.2f}%)"
        )
