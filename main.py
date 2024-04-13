from ui.gui import *
from sys import exit

if __name__ == "__main__":
    start_ui()

    while True:
        ui_running = ui_loop()
        if not ui_running:
            break
    
    exit()
