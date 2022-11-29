import discord

from Mysql import *
from Log import Log

class Bot:

    client = None
    connection = None

    @staticmethod
    def init(client):
        Bot.client = client
        logins = open('../database-login.txt', 'r').readlines()[0].split(';')
        Bot.connection = create_connection(logins[0], logins[1], logins[2], logins[3])
        if Bot.connection is None:
            Log.print("Connection failed")
            raise Exception("Connection failed")
    
    @staticmethod
    def store_message(message: discord.Message):
        #All messages will be stored in a database.
        username = message.author.name
        usertag = message.author.discriminator
        servername = message.guild.name
        channelname = message.channel.name
        content = message.content

        query = f"INSERT INTO messages (username, usertag, servername, channelname, content) VALUES ('{username}', '{usertag}', '{servername}', '{channelname}', '{content}')"
        execute_query(Bot.connection, query)
    
    @staticmethod
    def get_most_active_user(servername):
        query = f"SELECT username, usertag, COUNT(*) AS count FROM messages WHERE servername = '{servername}' GROUP BY username, usertag ORDER BY count DESC LIMIT 10"
        return execute_read_query(Bot.connection, query)