import discord.embeds
import interactions
from discord import app_commands
from discord.ext import commands

from discord import File
from easy_pil import Editor, load_image_async, Font
import asyncio 
from discord.ui import Button, button, View


#Variables
intents = discord.Intents.all()
intents.presences, intents.members, True, True
intents.guilds = True
user = discord.User
discord.Member = True
intents.members = True

client = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(client)

token = "Bot-Token"

client = interactions.Client(token=token)

client = commands.Bot(command_prefix="!", intents=intents)

get = discord.utils.get


@client.command(name="verificar")    #Comando para crear el Embed del boton de VERIFICAR con el prefijo ' ! '
async def verificar(ctx):
  await ctx.send(embed=discord.Embed(
	  title="Verificacion de usuario",
	  description=f"Presiona el boton para verificarte y ser parte de {ctx.guild.name}",
	  color=discord.Color.green()
  ), view=verificacion())

class verificacion(discord.ui.View):   #Creacion de interfaz de boton para verificacion
    @discord.ui.button(label="Verificar", style=discord.ButtonStyle.primary, emoji="📌")     
    async def button_callback(self:None, interaction:discord.Interaction, button):

     user = interaction.user  #Habilito interaccion del usuario
	    
     server = client.get_guild(1005204717128921119)  #Se obtiene el id del servidor
	    
     role = discord.utils.get(server.roles, name="Miembro")  #Se obtienen los roles del servidor
	    
     member = server.get_member(user.id)  #Se obtiene el id de usuario del servidor
	    
     await interaction.response.send_message(f"👤 Verificado correctamente!, Ya sos Miembro del servidor", ephemeral=True)   #Bot envia el mensaje


class CerrarBoton(View):   #Creo el boton para CERRAR el TICKET
  def __init__(self):
    super().__init__(timeout=None)
    
  @button(label="Cerrar ticket",
    style=discord.ButtonStyle.red, custom_id="cerrartiket", emoji="🔐")
  async def close(self, interaction: discord.Interaction, button: Button):
      await interaction.response.defer(ephemeral=True)
      await interaction.channel.send("El ticket se cerrara en 3 segundos, saludos!")
      await asyncio.sleep(3)
      category: discord.CategoryChannel  = discord.utils.get(interaction.guild.categories, id =1136832640683606026)
      rl: discord.role = interaction.guild.get_role(1136086840835846245)
      overwrites = {
      interaction.guild.default_role: discord.PermissionOverwrite(read_messages = False),
      rl: discord.PermissionOverwrite(read_messages = False, send_messages=True),
      interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
    }
      await interaction.channel.edit(category=category)
      await interaction.channel.send(embed=discord.Embed(
        description="Ticket cerrado",
        color= discord.Color.red()
      ),
      view=delete()
      )


class delete(View):  #Creo el boton para ELIMINAR el ticket
  def __init__(self):
    super().__init__(timeout=None)
    
  @button(label="Eliminar ticket",style=discord.ButtonStyle.blurple, emoji="🎫", custom_id="trash")
  async def trash(sefl, interaction: discord.Integration, button: Button):
   await interaction.response.defer()
   await interaction.channel.send("Se eliminara en 3 segundos")
   await asyncio.sleep(3)

   await interaction.channel.delete()


class CrearBoton(View):  #Creo el boton para CREAR el ticket
  def __init__(self):
    super().__init__(timeout=None)
    
  @button(label="Crear ticket",style=discord.ButtonStyle.blurple, emoji="🎫", custom_id="tickenopen")
  async def ticket(sefl, interaction: discord.Integration, button: Button):
    await interaction.response.defer(ephemeral=True)
    category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=1136793029345292348)
    for ch in category.text_channels:
      if ch.topic == f"{interaction.user.id}":
        await interaction.followup.send("Ya tenes un ticket pendiente en {0}".format(ch.mention), ephemeral=True)
        return
    rl: discord.role = interaction.guild.get_role(1136086840835846245)
    overwrites = {
      interaction.guild.default_role: discord.PermissionOverwrite(read_messages = False),
      rl: discord.PermissionOverwrite(read_messages = False, send_messages=True),
      interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
      interaction.guild.me: discord.PermissionOverwrite(read_messages = True, send_messages= True)
    }
    channel = await category.create_text_channel(
      name=str(interaction.user),
      topic=f"{interaction.user.id}",
      overwrites=overwrites
    )
    await channel.send(
      embed=discord.Embed(
      title="Ticket Creado!",
      description="🛎️Espera que un miembro del staff te atienda!",
      color=discord.Color.green()
      ),
      view = CerrarBoton()
    )
    if interaction.user.id:
       await interaction.followup.send(
      embed = discord.Embed(
      title="",
      description ="Tu ticket fue creado en {0}".format(channel.mention),
      color = discord.Color.dark_magenta()
      ),
      ephemeral=True)
       return


@client.command(name="ticket")   #Comando para crear el EMBED para la creacion del ticket con el prefijo ' ! '
@commands.has_permissions(administrator=True)
async def ticket(ctx):
  embed=discord.Embed(description="Hey! necesitas algun soporte o ayuda?. Crea un ticket ↓")
  embed.set_footer(text="ArcangelNetwork")
  await ctx.send(embed=embed, view = CrearBoton())


@client.event
async def on_ready():
   client.add_view(CrearBoton())
   client.add_view(CerrarBoton())
   client.add_view(delete())
   print("Bot listo")

#Se inicia el bot
client.run(token=token)
