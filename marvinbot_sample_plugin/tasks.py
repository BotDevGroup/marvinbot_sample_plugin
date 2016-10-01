from marvinbot.core import get_adapter
from marvinbot.utils import get_message
from marvinbot.handlers import Filters, CommandHandler, MessageHandler
from celery.utils.log import get_task_logger
from celery import task
from marvinbot_sample_plugin.models import WitnessedUser

log = get_task_logger(__name__)
adapter = get_adapter()


@task
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


@task()
def start_command(update, *args):
    log.info('Start command caught')
    adapter.bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!: {}".format(args))


@task()
def bowdown(update, *args):
    update.message.reply_text('Yes, master **bows**')


@task()
def gaze_at_pic(update):
    update.message.reply_text('Nice pic, bro')


@task()
def salutation_initiative(update):
    update.message.reply_text("'zup")


adapter.add_handler(CommandHandler('witness', witness_command, call_async=True))
adapter.add_handler(CommandHandler('start', start_command, call_async=True))
adapter.add_handler(MessageHandler(Filters.photo, gaze_at_pic))
adapter.add_handler(MessageHandler([Filters.text, lambda msg: msg.text.lower() in ['hola', 'hi', 'klk', 'hey']],
                                   salutation_initiative,
                                   strict=True))
