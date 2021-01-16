
import os.path
import os
import threading
import time
import logging
import sys

from dragonfly import RecognitionObserver, get_engine
from dragonfly.log import setup_log
from srabuilder import sleep, environment

# --------------------------------------------------------------------------
# Set up basic logging.

if False:
    # Debugging logging for reporting trouble
    logging.basicConfig(level=10)
    logging.getLogger("grammar.decode").setLevel(20)
    logging.getLogger("grammar.begin").setLevel(20)
    logging.getLogger("compound").setLevel(20)
    logging.getLogger("kaldi.compiler").setLevel(10)
else:
    setup_log()

def setup_engine():
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
    return engine

def load_environment_grammars(map_contexts_to_builder):
    envs = environment.load_environments(map_contexts_to_builder)
    environment.load_grammars(envs)

def run_engine():
    engine = get_engine()
    engine.prepare_for_recognition()
    try:
        print("Listening...")
        engine.do_recognition()
    except KeyboardInterrupt:
        pass