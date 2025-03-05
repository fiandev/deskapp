import os
from lib.Desktop import Desktop
from constants.paths import THIRD_PARTY_PROGRAM_PATH, DOWNLOAD_PATH, HISTORY_PATH

if __name__ == '__main__':
    # initalize path folder
    for folder in [THIRD_PARTY_PROGRAM_PATH, DOWNLOAD_PATH, HISTORY_PATH]:
        if not os.path.exists(folder):
            os.makedirs(folder)
    
    app = Desktop()
    app.mainloop()