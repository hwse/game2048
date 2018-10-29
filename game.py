import game_gui
import game_state
import logging

def main():
    logging.basicConfig(level=logging.DEBUG)
    state = game_state.GameState()
    gui = game_gui.GUI(state)
    gui.run()

if __name__ == '__main__':
    main()