# api_key: str | None = None
# data_url: str | None = None
# orders_url: str | None = None
# data_url = "https://api.data.sysstra.com/"

from .config import config


def set_api_key(key):
    """ Function to set api key """
    # global api_key
    config["api_key"] = key


def set_data_url(url):
    """ Function to set data url """
    # global data_url
    config["data_url"] = url


def set_orders_url(url):
    """ Function to set Orders URL """
    # global orders_url
    config["orders_url"] = url
