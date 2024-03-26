import tkinter as tk
import string

#Root
window = tk.Tk()
#test

#Top
greeting = tk.Label(text="Convert ->")
greeting.grid(column = 0, row = 0)


#frame 1 || Root = C0 R1 
frameLeft = tk.Frame()

#init
alph = list(string.ascii_uppercase)
print(alph)
charsTxtEnt = [] #Text
charsTxtIn = [] #Conversion targets
pos = 0
for letter in alph:
    charsTxtEnt.append(tk.Label(frameLeft, text=letter + " = "))
    charsTxtEnt[pos].grid(column=0, row=pos)
    charsTxtIn.append(tk.Entry(frameLeft, width = 2))
    charsTxtIn[pos].grid(column=2, row=pos)
    pos+=1

#frame 2 || Root = C2 R1  
frameRight = tk.Frame()

#user input || frameRight = C0 R0
sourceText = tk.Text(frameRight) 
sourceText.grid(column = 0, row = 0)

#Translate || frameRight = C0 R1
transFrame = tk.Frame(frameRight)
transFrame.grid(column = 0, row = 1)
transFrame.configure(highlightthickness=0)
transDisplay = []


def glossary(): # build translation
    outputString = []
    outputCodex = []
    index = 0
    for child in charsTxtIn:
        target = child.get().strip()
        if not target: # check if empty
            outputString.append(target)
            outputCodex.append(0)
        else:
            outputString.append(child.get().upper())
            outputCodex.append(1)
            
        index += 1
    return outputString, outputCodex

def labelUpdate(posX, widthSen, output, codex): #update existing or create new
    try:
        transDisplay[posX].config(text=output)
        transDisplay[posX].config(fg='red' if codex else 'black')
        
    except IndexError:
        if codex:
            transDisplay.append(tk.Label(transFrame, text = output,bd=0, fg = 'red'))
        else:
            transDisplay.append(tk.Label(transFrame, text = output,bd=0, fg = 'black'))
        transDisplay[posX].grid(column=posX%widthSen,row=int(posX/widthSen))

def translate(target, widthSen): # Translate
    posX = 0
    convertorStr, convertorCol = glossary() # pull translation
    #print(convertorStr)
    #print(convertorCol)
    for letter in target:
        output = ''
        codex = 0
        if letter == ' ': #spacing
            output = ' '
            codex = 0
        else:
            isUpper = letter.isupper()
            index = alph.index(letter.upper())
            output = convertorStr[index]
            if not output: # no translation
                output = letter
                codex = 1
            else: # translate
                if not letter.isupper():
                    output = output.lower()
                codex = 0
        #create
        labelUpdate(posX, widthSen, output, codex)
        #positioning
        posX += 1

translate("test", 50)

#init
frameLeft.grid(column = 0, row = 1)
frameRight.grid(column = 1, row = 1)

def clear_frame(target):
    for child in target.winfo_children():
        child.destroy()
        
def clear_translation(target):
    for child in target.winfo_children():
        child.config(text='')

ticks = 0
def ticktock():
    global ticks
    ticks += 0.25
    print(ticks)
    clear_translation(transFrame)
    translate(sourceText.get("1.0",'end-1c'), 50)
    #refresh every second
    window.after(250, ticktock)


window.after(1000, ticktock)
window.mainloop()