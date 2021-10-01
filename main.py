import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image
import numpy as np

import modifiedrc4
import stegano_audio
import stegano_image

# util
stegAud = stegano_audio.SteganoAudio()

def rc4ImportFile():
    file = filedialog.askopenfile(mode='rb')
    
    if file is not None:
        fileContent = file.read()

    rc4InputText.delete('0.0', 'end')
    rc4InputText.insert('0.0', fileContent)

def rc4ExportFile():
  out = rc4OutputText.get('0.0', 'end-1c')
  with open('file/output.txt', 'w') as file:
    file.write(out)

def runRC4():
  opChoice = rc4OpRadVar.get()
  input = rc4InputText.get('0.0', 'end-1c')
  keyA = rc4KeyAEntry.get()
  keyB = rc4KeyBEntry.get()

  out = ''

  if (opChoice == 1): # encrypt
    out = modifiedrc4.encrypt(input, keyA, keyB)
  else:
    out = modifiedrc4.decrypt(input, keyA, keyB)
  
  rc4OutputText.config(state="normal")
  rc4OutputText.delete("0.0", "end")
  rc4OutputText.insert("0.0", out)
  rc4OutputText.config(state="disabled")

def runSteg():
  mediaChoice = stegMediaRadVar.get()
  opChoice = stegOpRadVar.get()
  methodChoice = stegMethodCheckVar.get()
  encryptChoice = stegEncryptCheckVar.get()
  inputHiddenText = stegInputText.get('0.0', 'end-1c')
  keyA = rc4KeyAEntry.get()
  keyB = rc4KeyBEntry.get()
  outputHiddenText = ''

  if (mediaChoice == 1): # image
    if (methodChoice == 0): # sequential
      if (opChoice == 1): # embed
        if (encryptChoice == 1): # encrypt
          file = filedialog.askopenfile(mode='rb')
          inputHiddenText = modifiedrc4.encrypt(inputHiddenText, keyA, keyB)
          embedded_image_file = stegano_image.stegano_encode(inputHiddenText, np.array(Image.open(file)))
          Image.fromarray(embedded_image_file).save("/".join(file.name.split('/')[:-1]) + "/Hasil.png")
        elif (encryptChoice == 0):
          file = filedialog.askopenfile(mode='rb')
          embedded_image_file = stegano_image.stegano_encode(inputHiddenText, np.array(Image.open(file)))
          Image.fromarray(embedded_image_file).save("/".join(file.name.split('/')[:-1]) + "/Hasil.png")
      elif (opChoice == 2): # extract
        file = filedialog.askopenfile(mode='rb')
        secret_message = stegano_image.stegano_decode(np.array(Image.open(file)))
        if secret_message:
          # with open("./file/Hasil_decode_stegano.txt",'w') as f:
          print(secret_message)
          stegOutputText.config(state="normal")
          stegOutputText.delete("0.0", "end")
          stegOutputText.insert("0.0", secret_message)
          stegOutputText.config(state="disabled")
            # f.write(secret_message)
    elif (methodChoice == 1): # random
      if (opChoice == 1): # embed
        if (encryptChoice == 1): # encrypt
          file = filedialog.askopenfile(mode='rb')
          inputHiddenText = modifiedrc4.encrypt(inputHiddenText, keyA, keyB)
          embedded_image_file = stegano_image.stegano_acak(inputHiddenText, np.array(Image.open(file)))
          Image.fromarray(embedded_image_file).save("/".join(file.name.split('/')[:-1]) + "/HasilAcak.png")
        elif (encryptChoice == 0):
          file = filedialog.askopenfile(mode='rb')
          embedded_image_file = stegano_image.stegano_acak(inputHiddenText, np.array(Image.open(file)))
          Image.fromarray(embedded_image_file).save("/".join(file.name.split('/')[:-1]) + "/HasilAcak.png")
      elif (opChoice == 2): # extract
        file = filedialog.askopenfile(mode='rb')
        secret_message = stegano_image.stegano_acak_decode(np.array(Image.open(file)))
        print(f"Hasil : {secret_message}")
        if secret_message:
          # with open("file/Hasil_decode_stegano_acak.txt",'w') as f:
          # print(secret_message)
          stegOutputText.config(state="normal")
          stegOutputText.delete("0.0", "end")
          stegOutputText.insert("0.0", secret_message)
          stegOutputText.config(state="disabled")
            # f.write(secret_message)
  elif (mediaChoice == 2): # audio
    if (methodChoice == 0): # sequential
      if (opChoice == 1): # embed
        if (encryptChoice == 1): # encrypt
          file = filedialog.askopenfile(mode='r')
          inputHiddenText = modifiedrc4.encrypt(inputHiddenText, keyA, keyB)
          if file:
              filepath = os.path.abspath(file.name)
          stegAud.run(True, filepath, inputHiddenText)
        elif (encryptChoice == 0):
          file = filedialog.askopenfile(mode='r')
          if file:
              filepath = os.path.abspath(file.name)
          stegAud.run(True, filepath, inputHiddenText)
      elif (opChoice == 2): # extract
        file = filedialog.askopenfile(mode='r')
        if file:
            filepath = os.path.abspath(file.name)
        stegAud.run(False, filepath)
        outputHiddenText = stegAud.extractedText

        stegOutputText.config(state="normal")
        stegOutputText.delete("0.0", "end")
        stegOutputText.insert("0.0", outputHiddenText)
        stegOutputText.config(state="disabled")
    elif (methodChoice == 1): # random
      if (opChoice == 1): # embed
        if (encryptChoice == 1): # encrypt
          file = filedialog.askopenfile(mode='r')
          inputHiddenText = modifiedrc4.encrypt(inputHiddenText, keyA, keyB)
          if file:
              filepath = os.path.abspath(file.name)
          stegAud.run(True, filepath, inputHiddenText)
        elif (encryptChoice == 0):
          file = filedialog.askopenfile(mode='r')
          if file:
              filepath = os.path.abspath(file.name)
          stegAud.run(True, filepath, inputHiddenText, False)
      elif (opChoice == 2): # extract
        file = filedialog.askopenfile(mode='r')
        if file:
            filepath = os.path.abspath(file.name)
        stegAud.run(False, filepath)
        outputHiddenText = stegAud.extractedText

        stegOutputText.config(state="normal")
        stegOutputText.delete("0.0", "end")
        stegOutputText.insert("0.0", outputHiddenText)
        stegOutputText.config(state="disabled")

