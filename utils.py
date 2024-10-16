import datetime
import random
import re
from typing import List, Optional

import nextcord

popular_words = open("dict-popular.txt").read().splitlines()
all_words = set(word.strip() for word in open("dict-sowpods.txt"))

EMOJI_CODES = {
    "green": {
        "a": "<:1f1e6:938280353527906325>",
        "b": "<:1f1e7:938280353515315242>",
        "c": "<:1f1e8:938280353850875928>",
        "d": "<:1f1e9:938280353657929799>",
        "e": "<:1f1ea:938280354064785478>",
        "f": "<:1f1eb:938280353838276609>",
        "g": "<:1f1ec:938280353968291860>",
        "h": "<:1f1ed:938280353871839232>",
        "i": "<:1f1ee:938280354010239016>",
        "j": "<:1f1ef:938280353876021328>",
        "k": "<:1f1f0:938280354148675614>",
        "l": "<:1f1f1:938280353611780107>",
        "m": "<:1f1f2:938280353783775244>",
        "n": "<:1f1f3:938280353670504489>",
        "o": "<:1f1f4:938280354018656316>",
        "p": "<:1f1f5:938280353884414012>",
        "q": "<:1f1f6:938280354253537321>",
        "r": "<:1f1f7:938280354022850561>",
        "s": "<:1f1f8:938280354089947146>",
        "t": "<:1f1f9:938280353691476010>",
        "u": "<:1f1fa:938280353968304138>",
        "v": "<:1f1fb:938280353976696882>",
        "w": "<:1f1fc:938280353502752850>",
        "x": "<:1f1fd:938280354043789382>",
        "y": "<:1f1fe:938280840796995638>",
        "z": "<:1f1ff:938280841199616000>",
    },
    "yellow": {
        "a": "<:1f1e6:938280773906227230>",
        "b": "<:1f1e7:938280773910409256>",
        "c": "<:1f1e8:938280774057197639>",
        "d": "<:1f1e9:938280773918806066>",
        "e": "<:1f1ea:938280776057905152>",
        "f": "<:1f1eb:938280773977505832>",
        "g": "<:1f1ec:938280774006878208>",
        "h": "<:1f1ed:938280773910429726>",
        "i": "<:1f1ee:938280773998481418>",
        "j": "<:1f1ef:938280773910397028>",
        "k": "<:1f1f0:938280774120132628>",
        "l": "<:1f1f1:938280774011080715>",
        "m": "<:1f1f2:938280773922992138>",
        "n": "<:1f1f3:938280774002688010>",
        "o": "<:1f1f4:938280774065610822>",
        "p": "<:1f1f5:938280774019465286>",
        "q": "<:1f1f6:938280773881057392>",
        "r": "<:1f1f7:938280773994303568>",
        "s": "<:1f1f8:938280774191415357>",
        "t": "<:1f1f9:938280774023647233>",
        "u": "<:1f1fa:938280774002679858>",
        "v": "<:1f1fb:938280773910396979>",
        "w": "<:1f1fc:938280774006898749>",
        "x": "<:1f1fd:938280774065618984>",
        "y": "<:1f1fe:938280774115934228>",
        "z": "<:1f1ff:938280774145310801>",
    },
    "gray": {
        "a": "<:1f1e6:938280277627785347>",
        "b": "<:1f1e7:938280277703278593>",
        "c": "<:1f1e8:938280277988503633>",
        "d": "<:1f1e9:938280278026231858>",
        "e": "<:1f1ea:938280278038818926>",
        "f": "<:1f1eb:938280277862658059>",
        "g": "<:1f1ec:938280278051405844>",
        "h": "<:1f1ed:938280278126891058>",
        "i": "<:1f1ee:938280277980119120>",
        "j": "<:1f1ef:938280277988507649>",
        "k": "<:1f1f0:938280277900394537>",
        "l": "<:1f1f1:938280277862674503>",
        "m": "<:1f1f2:938280277678100501>",
        "n": "<:1f1f3:938280277866860555>",
        "o": "<:1f1f4:938280278189801502>",
        "p": "<:1f1f5:938280278017867776>",
        "q": "<:1f1f6:938280278097530941>",
        "r": "<:1f1f7:938280278038806538>",
        "s": "<:1f1f8:938280278110138468>",
        "t": "<:1f1f9:938280278055583764>",
        "u": "<:1f1fa:938280278043004958>",
        "v": "<:1f1fb:938280278051418153>",
        "w": "<:1f1fc:938280278131085332>",
        "x": "<:1f1fd:938280278105944074>",
        "y": "<:1f1fe:938280278177218560>",
        "z": "<:1f1ff:938280278215000064>",
    },
}


