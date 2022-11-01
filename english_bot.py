from bot_engine import get_query_url, get_bot_info, get_bot_updates
from bot_engine import bot_set_commands, bot_echo_polling, bot_send_sentences


def run_bot(debug=False):
    """If you want to run bot in debug mode
use debug=True
    """

    bot_url = get_query_url("BOT_TOKEN1")
    if debug:
        print(bot_url)
        print(get_bot_info(bot_url))
        print(get_bot_updates(bot_url))
        bot_echo_polling(bot_url, 5)
    else:
        bot_set_commands(bot_url)
        bot_send_sentences(bot_url, 2, True)
