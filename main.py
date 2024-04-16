import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.voice_states = True

# Substitua "TOKEN_DO_SEU_BOT" pelo token do seu bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Dicionário para armazenar os canais gerados pelo bot para cada membro
generated_channels = {}

@bot.event
async def on_ready():
    print('Bot pronto!')

@bot.event
async def on_voice_state_update(member, before, after):
    # Substitua "ID_DA_CALL_ESPECIFICA" pelo ID da call que deseja monitorar
    specific_call_id = 1223992067336704060
    if before.channel != after.channel:
        # Verifica se o usuário entrou na call específica
        if after.channel is not None and after.channel.id == specific_call_id:
            category_id = 1223969728771526751 # Substitua pelo ID da categoria
            guild = member.guild
            category = discord.utils.get(guild.categories, id=category_id)
            # Cria o canal de voz com o nome específico
            channel_name = f'📞Call de {member.display_name}'
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

# Substitua "TOKEN_DO_SEU_BOT" pelo token do seu bot
bot.run('MTIyOTc3MzIxODY0NzI0NDg1Mg.GcHN4x.Be7uiJkba3Ym7pLsU4dAg14_C52y8W0-MWtdj0')