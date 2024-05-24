import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# criei pra armazenar os canais gerados
generated_channels = {}

@bot.event
async def on_ready():
    print('Bot pronto!')

@bot.event
async def on_voice_state_update(member, before, after):
    
    specific_call_id = 1234567890987632134 # Substitua pelo ID da call
    if before.channel != after.channel:
        # Verifica se o usuário entrou na call específica
        if after.channel is not None and after.channel.id == specific_call_id:
            category_id = 1223969728771526751 # Substitua pelo ID da categoria
            guild = member.guild
            category = discord.utils.get(guild.categories, id=category_id)
            # Cria o canal de voz com o nome específico
            channel_name = f'📞{member.display_name} Call'
            channel = await category.create_voice_channel(channel_name)
            # Move o usuário para o novo canal
            await member.move_to(channel)
            # Define o canal para conexão do usuário
            await channel.set_permissions(member, connect=True, mute_members=True, move_members=True, manage_channels=True)
            # Armazena o canal gerado pelo bot para o membro
            generated_channels[member.id] = channel
        # Verifica se o usuário saiu da call
        if before.channel is not None and before.channel == generated_channels.get(member.id):
            # Verifica se o canal do usuário está vazio
            if len(before.channel.members) == 0:
                # Deleta o canal vazio
                await before.channel.delete()
                # Deleta a entrada do dicionário para liberar memória
                del generated_channels[member.id]

bot.run('substitua pelo seu token')
