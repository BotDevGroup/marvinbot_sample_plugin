import logging

log = logging.getLogger(__name__)


def configure(config):
    """Configure this module, given the config."""
    log.info("Initializing Sample Plugin, a random message: {}".format(config.get('init_message', 'None :(')))
