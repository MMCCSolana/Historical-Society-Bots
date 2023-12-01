import json
import discord
from discord.ext import commands
from difflib import get_close_matches, SequenceMatcher

# Load the JSON data
with open("unique_token_addresses.json", "r") as file:
    data = json.load(file)

# Bot setup
TOKEN = 'MTE1ODE2MTk1Njc3NjIwMjM0NA.GPcSWw.1AcGgT66_vGuuDbwwT51wpWdpI1hyex6y3GfDA'
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Ensure the bot can read message content

bot = commands.Bot(command_prefix='/', intents=intents)


def combined_fuzzy_search(query, data, top_n=5):
    """Return the top N matches for the given query combining name and number matching."""

    # Define a similarity function using SequenceMatcher
    def similarity(a, b):
        return SequenceMatcher(None, a, b).ratio()

    # Calculate similarity scores for each item in data
    scores = [(item, similarity(query.lower(), item['name'].lower())) for item in data]

    # Sort by similarity score in descending order and take top N
    sorted_matches = sorted(scores, key=lambda x: x[1], reverse=True)[:top_n]

    # Return the top N items
    return [match[0] for match in sorted_matches]


def number_to_ordinal(num):
    """Convert a number to its ordinal representation."""
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(num % 10, 'th')
    return f"{num}{suffix}"


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')


@bot.command()
async def get(ctx, *, query: str):
    """Search for the NFT sequence based on the name and number format."""
    top_matches = combined_fuzzy_search(query, data)
    if top_matches:
        response = "Here are the top matches:\n"
        for i, match in enumerate(top_matches, 1):
            ordinal_sequence = number_to_ordinal(int(match['sequence_number'].split()[-1].replace('#', '')))
            response += f"{i}. {match['name']} from {match['collection']} (This is the {ordinal_sequence} NFT minted on Solana)\n"
        await ctx.send(response)
    else:
        await ctx.send(f"No match found for {query}.")


bot.run(TOKEN)
