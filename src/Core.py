import random
from datetime import datetime, timedelta
import json
import asyncio
from os import getenv


class Core():
    def __init__(self, client):
        self.client = client

        self.server = getenv("SERVER")
        
        with open(f'data/{self.server}_bot_info.json', "r") as f:
            temp = json.load(f)
            self.channels = temp["from_channel"]
            self.to_channel = temp["to_channel"]  
            self.sending_hour = temp["sending_time"][0]
            self.sending_minute = temp["sending_time"][1]
            del temp

    def time_to_wait(self, hour:int, minute:int) -> float:
        """Checking the time the programm needs to sleep before sending again a puzzle"""
        now = datetime.now()
        target_time = datetime(now.year, now.month, now.day, hour, minute, 0)

        if now <= target_time:
            dt = target_time - now
        else:
            dt = target_time - now + timedelta(days=1)
        
        return dt.total_seconds()
    

    def WritingForDebug(self, DATETIME:datetime, debug_message:str) -> None:
        """ Writting in file what the bot does to debug easier"""
        with open('log.txt', "w") as debug:
            debug.write("Puzzle envoye a : " + str(DATETIME))
            debug.write("   |   ")
            debug.write(debug_message)
    

    def CheckIdAlreadySent(self, message, channel) -> bool:
        """check if puzzle has reaction "✅" """
        for reaction in message.reactions:
            if reaction.emoji == "✅":
                return True
        return False
        
        
    def GetMessageID(self, message) -> None:
        parts = message.split()

        # Rechercher le morceau qui commence par "id="
        for part in parts:
            if part.startswith("id="):
                # Extrait l'ID en supprimant le "id="
                id_argument = part[3:]
                break

        print("L'ID est:", id_argument)
  

    async def sending_puzzle(self) -> None:
        """ Envoyer le puzzle tous les jours à la même heure"""
        while True:
            # Defining the time to wait before sending it
            wait_time = self.time_to_wait(self.sending_hour, self.sending_minute)
            await asyncio.sleep(wait_time)

            # Finding the puzzle to send
            random_channels = list(self.channels.items())
            random.shuffle(random_channels)
            for channel_name, channel_id in random_channels:
                channel = self.client.get_channel(channel_id)
                async for message in channel.history(oldest_first=True):
                    if not self.CheckIdAlreadySent(message, channel):
                        destination = self.client.get_channel(self.to_channel)
                        # send the puzzle
                        await destination.send("**                          __Today's puzzle !__**")
                        await destination.send(message.attachments[0].url)
                        await destination.send(f"hint: ||{channel_name}||")
            
                        # react to the message
                        await message.add_reaction("✅")

                        # Log the sending
                        debug_message = f"[MESSAGE SENT]\t Wait time : {wait_time} | theme : {channel_name} | source message : {message.id}"
                        self.WritingForDebug(datetime.now(), debug_message)
                        return
