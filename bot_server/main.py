import discord 
from discord import Intents
from discord.ext import commands, tasks 
import random
import asyncio

activites=["Modération du serveur","faire la police","=help pour connaitre les commandes","wati bot de modération","vous surveiller"]
bot = commands.Bot(command_prefix = "=", description = "Bot multifonction",intents=Intents.all()) 

#salut les gars

#morpion 

player1 = ""
player2 = ""
turn = ""
gameOver = True
board = []

winningConditions = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

#morpion

@tasks.loop(seconds = 30)
async def Change_status():
	game= discord.Game(random.choice(activites))
	await bot.change_presence(status= discord.Status.online,activity = game)


@bot.event
async def on_ready():
	print("On est la !")
	Change_status.start()

@bot.event
async def on_message_delete(message):
	channel = message.guild.get_channel(807309607440744468)
	embed = discord.Embed(title = "", description = (f":wastebasket:** Le message envoyé par {message.author.mention} a été supprimé dans {message.channel.mention}**\n {message.content}"),color =0x4B0082 )
	embed.set_author(name = message.author,icon_url = message.author.avatar_url)
	embed.set_thumbnail(url = "")
	embed.set_footer(text = bot.user.name)
	await channel.send(embed = embed)


@bot.event 
async def on_message_edit(before,after):
	channel = before.guild.get_channel(807309607440744468)
	if before.author == bot.user: 
		return
	if before.content == after.content:
		return
	embed = discord.Embed(title = "", description = (f":keyboard:** Le message envoyé par {before.author.mention} a été édité dans {before.channel.mention}**"),color =0xEE82EE )
	embed.set_author(name = before.author,icon_url = before.author.avatar_url)
	embed.set_thumbnail(url ="")
	embed.add_field(name = "Ancien message", value	= before.content,inline = False)
	embed.add_field(name = "Nouveau message", value	= after.content,inline = False)
	embed.set_footer(text = (bot.user.name))
	await channel.send(embed = embed)

@bot.event
async def on_member_join(member):
	iconUrl = member.guild.icon_url
	usericon = member.avatar_url
	channel = member.guild.get_channel(807309619696238652)
	embed = discord.Embed(title = member.guild.name, description = (f"Bienvenue à toi **{member.name}** sur {member.guild.name} ! \n \n • Le Discord compte désormais **{member.guild.member_count}** personnes !"),color =0x28C361 )
	embed.set_thumbnail(url = usericon)
	embed.set_footer(icon_url = iconUrl, text = bot.user.name)
	await channel.send(embed = embed)
	print("embed good")
	try:
		target = member
		await target.send(f"Bienvenue sur **__{member.guild.name}__** ! 🌠 \n Tu peux y **faire ta publicité et partager tes créations** 🌎 , cependant si **tu quittes le serveur** elles seront supprimés. \n Passe un bon moment sur {member.guild.name} 😊 \n \n tu peux également allez participer aux giveaways si tu souhaites gagner de l'argent ici : https://discord.com/channels/807307761607507978/807309628160868352/820657933758103562")
	except:
		channel = member.guild.get_channel(807309609362391060)
		await channel.send(f"Impossible de souhaiter la bienvenue à {member.mention} ! ")
		print("pas bon")
	print("finis")

	


@bot.event
async def on_member_remove(member):
    salons = [807309638054707200, 807320197982846987, 807309638621462569, 807309640303247401]

    for salon in salons:
        channel_msg = member.guild.get_channel(salon)
        msg = await channel_msg.history().flatten()
        for message in msg:
            if message.author.id == member.id:
                await message.delete()

    embed = discord.Embed(title=member.guild.name, description=f"Adieu **{member.name}** à bientot sur {member.guild.name} ! \n \n • Le Discord compte désormais **{member.guild.member_count}** personnes !",color =0x8A0303 )
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(icon_url=member.guild.icon_url, text=bot.user.name)

    channel = member.guild.get_channel(807309619696238652)
    await channel.send(embed=embed)

