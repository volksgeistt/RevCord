import os
import discord
from discord.ext import commands
import json
import asyncio
import random
import colorama
import aiohttp
from colorama import Fore
import pyfiglet
import io
from pyfiglet import Figlet
import requests
import pyshorteners
import datetime
import string
from datetime import time

# ----- AUTH ----- #

def auth():
    def check_user_id(ctx):
        with open('Config.json', 'r') as file:
            data = json.load(file)
        user_id = str(ctx.author.id)
        return user_id in data.get("AUTHORIZED_USERS", [])
    return commands.check(check_user_id)

# ----- LOAD ----- #

with open('Config.json', 'r') as ok:
    config = json.load(ok)

# ------------------------- #

client = commands.Bot(command_prefix=config["PREFIX"], bot=False,case_insensitive=True,self_bot=True,help_command=None)
session = aiohttp.ClientSession()

def ascii_print(text):
    x = pyfiglet.Figlet(font="big")
    y = x.renderText(text)
    print(y)

@client.event
async def on_connect():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=config["ACTIVITY_NAME"]))
    ascii_print("# RevCord")
    print(f"{Fore.GREEN}[ CONNECTED ] -> Logged in as {client.user.name}.{Fore.RESET}")
    print(f"{Fore.MAGENTA}[ LOADED ] -> Total {len(client.commands)} Commands.{Fore.RESET}")

@client.event
async def on_command(ctx):
    print(f"\n\n{Fore.YELLOW}[ LOG ] -> '{ctx.command.name}' Command Has Been Triggered.")

@client.event
async def on_shutdown():
    await session.close()

# -------- HELP-MENU -----------#

@client.command(aliases=["h","commands","cmds","allcmd","allcmds"])
@auth()
async def help(ctx):
    command_list = [command.name for command in client.commands]
    ayotf = ", ".join(command_list)
    await ctx.send(f"# RevCord\n**__Commands__ ({len(client.commands)})**\n{ayotf}")
    await ctx.message.delete()

# -------- COMMANDS -------- #
@client.command(aliases=["rcvd"])
async def received(ctx, *, amount):
    await ctx.send(f"- Payment Of `{amount}` Has Been Received.")
    await ctx.message.delete()


@client.command()
@auth()
async def ltc(ctx):
    await ctx.send(config["LTC_ADDY"])
    await ctx.send(config["CRYPTO_PAY_PROOF_MSG"])
    await ctx.message.delete()


@client.command(aliases=["famapp","fam"])
@auth()
async def fampay(ctx):
    await ctx.send(config["FAMPAY"])
    await ctx.send(config["UPI_PAY_PROOF_MSG"])
    await ctx.message.delete()


@client.command(aliases=["omnicard"])
@auth()
async def omni(ctx):
    await ctx.send(config["OMNICARD"])
    await ctx.send(config["UPI_PAY_PROOF_MSG"])
    await ctx.message.delete()


@client.command()
@auth()
async def paytm(ctx):
    await ctx.send(config["PAYTM"])
    await ctx.message.delete()


@client.command()
@auth()
async def qr(ctx):
    await ctx.send(config["UPI_QR"])
    await ctx.send(config["UPI_PAY_PROOF_MSG"])
    await ctx.message.delete()


@client.command(aliases=["pp"])
@auth()
async def paypal(ctx):
    await ctx.send(config["PAYPAL_ID"])
    await ctx.message.delete()


@client.command(aliases=["av"])
@auth()
async def avatar(ctx, member: discord.Member):
    await ctx.send(f'{member.avatar_url}')
    await ctx.message.delete()

@client.command()
@auth()
async def restart(ctx):
    os.execl(sys.executable, sys.executable, *sys.argv)

@client.command(aliases=["shutdown","logoff"])
@auth()
async def logout(ctx):
    await ctx.message.delete()
    await ctx.send(f"- Logged Out")
    await client.close()


@client.command()
@auth()
async def ping(ctx):
    await ctx.send(f"Web-Socket Latency: {int(client.latency*1000)}ms!")
    await ctx.message.delete()

