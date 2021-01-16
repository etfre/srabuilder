
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