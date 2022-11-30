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
        #I use injection_protection() to prevent SQL injection.
        username = injection_protection(message.author.name)
        usertag = message.author.discriminator
        servername = injection_protection(message.guild.name)
        channelname = injection_protection(message.channel.name)
        content = injection_protection(message.content)

        query = f"INSERT INTO messages (username, usertag, servername, channelname, content) VALUES ('{username}', '{usertag}', '{servername}', '{channelname}', '{content}')"
        execute_query(Bot.connection, query)
    
    @staticmethod
    def get_most_active_user(servername):
        servername = injection_protection(servername)
        query = f"SELECT username, usertag, COUNT(*) FROM messages WHERE servername = '{servername}' GROUP BY username, usertag ORDER BY COUNT(*) DESC LIMIT 10"
        result = execute_read_query(Bot.connection, query)
        #remove sql injection protection
        for i in range(len(result)):
            result[i] = (remove_injection_protection(result[i][0]), result[i][1], result[i][2])
        return result