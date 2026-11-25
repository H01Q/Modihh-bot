
import os, random, asyncio, discord
from discord.ext import commands
from discord import app_commands

# ===== CONFIG =====
# Render me Environment Variable me TOKEN daalna, file me mat likhna
TOKEN = os.getenv("TOKEN")
# Gemini optional hai, nahi hogi to bhi bot chalega
GEMINI_KEY = os.getenv("API_KEY")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# ===== DATA LISTS =====
ROASTS = [
    "tera face dekh ke WiFi bhi disconnect ho jata hai 😭",
    "tu itna slow hai, Google bhi tujhe search karne se mana kar deta hai",
    "bhai tu background noise hai, main character mat ban",
    "tera dimaag airplane mode pe hai, kabhi on hi nahi hota",
    "tu wo notification hai jise sab ignore karte hai",
    "tere jokes pe hasna bhi ek punishment hai",
    "tu charging pe laga phone hai, 1% se aage badhta hi nahi",
    "bhai tu buffering me atka hua YouTube hai",
    "teri shakal dekh ke mirror bhi bolta hai - bhai rehne de",
    "tu exam me wo extra question hai jo koi attempt nahi karta",
]

SHAYARI = [
    "Mitron, dil se dil tak baat pahunch gayi, teri yaad ne fir neend uda di 🥀",
    "Chai thandi ho gayi, par teri yaadein abhi bhi garam hai ☕",
    "Aise Hi baithe the, achanak teri yaad aa gayi, aur mood romantic ho gaya 💌",
    "Raat lambi hai, baatein adhuri hai, aur tu online nahi hai 😔",
    "Dil garden garden ho gaya jab tera naam screen pe aaya 🌸",
]

JOKES = [
    "Pappu: Mummy, teacher ne bola mera dimaag khali hai. Mummy: Beta, khali plot ki keemat zyada hoti hai!",
    "Boy: Tumhari smile bohot cute hai. Girl: Thanks. Boy: Par tumhari DP wali smile aur zyada cute hai, kyunki wo meri wali nahi hai 😂",
    "Teacher: Kal homework kyu nahi kiya? Student: Sir, WiFi ne dhoka de diya, jaise usne diya tha.",
    "Mitron, exam me fail hona bhi ek kala hai, jo sabko nahi aati!",
]

TRUTH = [
    "Tera sabse bada crush kaun hai is server me? 👀",
    "Kabhi kisi ka message padh ke ignore kiya hai? Kiska?",
    "Sabse embarrassing moment kya tha school me?",
    "Kisi ko stalk kiya hai kabhi? Sach bol!",
    "Last baar kab roye the aur kyu?",
    "Kis cheez se sabse zyada dar lagta hai?",
]

DARE = [
    "Apni crush ko 'hi' bhej ke screenshot bhej 😈",
    "Agli 10 min tak sirf Modi style me baat kar - Mitron se shuru kar",
    "Apna last Google search yaha bhej",
    "Kisi random member ko 'I love you' bol ke aaja",
    "Apni gallery ki 3rd photo yaha bhej",
    "Apne crush ka naam loud me bol ke voice me aaja",
]

BHASHAN = [
    "Mitron! Aaj se har din, har raat, sirf Vikas hoga! Desh badal raha hai, aur tum bhi badal rahe ho! 💪",
    "Mitron, mai aapko batana chahta hu, ye jo pyaar hai na, yehi meri sabse badi taqat hai! 🇮🇳",
    "Bhaiyon aur Behno, aaj mai Mann Ki Baat karne aaya hu. Tum sab mere parivaar ho!",
    "Mitron! Chai pe charcha hogi, aur saath me duniya badlegi! ☕",
    "Desh ke yuvaon, tumhare andar jo Josh hai, wo hi naya Bharat banayega!",
    "Mitron, Digital India ka matlab hai - ab dil bhi online dhadkega! ❤️",
]

FACTS = [
    "India me har saal 1.5 lakh se zyada shadiyaan WhatsApp pe fix hoti hai (approx)!",
    "Ek din me insaan average 60,000 baar sochta hai!",
    "Discord pe pehla message 2015 me bheja gaya tha!",
    "Chai duniya ka dusra sabse zyada piya jaane wala drink hai, paani ke baad!",
    "Tumhare phone me tumhare toilet seat se zyada bacteria hote hai 😭",
]

