"""
This module contains the functions to send the daily puzzle
"""

import random
from datetime import datetime, timedelta
import asyncio


def time_to_wait(hour:int, minute:int) -> float:
    """Checking the time the programm needs to sleep before sending again a puzzle"""
    now = datetime.now()
    target_time = datetime(now.year, now.month, now.day, hour, minute, 0)

    if now <= target_time:
        dt = target_time - now
    else:
        dt = target_time - now + timedelta(days=1)

    return dt.total_seconds()


def log(time_stamp:datetime, debug_message:str) -> None:
    """ Writting in file what the bot does to debug easier"""
    with open('log.txt', 'w', encoding='utf-8') as debug:
        debug.write("Puzzle envoye a : " + str(time_stamp))
        debug.write("   |   ")
        debug.write(debug_message)


def check_id_already_sent(message) -> bool:
    """check if puzzle has reaction "✅" """
    for reaction in message.reactions:
        if reaction.emoji == '✅':
            return True
    return False


async def sending_puzzle(client, channels_in, channel_out, sending_hour, sending_minute) -> None:
    """ Envoyer le puzzle tous les jours à la même heure"""
    while True:
        # Defining the time to wait before sending it
        wait_time = time_to_wait(sending_hour, sending_minute)
        await asyncio.sleep(wait_time)

        # Finding the puzzle to send
        random_channels = list(channels_in.items())
        random.shuffle(random_channels)
        for channel_name, channel_id in random_channels:
            channel = client.get_channel(channel_id)
            async for message in channel.history(oldest_first=True):
                if not check_id_already_sent(message):
                    destination = client.get_channel(channel_out)
                    # send the puzzle
                    await destination.send("**                          __Today's puzzle !__**")
                    await destination.send(message.attachments[0].url)
                    await destination.send(f"hint: ||{channel_name}||")

                    # react to the message
                    await message.add_reaction("✅")

                    # Log the sending
                    debug_message = f"[MESSAGE SENT]\t \
                        Wait time : {wait_time} \
                        | theme : {channel_name} \
                        | source message : {message.id}"
                    log(datetime.now(), debug_message)
                    return