#@bot.event
#async def on_reaction_add(reaction, user):
#	await reaction.message.add_reaction(reaction.emoji)


@bot.event
async def on_command_error(ctx, error):
	if isinstance(error,commands.MissingRequiredArgument):
		await ctx.send("Il manque un argument.")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("Vous n'avez pas la permission d'effectuer cette commande.")
	elif isinstance(error, discord.Forbidden):
		await ctx.send("Je n'ai pas la permission d'effectuer cette commande.")
	elif isinstance(error,commands.CommandNotFound):
		await ctx.send("Cette commande n'existe pas.")

@bot.event
async def on_message(message):
	if message.content in ['Hello','Salut','Hey','hey','salut','hello','yo !','salut !','Salut !','hey ^^','salut ^^','wsh','coucou','yo','Yo','bonjour','slm','Bonjour']:
		await message.add_reaction("👋")
		
	await bot.process_commands(message)

@bot.command(name= "chineseText",aliases = ["chinese", "chinois","CHINESE","CHINOIS"])
@commands.has_permissions(send_messages = True)
async def chinese(ctx, *,texte):
	chineseCRC="丹书ㄈ力已下呂廾工丿片乚爪ㄇ口尸厶尺ㄎ丁凵人山父了乙"
	chineseText=[]
	for word in texte:
		for char in word:
			if char.isalpha():
				index= ord(char) - ord("a")
				transformed= chineseCRC[index]
				chineseText.append(transformed)
			else:
				chineseText.append(char)
		chineseText.append(" ")
	await ctx.send("".join(chineseText))


@bot.command(name ="clear",aliases=["CLEAR"])
@commands.has_permissions(manage_messages = True)
async def clear(ctx, nombre : int):
	messages =await ctx.channel.history(limit = nombre +1).flatten()
	for message in messages:
		await message.delete()


@bot.command(name = "serverinfo",aliases = ["si","servInfo","SI"])
@commands.has_permissions(administrator = True)
async def si(ctx):
	server = ctx.guild
	numberOfTextChannels = len(server.text_channels)
	numberOfVoiceChannels = len(server.voice_channels)
	serverDescription= server.description
	NumberOfPerson = server.member_count
	serverName = server.name
	NumberOfRole = len(server.roles)
	iconUrl = server.icon_url
	RegionServer=server.region
	NumbersOfSalons=len(server.channels)
	serverCreation=server.created_at
	EmojiList=server.emojis
	embed = discord.Embed(title = "__Informations du serveur__", description = "",color =0x84004f )
	embed.set_author(name = serverName , icon_url =server.icon_url)
	embed.set_thumbnail(url = iconUrl)
	embed.add_field(name = "Membres", value = NumberOfPerson, inline = True) 
	embed.add_field(name = "Membres en ligne", value = NumberOfPerson, inline = False) 
	embed.add_field(name = "Salons textuels", value = numberOfTextChannels , inline = False)
	embed.add_field(name = "Salons vocaux", value = numberOfVoiceChannels, inline = False)
	embed.add_field(name = "Rôles", value = NumberOfRole, inline = True)
	embed.add_field(name = "Région", value = RegionServer, inline = True)
	embed.add_field(name = "Salons", value = NumbersOfSalons, inline = True)
	embed.add_field(name = "Création du serveur", value = serverCreation, inline = False)
	embed.add_field(name = "Liste des emojis", value = EmojiList, inline = False) 
	embed.set_footer(icon_url =ctx.bot.user.avatar_url,text = bot.user.name)
	await ctx.send(embed = embed)



@bot.command(name= "SendEmbed",aliases=["embed"])
@commands.has_permissions(manage_messages = True)
async def embed(ctx,title, *,texte : str):
	embed= discord.Embed(title = title,description = "",color = ctx.author.color)
	embed.set_author(name =(f"{ctx.author.name}"), icon_url =ctx.author.avatar_url )
	embed.set_thumbnail(url = "")
	embed.add_field(name =("** **"),value = (f"{texte}"),inline = True)
	embed.set_footer(icon_url = ctx.guild.icon_url, text = bot.user.name)
	await ctx.send(embed = embed)



