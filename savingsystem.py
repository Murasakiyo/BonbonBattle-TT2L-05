import pickle

class SaveDataSystem:
    def __init__(self, file_name, player, game):
        self.file_name = file_name
        self.player = player
        self.game = game

    def get_save_data(self):
        return {
            'current_level': self.game.current_level,
            'healthpoints': self.player.healthpoints,
            'attackpoints': self.player.attackpoints,
            'speed': self.player.speed,
            'skip_cutscenes': self.player.game.skip_cutscenes,
            'current_currency': self.player.game.current_currency
        }
    
    def default_value(self):
        return {
            'current_level': 0,
            'healthpoints': 250,
            'attackpoints': 20,
            'speed': 400,
            'skip_cutscenes': False,
            'current_currency': 0
        }

    # serialize player_data and save to a file
    def save_data_file(self):
        player_data = self.get_save_data()
        with open(self.file_name, 'wb') as file:
            pickle.dump(player_data, file)

    # deserialize player_data and load from the file
    def load_data_file(self):
        try:
            with open(self.file_name, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:  # returns None if error occured (FileNotFound)
            print("hi")
            return self.default_value()
        