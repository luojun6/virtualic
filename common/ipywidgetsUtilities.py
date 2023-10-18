import ipywidgets as widgets
from utils.loggers import Logger, logging_handler
import logging

_logger = Logger(logger_name=__file__,
                 log_handler=logging_handler,
                 logging_level=logging.DEBUG)

def get_output_model_id(output_object: widgets.Output):
    try:
        model_id = output_object.outputs[0]["data"]["application/vnd.jupyter.widget-view+json"]["model_id"]
        
    except Exception as e:
        _logger.error(f"Failed to get model_id from {output_object.outputs}.")
        _logger.error(e)
        
    finally:
        return model_id if model_id else None
    