@bot.command(name = "Kickaccount",aliases = ["kick","k","KICK"])
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.User, *,reason = "Aucune"):
	await ctx.guild.kick(user, reason = reason)
	embed = discord.Embed(title = "**Kick**", description = "Un modérateur a expulsé un membre !",color =0xF0FF7A )
	embed.set_author(name = bot.user.name)
	embed.set_thumbnail(url = "https://www.wallpaperflare.com/static/263/716/31/uchiha-itachi-sharingan-eternal-mangekyou-sharingan-naruto-shippuuden-wallpaper.jpg")
	embed.add_field(name="Membre kick",value= user.name, inline =False)
	embed.add_field(name ="Raison", value = reason, inline = True)
	embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
	await ctx.send(embed = embed)


@bot.command(name = 'banaccount',aliases = ["ban","BAN"])
@commands.has_permissions(ban_members = True)
async def ban(ctx,user : discord.User, *,reason = "Aucune" ):
	await ctx.guild.ban(user, reason = reason)
	embed = discord.Embed(title = "**Bannissement**", description = "Un modérateur a frappé !",color =0xB20101 )
	embed.set_author(name = bot.user.name)
	embed.set_thumbnail(url = "https://emoji.gg/assets/emoji/6623_banhammer.png")
	embed.add_field(name="Membre banni",value= user.name, inline =False)
	embed.add_field(name ="Raison", value = reason, inline = True)
	embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)

	await ctx.send(embed = embed)


@bot.command(name = "unbanaccount", aliases=["unban","UNBAN"])
@commands.has_permissions(administrator = True)
async def unban(ctx,user , *,reason = "Aucune"):
	UserName, UserId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == UserName and i.user.discriminator == UserId:
			await ctx.guild.unban(i.user, reason = reason)
			await ctx.send(f"{user} à été unban.")
			return
	#Ici on sait que l'utilisateur n'est pas trouvé
	await ctx.send(f"L'utilisateur {user} n'est pas banni.")

async def createMutedRole(ctx):
	mutedRole = await ctx.guild.create_role(name="Muted",permissions=discord.Permissions(send_messages =False,speak = False))
	for channel in ctx.guild.channels:
		await channel.set_permissions(mutedRole, send_messages=False,speak=False)
	return mutedRole

async def getMutedRole(ctx):
	roles = ctx.guild.roles
	for role in roles:
		if role.id==807309589715484712:
			return role
	return await createMutedRole(ctx)

@bot.command(name = "mute",aliases=["MUTE"])
@commands.has_permissions(administrator = True)
async def mute(ctx,member : discord.Member,*, reason = "Aucune"):
	mutedRole= await getMutedRole(ctx)
	await member.add_roles(mutedRole,reason = reason)
	await ctx.send(f"{member.mention} est silencieux.")


@bot.command(name = "unmute",aliases =["UNMUTE"])
@commands.has_permissions(administrator = True)
async def unmute(ctx,member : discord.Member,*,reason = "Aucune"):
	mutedRole=await getMutedRole(ctx)
	await member.remove_roles(mutedRole, reason = reason)
	await ctx.send(f"{member.mention} peut parler à nouveau !")



@bot.command(name = "ChangeDelayStatus", aliases = ["DelayStatus","delaystatus"])
@commands.has_permissions(administrator = True)
async def ChangeDelay(ctx, secondes = 30):
	Change_status.change_interval(seconds = secondes)
	await ctx.send(f"Le status du bot sera mis à jour toutes les {secondes} secondes.")


@bot.command(name = "RandomChoice",aliases = ["choix","choice"])
@commands.has_permissions(send_messages = True)
async def chose(ctx,*,choix):
	choix1,choix2 = choix.split("|")
	choix_final = [choix1,choix2]
	rancoin = random.choice(choix_final)
	embed = discord.Embed(title = ("Choix aléatoire"), description = (f"J'ai choisi parmis ces deux possibilités : **{choix1}**  et  **{choix2}**"),color =0xFFB90F )
	embed.add_field(name="Mon choix",value= rancoin, inline =False)
	await ctx.send(embed= embed)

