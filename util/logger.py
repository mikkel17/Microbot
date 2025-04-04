

import logging

class SimpleLogger:
    def __init__(self, log_file='/opt/Microbot/app.log'):
        self.logger = logging.getLogger('SimpleLogger')
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.hasHandlers():
            # Create file handler which logs messages to a file
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)

            # Create a formatter and set it for the handler
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)

            # Add the handler to the logger
            self.logger.addHandler(file_handler)

    def debug(self, user, message):
        self.logger.debug(user + ' ' + message)

    def info(self, user, message):
        self.logger.info(user + ' - ' + message)

    def warning(self, user, message):
        self.logger.warning(user + ' ' + message)

    def error(self, user, message):
        self.logger.error(user + ' ' + message)

    def critical(self, user, message):
        self.logger.critical(user + ' ' + message)

# Example usage
if __name__ == "__main__":
    logger = SimpleLogger()