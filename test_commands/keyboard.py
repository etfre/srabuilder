# Low-level keyboard input module
#
# Based on the work done by the creators of the Dictation Toolbox
# https://github.com/dictation-toolbox/dragonfly-scripts
#
# and _multiedit-en.py found at:
# http://dragonfly-modules.googlecode.com/svn/trunk/command-modules/documentation/mod-_multiedit.html
#
# Modifications by: Tony Grosinger
#
# Licensed under LGPL

from dragonfly import *

try:
    from dragonfly.actions.keyboard import keyboard
    from dragonfly.actions.typeables import typeables

    if "semicolon" not in typeables:
        typeables["semicolon"] = keyboard.get_typeable(char=";")
except:
    pass

from srabuilder import rules


release = Key("shift:up, ctrl:up, alt:up")


# For repeating of characters.
specialCharMap = {
    "(pipe)": "|",
    "(dash)": "-",
    "period": ".",
    "comma": ",",
    "backslash": "\\",
    "downscore": "_",
    "asterisk": "*",
    "colon": ":",
    "(semicolon|semi colon)": ";",
    "at sign": "@",
    "[double] quote": '"',
    "single quote": "'",
    "number sign": "#",
    "dollar": "$",
    "percent": "%",
    "ampersand": "&",
    "slash": "/",
    "(equal|equals)": "=",
    "plus": "+",
    "space": " ",
    "bang": "!",
    "question": "?",
    "caret": "^",
    "north": "up",
    "south": "down",
    "west": "left",
    "east": "right",
    "page up": "pgup",
    "page down": "pgdown",
    "(home key|first)": "home",
    "(end key|final)": "end",
    "space": "space",
    "enter": "enter",
    "tab key": "tab",
}

# Modifiers for the press-command.
modifierMap = {
    "alt": "a",
    "angry": "a",
    "control": "c",
    "shift": "shift",
    "super": "w",
}

# Modifiers for the press-command, if only the modifier is pressed.
singleModifierMap = {
    "alt": "alt",
    "angry": "alt",
    "control": "ctrl",
    "shift": "shift",
    "super": "win",
}

letterMap = {
    "(alpha)": "a",
    "(bravo) ": "b",
    "(charlie) ": "c",
    "(danger) ": "d",
    "(eureka) ": "e",
    "(foxtrot) ": "f",
    "(gorilla) ": "g",
    "(hotel) ": "h",
    "(india) ": "i",
    "(juliet) ": "j",
    "(kilo) ": "k",
    "(lima) ": "l",
    "(michael) ": "m",
    "(november) ": "n",
    "(Oscar) ": "o",
    "(papa) ": "p",
    "(quiet) ": "q",
    "(romeo) ": "r",
    "(sierra) ": "s",
    "(tango) ": "t",
    "(uniform) ": "u",
    "(victor) ": "v",
    "(whiskey) ": "w",
    "(x-ray) ": "x",
    "(yankee) ": "y",
    "(zulu) ": "z",
}

# generate uppercase versions of every letter
upperLetterMap = {}
for letter in letterMap:
    upperLetterMap["upper " + letter] = letterMap[letter].upper()
letterMap.update(upperLetterMap)


grammarCfg = Config("multi edit")
grammarCfg.cmd = Section("Language section")
grammarCfg.cmd.map = Item(
    {
        # Navigation keys.
        "application key": release + Key("apps/3"),
        "win key": release + Key("win/3"),
        "copy that": release + Key("c-c"),
        "cut that": release + Key("c-x"),
        "paste that": release + Key("c-v"),
        "(hold|press) alt": Key("alt:down/3"),
        "release alt": Key("alt:up"),
        "(hold|press) shift": Key("shift:down/3"),
        "release shift": Key("shift:up"),
        "(hold|press) control": Key("ctrl:down/3"),
        "release control": Key("ctrl:up"),
        "release [all]": release,
        "single": Key("squote"),
        "double": Key("dquote"),
        "squiggle": Text("~"),
        "backtick": Key("backtick"),
        # Shorthand multiple characters.
        "double escape": Key("escape, escape"),  # Exiting menus.
        # Punctuation and separation characters, for quick editing.
        "colon": Key("colon"),
        "(semicolon|semi colon)": Key("semicolon"),
        "comma": Key("comma"),
        "dot": Key("dot"),  # cannot be followed by a repeat count
        "dash": Key("hyphen"),
        "downscore": Key("underscore"),
        "<letters>": Text("%(letters)s"),
        "<char>": Key("%(char)s"),
        "<modifierSingle> <letters>": Key("%(modifierSingle)s:down")
        + Text("%(letters)s")
        + Key("%(modifierSingle)s:up"),
        "<modifierSingle> <char>": Key("%(modifierSingle)s:down")
        + Key("%(char)s")
        + Key("%(modifierSingle)s:up"),
        "open angle": Key("langle"),
        "open brace": Key("lbrace"),
        "open bracket": Key("lbracket"),
        "open pen": Key("lparen"),
        "close angle": Key("rangle"),
        "close brace": Key("rbrace"),
        "close bracket": Key("rbracket"),
        "close pen": Key("rparen"),
        "(parentheses|pens)": Text("()"),
        "brackets": Text("[]"),
        "braces": Text("{}"),
        "escape": Key("escape"),
        "comma": Key("comma"),
        "home key": Key("home"),
        "end key": Key("end"),
        "delete": Key("del"),
        "snipe ": Key("backspace"),
        "before": Key("c-left"),
        "after": Key("c-right"),
        "hexadecimal": Text("0x"),
        "undo": Key("c-z"),
        "redo": Key("c-y"),
        "number <digits>": Text("%(digits)s"),
        "jump": Text(", "),
    },
    namespace={
        "Key": Key,
        "Text": Text,
    },
)


class KeystrokeRule(MappingRule):
    exported = False
    mapping = grammarCfg.cmd.map
    extras = [
        Dictation("text"),
        Dictation("text2"),
        Choice("char", specialCharMap),
        Choice("letters", letterMap),
        rules.digits,
        Choice("modifier1", modifierMap),
        Choice("modifier2", modifierMap),
        Choice("modifierSingle", singleModifierMap),
    ]
    defaults = {
        "n": 1,
    }


def root_rule():
    return KeystrokeRule(name="keystroke")