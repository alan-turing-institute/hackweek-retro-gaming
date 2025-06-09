from framework import Game
from interstitial import InterstitialState
from invadersgame import PlayGameState
from menu import MainMenuState

invaders_game: Game = Game("Invaders", 800, 600)
main_menu_state: MainMenuState = MainMenuState(invaders_game)
game_over_state: InterstitialState = InterstitialState(
    invaders_game, "G A M E  O V E R !", 5000, main_menu_state
)
play_game_state: PlayGameState = PlayGameState(invaders_game, game_over_state)
get_ready_state: InterstitialState = InterstitialState(
    invaders_game, "Get ready!!", 2000, play_game_state
)

main_menu_state.set_play_state(get_ready_state)

invaders_game.run(main_menu_state)
