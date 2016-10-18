from marvinbot_sample_plugin.tasks import (
    witness_command, start_command, gaze_at_pic, salutation_initiative
)
from marvinbot.handlers import CommonFilters, CommandHandler, MessageHandler
from marvinbot.signals import plugin_reload
from marvinbot.plugins import Plugin
from marvinbot.utils import localized_date
from datetime import timedelta

import logging

log = logging.getLogger(__name__)


class SamplePlugin(Plugin):
    def __init__(self):
        super(SamplePlugin, self).__init__('sample_plugin')

    def get_default_config(self):
        return {
            'short_name': self.name,
            'enabled': True,
            'init_message': 'Sample Initial Message :)'
        }

    def configure(self, config):
        log.info("Initializing Sample Plugin, a random message: {}".format(config.get('init_message', 'None :(')))

    def setup_handlers(self, adapter):
        # Subscribe to reload signal, but just for this plugin
        plugin_reload.connect(self.reload, sender=self)

        self.add_handler(CommandHandler('witness', witness_command, command_description='Tell the bot to witness you'))
        self.add_handler(CommandHandler('start', start_command, command_description='Does nothing, but takes arguments')
                         .add_argument('--prefix', help='Prepend this to the reply', default='')
                         .add_argument('words', nargs='*', help='Words to put on the reply'))
        self.add_handler(MessageHandler(CommonFilters.photo, gaze_at_pic))
        self.add_handler(MessageHandler([CommonFilters.text, lambda msg: msg.text.lower() in ['hola', 'hi', 'klk', 'hey']],
                                        salutation_initiative,
                                        strict=True))

        self.add_handler(CommandHandler('test', self.you_there,
                                        command_description="Sends back a simple response")
                         .add_argument('--foo', help='foo help')
                         .add_argument('--bar', help='bar help'), 0)

    def setup_schedules(self, adapter):
        # See: https://apscheduler.readthedocs.io/en/latest/modules/schedulers/base.html#apscheduler.schedulers.base.BaseScheduler.add_job
        # Give the job an explicit ID and tell it to replace existing, this avoids
        # scheduling the same thing several times, as the store is persistent.
        job = self.adapter.add_job(my_scheduled_func, 'interval', minutes=1,
                                   id='log something', name='some description',
                                   replace_existing=True)

        # Schedule cancelling the previous job
        self.adapter.add_job(cancel_my_scheduled_func, 'date', run_date=localized_date() + timedelta(minutes=5),
                             args=[job.id])

    def reload(self, sender, update):
        log.info("Reloading plugin: {}".format(str(sender)))
        if update:
            update.message.reply_text('Reloaded')

    def you_there(self, update, *args, **kwargs):
        log.info("Responding to you_there: args: %s, kwargs: %s", str(args), str(kwargs))
        update.message.reply_text('Me here 👀, are _you_? args:"{}", kwargs: "{}"'.format(str(args), str(kwargs)),
                                  parse_mode='Markdown')


def my_scheduled_func():
    log.info("my_scheduled_func running")


def cancel_my_scheduled_func(job_id):
    log.info("Cancelliny my_scheduled_func")
    adapter = cancel_my_scheduled_func.adapter
    adapter.remove_job(job_id)
