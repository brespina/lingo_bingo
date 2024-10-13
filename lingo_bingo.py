import random
from typing import List, Optional
import nextcord
from nextcord.ext import commands
# my token file
# from lingo_bingo_token import get_token
from your_token import get_token

# load words
with open("past_answers.txt", "r") as f:
    WORD_LIST = [word.strip().lower() for word in f.readlines() if len(word.strip()) == 5]

intents = nextcord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="w!", intents=intents)


class LingoBingoGame:
    def __init__(self, word: str):
        self.word = word
        self.attempts = []
        self.max_attempts = 6

    def guess(self, attempt: str) -> Optional[str]:
        if len(attempt) != len(self.word):
            return None

        result = []
        for i, letter in enumerate(attempt):
            if letter == self.word[i]:
                result.append("🟩")
            elif letter in self.word:
                result.append("🟨")
            else:
                result.append("⬛")

        self.attempts.append((attempt, "".join(result)))
        return "".join(result)

    def is_finished(self) -> bool:
        return len(self.attempts) == self.max_attempts or self.attempts[-1][1] == "🟩" * len(self.word)


def create_embed(user: nextcord.User, game: LingoBingoGame) -> nextcord.Embed:
    embed = nextcord.Embed(title="lingo bingo", description=f"attempt {len(game.attempts)}/{game.max_attempts}")
    embed.set_author(name=user.display_name, icon_url=user.avatar.url if user.avatar else None)
    for attempt, result in game.attempts:
        embed.add_field(name=attempt, value=result, inline=False)
    return embed


@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")


@bot.command(name="play")
async def play(ctx: commands.Context):
    word = random.choice(WORD_LIST)
    game = LingoBingoGame(word)
    embed = create_embed(ctx.author, game)
    await ctx.send(embed=embed)

    while not game.is_finished():
        try:
            guess_msg = await bot.wait_for(
                "message",
                check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                timeout=60.0
            )

            result = game.guess(guess_msg.content.lower())
            if result is None:
                await ctx.send(f"invalid guess. the word is {len(game.word)} letters long.")
            else:
                embed = create_embed(ctx.author, game)
                await ctx.send(embed=embed)

        except nextcord.errors.TimeoutError:
            await ctx.send("time's up! the word was: " + game.word)
            return

    if game.attempts[-1][1] == "🟩" * len(game.word):
        await ctx.send(f"congratulations! you guessed the word in {len(game.attempts)} attempts.")
    else:
        await ctx.send(f"game over! the word was: {game.word}")


if __name__ == "__main__":
    bot.run(get_token())
