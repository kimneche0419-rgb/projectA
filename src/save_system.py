import pickle
import os

SAVE_FILE = "data/echoes.pkl"

class SaveSystem:
    def __init__(self):
        self.echoes = []
        self.load_echoes()
        
    def save_death_echo(self, x, y, cause, chapter):
        echo_data = {
            'x': x,
            'y': y,
            'cause': cause,
            'chapter': chapter
        }
        self.echoes.append(echo_data)
        
        # Ensure data dir exists
        os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
            
        with open(SAVE_FILE, 'wb') as f:
            pickle.dump(self.echoes, f)
            print(f"Echo saved at ({x}, {y})")
            
    def load_echoes(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'rb') as f:
                    self.echoes = pickle.load(f)
            except Exception as e:
                print(f"Error loading save file: {e}")
                
    def get_echoes_for_chapter(self, chapter):
        return [e for e in self.echoes if e.get('chapter') == chapter]
