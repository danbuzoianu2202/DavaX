import os


class DevConfig:
    """
    Development configuration class.
    Contains settings for the development environment.
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'SimpleCache'
    DEBUG = True


class ProdConfig:
    """
    Production configuration class.
    Contains settings for the production environment.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///prod.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'SimpleCache'
    DEBUG = False


def get_config(name):
    """
    Get the configuration class based on the name.

    :param name: Configuration name, either 'dev' or 'prod'.
    :return: Configuration class.
    """
    if name == 'prod':
        return ProdConfig
    return DevConfig
