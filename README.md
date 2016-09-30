# Marvinbot Sample Plugin
A basic plugin for marvinbot. Provides a single command named `/witness`,
which stores the username, id, firstname and last name of the user who calls
it in a database. Subsequent calls to the command signal that the user already
exists.

# Requirements

- A working [Marvinbot](https://github.com/BotDevGroup/marvin) install

# Getting Started

Download the source:

    $ git clone git@github.com:BotDevGroup/marvinbot_sample_plugin.git

Install the plugin into your virtualenv:

    (venv)$ python setup.py develop

Open your marvinbot `settings.json` and `marvinbot_sample_plugin` to your
`plugins` list.

Optionally, append some configuration:

    "marvinbot_sample_plugin": {
        "init_message": "O HAI"
    }

Restart your marvinbot and talk to your bot :)
