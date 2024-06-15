import pickle

class SaveDataSystem:
    def __init__(self, file_name, game):
        self.file_name = file_name
        self.game = game

    def get_save_data(self):
        return {
            'current_level': self.game.current_level,
            'healthpoints': self.game.settings.current_healthpoints,
            'attackpoints': self.game.settings.current_attackpoints,
            'speed': self.game.settings.current_speed,
            'skip_cutscenes': self.game.skip_cutscenes,
            'current_currency': self.game.current_currency,
            'stan_dialogue_counter': self.game.settings.stan_dialogue_counter,
            'krie_intro': self.game.settings.krie_intro,
            'tutorial': self.game.tutorial,
            'end_level': self.game.settings.first_win5,
            'upgrade_atk_lvl': self.game.settings.current_atk_level,
            'upgrade_HP_lvl': self.game.settings.current_HP_level,
            'upgrade_spd_lvl': self.game.settings.current_spd_level
        }
    

    # serialize player_data and save to a file
    def save_data_file(self):
        player_data = self.get_save_data()
        with open(self.file_name, 'wb') as file:
            pickle.dump(player_data, file)

    # deserialize player_data and load from the file
    def load_data_file(self):
        # try:
        with open(self.file_name, 'rb') as file:
            return pickle.load(file)
        


        