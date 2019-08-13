import discord
import json
import os
from keep_alive import keep_alive

geckodriver = os.getcwd() + "/geckodriver"
os.system('chmod +x '+geckodriver)

with open('config.json') as config_json:
    config = json.load(config_json)
    
    class MyClient(discord.Client):

        async def cmdVideo(self, message):
            user = message.author.id
            voiceChannels = message.guild.voice_channels
            channelID = None
            channelName = None
            for channel in voiceChannels:
                for member in channel.members:
                    if user == member.id:
                        channelID = channel.id
                        channelName = channel.name
                        break
            guildID = message.guild.id

            if channelID and channelName:
                await message.channel.send(config['inviteMessage'].format(message, channelName, guildID, channelID))
            else:
                await message.channel.send(config['failedMessage'].format(message))
        
        async def cmdWatch(self, message):
            message.channel.send(config['watch2gether'].format(message,os.getenv('LINK')))

        commands = {'video': cmdVideo,
        'watch2gether': cmdWatch}

        async def parseCommand(self, command, args, message):
            if command not in self.commands:
                print('Bad command!')
            else:
                await self.commands[command](self,message)

        async def on_ready(self):
            await self.change_presence(activity=discord.Game(name=config['activityMessage']))
            print('Logged on as {0}!'.format(self.user))

        async def on_message(self, message):
            if message.content[0:len(config['prefix'])] == config['prefix']:
                print('Message from {0.author}: {0.content}'.format(message))
                commandContent = message.content[len( config['prefix']):].lower().split(' ')
                await self.parseCommand(command=commandContent[0], args=commandContent[1:], message=message)


client = MyClient()
keep_alive()
token=os.getenv('TOKEN')
client.run(token)
