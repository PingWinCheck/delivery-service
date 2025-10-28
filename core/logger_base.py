import logging

def get_logger(name: str, lvl=logging.INFO) -> logging.Logger:
    logging.basicConfig(format="%(levelname)-9s %(asctime)s - %(name)-25s| line%(lineno)-4s| %(message)s",
                        level=lvl)
    return logging.getLogger(name=name)