# root
root = tk.Tk()
root.title('Tugas 3 Kripto')
root.resizable(False, False)

## rc4 frame
rc4Frame = tk.Frame(root, padx=25, pady=15)
rc4Frame.grid(row=0, column=0)

### rc4 label
rc4Label = tk.Label(rc4Frame, text='RC4')
rc4Label.grid(row=0, column=0, sticky='n')

### rc4 input textbox
rc4InputLabel = tk.Label(rc4Frame, text='Input Text')
rc4InputLabel.grid(row=1, column=0)
rc4InputText = tk.Text(rc4Frame, height=15, width=20)
rc4InputText.grid(row=2, column=0)

### rc4 output textbox
rc4OutputLabel = tk.Label(rc4Frame, text='Output Text')
rc4OutputLabel.grid(row=1, column=1)
rc4OutputText = tk.Text(rc4Frame, height=15, width=20, state='disabled')
rc4OutputText.grid(row=2, column=1)

### rc4 key
rc4KeyALabel = tk.Label(rc4Frame, text='Key A')
rc4KeyALabel.grid(row=3, column=0, sticky='w')
rc4KeyAEntry = tk.Entry(rc4Frame)
rc4KeyAEntry.grid(row=3, column=0, sticky='e')

rc4KeyBLabel = tk.Label(rc4Frame, text='Key B')
rc4KeyBLabel.grid(row=4, column=0, sticky='w')
rc4KeyBEntry = tk.Entry(rc4Frame)
rc4KeyBEntry.grid(row=4, column=0, sticky='e')

