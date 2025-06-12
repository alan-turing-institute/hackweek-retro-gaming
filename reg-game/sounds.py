from pygame import mixer


class MusicPlayer:
    def __init__(self, filename: str = "sound/reggame-v2.mp3"):
        """
        Initializes the MusicPlayer instance.
        """
        self.game_theme = mixer.music.load(filename)
        self.volume: float = 0.3

    def start(self, filename: str = "sound/reggame-v2.mp3"):
        """
        Starts playing the background music.
        """
        mixer.music.load(filename)
        mixer.music.set_volume(self.volume)
        mixer.music.play(-1)

    def stop(self):
        """
        Stops the background music.
        """
        mixer.music.stop()


class SoundEffectPlayer:
    def __init__(self):
        """
        Initializes the SoundEffectPlayer instance.
        """
        self.hacker_alert: mixer.Sound = mixer.Sound("sound/hackeralert.ogg")
        self.hacker_alert.set_volume(0.5)
        self.sandbox_sound: mixer.Sound = mixer.Sound("sound/sandpit.wav")
        self.sandbox_sound.set_volume(0.5)
        self.hacking_sound: mixer.Sound = mixer.Sound("sound/hackingnoise-shorter.wav")
        self.hacking_sound.set_volume(0.05)
        self.hacking_won: mixer.Sound = mixer.Sound("sound/hackingover.wav")
        self.hacking_won.set_volume(0.4)
        self.hacking_lost: mixer.Sound = mixer.Sound("sound/shutdown.wav")
        self.hacking_won.set_volume(0.4)
        self.rotate_pipe_sound: mixer.Sound = mixer.Sound("sound/pipe_rotation.wav")
        self.rotate_pipe_sound.set_volume(0.8)

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
        self.hacking_sound.play(loops=-1)

    def stop_hacking_sound(self):
        """
        Plays the hacking sound effect.
        """
        self.hacking_sound.stop()

    def play_hacking_over(self):
        """
        Plays the hacking over sound effect.
        """
        self.hacking_won.play()

    def play_hacking_lost(self):
        """
        Plays the hacking over sound effect.
        """
        self.hacking_lost.play()

    def play_rotate_pipe_sound(self):
        """
        Plays the rotate pipe sound effect.
        """
        self.rotate_pipe_sound.play()
