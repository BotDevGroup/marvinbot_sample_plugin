from marvinbot.utils import get_message
from marvinbot.handlers import Filters, CommandHandler, MessageHandler
from marvinbot_sample_plugin.models import WitnessedUser
import logging

log = logging.getLogger(__name__)
adapter = None


def witness_command(update, *args):
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
    log.info('Start command caught')
    words = kwargs.get('words')
    prefix = kwargs.get('prefix')
    adapter.bot.sendMessage(chat_id=update.message.chat_id,
                            text="{prefix}I'm a bot, please talk to me!: {words}".format(words=words, prefix=prefix))


def bowdown(update, *args):
    update.message.reply_text('Yes, master **bows**')


def gaze_at_pic(update):
    update.message.reply_text('Nice pic, bro')


def salutation_initiative(update):
    update.message.reply_text("'zup")


def setup(new_adapter):
    global adapter
    adapter = new_adapter

    adapter.add_handler(CommandHandler('witness', witness_command, command_description='Tell the bot to witness you'))
    adapter.add_handler(CommandHandler('start', start_command, command_description='Does nothing, but takes arguments')
                        .add_argument('--prefix', help='Prepend this to the reply', default='')
                        .add_argument('words', nargs='*', help='Words to put on the reply'))
    adapter.add_handler(MessageHandler(Filters.photo, gaze_at_pic))
    adapter.add_handler(MessageHandler([Filters.text, lambda msg: msg.text.lower() in ['hola', 'hi', 'klk', 'hey']],
                                       salutation_initiative,
                                       strict=True))
