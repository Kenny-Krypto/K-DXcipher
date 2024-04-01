import tkinter as tk
import string
'''
Avg typing speed 40-60 wpm
or 240-360 chars per min, max 6 chars per second, ~150ms

Optimizations: (entry = user input to be translated)
    Range edit, -- last update len of entry to next update len of entry (include + and -) 
        -update between lengths
    Copy and paste -- detect and refresh entry
        - refresh all, or compare with last entry
'''
widthLimit = 100 #tbd

#Root
window = tk.Tk()
window.title('K-DXcipher')
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=2)

#Top will be removed
greeting = tk.Label(text="Convert ->")
greeting.grid(column = 0, row = 0, sticky="w")

''' Frame Left [GUI] '''
frameLeft = tk.Frame(window, width = 75, height = 550, highlightbackground="black", highlightthickness=1)

#init vars
alph = list(string.ascii_uppercase)
charsTxtEnt = [] #Text
charsTxtIn = [] #Conversion targets
pos = 0
for letter in alph:
    charsTxtEnt.append(tk.Label(frameLeft, text=letter + " = "))
    charsTxtEnt[pos].grid(column=0, row=pos)
    charsTxtIn.append(tk.Entry(frameLeft, width = 2))
    charsTxtIn[pos].grid(column=2, row=pos)
    pos+=1

''' Frame Right [GUI] '''
frameRightCanvas = tk.Canvas(window,height = 550, width= 500)
frameRightCanvas.grid(row = 1, column = 1,sticky="NSEW")
frameRightCanvas.grid_rowconfigure(2, weight=1)
frameRightCanvas.grid_columnconfigure(0, weight=1)

frameRight = tk.Frame(frameRightCanvas,height = 550, width= 500)
frameRightCanvas.create_window(10,10,anchor='nw',window=frameRight)

scrollbar = tk.Scrollbar(window, orient="vertical")
scrollbar.grid(row=0, column=2, sticky='ns')
scrollbar.config(command = frameRightCanvas.yview)

frameRightCanvas.config(yscrollcommand=scrollbar.set)

#user input || frameRight = C0 R0
sourceText = tk.Text(frameRight) 
sourceText.grid(column = 0, row = 0,sticky="NSEW")

#Translate || frameRight = C0 R1
transFrame = tk.Frame(frameRight)
transFrame.grid(column = 0, row = 1,sticky="NSEW")
transFrame.configure(highlightthickness=0)
transDisplay = []

''' Top Stucture '''

#init
frameLeft.grid(column = 0, row = 1, sticky="w")
frameLeft.grid_propagate(0)
frameRight.grid(column = 1, row = 1)
frameRight.grid_propagate(0)

''' Functions '''

def glossary(): # build translation
    outputString = []
    outputCodex = []
    index = 0
    for child in charsTxtIn: #Uses a global Var
        target = child.get().strip()
        if not target: # check if empty
            outputString.append(target)
            outputCodex.append(0) # color red
        else:
            outputString.append(child.get().upper())
            outputCodex.append(1) # color black
            
        index += 1
    return outputString, outputCodex

def labelUpdate(index, widthSen, output, codex): #update existing or create new
    try: # check if existing
        if output == '\n':
            transDisplay[index].config(text=" | ")
        else:
            transDisplay[index].config(text=output)
        transDisplay[index].config(fg='red' if codex else 'black')
        
    except IndexError: # create new label
        if codex:
            transDisplay.append(tk.Label(transFrame, text = output,bd=0, fg = 'red'))
        else:
            transDisplay.append(tk.Label(transFrame, text = output,bd=0, fg = 'black'))
        transDisplay[index].grid(column=index%widthSen,row=int(index/widthSen))

def translate(target, widthSen): # Translate
    index = 0
    convertorStr, convertorCol = glossary() # pull translation
    for letter in target:
        output = ''
        codex = 0
        if letter == ' ': #spacing
            output = ' '
            codex = 0
        elif letter == '\n': #newLine
            output = '\n'
            codex = 0
        elif letter.upper() in alph: # letter
            isUpper = letter.isupper()
            indexing = alph.index(letter.upper())
            output = convertorStr[indexing]
            if not output: # no translation
                output = letter
                codex = 1
            else: # translate
                if not letter.isupper():
                    output = output.lower()
                codex = 0
        else:
            output = ' '
            codex = 0
            
        #create/update existing labels
        labelUpdate(index, widthSen, output, codex)
        #positioning
        index += 1

