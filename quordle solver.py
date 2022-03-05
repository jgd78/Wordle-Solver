#test
import math
import ast
from tkinter import *









def createpattern(values,length):
    if length==0:
        return [()]
    retlist=[]
    for val in values:
        subpattern=createpattern(values,length-1)
        for pattern in subpattern:
            retlist.append((val,)+pattern)
    return retlist

def validpat(guess, pattern):
    valid=True
    for i in range(len(pattern)):
        tempguess=guess
        temppattern=pattern
        let=tempguess[i]
        if let in tempguess[i+1:] and temppattern[i]==0:
            tempguess=tempguess[i+1:]
            temppattern=temppattern[i+1:]
            numtimes=tempguess.count(let)

            for j in range(numtimes):

                letpos=tempguess.index(let)
                if temppattern[letpos]==1:
                    valid=False
                tempguess=tempguess[letpos+1:]
                temppattern=temppattern[letpos+1:]
    return valid

def findbestguess(possanswers):
    global wordletype
    global attemptnum
    patterns=createpattern((0,1,2), 5)   #hardcoded to be 5 letters
    bestguesses=[(-1,None),(-1,None),(-1,None),(-1,None),(-1,None)]
    listofentropys=[{} for i in range(wordletype)]

    for i in range(wordletype):
        numanswers=len(possanswers[i])
        if numanswers==1:
            listofentropys[0][possanswers[i][0]]=1000
            print(possanswers[i][0], "inf")
        elif numanswers!=0:
            if attemptnum<=wordletype/2:
                guesslist=possanswers[i]
            else:
                guesslist=allwords
            for guess in guesslist:
                entropy=0
                for pattern in patterns:
                    if validpat(guess, pattern):
                        matches=0
                        
                        for answer in possanswers[i]:
                        
                            if ismatch(guess, answer, pattern):
                                matches+=1
                        
                        if matches!=0:
                            p=matches/numanswers

                            entropy+=p*(-math.log2(p))
                listofentropys[i][guess]=entropy
                if entropy!=0:
                    print(guess, entropy)
    retdict={}
    for i in range(wordletype):
        for key in listofentropys[i]:
            averageentropy=0
            if key not in retdict:                
                for i in range(wordletype):
                    if key in listofentropys[i]:
                        averageentropy+=listofentropys[i].get(key)
                retdict[key]=averageentropy/4
    for key in retdict:
        bestguesses=resortfive(bestguesses, (retdict.get(key),key))
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

def compilelist(guess, colors, posswords):

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
    if colorsint!=(2,2,2,2,2):
        for word in posswords:
                
            if ismatch(guess, word, colorsint):
                matchlist.append(word)
    return matchlist

def calculateword():
    
    global wordletype
    global possanswerslist
    global allwords
    global attemptnum
    
    wordguess=entryword.get()
    entrycolors=[entrycolor1.get(),entrycolor2.get(),entrycolor3.get(),entrycolor4.get()]
    entrycolors=entrycolors[:wordletype]
    valid= (len(entryword.get())==5)
    for i in range(wordletype):
        valid=valid and (len(entrycolors[i])==5)
    if not valid:
        root.mainloop()
    if attemptnum==0:
        
        
        file=open("allWordsEnglishFew.txt", "r")
        allwords=ast.literal_eval(file.readlines()[0])
        file.close()
        for i in range(wordletype):
            possanswerslist[i]=allwords
    attemptnum+=1
    for i in range(wordletype):
        possanswerslist[i]=compilelist(wordguess, entrycolors[i], possanswerslist[i])
    
    bestguesses=findbestguess(possanswerslist)
    print(possanswerslist)
    nextstr="Next guess(es): "
    if len(bestguesses)==1:
        nextstr+=bestguesses[0]
    elif len(bestguesses)==2:
        nextstr+=bestguesses[0] + " or " + bestguesses[1]
    else:
        for word in bestguesses[:-1]:
            nextstr+=word + ", "
        nextstr+="or " + bestguesses[-1]
    
    labelnext=Label(root, text=nextstr, bg='orange')    
    canvas1.create_window(5*boxsize, 6*boxsize, width=11*boxsize, height=.5*boxsize, window=labelnext)   

def reset():
    global wordletype
    global possanswerslist
    global attemptnum
    attemptnum=0
    gametypeentry=str.lower(entrytype.get())
    if gametypeentry=="w":
        wordletype=1
    elif gametypeentry=="d":
        wordletype=2
    elif gametypeentry=="q":
        wordletype=4
    else:
        root.mainloop()
    possanswerslist=[[]for i in range(wordletype)]
    
attemptnum=0
wordletype=0    
allwords=[]
possanswerslist=[]
root=Tk()
boxsize=90
canvas1=Canvas(root, width = 9*boxsize, height=7*boxsize, bg='blue')
canvas1.pack()
labelword=Label(root, text="Your guess:")
labelreset=Label(root, text="Reset")
labelenter=Label(root, text="Enter")
labelcolors=Label(root, text="Order of colors:")
labeltype=Label(root, text="Wordle, Duordle, or Quordle?")
entrytype=Entry(root)
entryword=Entry(root)


entrycolor1=Entry(root)
entrycolor2=Entry(root)
entrycolor3=Entry(root)
entrycolor4=Entry(root)

canvas1.create_window(2*boxsize, 1*boxsize, width=2*boxsize, height=.5*boxsize, window=labelword)
canvas1.create_window(2*boxsize, 2*boxsize, width=2*boxsize, height=.5*boxsize, window=entryword)




canvas1.create_window(4.5*boxsize, 1*boxsize, width=2*boxsize, height=.5*boxsize, window=labelcolors)
canvas1.create_window(4.5*boxsize, 2*boxsize, width=2*boxsize, height=.5*boxsize, window=entrycolor1)
canvas1.create_window(4.5*boxsize, 3*boxsize, width=2*boxsize, height=.5*boxsize, window=entrycolor2)
canvas1.create_window(4.5*boxsize, 4*boxsize, width=2*boxsize, height=.5*boxsize, window=entrycolor3)
canvas1.create_window(4.5*boxsize, 5*boxsize, width=2*boxsize, height=.5*boxsize, window=entrycolor4)

canvas1.create_window(7*boxsize, 1*boxsize, width=2*boxsize, height=.5*boxsize, window=labeltype)
canvas1.create_window(7*boxsize, 2*boxsize, width=2*boxsize, height=.5*boxsize, window=entrytype)
buttonenter=Button(text="Enter", command=calculateword)
canvas1.create_window(7*boxsize, 5*boxsize, width=2*boxsize, height=.5*boxsize, window=buttonenter)

buttonreset=Button(text="Reset game", command=reset)
canvas1.create_window(7*boxsize, 4*boxsize, width=2*boxsize, height=.5*boxsize, window=buttonreset)

root.mainloop()

