import tkinter as tk
import string

#Root
window = tk.Tk()
window.title('K-DXcipher')
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=2)



#Top
greeting = tk.Label(text="Convert ->")
greeting.grid(column = 0, row = 0, sticky="w")


#frame 1 || Root = C0 R1 
frameLeft = tk.Frame(window, width = 75, height = 550, highlightbackground="black", highlightthickness=1)

#init
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

#frame 2 || Root = C2 R1  
frameRight = tk.Canvas(window)
frameRight.grid(sticky="NSEW")
frameRight.grid_rowconfigure(2, weight=1)
frameRight.grid_columnconfigure(0, weight=1)


#scrollbar = tk.Scrollbar(window, orient="vertical", command=frameRight.yview)
#scrollbar.grid(row=0, column=2, sticky='ns')

#user input || frameRight = C0 R0
sourceText = tk.Text(frameRight) 
sourceText.grid(column = 0, row = 0,sticky="NSEW")

#Translate || frameRight = C0 R1
transFrame = tk.Frame(frameRight)
transFrame.grid(column = 0, row = 1,sticky="NSEW")
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
        else: # letter
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
        #create/update existing labels
        labelUpdate(index, widthSen, output, codex)
        #positioning
        index += 1

translate("test", 50) # init

#init
frameLeft.grid(column = 0, row = 1, sticky="w")
frameLeft.grid_propagate(0)
frameRight.grid(column = 1, row = 1)

def clear_frame(target): # destory
    for child in target.winfo_children():
        child.destroy()
        
def clear_translation(target): # clear labels
    for child in target.winfo_children():
        child.config(text='')

ticks = 0 # tracker 84324
def ticktock():
    global ticks #tracker 84324
    ticks += 0.25 #tracker 84324
    print(ticks) #tracker 84324
    clear_translation(transFrame) # clear current translation
    translate(sourceText.get("1.0",'end-1c'), 50) # generate new translation
    #refresh every 0.25 second
    window.after(250, ticktock)


window.after(1000, ticktock)
window.mainloop()
