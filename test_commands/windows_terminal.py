from dragonfly import *
from srabuilder import rules

import urllib.parse
import time
import uuid
import os
import tempfile


def enter_command(cmd):
    Text(cmd).execute()
    Key("enter").execute()


directions = {"up": "up", "right": "right", "down": "down", "left": "left"}


basic = {
    # "new panel right": Text("python -m flask run") + Key("cs-d"),
    "duplicate tab": Key("cs-d"),
    "close tab": Key("cs-w"),
    "tab right": Key("c-tab"),
    "tab left": Key("cs-tab"),
    "new panel right": Key("as-plus"),
    "new panel down": Key("as-minus"),
    "close panel": Key("cs-w"),
    "focus <directions>": Key("a-%(directions)s"),
    # "focus right": Key('a-right'),
    # "focus down": Key('a-down'),
    # "focus left": Key('a-left'),
}

repeat = {
    "resize <directions>": Key("as-%(directions)s"),
}


def rule_builder():
    builder = rules.RuleBuilder()
    extras = [Choice("directions", directions)]
    defaults = {"n": 1}
    builder.basic.append(
        MappingRule(
            mapping=basic,
            extras=extras,
            exported=False,
            defaults=defaults,
            name="windows_terminal_basic",
        )
    )
    builder.repeat.append(
        MappingRule(
            mapping=repeat,
            extras=extras,
            exported=False,
            defaults=defaults,
            name="windows_terminal_repeat",
        )
    )
    return builder


# on_load() => extensions.register('terminal.wsl.py', wsl)
# is_active() => window.test('MINGW64') || window.test('evan@')

# paths := home='~' | (oh see h)='~/lp/och' | downloads='/c/users/fredere1/downloads' | projects='~/lp'

# unzip = 'unzip '