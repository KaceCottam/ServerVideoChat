import discord
import json

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

        commands = {'video': cmdVideo}

        async def parseCommand(self, command, args, message):
            if command not in self.commands:
                print('Bad command!')
            else:
                await self.cmdVideo(message)

        async def on_ready(self):
            print('Logged on as {0}!'.format(self.user))

        async def on_message(self, message):
            if message.content[0:len(config['prefix'])] == config['prefix']:
                print('Message from {0.author}: {0.content}'.format(message))
                commandContent = message.content[len( config['prefix']):].lower().split(' ')
                await self.parseCommand(command=commandContent[0], args=commandContent[1:], message=message)


client = MyClient()
with open('auth.json') as auth:
    client.run(json.load(auth)['token'])