# Warn system - simple memory me
warns = {}

# ===== EVENTS =====
@bot.event
async def on_ready():
    print(f"{bot.user} is online ✅")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} slash commands synced")
    except Exception as e:
        print("Sync error:", e)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    # Modi mention pe reply
    if bot.user in message.mentions:
        await message.channel.send(f"Mitron! {message.author.mention} ne mujhe yaad kiya! Bolo, kya seva karu? `/help` likh ke saare commands dekh lo! 🇮🇳")
    await bot.process_commands(message)

# ===== HELP =====
@bot.tree.command(name="help", description="Saare commands ki list dekho")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(title="🇮🇳 Narendar Modih - Full Command List", description="Mitron! Ye raha pura darbar!", color=0xff7b00)
    embed.add_field(name="🎉 FUN", value="`/roast` `/shayari` `/joke` `/meme` `/8ball` `/dice` `/coinflip` `/truth` `/dare` `/ship` `/love` `/slap` `/hug` `/kiss` `/pat` `/rps` `/fact` `/pp` `/gay`", inline=False)
    embed.add_field(name="🇮🇳 MODI SPECIAL", value="`/modi` `/bhashan` `/mannkibaat` `/mitron` `/vikas` `/acchedin` `/chai`", inline=False)
    embed.add_field(name="🛡️ ADMIN", value="`/kick` `/ban` `/unban` `/mute` `/unmute` `/clear` `/warn` `/warnings` `/slowmode` `/lock` `/unlock` `/nick` `/addrole` `/removerole` `/lockdown`", inline=False)
    embed.add_field(name="ℹ️ UTILITY", value="`/ping` `/avatar` `/userinfo` `/serverinfo` `/say` `/poll` `/announce`", inline=False)
    embed.add_field(name="Prefix bhi chalta hai", value="`!ping` `!roast @user` `!bhashan` jaise", inline=False)
    await interaction.response.send_message(embed=embed)

# ===== FUN SLASH =====
@bot.tree.command(name="roast", description="Kisi ko roast karo Modi style me")
@app_commands.describe(user="Jisko roast karna hai")
async def roast(interaction: discord.Interaction, user: discord.Member = None):
    target = user or interaction.user
    await interaction.response.send_message(f"{target.mention} {random.choice(ROASTS)}")

@bot.tree.command(name="shayari", description="Ek mast shayari suno")
async def shayari(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(SHAYARI))

@bot.tree.command(name="joke", description="Ek ganda wala joke")
async def joke(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(JOKES))

@bot.tree.command(name="fact", description="Ek random fact")
async def fact(interaction: discord.Interaction):
    await interaction.response.send_message(f"🧠 **Fact:** {random.choice(FACTS)}")

@bot.tree.command(name="8ball", description="Magic 8 Ball se pucho")
@app_commands.describe(question="Tera sawal kya hai?")
async def eightball(interaction: discord.Interaction, question: str):
    ans = ["Haan bilkul! 💯", "Nahi bhai, rehne de 🙅", "Mitron, pakka hoga!", "Shayad... 50-50 hai", "Bhai soch bhi mat 😂", "100% YES!", "Sapne me bhi nahi", "Thoda wait kar, ho jayega"]
    await interaction.response.send_message(f"🎱 **Q:** {question}\n**A:** {random.choice(ans)}")

@bot.tree.command(name="dice", description="Dice roll karo")
async def dice(interaction: discord.Interaction):
    await interaction.response.send_message(f"🎲 Dice bola: **{random.randint(1,6)}**")

@bot.tree.command(name="coinflip", description="Heads ya Tails?")
async def coinflip(interaction: discord.Interaction):
    await interaction.response.send_message(f"🪙 Coin bola: **{random.choice(['Heads 👑', 'Tails 🦅'])}**")

@bot.tree.command(name="truth", description="Truth pucho")
async def truth(interaction: discord.Interaction):
    await interaction.response.send_message(f"👀 **Truth:** {random.choice(TRUTH)}")

@bot.tree.command(name="dare", description="Dare lo")
async def dare(interaction: discord.Interaction):
    await interaction.response.send_message(f"😈 **Dare:** {random.choice(DARE)}")

