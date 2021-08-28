from pyrogram import Client, filters, emoji
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent)
import requests
bot = Client('url_bot',
        config_file='config.ini',
        parse_mode='html')
@bot.on_message(filters.command(['start','help']))
def start_command(client, message):
    greet_message = f"""
    hey {message.from_user.first_name} {emoji.SPARKLES} ,
    just send me a link {emoji.LINK}{emoji.LINK} and get the shortend url
    of the link {emoji.LINK}.
    """
    message.reply_text(greet_message)

@bot.on_message(filters.regex("https" or "http"))
def shortner(client, message):
    if "/alias" not in message.text:
        short_url = requests.get(f"https://tinyurl.com/api-create.php?url={message.text}")
        result = f"""
        long url {emoji.CHAINS}:
            {message.text }
        short url {emoji.LINK}:
            {short_url.text}
            """
        message.reply_text(result, disable_web_page_preview = True)
@bot.on_message(filters.command(['alias']))
def alias(client, message):
    url = message.reply_to_message.text
    print(url)
    splitted = message.text.split()
    re = requests.get(f"https://tinyurl.com/api-create.php?url={url}&alias={splitted[1]}")
    print(re.text)
    if re.text != 'Error':
        try:
            message.reply_text(re.text)
        except:
            message.reply_text("sorry the alias is not avilable")
    elif re.text == 'Error':
        message.reply_text("sorry the url is not avilable")
@bot.on_inline_query()
def answer(client, inline_query):
    link = requests.get(f"https://tinyurl.com/api-create.php?url={inline_query['query']}")
    if link.text != "Error":
        inline_query.answer(
            results = [
                InlineQueryResultArticle(
                    title = "shortned link",
                    input_message_content = InputTextMessageContent(link.text),
                description = link.text,
                thumb_url = "https://i.imgur.com/wMG9viI.png")],
            cache_time = 1

        )

bot.run()