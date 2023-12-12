import logging

def exception_handler(err):
    logging.error(err)
    return 'Sorry, there was an internal error on my end! Please try chatting again later.'