@bot.tree.command(name="ship", description="Do logo ko ship karo")
@app_commands.describe(user1="Pehla banda", user2="Dusra banda")
async def ship(interaction: discord.Interaction, user1: discord.Member, user2: discord.Member = None):
    u2 = user2 or interaction.user
    pct = random.randint(0, 100)
    if pct > 85:
        msg = "🔥 PERFECT JODI! Shaadi kab hai?"
    elif pct > 60:
        msg = "❤️ Kaafi jam rahe ho dono!"
    elif pct > 30:
        msg = "😐 Thoda try karna padega..."
    else:
        msg = "💔 Bhai rehne de, dost hi rehne do"
    await interaction.response.send_message(f"💘 {user1.mention} x {u2.mention} = **{pct}%**\n{msg}")

@bot.tree.command(name="love", description="Love % check karo")
@app_commands.describe(user="Kiska love check karna hai?")
async def love(interaction: discord.Interaction, user: discord.Member = None):
    target = user or interaction.user
    pct = random.randint(0, 100)
    await interaction.response.send_message(f"💖 {target.mention} ka love meter: **{pct}%** {'💘 Full pyaar!' if pct>80 else '🙂 Thoda thoda' if pct>40 else '😭 Single hi rahega'}")

@bot.tree.command(name="slap", description="Kisi ko thappad maro")
@app_commands.describe(user="Kisko marna hai?")
async def slap(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(f"👋 {interaction.user.mention} ne {user.mention} ko zor ka thappad mara! *CHATAK* 😭")

@bot.tree.command(name="hug", description="Kisi ko hug do")
@app_commands.describe(user="Kisko hug dena hai?")
async def hug(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(f"🤗 {interaction.user.mention} ne {user.mention} ko tight wala hug diya! Aww 🥰")

@bot.tree.command(name="kiss", description="Kisi ko kiss do")
@app_commands.describe(user="Kisko?")
async def kiss(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(f"😘 {interaction.user.mention} ne {user.mention} ko kiss diya! Haye! 💋")

@bot.tree.command(name="pat", description="Sar pe haath phero")
@app_commands.describe(user="Kisko?")
async def pat(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(f"🐱 {interaction.user.mention} ne {user.mention} ko pyaar se pat kiya! Good boy/girl 🥺")

@bot.tree.command(name="rps", description="Rock Paper Scissors khelo")
@app_commands.describe(choice="Kya choose karoge?")
@app_commands.choices(choice=[app_commands.Choice(name="Rock 🪨", value="rock"), app_commands.Choice(name="Paper 📄", value="paper"), app_commands.Choice(name="Scissors ✂️", value="scissors")])
async def rps(interaction: discord.Interaction, choice: str):
    bot_choice = random.choice(["rock", "paper", "scissors"])
    emoji = {"rock":"🪨","paper":"📄","scissors":"✂️"}
    if choice == bot_choice:
        res = "Draw! 🤝"
    elif (choice=="rock" and bot_choice=="scissors") or (choice=="paper" and bot_choice=="rock") or (choice=="scissors" and bot_choice=="paper"):
        res = "Tu jeet gaya! 🏆"
    else:
        res = "Mai jeet gaya! Mitron, mai haar nahi sakta 😎"
    await interaction.response.send_message(f"Tu: {emoji[choice]} | Mai: {emoji[bot_choice]}\n**{res}**")

@bot.tree.command(name="pp", description="PP size check (mazak me)")
@app_commands.describe(user="Kiska check karna hai?")
async def pp(interaction: discord.Interaction, user: discord.Member = None):
    target = user or interaction.user
    size = random.randint(0, 20)
    await interaction.response.send_message(f"🍆 {target.mention} ka PP size: **{size}cm** {'8====D' + '='*size + 'D' if size>0 else 'Nahi hai bhai 😭'}")

@bot.tree.command(name="gay", description="Gay meter check")
@app_commands.describe(user="Kiska?")
async def gay(interaction: discord.Interaction, user: discord.Member = None):
    target = user or interaction.user
    pct = random.randint(0, 100)
    await interaction.response.send_message(f"🏳️‍🌈 {target.mention} is **{pct}%** gay!")

@bot.tree.command(name="meme", description="Ek random meme text")
async def meme(interaction: discord.Interaction):
    memes = ["Mitron jab teacher bolti hai - kal test hai 😭", "Jab mummy kahe - phone rakh de, aur tu 2 min aur bol de 😂", "POV: Tu 3 baje tak online tha aur subah 6 baje uthna hai", "Jab crush online aaye aur tu typing... dekh ke delete kar de"]
    await interaction.response.send_message(f"😂 {random.choice(memes)}")

# ===== MODI SPECIAL =====
@bot.tree.command(name="modi", description="Modi ji ka random dialogue")
async def modi(interaction: discord.Interaction):
    await interaction.response.send_message(f"🇮🇳 {random.choice(BHASHAN)}")

@bot.tree.command(name="bhashan", description="Ek lamba bhashan suno")
async def bhashan(interaction: discord.Interaction):
    await interaction.response.send_message(f"🎤 **MITRON!**\n{random.choice(BHASHAN)}\n\nAur ant me mai yehi kahunga - **Aise Hi** chalta rahe, pyaar badhta rahe! Jai Hind! 🇮🇳")

@bot.tree.command(name="mannkibaat", description="Mann Ki Baat")
async def mann(interaction: discord.Interaction):
    topics = ["Aaj mai baat karunga - neend ke baare me. So jao mitron, kal subah gym bhi jana hai!", "Aaj ki Mann Ki Baat - Pyaar me padna acha hai, par padhai me bhi padh lo!", "Mitron, aaj mai chahta hu tum sab ek dusre ko hug do, pyaar baanto!"]
    await interaction.response.send_message(f"📻 **Mann Ki Baat:**\n{random.choice(topics)}")

@bot.tree.command(name="mitron", description="Mitron bolo")
async def mitron(interaction: discord.Interaction):
    await interaction.response.send_message("MITRON!!! 🔊🔊🔊")

@bot.tree.command(name="vikas", description="Vikas check karo")
async def vikas(interaction: discord.Interaction):
    await interaction.response.send_message(f"📈 Aaj ka Vikas: **{random.randint(50, 999)}%** badh gaya! Desh aage badh raha hai!")

@bot.tree.command(name="acchedin", description="Acche din kab aayenge?")
async def acchedin(interaction: discord.Interaction):
    await interaction.response.send_message("Mitron, Acche Din aa gaye hai! Tum is server me ho, isse acha din kya hoga? 🥳")

@bot.tree.command(name="chai", description="Chai pe charcha")
async def chai(interaction: discord.Interaction):
    await interaction.response.send_message(f"☕ {interaction.user.mention} ke liye ek garam chai! Charcha shuru karo Mitron!")

# ===== UTILITY =====
@bot.tree.command(name="ping", description="Bot ka ping dekho")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 Pong! **{round(bot.latency*1000)}ms** - Ekdum fast, jaise Vikas!")

@bot.tree.command(name="avatar", description="Kisi ka avatar dekho")
@app_commands.describe(user="Kiska avatar?")
async def avatar(interaction: discord.Interaction, user: discord.Member = None):
    target = user or interaction.user
    embed = discord.Embed(title=f"{target.name} ka Avatar", color=0x00ff00)
    embed.set_image(url=target.display_avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="userinfo", description="Kisi ki info dekho")
@app_commands.describe(user="Kiski info?")
async def userinfo(interaction: discord.Interaction, user: discord.Member = None):
    target = user or interaction.user
    embed = discord.Embed(title=f"{target.name}", color=0x3498db)
    embed.add_field(name="ID", value=target.id, inline=True)
    embed.add_field(name="Joined", value=target.joined_at.strftime("%d %b %Y") if target.joined_at else "N/A", inline=True)
    embed.add_field(name="Top Role", value=target.top_role.mention, inline=True)
    embed.set_thumbnail(url=target.display_avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="serverinfo", description="Server ki info")
async def serverinfo(interaction: discord.Interaction):
    g = interaction.guild
    embed = discord.Embed(title=f"{g.name}", color=0xff7b00)
    embed.add_field(name="Members", value=g.member_count, inline=True)
    embed.add_field(name="Channels", value=len(g.channels), inline=True)
    embed.add_field(name="Created", value=g.created_at.strftime("%d %b %Y"), inline=True)
    if g.icon:
        embed.set_thumbnail(url=g.icon.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="say", description="Bot se kuch bulwao")
@app_commands.describe(text="Kya bolwana hai?")
async def say(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(f"Mitron ne bola: {text}")

@bot.tree.command(name="poll", description="Poll banao")
@app_commands.describe(question="Sawal kya hai?", option1="Option 1", option2="Option 2")
async def poll(interaction: discord.Interaction, question: str, option1: str, option2: str):
    embed = discord.Embed(title=f"📊 Poll: {question}", description=f"1️⃣ {option1}\n2️⃣ {option2}", color=0x9b59b6)
    await interaction.response.send_message(embed=embed)
    msg = await interaction.original_response()
    await msg.add_reaction("1️⃣")
    await msg.add_reaction("2️⃣")

# ===== ADMIN SLASH =====
@bot.tree.command(name="kick", description="Kisi ko kick karo [ADMIN]")
@app_commands.describe(user="Kisko kick karna hai?", reason="Reason kya hai?")
@app_commands.default_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason"):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("Bhai tu admin nahi hai, Mitron! ❌", ephemeral=True); return
    await user.kick(reason=reason)
    await interaction.response.send_message(f"👢 {user.mention} ko kick kar diya! Reason: {reason}")

@bot.tree.command(name="ban", description="Kisi ko ban karo [ADMIN]")
@app_commands.describe(user="Kisko ban karna hai?", reason="Reason?")
@app_commands.default_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason"):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("Tu admin nahi hai bhai ❌", ephemeral=True); return
    await user.ban(reason=reason)
    await interaction.response.send_message(f"🔨 {user.mention} ko ban kar diya! Bye bye! Reason: {reason}")

@bot.tree.command(name="unban", description="Kisi ko unban karo [ADMIN]")
@app_commands.describe(user_id="Ban wale bande ki ID")
@app_commands.default_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, user_id: str):
    try:
        user = await bot.fetch_user(int(user_id))
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"✅ {user.mention} ko unban kar diya!")
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}", ephemeral=True)

@bot.tree.command(name="mute", description="Kisi ko timeout/mute karo [ADMIN]")
@app_commands.describe(user="Kisko?", minutes="Kitne minute ke liye? (default 10)")
@app_commands.default_permissions(moderate_members=True)
async def mute(interaction: discord.Interaction, user: discord.Member, minutes: int = 10):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message("Tu mod nahi hai ❌", ephemeral=True); return
    import datetime
    await user.timeout(datetime.timedelta(minutes=minutes))
    await interaction.response.send_message(f"🔇 {user.mention} ko {minutes} min ke liye mute kar diya! Chup chap baithega ab 😂")

@bot.tree.command(name="unmute", description="Unmute karo [ADMIN]")
@app_commands.describe(user="Kisko?")
@app_commands.default_permissions(moderate_members=True)
async def unmute(interaction: discord.Interaction, user: discord.Member):
    import datetime
    await user.timeout(None)
    await interaction.response.send_message(f"🔊 {user.mention} ko unmute kar diya!")

@bot.tree.command(name="clear", description="Messages delete karo [ADMIN]")
@app_commands.describe(amount="Kitne messages? (max 100)")
@app_commands.default_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int = 10):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("Permission nahi hai ❌", ephemeral=True); return
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"🧹 {len(deleted)} messages saaf kar diye! Mitron, safai ho gayi!", ephemeral=True)

