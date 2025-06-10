import pygame


class MusicPlayer:
    def __init__(self):
        """
        Initializes the MusicPlayer instance.
        """
        self.is_playing = False

    def start(self):
        """
        Starts playing the background music.
        """
        if not self.is_playing:
            load_background_music()
            play_background_music()
            self.is_playing = True

    def stop(self):
        """
        Stops the background music.
        """
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False

    def toggle(self):
        """
        Toggles the background music on or off.
        """
        if self.is_playing:
            self.stop()
        else:
            self.start()
# def init():
#     """
#     Initializes the pygame mixer for background music.
#     """
#     pygame.mixer.init()
#     pygame.mixer.set_num_channels(8)
    # pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
def load_background_music():
    pygame.mixer.music.load("sound/reggame.mp3")

def play_background_music():
    """
    Plays the background music in a loop.
    """
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely
    pygame.mixer.music.set_volume(0.25)  # Set volume to 50%