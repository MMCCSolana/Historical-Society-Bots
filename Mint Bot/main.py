import discord
import requests
import json
import re  # Import the regular expression module

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

client = discord.Client(intents=intents)

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n:,}{suffix}"  # Updated line

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Regular expression to match /mint followed by optional space and a number
    match = re.match(r'/mint ?(\d+)', message.content)

    if match:
        # Get the inscription number from the regular expression match
        inscription_number = match.group(1)

        # Load the JSON data
        with open('data.json') as f:
            data = json.load(f)

        # Find the entry with the matching inscription number
        for entry in data:
            if entry['sequence_number'] == f'SOL Inscription #{inscription_number}':
                token_address = entry['token_address']
                break
        else:
            await message.channel.send('Mint not found.')
            return

        # Fetch the image from the Magic Eden API
        response = requests.get(f'https://api-mainnet.magiceden.dev/v2/tokens/{token_address}')
        response_json = response.json()

        # Extract the image URL and NFT name
        image_url = response_json['image']
        nft_name = response_json['name']

        # Create the Solscan URL
        solscan_url = f'https://solscan.io/token/{token_address}'

        # Format the inscription number as an ordinal
        ordinal_inscription_number = ordinal(int(inscription_number))

        # Send the formatted message back to the user
        await message.channel.send(f'{nft_name} was the {ordinal_inscription_number} NFT minted on Solana\n{image_url}\n[Solscan Link]({solscan_url})')

# Run the bot
client.run('MTE1NzE1MDYyMTQ2ODcyMTMwMg.Gq0x6f.MTjbWv1vf154xmmMLO8ld8wAQGfyBFdBu5rb48')