@bot.command(name = "shifumi",aliases = ["pfc"])
async def shifumi(ctx, symbole):
	Possibilites = ["Pierre","Feuille","Ciseaux"]
	symbole = symbole.capitalize()
	symbole_bot = random.choice(Possibilites)
	try:
		assert symbole in Possibilites
		if symbole == Possibilites[0] and symbole_bot == Possibilites[0]:
			vainqueur = "Egalité"
			symbole ="🤜"
			symbole_bot = "🤜"
		elif symbole == Possibilites[0] and symbole_bot == Possibilites[1]:
			vainqueur = "Tu as perdu !"
			symbole ="🤜"
			symbole_bot = "✋"
		elif symbole == Possibilites[0] and symbole_bot == Possibilites[2]:
			vainqueur = "Tu as gagné !"
			symbole ="🤜"
			symbole_bot = "✌️"
		elif symbole == Possibilites[1] and symbole_bot == Possibilites[0]:
			vainqueur = "Tu as gagné !"
			symbole_bot = "🤜"
			symbole = "✋"
		elif symbole == Possibilites[1] and symbole_bot == Possibilites[1]:
			vainqueur = "Egalité"
			symbole_bot = "✋"
			symbole = "✋"
		elif symbole == Possibilites[1] and symbole_bot == Possibilites[2]:
			vainqueur = "Tu as perdu !"
			symbole = "✋"
			symbole_bot = "✌️"
		elif symbole == Possibilites[2] and symbole_bot == Possibilites[0]:
			vainqueur = "Tu as perdu !"
			symbole_bot = "🤜"
			symbole = "✌️"
		elif symbole == Possibilites[2] and symbole_bot == Possibilites[1]:
			vainqueur = "Tu as gagné !"
			symbole_bot = "✋"
			symbole = "✌️"
		elif symbole == Possibilites[2] and symbole_bot == Possibilites[2]:
			vainqueur = "Egalité"
			symbole = "✌️"
			symbole_bot = "✌️"
	except:
		await ctx.send("Le choix n'est pas valable. **Ex : =shifumi Pierre ou Feuille ou Ciseaux**.")
	embed = discord.Embed(title ="" , description = "",color =0xB20101 )
	embed.set_author(name ="")
	embed.set_thumbnail(url = "")
	embed.add_field(name =(f"{ctx.message.author.name}"), value = symbole, inline = True)
	embed.add_field(name =(f"VS"), value = ":zap:", inline = True)
	embed.add_field(name =(f"{bot.user.name}"), value = symbole_bot, inline = True)
	embed.add_field(name ="Résultat", value = vainqueur, inline = False)
	embed.set_footer(icon_url = ctx.guild.icon_url, text = bot.user.name)
	await ctx.send(embed = embed)
	
@bot.command(name = "ProfilPicture", aliases = ["pp"])
@commands.has_permissions(send_messages = True)
async def pp(ctx, user : discord.User):
	await ctx.send(f"👥 **{ctx.message.author.name}**, voici la photo de profil de **__{user}__** : {user.avatar_url}")
	
	
	
@bot.command(name = "PrivateMessage", aliases = ["messageprive","dm","mp"])
@commands.has_permissions(administrator = True)
async def dm(ctx,user : discord.Member,*,message):
	try:
		target = user
		await target.send(message)

		await ctx.channel.send("' " + message + " ' à été envoyé à " + target.name)

	except:
		await ctx.channel.send("Je ne peux pas mp cet utilisateur.") 


@bot.command(name = "Dmall")
@commands.has_permissions(administrator = True)
async def alldm(ctx,*, args =None):
	if args != None:
		members = ctx.guild.members
		for member in members:
			try:
				await member.send(args)
				print("'" + args + "' sent to" + member.name)

			except:
				print("peut pas envoyé " + args + "'à" + member.name)

	else:
		await ctx.channel.send("pas d'argument")
	
