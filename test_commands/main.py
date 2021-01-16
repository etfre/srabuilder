"""
Command-module loader for Kaldi.

This script is based on 'dfly-loader-wsr.py' written by Christo Butcher and
has been adapted to work with the Kaldi engine instead.

This script can be used to look for Dragonfly command-modules for use with
the Kaldi engine. It scans the directory it's in and loads any ``_*.py`` it
finds.
"""


# TODO Have a simple GUI for pausing, resuming, cancelling and stopping
# recognition, etc

import os.path
import os
import threading
import time
import logging
import sys

from dragonfly import RecognitionObserver, get_engine
from dragonfly.log import setup_log
from srabuilder import sleep, environment

import contexts
import global_
import python
import firefox
import javascript
import vscode
import visual_studio
import bash
import stardew
import python_terminal
import windows_terminal


# --------------------------------------------------------------------------
# Simple recognition observer class.


class Observer(RecognitionObserver):
    def on_begin(self):
        print("Speech started.")

    def on_recognition(self, words):
        print("Recognized:", " ".join(words))

    def on_failure(self):
        print("Sorry, what was that?")


def command_line_loop(engine):
    while True:
        user_input = input("> ")
        if user_input:
            time.sleep(4)
            try:
                engine.mimic(user_input)
            except Exception as e:
                print(e)


# --------------------------------------------------------------------------
# Main event driving loop.


def main(args):
    logging.basicConfig(level=logging.INFO)
    # use abspath for model dir, this may change with app freezing
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(current_dir, "..", "kaldi_model")
    # Set any configuration options here as keyword arguments.
    engine = get_engine(
        "kaldi",
        model_dir=model_dir,
        expected_error_rate_threshold=0.05,
        # tmp_dir='kaldi_tmp',  # default for temporary directory
        # vad_aggressiveness=3,  # default aggressiveness of VAD
        vad_padding_start_ms=0,  # default ms of required silence surrounding VAD
        # vad_padding_end_ms=500,  # default ms of required silence surrounding VAD
        vad_padding_end_ms=250,  # default ms of required silence surrounding VAD
    )
    # Call connect() now that the engine configuration is set.
    engine.connect()

    # Register a recognition observer
    observer = Observer()
    observer.register()

    sleep.load_sleep_wake_grammar(True)

    map_contexts_to_builder = {
        (): global_.rule_builder(),
        (contexts.firefox,): firefox.rule_builder(),
        (contexts.bash,): bash.rule_builder()
        .merge(python_terminal.rule_builder())
        .merge(windows_terminal.rule_builder()),
        (contexts.vscode,): vscode.rule_builder(),
        (contexts.vscode, contexts.python): python.rule_builder(),
        (contexts.vscode, contexts.javascript): javascript.rule_builder(),
        (contexts.visual_studio,): visual_studio.rule_builder(),
    }
    envs = environment.load_environments(engine, map_contexts_to_builder)
    environment.load_grammars(envs)
    import _dictation

    _dictation.load_grammar()

    # Start the engine's main recognition loop
    # engine.mimic('alpha three bravo charlie zulu eight six')
    engine.prepare_for_recognition()
    engine.mimic("start listening")

    # threading.Thread(target=command_line_loop, args=(engine,), daemon=True).start()
    try:
        # Loop forever
        print("Listening...")
        engine.do_recognition()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main(sys.argv[1:])
