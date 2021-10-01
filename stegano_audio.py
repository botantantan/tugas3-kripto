import wave
import os
import audio_metadata
import random

class SteganoAudio:
  def __init__(self):
    # self.audioFilePath = audioFilePath
    # self.text = text
    pass
  
  def getAudioByte(self, audioFilePath):
    self.audioFile = wave.open(audioFilePath, mode='rb')
    self.frameByte = bytearray(list(self.audioFile.readframes(self.audioFile.getnframes())))
  
  def encryptText(self, text):
    pass

  def textEmbedding(self, audioFilePath, text, rand=False):
    self.getAudioByte(audioFilePath)

    # metadata = audio_metadata.load(audioFilePath)
    # print(metadata['streaminfo'])

    if (rand):
      self.text = text
    else:
      self.text = text + int((len(self.frameByte) - (len(text)*8*8))/8) * '#'

    self.bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in self.text])))
    
    if (rand):
      textPos, temp = 0, 0
      textPosArr = []
      for i in range(len(self.bits)):
        temp = random.randint(1, 5)*3
        if (textPos+15 > len(self.frameByte)):
          temp = 1
        textPos += temp
        textPosArr.append(textPos)
      
      for i in range(len(self.frameByte)):
        self.frameByte[i] = (self.frameByte[i] & 252)

      for i, bit in enumerate(self.bits):
        self.frameByte[textPosArr[i]] = (self.frameByte[textPosArr[i]] & 252) | (bit+2)

    else:
      for i, bit in enumerate(self.bits):
        self.frameByte[i] = (self.frameByte[i] & 252) | (bit+2)
    
    self.modifiedFrameByte = bytes(self.frameByte)
    self.embeddedAudioFile = os.path.splitext(audioFilePath)[0]+'-Embedded.wav'
    with wave.open(self.embeddedAudioFile, 'wb') as out:
      out.setparams(self.audioFile.getparams())
      out.writeframes(self.modifiedFrameByte)
  
  def textExtraction(self, audioFilePath):
    self.getAudioByte(audioFilePath)

    # metadata = audio_metadata.load(audioFilePath)
    # print(metadata['streaminfo'])

    self.extractedByte = []
    for i in range(len(self.frameByte)):
      if (self.frameByte[i] & 2):
        self.extractedByte.append(self.frameByte[i] & 1)

    self.extractedText = ''.join(chr(int(''.join(map(str, self.extractedByte[i:i+8])), 2)) for i in range(0, len(self.extractedByte), 8))
    self.extractedText = self.extractedText.split('###')[0]

  def run(self, op, audioFilePath, text=None, random=False):
    if (op):
      if (random):
        self.textEmbedding(audioFilePath, text, random)
        print('done')
      else:
        self.textEmbedding(audioFilePath, text)
        print('done')
    else:
      self.textExtraction(audioFilePath)
      print(self.extractedText)
      print('done')