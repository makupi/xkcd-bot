import json


class Config:
    @staticmethod
    def get_config():
        with open("config.json", "r") as read_file:
            config = json.load(read_file)
        return config

    @staticmethod
    def set_config(config):
        with open("config.json", "w") as write_file:
            json.dump(config, write_file)

        if not all(k in config for k in ('token', 'prefix', 'game', 'mongodb')):
            raise ValueError

    @staticmethod
    def get_token():
        config = Config.get_config()
        return config.get('token')

    @staticmethod
    def get_prefix():
        config = Config.get_config()
        return config.get('prefix')

    @staticmethod
    def get_game():
        config = Config.get_config()
        return config.get('game')
 
    @staticmethod
    def get_dbl_token():
        config = Config.get_config()
        return config.get('dblToken')

    @staticmethod
    def set_prefix(prefix):
        config = Config.get_config()
        config['prefix'] = prefix
        Config.set_config(config)

    @staticmethod
    def set_game(game):
        config = Config.get_config()
        config['game'] = game
        Config.set_config(config)
