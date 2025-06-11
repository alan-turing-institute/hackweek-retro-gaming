from pygame import mixer


class MusicPlayer:
    def __init__(self):
        """
        Initializes the MusicPlayer instance.
        """
        self.game_theme = mixer.music.load("sound/reggame.mp3")
        self.is_playing = False
        self.volume = 0.3

    def start(self):
        """
        Starts playing the background music.
        """
        if not self.is_playing:
            mixer.music.set_volume(self.volume)
            mixer.music.play(-1)
            self.is_playing = True

    def stop(self):
        """
        Stops the background music.
        """
        if self.is_playing:
            mixer.music.stop()
            self.is_playing = False

    def toggle(self):
        """
        Toggles the background music on or off.
        """
        if self.is_playing:
            self.stop()
        else:
            self.start()


class SoundEffectPlayer:
    def __init__(self):
        """
        Initializes the SoundEffectPlayer instance.
        """
        self.sandbox_sound = mixer.Sound("sound/playershoot.wav")
        self.sandbox_sound.set_volume(0.5)

    def play_sandbox_sound(self):
        """
        Plays the sandbox sound effect.
        """
        self.sandbox_sound.play()