def generate_colored_word(guess: str, answer: str) -> str:
    """
    builds a string of emoji codes where each letter is
    colored based on the key:

    - same letter, same place: green
    - same letter, different place: yellow
    - different letter: gray

    args:
        word (str): the word to be colored
        answer (str): the answer to the word

    returns:
        str: a string of emoji codes
    """
    colored_word = [EMOJI_CODES["gray"][letter] for letter in guess]
    guess_letters: List[Optional[str]] = list(guess)
    answer_letters: List[Optional[str]] = list(answer)
    # change colors to green if same letter and same place
    for i in range(len(guess_letters)):
        if guess_letters[i] == answer_letters[i]:
            colored_word[i] = EMOJI_CODES["green"][guess_letters[i]]
            answer_letters[i] = None
            guess_letters[i] = None
    # change colors to yellow if same letter and not the same place
    for i in range(len(guess_letters)):
        if guess_letters[i] is not None and guess_letters[i] in answer_letters:
            colored_word[i] = EMOJI_CODES["yellow"][guess_letters[i]]
            answer_letters[answer_letters.index(guess_letters[i])] = None
    return "".join(colored_word)


def generate_blanks() -> str:
    """
    generate a string of 5 blank white square emoji characters

    returns:
        str: a string of white square emojis
    """
    return "\N{WHITE MEDIUM SQUARE}" * 5


def generate_puzzle_embed(user: nextcord.User, puzzle_id: int) -> nextcord.Embed:
    """
    generate an embed for a new puzzle given the puzzle id and user

    args:
        user (nextcord.User): The user who submitted the puzzle
        puzzle_id (int): The puzzle ID

    returns:
        nextcord.Embed: The embed to be sent
    """
    embed = nextcord.Embed(title="Wordle Clone")
    embed.description = "\n".join([generate_blanks()] * 6)
    embed.set_author(name=user.name, icon_url=user.display_avatar.url)
    embed.set_footer(
        text=f"ID: {puzzle_id} ︱ to play, use the command /play!\n"
        "to guess, reply to this message with a word."
    )
    return embed


def update_embed(embed: nextcord.Embed, guess: str) -> nextcord.Embed:
    """
    updates the embed with the new guesses

    args:
        embed (nextcord.Embed): the embed to be updated
        puzzle_id (int): the puzzle ID
        guess (str): the guess made by the user

    returns:
        nextcord.Embed: The updated embed
    """
    puzzle_id = int(embed.footer.text.split()[1])
    answer = popular_words[puzzle_id]
    colored_word = generate_colored_word(guess, answer)
    empty_slot = generate_blanks()
    # replace the first blank with the colored word
    embed.description = embed.description.replace(empty_slot, colored_word, 1)
    # check for game over
    num_empty_slots = embed.description.count(empty_slot)
    if guess == answer:
        if num_empty_slots == 0:
            embed.description += "\n\nphew!"
        if num_empty_slots == 1:
            embed.description += "\n\ngreat!"
        if num_empty_slots == 2:
            embed.description += "\n\nsplendid!"
        if num_empty_slots == 3:
            embed.description += "\n\nimpressive!"
        if num_empty_slots == 4:
            embed.description += "\n\nmagnificent!"
        if num_empty_slots == 5:
            embed.description += "\n\ngenius!"
    elif num_empty_slots == 0:
        embed.description += f"\n\nthe answer was {answer}!"
    return embed


def is_valid_word(word: str) -> bool:
    """
    validates a word

    args:
        word (str): the word to validate

    returns:
        bool: whether the word is valid
    """
    return word in all_words


def random_puzzle_id() -> int:
    """
    generates a random puzzle id

    returns:
        int: a random puzzle id
    """
    return random.randint(0, len(popular_words) - 1)