@client.command(aliases=["fuckoff"])
@auth()
async def ban(ctx, member: discord.Member = None):
    await member.ban(reason=f"Banned By {ctx.author}")
    await ctx.send(f"- Successfully Banned **{member}**")

@client.command()
@auth()
async def kick(ctx, member: discord.Member = None):
    await member.kick(reason=f"Kicked By {ctx.author}")
    await ctx.send(f"- Successfully Kicked **{member}**")

@client.command()
@auth()
async def block(ctx, user: discord.User):
    await user.block()
    await ctx.message.delete()

@client.command()
@auth()
async def clone(ctx):
  tckitn = [ctx.channel.category, ctx.channel.position]
  await ctx.channel.clone()
  await ctx.channel.delete()
  nukedchannel = tckitn[0].text_channels[-1]
  await nukedchannel.edit(position=tckitn[1])
  await nukedchannel.send(f"- Channel Cloned")

@client.command(aliases=["asci"])
@auth()
async def ascii(ctx, *, text):
    f = Figlet(font='standard')
    ascii_art = f.renderText(text)
    await ctx.send(f'```{ascii_art}```')
    await ctx.message.delete()


@client.command()
@auth()
async def vouch(ctx, *, content):
    w = config["VOUCH_USER_ID"]
    await ctx.send(f'`+rep {w} {content}`')
    await ctx.send(config["VOUCH_SERVER_LINK"])
    await ctx.message.delete()

@client.command()
@auth()
async def spam(ctx, amount: int, *, content):
    for fuckup in range(amount):
        await ctx.send(content)
        await asyncio.sleep(0.05)
        await ctx.message.delete()

@client.command(aliases=['shorten'])
@auth()
async def tinyurl(ctx, url: str):
    cut = pyshorteners.Shortener()
    try:
        t = cut.tinyurl.short(url)
        await ctx.send(f"- Your TinyURL: {t}")
    except pyshorteners.exceptions.ShorteningError:
        await ctx.send("- URL Is Incorrect")

@client.command()
@auth()
async def boosts(ctx):
    await ctx.send(f"This Server Has {ctx.guild.premium_subscription_count} Boosts.")

@client.command()
@auth()
async def randomip(ctx):
    mvp = [random.randint(0, 255) for forgesb in range(4)]
    pussi = ".".join(map(str, mvp))
    await ctx.send(f"- Random IP: {pussi}")

@client.command(aliases=["ip-info"])
@auth()
async def ipinfo(ctx, ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url).json()
    if response["status"] == "fail":
        await ctx.send(f"- The Provided IP Is Incorrect.")
        return
    await ctx.send(f"- **IP Address:** {response['query']}\n- **Location:** {response['city']}, {response['regionName']}, {response['country']}\n- **ISP:** {response['isp']}\n- **Organization:** {response['org']}\n- **Timezone:** {response['timezone']}")

@client.command(aliases=['solve','calculate'])
@auth()
async def calc(ctx, *, expression):
    try:
        sol = eval(expression)
        await ctx.send(f'{sol}')
        await ctx.message.delete()
    except:
        await ctx.send('> Invalid Expression. Use Operators Such As ( + , - , * , / )')
        await ctx.message.delete()

@client.command(aliases=['purge'])
@auth()
async def clear(ctx, purge_amount: int):
    if purge_amount <= 0:
        await ctx.send("- Provide Any Integer Value To Execute Command.")
        return
    if purge_amount > 100:
        await ctx.send("- You Can't Delete Messages More Than 100 At Once.")
        return
    channel = ctx.channel
    def is_bot_message(message):
        return message.author.id == ctx.bot.user.id
    messages = await channel.history(limit=purge_amount + 1).flatten()
    bot_messages = filter(is_bot_message, messages)
    for message in bot_messages:
        await asyncio.sleep(0.1)
        await message.delete()


