from marvinbot.net import fetch_from_telegram
from marvinbot.utils import get_message
from marvinbot_sample_plugin.models import WitnessedUser
import telegram
import logging

log = logging.getLogger(__name__)


def witness_command(update, *args):
    adapter = witness_command.plugin.adapter
    message = get_message(update)
    user_data = message.from_user

    log.info('Witnessing user: %s', user_data.id)

    user = WitnessedUser.by_id(user_data.id)
    if not user:
        user = WitnessedUser(id=user_data.id, first_name=user_data.first_name,
                             last_name=user_data.last_name, username=user_data.last_name)
        user.save()
        adapter.bot.sendMessage(chat_id=update.message.chat_id, text="To Valhalla! (created)")
    else:
        adapter.bot.sendMessage(chat_id=update.message.chat_id, text="Mediocre! (already existed)")


def start_command(update, *args, **kwargs):
    adapter = start_command.plugin.adapter
    log.info('Start command caught')
    words = kwargs.get('words')
    prefix = kwargs.get('prefix')
    adapter.bot.sendMessage(chat_id=update.message.chat_id,
                            text="{prefix}I'm a bot, please talk to me!: {words}".format(words=words, prefix=prefix))


def bowdown(update, *args):
    update.message.reply_text('Yes, master **bows**')


def gaze_at_pic(update):
    # So the user sees we are doing something
    adapter = gaze_at_pic.plugin.adapter
    adapter.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)

    def photo_responder(filename):
        log.info('File {} finished downloading, notifying user'.format(filename))
        update.message.reply_text('Nice pic, bro: {}'.format(filename))

    filename, async = fetch_from_telegram(adapter, update.message.photo[-1].file_id,
                                          on_done=photo_responder)


def salutation_initiative(update):
    update.message.reply_text("'zup")
