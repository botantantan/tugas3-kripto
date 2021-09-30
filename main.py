import tkinter as tk
from tkinter import filedialog

# util
filepath = ''

def importFile():
  file = filedialog.askopenfile(mode='r')
  if file is not None:
    fileContent = file.read()

  inputText.delete('0.0', 'end')
  inputText.insert('0.0', fileContent)

def exportFile():
  out = outputText.get('0.0', 'end-1c')
  with open('file/output.txt', 'w') as file:
    file.write(out)

def runProgram():
  pass

# root
root = tk.Tk()
root.title('Tugas 3 Kripto')
root.resizable(False, False)

## top frame
topFrame = tk.Frame(root, padx=25, pady=15)
topFrame.grid(row=0, column=0)

# input textbox
inputLabel = tk.Label(topFrame, text='Input Text')
inputLabel.grid(row=0, column=0)
inputText = tk.Text(topFrame, height=20, width=20)
inputText.grid(row=1, column=0)

# output textbox
outputLabel = tk.Label(topFrame, text='Output Text')
outputLabel.grid(row=0, column=1)
outputText = tk.Text(topFrame, height=20, width=20, state='disabled')
outputText.grid(row=1, column=1)

outputMediaLabel = tk.Label(topFrame, text='Media')
outputMediaLabel.grid(row=0, column=2)
outputMediaText = tk.Text(topFrame, height=20, width=20, state='disabled')
outputMediaText.grid(row=1, column=2)

## bot frame
botFrame = tk.Frame(root, padx=25, pady=15)
botFrame.grid(row=1, column=0)

# key
keyLabel = tk.Label(botFrame, text='Key')
keyLabel.grid(row=0, column=0, sticky='w')
keyEntry = tk.Entry(botFrame)
keyEntry.grid(row=0, column=1, sticky='w')

# io button
importBtn = tk.Button(botFrame, text='Import File', command=lambda:importFile())
importBtn.grid(row=1, column=0, sticky='w')
exportBtn = tk.Button(botFrame, text='Export File', command=lambda:exportFile())
exportBtn.grid(row=1, column=1, sticky='w')

# operation
mediaRadVar = tk.IntVar()
imgRadBtn = tk.Radiobutton(botFrame, text='Image', variable=mediaRadVar, value=1)
imgRadBtn.grid(row=0, column=2, sticky='w')
audRadBtn = tk.Radiobutton(botFrame, text='Audio', variable=mediaRadVar, value=2)
audRadBtn.grid(row=1, column=2, sticky='w')

opRadVar = tk.IntVar()
encryptRadBtn = tk.Radiobutton(botFrame, text='Encrypt', variable=opRadVar, value=1)
encryptRadBtn.grid(row=0, column=3, sticky='w')
decryptRadBtn = tk.Radiobutton(botFrame, text='Decrypt', variable=opRadVar, value=2)
decryptRadBtn.grid(row=1, column=3, sticky='w')

methodCheckVar = tk.IntVar()
methodCheckBtn = tk.Checkbutton(botFrame, text='Random', variable=methodCheckVar, onvalue=1, offvalue=0)
methodCheckBtn.grid(row=2, column=2, sticky='w')

encryptCheckVar = tk.IntVar()
encryptCheckBtn = tk.Checkbutton(botFrame, text='Encrypt Message', variable=encryptCheckVar, onvalue=1, offvalue=0)
encryptCheckBtn.grid(row=2, column=3, sticky='w')

# run
runBtn = tk.Button(botFrame, text='Run Program', command=lambda:runProgram())
runBtn.grid(row=2, column=0, sticky='w')

root.mainloop()