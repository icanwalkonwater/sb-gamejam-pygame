import os
from typing import Dict

from pygame import mixer


class MusicManager:
    __sound_effects: Dict[str, mixer.Sound] = {}

    @classmethod
    def init(cls):
        mixer.init(22100, -16, 2, 64)
        cls.__sound_effects: Dict[str, mixer.Sound] = {
            'gust': mixer.Sound(os.path.join("assets", "audio", "gust.wav")),
            'slam': mixer.Sound(os.path.join("assets", "audio", "slam-1.ogg"))
        }

    @classmethod
    def play_music(cls):
        mixer.music.load(os.path.join("assets", "audio", "Musique combat.mp3"))
        mixer.music.play(-1)

    @classmethod
    def stop_music(cls):
        mixer.music.stop()

    @classmethod
    def play_sound_effect(cls, name: str):
        cls.__sound_effects[name].play()
