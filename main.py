import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="=", intents=intents)

# IDs
CATEGORY_ID = 1366046385559965858
TARGET_CHANNEL_ID_NOTIFICATION = 1367085229692424285
TARGET_CHANNEL_ID_DONE = 1366077173223391303
TARGET_CHANNEL_ID_TICKET = 1366077579089412147
REQUIRED_ROLE_ID = 1367089926050680882

# Colors
DARK_GRAY = discord.Color.from_str("#2C2F33")
BLUE = discord.Color.from_str("#3A3476")

# ----- Lose Modal -----
class BreathingModal(discord.ui.Modal, title="（ノ・.・）"):
    server_ad = discord.ui.TextInput(
        label="ㅤ৴ㅤㅤ❀ㅤㅤserverㅤad",
        placeholder="ㅤ.ㅤno spoiler walls",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=4000,
    )
    invite_link = discord.ui.TextInput(
        label="ㅤ৴ㅤㅤ❀ㅤㅤinviteㅤlink",
        placeholder="ㅤ.ㅤvanities = batch",
        style=discord.TextStyle.short,
        required=True,
        max_length=200,
    )
    type_info = discord.ui.TextInput(
        label="ㅤ৴ㅤㅤ❀ㅤㅤpaidㅤtype",
        placeholder="ㅤ.ㅤpoint or invite?",
        style=discord.TextStyle.short,
        required=True,
        max_length=100,
    )

    def __init__(self, original_message):
        super().__init__()
        self.original_message = original_message

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        thread = await self.original_message.create_thread(name="◞  ◟)✿︎")
        embed = discord.Embed(description=f"```{self.server_ad.value}```", color=DARK_GRAY)
        await thread.send(content=self.server_ad.value, embed=embed)
        await thread.send(self.invite_link.value)
        await thread.send(f"# <:reply:1367350602270511266> {self.type_info.value}")
        await interaction.followup.send(
            "_ _\n\n\n                  **wait   for   approval** <a:blue_swirl:1367097762989998131>\n                   *do  not  ping  anyone.*\n\n\n_ _",
        )

class ClickButton(discord.ui.View):
    def __init__(self, original_message):
        super().__init__(timeout=None)
        self.original_message = original_message

    @discord.ui.button(label="ㅤclickㅤ⠀⸺ㅤ⠀𝜗♥︎⠀♪ㅤ", style=discord.ButtonStyle.secondary)
    async def click_me_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(LoseModal(self.original_message))

# ----- Notification Modal -----
class NotificationModal(discord.ui.Modal, title="（・＿＼）"):
    notification = discord.ui.TextInput(
        label="ㅤ৴ㅤㅤ❀ㅤㅤnotification",
        placeholder="ㅤ.ㅤping / dm",
        required=True,
        style=discord.TextStyle.short
    )
    urgency = discord.ui.TextInput(
        label="ㅤ৴ㅤㅤ❀ㅤㅤurgency",
        placeholder="ㅤ.ㅤno need to lie",
        required=True,
        style=discord.TextStyle.short
    )
    sep_time = discord.ui.TextInput(
        label="ㅤ৴ㅤㅤ❀ㅤㅤsepㅤtime",
        placeholder="ㅤ.ㅤbatch / 1h / 2h / ovn || ovn = urg paids only",
        required=True,
        style=discord.TextStyle.short
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        user = interaction.user
        current_channel = interaction.channel
        target_channel = interaction.guild.get_channel(TARGET_CHANNEL_ID_NOTIFICATION)
        if target_channel:
            await target_channel.send(
                f"_ _\nㅤㅤㅤㅤㅤ~~      ~~⠀⠀{user.mention}⠀⠀{current_channel.mention}⠀⠀✿\nㅤㅤㅤ**{self.sep_time.value}**⠀⠀.⠀⠀<a:01_heart:1367097767092031500>⠀⠀[⠀{self.urgency.value}⠀]⠀⠀**{self.notification.value}**\n_ _"
            )
        try:
            await current_channel.edit(name=f"{user.name}﹕{self.sep_time.value}﹕{self.notification.value}")
        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to edit the channel name.", ephemeral=True)
            return

        await interaction.followup.send(
            "_ \n\n _ ⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀[*queued*](https://discord.com/channels/1314982962919379044/1318526765710184488)⠀♡\n"
            "_ _  ⠀  ⠀ ⠀⠀⠀⠀ ⠀⠀⠀⠀ *check  pings  &  dms.*\n\n_ _",
            ephemeral=False
        )

class ClickMeView(discord.ui.View):
    @discord.ui.button(label="ㅤi don't know if i could . . .ㅤ", style=discord.ButtonStyle.secondary)
    async def click_me(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NotificationModal())

# ----- Ticket Close Button -----
class RegretButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="ㅤ(っ- ‸ – ς)ㅤ",
        style=discord.ButtonStyle.danger
    )
    async def regret_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "_ _\n\n    <a:4purplebabystar:1367097764974039041>  result  has  been  **sent**  ♡\n     ₊   click button to close ticket\n\n_ _",
            view=CloseTicketView()  # 👈 close button included here
        )
        