@bot.tree.command(name="warn", description="Kisi ko warn do [ADMIN]")
@app_commands.describe(user="Kisko?", reason="Kyu?")
@app_commands.default_permissions(moderate_members=True)
async def warn(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason"):
    warns.setdefault(str(user.id), []).append(reason)
    count = len(warns[str(user.id)])
    await interaction.response.send_message(f"⚠️ {user.mention} ko warn #{count} mila! Reason: {reason}\nAb sudhar ja bhai!")

@bot.tree.command(name="warnings", description="Kisi ke warnings dekho")
@app_commands.describe(user="Kiska?")
async def warnings(interaction: discord.Interaction, user: discord.Member):
    lst = warns.get(str(user.id), [])
    if not lst:
        await interaction.response.send_message(f"✅ {user.mention} ekdum clean hai, koi warn nahi!")
    else:
        await interaction.response.send_message(f"⚠️ {user.mention} ke {len(lst)} warns:\n" + "\n".join([f"{i+1}. {w}" for i,w in enumerate(lst)]))

@bot.tree.command(name="slowmode", description="Channel slowmode lagao [ADMIN]")
@app_commands.describe(seconds="Kitne seconds? 0 = off")
@app_commands.default_permissions(manage_channels=True)
async def slowmode(interaction: discord.Interaction, seconds: int = 5):
    await interaction.channel.edit(slowmode_delay=seconds)
    await interaction.response.send_message(f"🐢 Slowmode set: {seconds} sec! Ab aaram se bolo Mitron!")

@bot.tree.command(name="lock", description="Channel lock karo [ADMIN]")
@app_commands.default_permissions(manage_channels=True)
async def lock(interaction: discord.Interaction):
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
    await interaction.response.send_message("🔒 Channel lock ho gaya! Ab koi nahi bolega!")

@bot.tree.command(name="unlock", description="Channel unlock karo [ADMIN]")
@app_commands.default_permissions(manage_channels=True)
async def unlock(interaction: discord.Interaction):
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
    await interaction.response.send_message("🔓 Channel unlock ho gaya! Bolo Mitron!")

@bot.tree.command(name="nick", description="Kisi ka nickname badlo [ADMIN]")
@app_commands.describe(user="Kiska?", nickname="Naya naam?")
@app_commands.default_permissions(manage_nicknames=True)
async def nick(interaction: discord.Interaction, user: discord.Member, nickname: str):
    await user.edit(nick=nickname)
    await interaction.response.send_message(f"✏️ {user.mention} ka naya naam: **{nickname}**")

@bot.tree.command(name="addrole", description="Role do [ADMIN]")
@app_commands.describe(user="Kisko?", role="Kaunsi role?")
@app_commands.default_permissions(manage_roles=True)
async def addrole(interaction: discord.Interaction, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await interaction.response.send_message(f"✅ {user.mention} ko **{role.name}** role de di!")

@bot.tree.command(name="removerole", description="Role hatao [ADMIN]")
@app_commands.describe(user="Kiska?", role="Kaunsi?")
@app_commands.default_permissions(manage_roles=True)
async def removerole(interaction: discord.Interaction, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await interaction.response.send_message(f"❌ {user.mention} se **{role.name}** role hata di!")

@bot.tree.command(name="announce", description="Announcement bhejo [ADMIN]")
@app_commands.describe(text="Kya announce karna hai?", channel="Kis channel me?")
@app_commands.default_permissions(manage_messages=True)
async def announce(interaction: discord.Interaction, text: str, channel: discord.TextChannel = None):
    ch = channel or interaction.channel
    embed = discord.Embed(title="📢 ANNOUNCEMENT - MITRON!", description=text, color=0xff0000)
    embed.set_footer(text=f"By {interaction.user.name}")
    await ch.send(embed=embed)
    await interaction.response.send_message("✅ Announcement bhej di!", ephemeral=True)

# ===== PREFIX COMMANDS (purane wale bhi chalenge) =====
@bot.command(name="ping")
async def ping_p(ctx):
    await ctx.send(f"Pong! {round(bot.latency*1000)}ms")

@bot.command(name="roast")
async def roast_p(ctx, user: discord.Member = None):
    target = user or ctx.author
    await ctx.send(f"{target.mention} {random.choice(ROASTS)}")

@bot.command(name="bhashan")
async def bhashan_p(ctx):
    await ctx.send(f"🎤 MITRON! {random.choice(BHASHAN)}")

@bot.command(name="shayari")
async def shayari_p(ctx):
    await ctx.send(random.choice(SHAYARI))

@bot.command(name="joke")
async def joke_p(ctx):
    await ctx.send(random.choice(JOKES))

@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear_p(ctx, amount: int = 10):
    deleted = await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"🧹 {len(deleted)-1} messages saaf!", delete_after=3)

# ===== RUN =====
if __name__ == "__main__":
    if not TOKEN:
        print("TOKEN nahi mila! Render me Environment Variable me TOKEN daal")
    else:
        bot.run(TOKEN)
