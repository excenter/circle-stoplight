from pygame import mixer
import time
import os
from pyogg import VorbisFile
import random


def selectFile(old_state, new_state):
    pass
    sounds_folder = "sounds"
    folder_path = sounds_folder + "/" + old_state + "2" + new_state
    print(folder_path)
    ra = random.choice(os.listdir(folder_path))
    return folder_path + "/" + ra


def playPath(path):
    print(path)
    mixer.quit
    sound = VorbisFile(path)
    frequency = sound.frequency
    mixer.init(frequency=frequency)
    mixer.music.load(path)
    mixer.music.set_volume(1.0)
    mixer.music.fadeout(15)
    mixer.music.play()

    # while mixer.music.get_busy() == True:
    #     pass


def play_audio_from_state(old_state, new_state):
    try:
        print("received states: " + old_state + ", " + new_state)
        selected_sound = selectFile(old_state, new_state)
        print(selected_sound)
        playPath(selected_sound)

    except:
        print("failed to play audio")


if __name__ == "__main__":
    # playPath("sounds/broken2building/prehub10.mp3")
    # time.sleep(6)
    # print(selectFile("broken", "good"))
    # selected_sound = selectFile("broken", "xxx")
    # selected_sound = "../sounds/wii.ogg"
    # playPath(selected_sound)
    # time.sleep(30)
    # try:
    #     selected_sound = selectFile("building", "good")
    #     playPath(selected_sound)
    #     time.sleep(6)

    # except:
    #     print("failed to play audio")
    # play_audio_from_state("building", "good")
    # time.sleep(10)
    states = ["building", "broken", "good"]
    old_state = random.choice(states)
    while True:
        state = random.choice(states)
        if old_state != state:
            play_audio_from_state(old_state, state)
        else:
            print("duplicate")
        old_state = state
        time.sleep(2)
