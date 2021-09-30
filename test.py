from stegano_audio import *

steganoAudio = SteganoAudio()
steganoAudio.run(True, "file/audio.wav", "inipesanrahasia")
steganoAudio.run(False, "file/audio-Embedded.wav")