def translateV2(target, widthSen, lastIndex, newIndex): # Translate
    start = lastIndex
    last = newIndex
    if lastIndex > newIndex:
        start = newIndex
        last = lastIndex
    index = 0
    convertorStr, convertorCol = glossary() # pull translation
    for index in range(start,last):
        letter = ""
        try:
            letter = target[index]
        except IndexError:
            letter = ' '
        output = ''
        codex = 0
        if letter == ' ': #spacing
            output = ' '
            codex = 0
        elif letter == '\n': #newLine
            output = '\n'
            codex = 0
        elif letter.upper() in alph: # letter
            isUpper = letter.isupper()
            indexing = alph.index(letter.upper())
            output = convertorStr[indexing]
            if not output: # no translation
                output = letter
                codex = 1
            else: # translate
                if not letter.isupper():
                    output = output.lower()
                codex = 0
        else:
            output = ' '
            codex = 0
            
        #create/update existing labels
        labelUpdate(index, widthSen, output, codex)
        #positioning
        #index += 1
''' TextBox Functions'''

def getTextIndex(textBox, targetIndex): # obtain str index given [Line.CharIndex]
    lineNum, charPos = targetIndex.split('.')
    line = 1
    index = int(charPos)
    while line < int(lineNum):
        numStr = str(line)
        index += len(textBox.get(numStr + ".0", numStr + '.end')) + 1
        line += 1
    return index
    
def getTextSelectIndex(textBox, targetIndexes):
    leftmost = getTextIndex(textBox, textBox.index(targetIndexes[0]))
    rightmost = getTextIndex(textBox, textBox.index(targetIndexes[1]))
    return [leftmost,rightmost]

''' Clean Up Functions '''

def clear_frame(target): # destory
    for child in target.winfo_children():
        child.destroy()
        
def clear_translation(target): # clear labels
    for child in target.winfo_children():
        child.config(text='')
        
''' Key Binding Code '''

keyPressHistory = []
def keyPressDetector(event): # detect key press 
    global phraseLen
    global isHighlight
    if event.keysym=='Control_L': # record control L in case of pasting
        if event.keysym not in keyPressHistory: # stop dups
            keyPressHistory.append(event.keysym)
    if event.keysym=='v':
        if 'Control_L' in keyPressHistory: #paste detected
            if event.keysym not in keyPressHistory: # stop dups
                keyPressHistory.append(event.keysym)
            phraseLen = 0
            phraseLenLock = True
    if event.keysym=='Shift_L':
        if event.keysym not in keyPressHistory: # stop dups
            keyPressHistory.append(event.keysym)
    if event.keysym=='Shift_R':
        if event.keysym not in keyPressHistory: # stop dups
            keyPressHistory.append(event.keysym)
    if isHighlight: #
        if 'Shift_L' not in keyPressHistory and 'Shift_R' not in keyPressHistory:
            left, right = getTextSelectIndex(sourceText, currentHighlight)
            currentText = sourceText.get("1.0",'end-1c')
            if right-left == 1:
                translateV2(currentText, widthLimit, left, right)
            else:
                translateV2(currentText, widthLimit, left, maxLen)
def keyReleaseDetector(event): #clear held down pressed keys from history
    if event.keysym in keyPressHistory:
        keyPressHistory.pop(keyPressHistory.index(event.keysym))
    if event.keysym=='v': 
        phraseLenLock = False
            
window.bind("<KeyRelease>", keyReleaseDetector)
window.bind("<KeyPress>", keyPressDetector)

''' Test Code '''

        
''' end Text Code '''

'''  Starting program / Main Loop '''

translate("Initializing", widthLimit) # init
clear_translation(transFrame) # clear init
#Global Vars
phraseLenLock = False
phraseLen = 0
isHighlight = False
currentHighlight = []
maxLen = 0
ticks = 0 # tracker 84324
def ticktock(): # Main Loop
    #init
    global isHighlight
    global currentHighlight
    global maxLen
    global phraseLen
    global ticks #tracker 84324
    #current input:
    userInput = sourceText.get("1.0",'end-1c')
    #Highlighted Text:
    currentHighlight = sourceText.tag_ranges("sel")
    isHighlight = True if currentHighlight else False
    #Max Length before any edits:
    maxLen = len(userInput)
    #Test
    ticks += 0.10 #tracker 84324
    print(ticks) #tracker 84324
    #print(phraseLen) #tracker 78465
    #Main function:
    translateV2(userInput, widthLimit, phraseLen, maxLen) # generate new translation
    #Update range edit:
    if not phraseLenLock:
        phraseLen = maxLen
    #refresh every 0.10 second
    window.after(100, ticktock)
    
window.after(1000, ticktock)
window.mainloop()

