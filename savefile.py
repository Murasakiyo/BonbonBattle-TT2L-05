import pickle
import os  # use os module to check if the file exists

class SaveDataSystem:

    # check if the saved game state file exists
    @staticmethod   # define static method (can be called without object)
    def check_saved_state(file_path):
        return os.path.exists(file_path) 
        # return True if the file exists and vice versa
        

    # serialize current_state_data and save to file
    @staticmethod  
    def save_game_state(current_state_data, file_path):  
        # file_path (the path to the file where the game state will be saved)
        with open(file_path, 'wb') as file:
            pickle.dump(current_state_data, file)


    # load a saved game state from a file, deserialize the game state from the file
    @staticmethod        
    def load_game_state(file_path): 
        # file_path (the path to the file from which the game state will be loaded)
        try:  
            with open(file_path, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:  # returns None if error occured (FileNotFound)
            return None
        

