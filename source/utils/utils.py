import logging
import os
import shutil


def configure_logging(log_level, logging_format):
    """
    Configures the system logs
    """
    logging.basicConfig(
        format=logging_format,
        level=log_level,
        handlers=[logging.StreamHandler()])

    # The 'neobolt' logger really spams the logging so I increase his level
    logging.getLogger("neobolt").setLevel(logging.WARNING)


def copy_tree(src, dst):
    """
    Copies recursively a chosen dir and it files to destination dir
    """
    if not os.path.exists(dst):
        os.makedirs(dst)
    names = os.listdir(src)
    for name in names:
        src_name = os.path.join(src, name)
        dst_name = os.path.join(dst, name)

        if os.path.isdir(src_name):
            copy_tree(src_name, dst_name)
        else:
            shutil.copy2(src_name, dst_name)


def reset_neo4j_db(driver):
    """
    Resets the neo4j db
    Args:
        driver: The neo4j driver
    """
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
