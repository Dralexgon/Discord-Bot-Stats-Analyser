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

        query = f"INSERT INTO messages (username, usertag, servername, channelname, content, timesamp) VALUES ('{username}', '{usertag}', '{servername}', '{channelname}', '{content}', '{message.created_at}')"
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
    
    @staticmethod
    def get_most_use_letter(servername):
        servername = injection_protection(servername)
        query = f"SELECT content FROM messages WHERE servername = '{servername}'"
        result = execute_read_query(Bot.connection, query)
        #remove sql injection protection and convert to lowercase
        for i in range(len(result)):
            result[i] = remove_injection_protection(result[i][0]).lower()
        #count letters
        letters = {}
        for message in result:
            for letter in message:
                if letter == ' ':
                    continue
                if letter in letters:
                    letters[letter] += 1
                else:
                    letters[letter] = 1
        #sort letters and keep it like a dict
        letters = dict(sorted(letters.items(), key=lambda item: item[1], reverse=True))
        #only keep the 10 most used letters
        letters = dict(list(letters.items())[:10])
        return letters