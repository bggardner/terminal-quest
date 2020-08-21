from kano.logging import logger
from .apps import load_app_state, save_app_state

def save_app_state_with_dialog(app_name, data):
    save_app_state(app_name, data)

def save_app_state_variable_with_dialog(app_name, variable, value):
    logger.debug(
        'save_app_state_variable_with_dialog {} {} {}'
        .format(app_name, variable, value)
    )

    data = load_app_state(app_name)
    data[variable] = value

    save_app_state_with_dialog(app_name, data)
