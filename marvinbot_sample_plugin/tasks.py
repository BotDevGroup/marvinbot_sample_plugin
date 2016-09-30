from marvinbot.core import get_adapter
from marvinbot.utils import get_message
from marvinbot.handlers import CommandHandler
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

adapter.add_handler(CommandHandler('witness', witness_command, call_async=True))
