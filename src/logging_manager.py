import logging
import os
import traceback


class TextWidgetHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.write_output(msg)



def configure_logging(terminal):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        try:
            # Set up logging to write logs to a file
            logs_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
            os.makedirs(logs_folder, exist_ok=True)
            log_file = os.path.join(logs_folder, "app.log")
            logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

            # Set up exception handling to log exceptions
            def handle_exception(exc_type, exc_value, exc_traceback):
                logger = logging.getLogger()
                logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

            import sys

            sys.excepthook = handle_exception

            logger.addHandler(TextWidgetHandler(terminal))  # Add the TextWidgetHandler to the logger

            logger.info("Logging configured")
        except Exception as e:
            traceback.print_exc()  # Print the traceback information

    return logger