def daily_puzzle_id() -> int:
    """
    calculates the puzzle id for the daily puzzle

    returns:
        int: the puzzle id for the daily puzzle
    """
    # calculate days since 1/1/2022 and mod by the number of puzzles
    num_words = len(popular_words)
    time_diff = datetime.datetime.now().date() - datetime.date(2022, 1, 1)
    return time_diff.days % num_words


def is_game_over(embed: nextcord.Embed) -> bool:
    """
    checks if the game is over in the embed

    args:
        embed (nextcord.Embed): The embed to check

    returns:
        bool: Whether the game is over
    """
    return "\n\n" in embed.description


def generate_info_embed() -> nextcord.Embed:
    """
    generates an embed with information about the bot

    returns:
        nextcord.Embed: The embed to be sent
    """
    join_url = "https://discord.com/api/oauth2/authorize?client_id=938502854921027584&permissions=11264&scope=bot%20applications.commands"
    discord_url = "https://discord.gg/fPrdqh3Zfu"
    youtube_url = "https://www.youtube.com/watch?v=0p_eQGKFY3I"
    github_url = "https://github.com/DenverCoder1/discord-wordle-clone"
    return nextcord.Embed(
        title="about discord wordle clone",
        description=(
            "discord wordle clone is a game of wordle-like puzzle solving.\n\n"
            "**You can start a game with**\n\n"
            ":sunny: `/play daily` - play the puzzle of the day\n"
            ":game_die: `/play random` - play a random puzzle\n"
            ":boxing_glove: `/play id <puzzle_id>` - play a puzzle by id\n\n"
            f"<:member_join:942985122846752798> [add this bot to your server]({join_url})\n"
            f"<:discord:942984508586725417> [join my discord server]({discord_url})\n"
            f"<:youtube:942984508976795669> [youtube tutorial on the making of this bot]({youtube_url})\n"
            f"<:github:942984509673066568> [view the source code on github]({github_url})\n"
        ),
    )


async def process_message_as_guess(bot: nextcord.Client, message: nextcord.Message) -> bool:
    """
    check if a new message is a reply to a wordle game.
    If so, validate the guess and update the bot's message.

    args:
        bot (nextcord.Client): the bot
        message (nextcord.Message): the new message to process

    Returns:
        bool: True if the message was processed as a guess, False otherwise
    """
    # get the message replied to
    ref = message.reference
    if not ref or not isinstance(ref.resolved, nextcord.Message):
        return False
    parent = ref.resolved

    # if the parent message is not the bot's message, ignore it
    if parent.author.id != bot.user.id:
        return False

    # check that the message has embeds
    if not parent.embeds:
        return False

    embed = parent.embeds[0]

    guess = message.content.lower()

    # check that the user is the one playing
    if (
        embed.author.name != message.author.name
        or embed.author.icon_url != message.author.display_avatar.url
    ):
        reply = "start a new game with /play"
        if embed.author:
            reply = f"this game was started by {embed.author.name}. " + reply
        await message.reply(reply, delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # check that the game is not over
    if is_game_over(embed):
        await message.reply("the game is already over. start a new game with /play", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # strip mentions from the guess
    guess = re.sub(r"<@!?\d+>", "", guess).strip()

    bot_name = message.guild.me.nick if message.guild and message.guild.me.nick else bot.user.name

    if len(guess) == 0:
        await message.reply(
            "i am unable to see what you are trying to guess.\n"
            "please try mentioning me in your reply before the word you want to guess.\n\n"
            f"**for example:**\n{bot.user.mention} crate\n\n"
            f"to bypass this restriction, you can start a game with `@\u200b{bot_name} play` instead of `/play`",
            delete_after=14,
        )
        try:
            await message.delete(delay=14)
        except Exception:
            pass
        return True

    # check that a single word is in the message
    if len(guess.split()) > 1:
        await message.reply("please respond with a single 5-letter word.", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # check that the word is valid
    if not is_valid_word(guess):
        await message.reply("that is not a valid word", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # update the embed
    embed = update_embed(embed, guess)
    await parent.edit(embed=embed)

    # attempt to delete the message
    try:
        await message.delete()
    except Exception:
        pass

    return True