### rc4 io
rc4ImportBtn = tk.Button(rc4Frame, text='Import File', command=lambda:rc4ImportFile())
rc4ImportBtn.grid(row=3, column=1, sticky='w')
rc4ExportBtn = tk.Button(rc4Frame, text='Export File', command=lambda:rc4ExportFile())
rc4ExportBtn.grid(row=4, column=1, sticky='w')

### rc4 op radio
rc4OpRadVar = tk.IntVar()
rc4EncryptRadBtn = tk.Radiobutton(rc4Frame, text='Encrypt', variable=rc4OpRadVar, value=1)
rc4EncryptRadBtn.grid(row=3, column=1, sticky='e')
rc4DecryptRadBtn = tk.Radiobutton(rc4Frame, text='Decrypt', variable=rc4OpRadVar, value=2)
rc4DecryptRadBtn.grid(row=4, column=1, sticky='e')

### rc4 run
rc4RunBtn = tk.Button(rc4Frame, text='Run RC4', command=lambda:runRC4())
rc4RunBtn.grid(row=5, column=0, sticky='w')

## stegano frame
stegFrame = tk.Frame(root, padx=25, pady=15)
stegFrame.grid(row=1, column=0)

### stegano label
stegLabel = tk.Label(stegFrame, text='Steganography')
stegLabel.grid(row=0, column=0, sticky='n')

### stegano output textbox
stegInputLabel = tk.Label(stegFrame, text='Input Text')
stegInputLabel.grid(row=1, column=0)
stegInputText = tk.Text(stegFrame, height=2, width=20)
stegInputText.grid(row=1, column=1)

### stegano output textbox
stegOutputLabel = tk.Label(stegFrame, text='Hidden Text')
stegOutputLabel.grid(row=2, column=0)
stegOutputText = tk.Text(stegFrame, height=2, width=20, state='disabled')
stegOutputText.grid(row=2, column=1)

### stegano media radio
stegMediaRadVar = tk.IntVar()
stegImgRadBtn = tk.Radiobutton(stegFrame, text='Image', variable=stegMediaRadVar, value=1)
stegImgRadBtn.grid(row=3, column=0, sticky='w')
stegAudRadBtn = tk.Radiobutton(stegFrame, text='Audio', variable=stegMediaRadVar, value=2)
stegAudRadBtn.grid(row=4, column=0, sticky='w')

### stegano op radio
stegOpRadVar = tk.IntVar()
stegEmbedRadBtn = tk.Radiobutton(stegFrame, text='Embed', variable=stegOpRadVar, value=1)
stegEmbedRadBtn.grid(row=3, column=1, sticky='w')
stegExtRadBtn = tk.Radiobutton(stegFrame, text='Extract', variable=stegOpRadVar, value=2)
stegExtRadBtn.grid(row=4, column=1, sticky='w')

### stegano run
stegRunBtn = tk.Button(stegFrame, text='Run Steganography', command=lambda:runSteg())
stegRunBtn.grid(row=5, column=0, sticky='w')

### stegano method check
stegMethodCheckVar = tk.IntVar()
stegMethodCheckBtn = tk.Checkbutton(stegFrame, text='Random', variable=stegMethodCheckVar, onvalue=1, offvalue=0)
stegMethodCheckBtn.grid(row=3, column=2, sticky='w')

### stegano encrypt
stegEncryptCheckVar = tk.IntVar()
stegEncryptCheckBtn = tk.Checkbutton(stegFrame, text='Encrypt', variable=stegEncryptCheckVar, onvalue=1, offvalue=0)
stegEncryptCheckBtn.grid(row=4, column=2, sticky='w')

root.mainloop()