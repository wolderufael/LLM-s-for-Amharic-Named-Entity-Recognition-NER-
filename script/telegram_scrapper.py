from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv

# Load environment variables once
load_dotenv('.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')


class Scrapper:
    # Function to scrape data from a single channel
    async def scrape_channel(self,client, channel_username, writer, media_dir):
        entity = await client.get_entity(channel_username)
        channel_title = entity.title  # Extract the channel's title
        async for message in client.iter_messages(entity, limit=10000):
            media_path = None
            if message.media and hasattr(message.media, 'photo'):
                # Create a unique filename for the photo
                filename = f"{channel_username}_{message.id}.jpg"
                media_path = os.path.join(media_dir, filename)
                # Download the media to the specified directory if it's a photo
                await client.download_media(message.media, media_path)
            
            # Write the channel title along with other data
            writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path])

    async def main(self):
        # Initialize the client using async with
        async with TelegramClient('scraping_session', api_id, api_hash) as client:
            await client.start()

            # Create a directory for media files
            media_dir = 'data/photos'
            os.makedirs(media_dir, exist_ok=True)

            # Open the CSV file and prepare the writer
            with open('data/adamagebeya_telegram_data.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])  # Include channel title in the header

                # List of channels to scrape
                channels = [
                    '@gebeyaadama',  # Telegram channel
                ]

                # scrape data into the a CSV file
                for channel in channels:
                    await self.scrape_channel(client, channel, writer, media_dir)
                    print(f"Scraped data from {channel}")

