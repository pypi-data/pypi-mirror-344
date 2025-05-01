# -*- coding: utf-8 -*-

import logging


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s][%(levelname)s] %(message)s",
        datefmt="%Y.%m.%d %H:%M:%S",
    )
