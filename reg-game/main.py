from config import SCREEN_HEIGHT, SCREEN_WIDTH
from framework import Game
from interstitial import InterstitialState
from menu import MainMenuState
from pipe_game import PipeGameState
from reg_game import PlayGameState

reg_game: Game = Game("The REG Game", SCREEN_WIDTH, SCREEN_HEIGHT)

main_menu_state: MainMenuState = MainMenuState(reg_game)
game_over_state: InterstitialState = InterstitialState(
    reg_game, "G A M E  O V E R !", 5000, main_menu_state
)

pipe_game_state: PipeGameState = PipeGameState(reg_game, game_over_state)

play_game_state: PlayGameState = PlayGameState(
    reg_game, game_over_state, pipe_game_state
)
pipe_game_state.play_game_state = play_game_state

prepare_for_challenge: InterstitialState = InterstitialState(
    reg_game, "Defence and Security need you!", 2000, play_game_state
)

main_menu_state.set_play_state(prepare_for_challenge)

reg_game.run(main_menu_state)