# ----- Slash Commands -----
@bot.tree.command(name="breathing", description="ticket　⊹　　　₊　　　⁺")
async def lose(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild
    user = interaction.user
    category = discord.utils.get(guild.categories, id=CATEGORY_ID)
    if not category:
        await interaction.followup.send("Category not found.")
        return

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True)
    }

    channel = await guild.create_text_channel(name=f"w﹕{user.name}", category=category, overwrites=overwrites)

    embed = discord.Embed(
        description="<:00:1367082106341167216>\n<:00:1367082106341167216><:00:1367082106341167216><:00:1367082106341167216><:00:1367082106341167216><:00:1367082106341167216><:00:1367082106341167216><a:05_blue_moon:1367097760729403495>‎‎‎‎‎‎‎⡴<:00:1367082106341167216>just tell me how<:00:1367082106341167216>⟡ ₊\n<:00:1367082106341167216><:00:1367082106341167216><:00:1367082106341167216><:00:1367082106341167216><:00:1367082106341167216><:00:1367082106341167216>♪  ♪<:00:1367082106341167216>to keep breathing<:00:1367082106341167216>✿\n<:00:1367082106341167216>",
        color=DARK_GRAY
    )
    embed.set_image(url="https://media.discordapp.net/attachments/1366347959343517716/1367337344516231275/Untitled202_20250501110957.png?ex=681437a2&is=6812e622&hm=a00989c4be6ad411e206e4530a058a8622b4e143d010e28dc712303b528bbd17&=&format=webp&quality=lossless&width=1056&height=624")

    view = ClickButton(None)
    message = await channel.send(embed=embed, view=view)
    view.original_message = message

    await interaction.followup.send(
        f"_ \n\n\n _　　　　<:blue_flower:1367358723269595249>          ⁺     ⊹\n_ _　　　　{channel.mention}\n\n\n_ _"
    )

@bot.tree.command(name="dreams", description="finished　⊹　　　₊　　　⁺")
async def nobody(interaction: discord.Interaction):
    embed = discord.Embed()
    embed.set_image(url="https://media.discordapp.net/attachments/1366347959343517716/1367343024371404910/Untitled202_20250501113237.png?ex=68143ced&is=6812eb6d&hm=e3914c498a94052859630fc9b1868aa75cbadfacb786b70d60009716122f176a&=&format=webp&quality=lossless&width=1056&height=624")
    await interaction.response.send_message(
        content="_ _\n　　　✧ ‿︵ 　~~　　~~ 　while pretending i'm not drowning\n_ _",
        embed=embed,
        view=ClickMeView()
    )

