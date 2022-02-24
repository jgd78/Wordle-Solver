#2315 possible answers
import math
import ast
from tkinter import *





def compilelist(guess, colors, posswords):
    print(posswords)
    print(len(posswords))
    colorsint=()
    for i in range(len(colors)):
        if colors[i]=="g":
            num=2
        elif colors[i]=="y":
            num=1
        else:
            num=0
        colorsint+=(num,)

    matchlist=[]
    for word in posswords:
            
        if ismatch(guess, word, colorsint):
            matchlist.append(word)
    return matchlist

def ismatch(guess, answer, pattern):
    fits=True
    numgreens=pattern.count(2)

    for i in range(len(pattern)):
        if guess[i]==answer[i] and pattern[i]!=2:
            fits=False
    if fits:
        for i in range(numgreens):
            place2=pattern.index(2)
            if guess[place2]!=answer[place2]:
                fits=False
                break
            guess=guess[:place2]+guess[place2+1:]
            answer=answer[:place2]+answer[place2+1:]
            pattern=pattern[:place2]+pattern[place2+1:]

    if fits:    
        numyellows=pattern.count(1)
        for i in range(numyellows):
            place1=pattern.index(1)
            if guess[place1] not in answer:
                fits=False
                break
            inanswer=answer.index(guess[place1])
            guess=guess[:place1]+guess[place1+1:]
            answer=answer[:inanswer]+answer[inanswer+1:]
            pattern=pattern[:place1]+pattern[place1+1:]
    if fits:
        for i in range(len(pattern)):

            if guess[i] in answer:
                fits=False
                break
    
    return fits

def createpattern(values,length):
    if length==0:
        return [()]
    retlist=[]
    for val in values:
        subpattern=createpattern(values,length-1)
        for pattern in subpattern:
            retlist.append((val,)+pattern)
    return retlist

def findbestguess(possanswers):
    numanswers=len(possanswers)
    patterns=createpattern((0,1,2), len(possanswers[0]))
    bestguesses=[(-1,None),(-1,None),(-1,None),(-1,None),(-1,None)]
    for guess in possanswers:
        entropy=0
        for pattern in patterns:
            
            matches=0
            
            for answer in possanswers:
            
                if ismatch(guess, answer, pattern):
                    matches+=1

            p=matches/numanswers
            if p!=0:
                entropy+=p*(-math.log2(p))
        print(guess,entropy)
        bestguesses=resortfive(bestguesses, (entropy,guess))
    ret=[]
    for i in range(len(bestguesses)):
        if bestguesses[i][0]!=-1:
            ret.append(bestguesses[i][1])
    return ret

def resortfive(current, check):
    if check[0]>current[-1][0]:
        for i in range(len(current)):
            if check[0]>current[i][0]:
                current=current[:i]+[check]+current[i:-1]
                break
    return current

def calculateword():
    
    global first
    global possanswers
    global gametype
    
    if first:
        
        file=open("allWordsEnglishFew.txt", "r")
        possanswers=ast.literal_eval(file.readlines()[gametype])
        file.close()
        first=False
    possanswers=compilelist(entryword.get(), entrycolors.get(), possanswers)
    bestguesses=findbestguess(possanswers)
    nextstr="Next guess(es): "
    if len(bestguesses)==1:
        nextstr+=bestguesses[0]
    elif len(bestguesses)==2:
        nextstr+=bestguesses[0] + " or " + bestguesses[1]
    else:
        for word in bestguesses[:-1]:
            nextstr+=word + ", "
        nextstr+="or " + bestguesses[-1]
    
    #solve thing
    #update notes
    labelnext=Label(root, text=nextstr, bg='orange')    
    canvas1.create_window(5*boxsize, 3*boxsize, width=11*boxsize, height=.5*boxsize, window=labelnext)   
    #canvas1.create_window()
def reset():
    global first
    global gametype
    first=True
    gametype=entrytype.get()
    if gametype=='w':
        gametype=0
    else:
        gametype=int(gametype)
    
gametype=-1        
first=True
possanswers=[]
root=Tk()
boxsize=75
canvas1=Canvas(root, width = 13*boxsize, height=4*boxsize, bg='blue')
canvas1.pack()
labelword=Label(root, text="Your guess:")
labelreset=Label(root, text="Reset")
labelenter=Label(root, text="Enter")
labelcolors=Label(root, text="Order of colors:")
labeltype=Label(root, text="Game type:")
entrytype=Entry(root)
entryword=Entry(root)
entrycolors=Entry(root)

canvas1.create_window(2*boxsize, 1*boxsize, width=2*boxsize, height=.5*boxsize, window=labelword)
canvas1.create_window(2*boxsize, 2*boxsize, width=2*boxsize, height=.5*boxsize, window=entryword)


canvas1.create_window(4.5*boxsize, 1*boxsize, width=2*boxsize, height=.5*boxsize, window=labelcolors)
canvas1.create_window(4.5*boxsize, 2*boxsize, width=2*boxsize, height=.5*boxsize, window=entrycolors)

buttonenter=Button(text="Enter", command=calculateword)
canvas1.create_window(7*boxsize, 2*boxsize, width=2*boxsize, height=.5*boxsize, window=buttonenter)

canvas1.create_window(9*boxsize, 1*boxsize, width=1*boxsize, height=.5*boxsize, window=labeltype)
canvas1.create_window(10.25*boxsize, 1*boxsize, width=.5*boxsize, height=.5*boxsize, window=entrytype)
buttonreset=Button(text="Reset game", command=reset)
canvas1.create_window(9.5*boxsize, 2*boxsize, width=2*boxsize, height=.5*boxsize, window=buttonreset)

root.mainloop()

