from config import SCREEN_HEIGHT, SCREEN_WIDTH
from framework import Game
from interstitial import InterstitialState
from menu import MainMenuState
from reg_game import PlayGameState

reg_game: Game = Game("The REG Game", SCREEN_WIDTH, SCREEN_HEIGHT)

main_menu_state: MainMenuState = MainMenuState(reg_game)
game_over_state: InterstitialState = InterstitialState(
    reg_game, "G A M E  O V E R !", 12000, main_menu_state
)

play_game_state: PlayGameState = PlayGameState(reg_game, game_over_state)

prepare_for_challenge: InterstitialState = InterstitialState(
    reg_game,
    "Regina, we need you!\n\nWe are under attack and you are our last line of defence!\n\nProtect our terminals!",
    5000,
    play_game_state,
    background_path="img/forest_back_550_x_400.png",
)

main_menu_state.set_play_state(prepare_for_challenge)

reg_game.run(main_menu_state)
