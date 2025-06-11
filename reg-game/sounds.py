from pygame import mixer


class MusicPlayer:
    def __init__(self):
        """
        Initializes the MusicPlayer instance.
        """
        self.game_theme = mixer.music.load("sound/reggame-v2.mp3")
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
        self.hacker_alert = mixer.Sound("sound/hackeralert.ogg")
        self.hacker_alert.set_volume(0.5)
        self.sandbox_sound = mixer.Sound("sound/playershoot.wav")
        self.sandbox_sound.set_volume(0.5)
        self.hacking_sound = mixer.Sound("sound/hackingnoise-shorter.wav")
        self.hacking_sound.set_volume(0.05)

    def play_sandbox_sound(self):
        """
        Plays the sandbox sound effect.
        """
        self.sandbox_sound.play()

    def play_hacker_alert(self):
        """
        Plays the hacker alert sound effect.
        """
        self.hacker_alert.play()

    def play_hacking_sound(self):
        """
        Plays the hacking sound effect.
        """
        self.hacking_sound.play(loops = -1)

    def stop_hacking_sound(self):
        """
        Plays the hacking sound effect.
        """
        self.hacking_sound.stop()