@bot.tree.command(name="done", description="miel only")
@app_commands.describe(sep="sep time", user="who", link="invite link", edit="ticket channel")
@app_commands.checks.has_role(REQUIRED_ROLE_ID)
async def done(interaction: discord.Interaction, sep: str, user: discord.User, link: str, edit: discord.TextChannel = None):
    await interaction.response.defer(ephemeral=True)
    target_channel = interaction.guild.get_channel(TARGET_CHANNEL_ID_DONE)
    if not target_channel:
        await interaction.followup.send("Target channel not found.")
        return

    await target_channel.send(f"_ _\n\n                          ₊ ⊹      *{sep}* <a:004_blue_ghost:1367359639628414978> {user.mention}\n\n_ _ [⠀]( {link} )")
    await target_channel.send("_ _\n\n\n-# _ _  <a:pixwing:1367097770506326046>  (｡˘﹏˘｡)っ  **wait  awhile  to  count  invites**         ***!***\n\n\n_ _")

    if edit:
        try:
            await edit.edit(name="w4s")
        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to rename that channel.")
            return

    await interaction.followup.send("Done!")

@bot.tree.command(name="dm", description="miel only")
@app_commands.describe(user="who's going to be DMed")
@app_commands.checks.has_role(REQUIRED_ROLE_ID)
async def dm(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer(ephemeral=True)
    try:
        await user.send(
            f"_ \n\n\n\n\n _        sep  over.   ﹙   <:emoji_35:1367097773014384702>   ﹚   {user.mention}   ✿\n-# _ _         check invites    .    ◟⠀run **/door** in ticket\n\n\n\n\n_ _"
        )
        await interaction.followup.send("User has been DMed.")
    except discord.Forbidden:
        await interaction.followup.send("I couldn't DM that user. They might have DMs off.")

# ----- Regret Command and Close Ticket View -----
class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="", style=discord.ButtonStyle.danger, emoji="<a:bluespinningheart:1367355716569923644>", custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()  # Acknowledge the click immediately
        await interaction.channel.delete()

@bot.tree.command(
    name="door",
    description="results　⊹　　　₊　　　⁺"
)
@app_commands.describe(
    invites=". invites gained",
    portals=". other portals that posted",
    type=". server type you massed",
    link=". server invite link"
)
async def regret(
    interaction: discord.Interaction,
    invites: int,
    portals: str,
    type: str,
    link: str
):
    await interaction.response.defer(ephemeral=True)  # just defers, not the message that follows

    user = interaction.user
    guild = interaction.guild

    review_channel = guild.get_channel(TARGET_CHANNEL_ID_TICKET)
    if review_channel is None:
        await interaction.followup.send("Review channel not found.")
        return

    content = f"_ _\n                                **__{invites}__    invites**    ◟︵ ｡\n[⠀]({link})"

    embed = discord.Embed(description=f"(+{portals}p)‎ ‎‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎‎‎‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎‎ ‎‎ ‎ ‎ ‎ ‎ཀ‎ ‎‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎‎‎‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎‎ ‎‎ ‎ ‎ ‎ {type}")
    embed.set_image(url="https://media.discordapp.net/attachments/1366347959343517716/1367347180444057671/Untitled201_20250501114858.png?ex=681440cb&is=6812ef4b&hm=1a090164d5ceed30a01d86c21f8449462bdb88b7eebcd630fffb2353321ab9df&=&format=webp&quality=lossless")
    embed.set_footer(
        text=f"{user.name}‎ㅤㅤㅤ‎⟢ㅤㅤㅤthankq for massing",
        icon_url=user.avatar.url if user.avatar else discord.Embed.Empty
    )

    await review_channel.send(content=content, embed=embed)

    await interaction.followup.send(
        "_ _\n\n    <a:4purplebabystar:1367097764974039041>  result  has  been  **sent**  ♡\n     ₊   click button to close ticket\n\n_ _",
        view=CloseTicketView()
    )

# ----- Events -----
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(e)
    activity = discord.Streaming(
        name="freya ridings 𝜗℘",
        url="https://www.twitch.tv/sexcmiel"
    )
    await bot.change_presence(status=discord.Status.idle, activity=activity)

bot.run(TOKEN)
