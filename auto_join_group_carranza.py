from telethon import TelegramClient, events
from telethon.tl.functions.messages import ImportChatInviteRequest
import re
from dotenv import load_dotenv
import os
import time
import logging

load_dotenv()

# VARIABLES
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE')
username=os.getenv('USERNAME')
#group_link corresponds to the link of the group you want scrap/scan (i.e carranza group)
group_link=os.getenv('GROUP_LINK')

# Configure the logging settings
logging.basicConfig(filename='telegram_scraper.log', level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')


client = TelegramClient(username, api_id, api_hash)

async def main():
    try:
        await client.start(phone=phone_number)

        channel_to_scan = await client.get_entity(group_link)

        @client.on(events.NewMessage(chats=channel_to_scan))
        async def handle_new_message(event):
            # check if the message contains a link
            if event.text:
                start_time = time.time()

                # regex to find the "group code" i.e the second part of the link
                match = re.search(r'https://t\.me/\+([A-Za-z0-9_]+)', event.text)
                if match:
                    group_code = match.group(1)
                    try:
                        await client(ImportChatInviteRequest(group_code))
                    except Exception as e:
                        error_message = f'Error: {str(e)}'
                        logging.error(error_message)
                    
                    group_url = f'https://t.me/+{group_code}'
                    logging.info(f'Found a group link: {group_code}')
                    logging.info(f'Found a group link "{group_url}"')
                end_time = time.time()
                print(f"delay : {end_time - start_time}")

        await client.run_until_disconnected()
    except Exception as e:
        error_message = f'An unexpected error occurred: {str(e)}'
        logging.error(error_message)

if __name__ == '__main__':
    client.loop.run_until_complete(main())