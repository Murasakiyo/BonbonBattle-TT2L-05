import pickle

class SaveDataSystem:
    def __init__(self, file_name, player):
        self.file_name = file_name
        self.player = player

    def get_save_data(self, player):
        return {
            'current_healthpoints': player.healthpoints,
            'current_attackpoints': player.attackpoints,
            'current_speed': player.speed
        }
    
    # serialize player_data and save to a file
    def save_data_file(self, player):
        player_data = self.get_save_data(player)
        with open(self.file_name, 'wb') as file:
            pickle.dump(player_data, file)

    # deserialize player_data and load from the file
    def load_data_file(self):
        try:
            with open(self.file_name, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:  # returns None if error occured (FileNotFound)
            return None