@bot.command(name = "TicTacToe",aliases = ["morpion","ttt"])
@commands.has_permissions(send_messages = True)
async def TicTacToe(ctx, p1: discord.Member, p2: discord.Member):
	global count
	global player1
	global player2
	global turn
	global gameOver

	if gameOver:
		global board
		board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
		":white_large_square:", ":white_large_square:", ":white_large_square:",
		":white_large_square:", ":white_large_square:", ":white_large_square:"]
		turn = ""
		gameOver = False
		count = 0
		
		player1 = p1
		player2 = p2
		
		# print the board
		line = ""
		for x in range(len(board)):
			if x == 2 or x == 5 or x == 8:
				line += " " + board[x]
				await ctx.send(line)
				line = ""
			else:
				line += " " + board[x]

		# determine who goes first
		num = random.randint(1, 2)
		if num == 1:
			turn = player1
			await ctx.send(f"{player1} c'est ton tour.")
		elif num == 2:
			turn = player2
			await ctx.send(f"{player2} c'est ton tour.")
	else:
		await ctx.send("Une partie est déjà en cours.")


@bot.command(name = "place",aliases = ["pos","position"])
async def place(ctx,pos : int):
	global turn
	global player1
	global player2
	global board
	global count

	if not gameOver:
		mark = "" 
		if turn == ctx.author:
			if turn == player1:
				mark = "❌"
			elif turn == player2:
				mark = "⚪"
			if 0<pos<10 and board[pos - 1] == ":white_large_square:":
				board[pos - 1] = mark
				count +=1
				#print board 
				line = ""
				for i in range(len(board)):
					if i == 2 or i== 5 or i == 8:
						line+= " " + board[i]
						await ctx.send(line)
						line = ""
					else:
						line+=" " + board[i]

				checkWinner(winningConditions,mark)
				if gameOver:
					await ctx.send(mark + " win !")
				elif count >= 9 :
					await ctx.send("égalité !")

				else:
					#witch turn 
					if turn == player1:
						turn = player2
						await ctx.send(f"Au tour de {player2}")
					
					elif turn == player2:
						turn = player1
						await ctx.send(f"Au tour de {player1}")
					
			else:
				await ctx.send("Veuillez choisir un nombre entre 1 et 9 et assurez vous de choisir une case vide.")
		else:
			await ctx.send("Ce n'est pas votre tour.")
	else:
		await ctx.send("Veuillez démarrer une partie avec la commande : ```+morpion [player1] [player2]```")

@bot.command(name = "MorpionStop",aliases = ["mstop"])
@commands.has_permissions(manage_messages = True)
async def StopMorpion(ctx):
	global gameOver
	gameOver = True
	await ctx.send("La partie à été interrompue.")


def checkWinner(winningConditions, mark):
	global gameOver
	for condition in winningConditions:
		if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
			gameOver = True


@TicTacToe.error
async def TicTacToeError(ctx,error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Pour démarrer une partie veuillez préciser le deuxieme joueur.")
	if isinstance(error, commands.BadArgument):
		await ctx.send("Nom du joueur incorrect ! Indiquez l'identifiant du deuxieme joueur ou le mentionner.")

@chose.error
async def chose_error(ctx,error):
	if isinstance(error,commands.MissingRequiredArgument):
		await ctx.send("Cette commande prend en argument les deux choix séparés d'un **|** ! \n \n Ex : =RandomChoice Nico Robin / Nami .")

@chinese.error
async def chinese_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Cette commande prend en argument le texte à traduire.")

@pp.error
async def pp_error(ctx,error):
	if isinstance(error,commands.MissingRequiredArgument):
		await ctx.send((f"👥 **{ctx.message.author.name}**, voici votre photo de profil : {ctx.message.author.avatar_url}"))

@dm.error
async def dm_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Cette commande prend en argument l'identifiant de chaque membre à contacter et le texte à envoyer.")

bot.run("NzgyMzAyNzAwODU0NzA2MjI3.X8KOKg.rsGojV2Amgbz23pWyw5QlDId6Ho")