@client.command(aliases=['pltc'])
@auth()
async def ltcprice(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/litecoin'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        price = data['market_data']['current_price']['usd']
        price_change_percentage_24h = data['market_data']['price_change_percentage_24h']
        await ctx.send(f"""
- Litecoin Price: ${price:.2f}
- 24h Price Change: {price_change_percentage_24h:.2f}%""")
        await ctx.message.delete()
    except requests.exceptions.RequestException as e:
        await ctx.send(f"> Unable To Get LiteCoin Price.")
        await ctx.message.delete()

@client.command(aliases=['bal'])
@auth()
async def getbal(ctx, ltcaddress):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')
    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8  
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.send("Invalid LiteCoin Address, Please Check.")
        return
    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.send("Unable To Fetch Balance.")
        return
    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price
    await ctx.message.delete()
    response_message = await ctx.send(f"- **Current Balance:** {usd_balance:.2f}$\n- **Total Received:** {usd_total_balance:.2f}$\n- **Unconfirmed LTC:** {usd_unconfirmed_balance:.2f}$")
    await asyncio.sleep(180)
    await response_message.delete()

@client.command()
@auth()
async def github(ctx, username):
    api_url = f'https://api.github.com/users/{username}'
    response = requests.get(api_url)
    if response.status_code == 200:
        user_data = response.json()
        wtff = {
            '- Username': user_data['login'],
            '- Followers': user_data['followers'],
            '- Following': user_data['following'],
            '- Repositories': user_data['public_repos'],
        }
        final = '\n'.join([f'{key}: {value}' for key, value in wtff.items()])
        await ctx.send(f'# GitHub Info:\n{final}')
        await ctx.message.delete()
    else:
        await ctx.send(f'- Error: {response.status_code}')
        await ctx.message.delete()



@client.command()
@auth()
async def checkvanity(ctx, invite_code):
    try:
        invite = await client.fetch_invite(invite_code)
        guild = invite.guild
        await ctx.send(f'- **The Invite Code Is Already Taken!**\n- Guild Name: {guild.name}\n- Guild ID: {guild.id}')
    except discord.NotFound:
        await ctx.send('- The Invite Code Is Available.')
    except discord.errors.HTTPException as e:
        await ctx.send(f'- Error Checking Invite Code -> {e}')
        await ctx.message.delete()


@client.command()
@auth()
async def leavegroups(ctx):
    for channel in client.private_channels:
        if isinstance(channel, discord.GroupChannel):
            await channel.leave()
            await ctx.message.delete()
            await ctx.message.delete()


@client.command(aliases=["adminserver"])
@auth()
async def adminservers(ctx):
    admin_servers = []
    for guild in client.guilds:
        if guild.me.guild_permissions.administrator:
            admin_servers.append(discord.utils.escape_markdown(guild.name))
    if not admin_servers:
        await ctx.reply("- You Don't Have Any Server With `Admin` Permission.")
    else:
        servers_list = "\n".join(admin_servers)
        await ctx.reply(
            f"**Servers With Admin Perms:**\n```{servers_list}```")
        await ctx.message.delete()


@client.command(aliases=["ui", "uinfo"])
@auth()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    roles = [role.name for role in member.roles[1:]]
    roles_str = ', @'.join(roles) if roles else 'None'
    created_at = member.created_at.strftime("%Y-%m-%d %H:%M:%S")
    joined_at = member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
    user_info = (
        f"# **UserInfo Statistics**\n**Username:** {member.name}\n**Discriminator:** #{member.discriminator}\n**User ID:** {member.id}\n**Created At:** {created_at}\n**Joined At:** {joined_at}\n**Roles:** {roles_str}"
    )
    await ctx.reply(user_info)
    await ctx.message.delete()

@client.command()
@auth()
async def truth(ctx):
  content = requests.get("https://api.truthordarebot.xyz/v1/truth").text
  data = json.loads(content)
  text = data["question"]
  await ctx.reply(f"- {text}")


@client.command()
@auth()
async def dare(ctx):
  content = requests.get("https://api.truthordarebot.xyz/v1/dare").text
  data = json.loads(content)
  text = data["question"]
  await ctx.reply(f"- {text}")

@client.command()
@auth()
async def pussy(ctx):
    try:
        async with session.get("http://api.nekos.fun:8080/api/pussy") as response:
            data = await response.json()
        image = data["image"]
        async with session.get(image) as img_response:
            image_data = await img_response.read()
        file = discord.File(io.BytesIO(image_data), filename="pussy.jpg")
        await ctx.send(file=file)
        await ctx.message.delete()
    except Exception as e:
        print(f"{Fore.RED}[ ERROR ] -> An Error Occured: ( {e} )")

@client.command()
@auth()
async def cum(ctx):
    try:
        async with session.get("http://api.nekos.fun:8080/api/cum") as response:
            data = await response.json()
        image = data["image"]
        async with session.get(image) as img_response:
            image_data = await img_response.read()
        file = discord.File(io.BytesIO(image_data), filename="cum.jpg")
        await ctx.send(file=file)
        await ctx.message.delete()
    except Exception as e:
        print(f"{Fore.RED}[ ERROR ] -> An Error Occured: ( {e} )")

@client.command()
@auth()
async def blowjob(ctx):
    try:
        async with session.get("http://api.nekos.fun:8080/api/blowjob") as response:
            data = await response.json()
        image = data["image"]
        async with session.get(image) as img_response:
            image_data = await img_response.read()
        file = discord.File(io.BytesIO(image_data), filename="blowjob.jpg")
        await ctx.send(file=file)
        await ctx.message.delete()
    except Exception as e:
        print(f"{Fore.RED}[ ERROR ] -> An Error Occured: ( {e} )")

@client.command()
@auth()
async def hentai(ctx):
    try:
        async with session.get("http://api.nekos.fun:8080/api/hentai") as response:
            data = await response.json()
        image = data["image"]
        async with session.get(image) as img_response:
            image_data = await img_response.read()
        file = discord.File(io.BytesIO(image_data), filename="hentai.jpg")
        await ctx.send(file=file)
        await ctx.message.delete()
    except Exception as e:
        print(f"{Fore.RED}[ ERROR ] -> An Error Occured: ( {e} )")

@client.command()
@auth()
async def nickall(ctx, *, name):
  for kids in ctx.guild.members:
      await kids.edit(nick=name)
      await ctx.message.delete()

def rand_nick():
    a = [
    "Happy", "Silly", "Lucky", "Clever", "Gentle", "Levis", "Carlo", "Karlos",
    "Meow", "Wave", "Stuff", "Boosts", "OwO", "Dyno", "Dynoxy", "Tranlucent",
    "Radiant", "Zesty", "Magical", "Vibrant", "Breezy", "Enchanted", "Harmonious",
    "Inquisitive", "Vivacious", "Whimsical", "Adventurous", "Captivating", "Delightful",
    "Energetic", "Fantastic", "Gleaming", "Joyful", "Majestic", "Nifty", "Optimistic",
    "Playful", "Quirky", "Rambunctious", "Spectacular", "Thrilling", "Unique", "Vivid",
    "Wondrous", "Xtraordinary", "Yummy", "Zippy",
    "Serene", "Joyous", "Zany", "Witty", "Cheerful", "Epic", "Bubbly", "Spiffy",
    "Mellow", "Wacky", "Dazzling", "Ecstatic", "Funky", "Jolly", "Mystical", "Glorious",
    "Plucky", "Radiant", "Sassy", "Vibrant", "Wholesome", "Snazzy", "Whizzy", "Dapper",
    "Snuggly", "Fizzy", "Giggly", "Jubilant", "Kindred", "Lively", "Majestic", "Nifty",
    "Oddball", "Peculiar", "Quaint", "Radiant", "Sunny", "Tranquil", "Upbeat", "Vivid",
    "Wondrous", "Yummy", "Zippy", "Exquisite", "Glowing", "Enchanting", "Divine", "Breathtaking",
    "Marvelous", "Enigmatic", "Ethereal",    "Oliver", "Emma", "Liam", "Ava", "Noah", "Isabella", "Sophia", "Jackson",
    "Lucas", "Benjamin", "Mia", "Ethan", "Elijah", "Harper", "Evelyn", "Alexander",
    "James", "Aiden", "Grace", "Abigail", "Henry", "Charlotte", "Scarlett", "Sebastian",
    "Amelia", "Chloe", "Owen", "Mila", "Carter", "Aria", "Lily", "Zoe", "Luna",
    "Mateo", "Layla", "Jack", "Ella", "Avery", "Nora", "Levi", "Riley", "Sofia",
    "Caleb", "Aubrey", "Wyatt", "Hazel", "Gabriel", "Ellie", "Aiden", "Stella", "Julian","Mechanics", "Kinematics", "Dynamics", "Force", "Motion", "Energy", "Work",
    "Power", "Momentum", "Impulse", "Friction", "Tension", "Gravity", "Acceleration", "Velocity",
    "Speed", "Mass", "Inertia", "Pressure", "Density", "Buoyancy", "Torque", "Rotational", "Equilibrium",
    "Circular", "Motion", "Angular", "Momentum", "Centripetal", "Force", "Pendulum", "Wave", "Frequency",
    "Amplitude", "Wavelength", "Period", "Electromagnetism", "Electricity", "Magnetism", "Voltage", "Current",
    "Resistance", "Ohm's", "Law", "Circuit", "Capacitor", "Inductor", "Electromagnetic", "Field", "Quantum",
    "Mechanics", "Wave", "Particle", "Light", "Sound", "Optics", "Refraction", "Reflection", "Interference",
    "Diffraction", "Thermodynamics", "Temperature", "Heat", "Thermal", "Expansion", "Entropy", "Conservation",
    "Law", "Thermal", "Conduction", "Convection", "Radiation", "Nuclear", "Physics", "Particle", "Physics",
    "Quantum", "Physics", "Relativity", "Theory", "General", "Special", "Atomic", "Nuclear", "Particle",
    "Astrophysics", "Cosmology", "Dark", "Matter", "Dark", "Energy", "String", "Theory", "Unified", "Field",
    "Brim", "Viper", "Omen", "Raze", "Sova", "Sage", "Cypher", "Phoenix", "Jett", "Breach", "Reyna", "Killjoy", "Skye", "Yoru", "Astra",
    "Barbarian", "Archer", "Goblin", "Giant", "Wall Breaker", "Balloon", "Wizard", "Healer",
    "Dragon", "P.E.K.K.A", "Minion"]

    b = [
    "Dog", "Cat", "Panda", "Tiger", "Elephant", "Nitro", "Switch", "VPN",
    "Gamer", "Developer", "Hannah", "UwU", "Twicth", "YouTube", "Jungle",
    "Astronaut", "Rainbow", "Galaxy", "Comet", "Cosmic", "Sonic", "Aqua",
    "Pixel", "Nebula", "Stellar", "Orbit", "Quasar", "Gravity", "Infinity",
    "Celestial", "Ninja", "Galactic", "Eclipse", "Radiance", "Techno", "Lunar",
    "Nova", "Starlight", "Meteor", "Pulsar", "Saturn", "Supernova", "Aurora",
    "Abyss", "Zodiac", "Rocket", "Cosmos", "Meteorite",
    "Penguin", "Frosty", "Thunder", "Blizzard", "Shadow", "Blaze", "Whisper", "Storm",
    "Flare", "Phoenix", "Thunderbolt", "Frostbite", "Whirlwind", "Tornado", "Mystique", "Quasar",
    "Avalanche", "Thunderclap", "Starstrike", "Nebulon", "Aether", "Lunarflare", "Zephyr", "Cerulean",
    "Inferno", "Solaris", "Vortex", "Luminary", "Bliss", "Crimson", "Nebula", "Sorcery",
    "Warp", "Shimmer", "Astral", "Polaris", "Frostfall", "Zephyrus", "Serpent", "Luminosity",
    "Cynosure", "Ignition", "Abyssal", "Vortex", "Zephyr", "Harmony", "Ecliptic", "Flametide",
    "Galaxia", "Moonshade",    "Lillian", "Isaac", "Grace", "Ezra", "Ivy", "Santiago", "Aurora", "Nathan", "Emilia",
    "Christian", "Penelope", "Samuel", "Scarlet", "Jaxon", "Nova", "Christopher", "Lily",
    "Maverick", "Zara", "Josiah", "Ariana", "John", "Taylor", "Leo", "Hannah", "David",
    "Madison", "Muhammad", "Addison", "Isaiah", "Eleanor", "Lincoln", "Natalie", "Joseph",
    "Brooklyn", "Hunter", "Savannah", "Anthony", "Anna", "Jonathan", "Leah", "Dylan", "Lillian",
    "Leo", "Aaliyah", "Aaron", "Zoe", "Eli", "Hailey", "Nicholas", "Peyton",
    "Cell", "Prokaryote", "Eukaryote", "Organelle", "Nucleus", "Mitochondria", "Chloroplast",
    "Endoplasmic", "Reticulum", "Golgi", "Apparatus", "Lysosome","Atom", "Element", "Compound", "Molecule", "Ion", "Cation", "Anion", "Periodic",
    "Table", "Period", "Group", "Metal", "Nonmetal", "Metalloid", "Alkali", "Alkaline", "Earth",
    "Transition", "Halogen", "Noble", "Gas", "Organic", "Inorganic", "Biochemistry", "Physical",
    "Chemistry", "Analytical", "Chemistry", "Thermodynamics", "Reaction", "Equation", "Stoichiometry",
    "Avogadro's", "Law", "Kinetics", "Catalyst", "Enzyme", "Redox", "Oxidation", "Reduction", "Entropy",
    "Spontaneous", "Reaction", "Activation", "Energy", "Exothermic", "Endothermic", "Electrochemistry",
    "Electrolyte", "Galvanic", "Cell", "Electrolysis", "Solubility", "Solution", "Concentration", "Molarity",
    "Molality", "Boiling", "Point", "Freezing", "Point", "Colligative", "Properties", "Acid", "Base",
    "pH", "Buffer", "Titration", "Organic", "Chemistry", "Alkane", "Alkene", "Alkyne", "Isomer", "Hydrocarbon",
    "Functional", "Group", "Aromatic", "Compound", "Carbohydrate", "Protein", "Lipid", "Nucleic", "Acid",
    "Polymer", "Monomer", "Cell", "Biology", "Genetics", "Evolution", "Ecology", "Microbiology", "Botany",
    "Zoology", "Taxonomy", "Physiology", "Anatomy", "Biotechnology", "Bioinformatics", "Molecular", "Biology",
    "Cell", "Division", "Meiosis", "Mitosis", "DNA", "RNA", "Protein", "Synthesis", "Genome", "Mutation",
    "Ghost", "Spectre", "Bulldog", "Guardian", "Phantom", "Vandal", "Marshal", "Operator", "Ares", "Odin",
    "Hog Rider", "Valkyrie", "Golem", "Witch", "Lava Hound","Bowler", "Baby Dragon", "Miner", "Electro Dragon",
    "Yeti", "Ice Golem", "Headhunter"]
    
    c = random.choice(a) + random.choice(b)
    random_number = ''.join(random.choices(string.digits, k=3))
    c += random_number
    return c

@client.command()
@auth()
async def nickallrandom(ctx):
    await ctx.message.delete()
    authr = ctx.author.top_role
    for member in ctx.guild.members:
        if member.top_role <= authr:
            new_nick = rand_nick()
            try:
                await member.edit(nick=new_nick)
                await asyncio.sleep(2)
            except discord.Forbidden:
                print(f"{Fore.RED}[ ERROR ] -> Unable To Change Nick For {member.display_name}! ( Insufficient Perms )")
                await asyncio.sleep(2)
        else:
            print(f"{Fore.RED}[ ERROR ] -> Skipping {member.display_name}. ( User Have Higher Role )")
            await asyncio.sleep(2)


client.run(config["TOKEN"])
