import discord
from discord import utils
import config

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_raw_reaction_add(self, payload):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        try:
            emoji = str(payload.emoji)
            role_id = config.roles.get(emoji)

            if role_id is not None:
                role = utils.get(message.guild.roles, id=role_id)

                if role is not None:
                    member = await message.guild.fetch_member(payload.user_id)

                    if member is not None:
                        member_roles_ids = [r.id for r in member.roles]
                        if role.id not in member_roles_ids:
                            await member.add_roles(role)
                            print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))

                            # Send a welcome message
                            await channel.send(f'Привет, {member.mention}! Добро пожаловать на сервер. Ты получил роль {role.name}.')
                        else:
                            await message.remove_reaction(payload.emoji, member)
                            print('[INFO] Role already assigned, reaction removed.')
                    else:
                        print('[ERROR] Member is None, unable to find member with id:', payload.user_id)
                else:
                    print('[ERROR] Role is None, check your config.py for a valid role ID for emoji:', emoji)
            else:
                print('[ERROR] Role ID is None, check your config.py for a valid role ID for emoji:', emoji)

        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print('[ERROR] An error occurred: ' + repr(e))

    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        try:
            emoji = str(payload.emoji)
            role_id = config.roles.get(emoji)

            if role_id is not None:
                role = utils.get(message.guild.roles, id=role_id)

                if role is not None:
                    member = await message.guild.fetch_member(payload.user_id)

                    if member is not None:
                        await member.remove_roles(role)
                        print('[SUCCESS] Role {0.name} has been removed from user {1.display_name}'.format(role, member))
                    else:
                        print('[ERROR] Member is None, unable to find member with id:', payload.user_id)
                else:
                    print('[ERROR] Role is None, check your config.py for a valid role ID for emoji:', emoji)
            else:
                print('[ERROR] Role ID is None, check your config.py for a valid role ID for emoji:', emoji)

        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print('[ERROR] An error occurred: ' + repr(e))

    async def on_message(self, message):
        msg = input("введите сообщение: ")
        await message.channel.send(msg)

intents = discord.Intents.default()
intents.messages = True
client = MyClient(intents=intents)
client.run("MTE3Mjk1ODY1ODEzMzQ5NTg0OQ.GuoLiJ.U6GrjDdae1GDSRN04ZNRC_8m3Tgbqit8MmEj2c")