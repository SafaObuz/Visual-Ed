from ui.gui import *
from sys import exit

if __name__ == "__main__":
    start_ui()
    set_gpt_message("The GPT Response Goes Here")
    #print_multiple_choice(["Option 1", "Option B", "Option C", "Option D", "Option E"])
    #if this is called multiple times in a loop, it will flicker. One time
    #move_gpt_onscreen() same stuff
    #select_multiple_choice(i : int):

    while True:
        ui_running = ui_loop()
        if not ui_running:
            break

    exit()