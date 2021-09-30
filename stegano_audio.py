import wave
import os
import audio_metadata
from audio_metadata.models import StreamInfo

class SteganoAudio:
  def __init__(self):
    # self.audioFilePath = audioFilePath
    # self.text = text
    pass
  
  def getAudioByte(self, audioFilePath):
    self.audioFile = wave.open(audioFilePath, mode='rb')
    self.frameByte = bytearray(list(self.audioFile.readframes(self.audioFile.getnframes())))
  
  def encryptText(self):
    pass

  def textEmbedding(self, audioFilePath, text):
    self.getAudioByte(audioFilePath)

    # print('sample rate: {}'.format(self.audioFile.getframerate()))
    metadata = audio_metadata.load(audioFilePath)
    print(metadata['streaminfo'])

    self.text = text + int((len(self.frameByte) - (len(text)*8*8))/8) * '#'
    self.bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in self.text])))
    
    for i, bit in enumerate(self.bits):
      self.frameByte[i] = (self.frameByte[i] & 254) | bit
    self.modifiedFrameByte = bytes(self.frameByte)

    self.embeddedAudioFile = os.path.splitext(audioFilePath)[0]+'-Embedded.wav'
    with wave.open(self.embeddedAudioFile, 'wb') as out:
      out.setparams(self.audioFile.getparams())
      out.writeframes(self.modifiedFrameByte)
  
  def textExtraction(self, audioFilePath):
    self.getAudioByte(audioFilePath)
    
    # print('sample rate: {}'.format(self.audioFile.getframerate()))
    metadata = audio_metadata.load(audioFilePath)
    print(metadata['streaminfo'])

    self.extractedByte = [self.frameByte[i] & 1 for i in range(len(self.frameByte))]
    self.extractedText = ''.join(chr(int(''.join(map(str, self.extractedByte[i:i+8])), 2)) for i in range(0, len(self.extractedByte), 8))
    self.extractedText = self.extractedText.split('###')[0]

  def run(self, op, audioFilePath, text=None):
    if (op):
      self.textEmbedding(audioFilePath, text)
    else:
      self.textExtraction(audioFilePath)
      print(self.extractedText)