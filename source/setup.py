import logging
import os
import shutil

from source.config import LOGGING_FORMAT


def configure_logging():
    logging.basicConfig(
        format=LOGGING_FORMAT,
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()])

    # The 'neobolt' logger really spams the logging so I increase his level
    logging.getLogger("neobolt").setLevel(logging.WARNING)


def copy_files_to_neo4j_server(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    names = os.listdir(src)
    for name in names:
        src_name = os.path.join(src, name)
        dst_name = os.path.join(dst, name)

        if os.path.isdir(src_name):
            copy_files_to_neo4j_server(src_name, dst_name)
        else:
            shutil.copy2(src_name, dst_name)
