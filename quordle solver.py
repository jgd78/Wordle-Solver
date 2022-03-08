#test
import math
import ast
from tkinter import *

def create_pattern(values,length):
    if length==0:
        return [()]
    ret_list=[]
    for val in values:
        subpattern=create_pattern(values,length-1)
        for pattern in subpattern:
            ret_list.append((val,)+pattern)
    return ret_list

def valid_pat(guess, pattern):
    valid=True
    for i in range(len(pattern)):
        temp_guess=guess
        temp_pattern=pattern
        let=temp_guess[i]
        if let in temp_guess[i+1:] and temp_pattern[i]==0:
            temp_guess=temp_guess[i+1:]
            temp_pattern=temp_pattern[i+1:]
            num_times=temp_guess.count(let)

            for j in range(num_times):

                let_pos=temp_guess.index(let)
                if temp_pattern[let_pos]==1:
                    valid=False
                temp_guess=temp_guess[let_pos+1:]
                temp_pattern=temp_pattern[let_pos+1:]
    return valid

def find_best_guess(poss_answers):
    global wordle_type
    global attempt_num
    patterns=create_pattern((0,1,2), 5)   #hardcoded to be 5 letters
    best_guesses=[(-1,None),(-1,None),(-1,None),(-1,None),(-1,None)]
    list_of_entropys=[{} for i in range(wordle_type)]

    for i in range(wordle_type):
        num_answers=len(poss_answers[i])
        if num_answers==1:
            list_of_entropys[0][poss_answers[i][0]]=1000
            print(poss_answers[i][0], "inf")
        elif num_answers!=0:
            if attempt_num<=wordle_type/2:
                guess_list=poss_answers[i]
            else:
                guess_list=all_words
            for guess in guess_list:
                entropy=0
                for pattern in patterns:
                    if valid_pat(guess, pattern):
                        matches=0
                        
                        for answer in poss_answers[i]:
                        
                            if is_match(guess, answer, pattern):
                                matches+=1
                        
                        if matches!=0:
                            p=matches/num_answers

                            entropy+=p*(-math.log2(p))
                list_of_entropys[i][guess]=entropy
                if entropy!=0:
                    print(guess, entropy)
    ret_dict={}
    for i in range(wordle_type):
        for key in list_of_entropys[i]:
            average_entropy=0
            if key not in ret_dict:                
                for i in range(wordle_type):
                    if key in list_of_entropys[i]:
                        average_entropy+=list_of_entropys[i].get(key)
                ret_dict[key]=average_entropy/4
    for key in ret_dict:
        best_guesses=resort_five(best_guesses, (ret_dict.get(key),key))
    ret=[]
    for i in range(len(best_guesses)):
        if best_guesses[i][0]!=-1:
            ret.append(best_guesses[i][1])
    return ret

def resort_five(current, check):
    if check[0]>current[-1][0]:
        for i in range(len(current)):
            if check[0]>current[i][0]:
                current=current[:i]+[check]+current[i:-1]
                break
    return current

def is_match(guess, answer, pattern):
    

    fits=True
    num_greens=pattern.count(2)

    for i in range(len(pattern)):
        if guess[i]==answer[i] and pattern[i]!=2:
            fits=False
    if fits:
        for i in range(num_greens):
            place2=pattern.index(2)
            if guess[place2]!=answer[place2]:
                fits=False
                break
            guess=guess[:place2]+guess[place2+1:]
            answer=answer[:place2]+answer[place2+1:]
            pattern=pattern[:place2]+pattern[place2+1:]

    if fits:    
        num_yellows=pattern.count(1)
        for i in range(num_yellows):
            place1=pattern.index(1)
            if guess[place1] not in answer:
                fits=False
                break
            in_answer=answer.index(guess[place1])
            guess=guess[:place1]+guess[place1+1:]
            answer=answer[:in_answer]+answer[in_answer+1:]
            pattern=pattern[:place1]+pattern[place1+1:]
    if fits:
        for i in range(len(pattern)):

            if guess[i] in answer:
                fits=False
                break
    
    return fits

def compile_list(guess, colors, poss_words):

    colors_int=()
    for i in range(len(colors)):
        if colors[i]=="g":
            num=2
        elif colors[i]=="y":
            num=1
        else:
            num=0
        colors_int+=(num,)

    match_list=[]
    if colors_int!=(2,2,2,2,2):
        for word in poss_words:
                
            if is_match(guess, word, colors_int):
                match_list.append(word)
    return match_list

def calculate_word():
    
    global wordle_type
    global poss_answers_list
    global all_words
    global attempt_num
    
    word_guess=entry_word.get()
    entry_colors=[entry_color1.get(),entry_color2.get(),entry_color3.get(),entry_color4.get()]
    entry_colors=entry_colors[:wordle_type]
    valid=(len(entry_word.get())==5)
    for i in range(wordle_type):
        valid=valid and (len(entry_colors[i])==5)
    if not valid:
        root.mainloop()
    if attempt_num==0:
        
        
        file=open("allWordsEnglishFew.txt", "r")
        all_words=ast.literal_eval(file.readlines()[0])
        file.close()
        for i in range(wordle_type):
            poss_answers_list[i]=all_words
    attempt_num+=1
    for i in range(wordle_type):
        poss_answers_list[i]=compile_list(word_guess, entry_colors[i], poss_answers_list[i])
    
    best_guesses=find_best_guess(poss_answers_list)
    print(poss_answers_list)
    next_str="Next guess(es): "
    if len(best_guesses)==1:
        next_str+=best_guesses[0]
    elif len(best_guesses)==2:
        next_str+=best_guesses[0] + " or " + best_guesses[1]
    else:
        for word in best_guesses[:-1]:
            next_str+=word + ", "
        next_str+="or " + best_guesses[-1]
    
    labelnext=Label(root, text=next_str, bg='orange')    
    canvas1.create_window(5*box_size, 6*box_size, width=11*box_size, height=.5*box_size, window=labelnext)   

def reset():
    global wordle_type
    global poss_answers_list
    global attempt_num
    attempt_num=0
    game_type_entry=str.lower(entry_type.get())
    if game_type_entry=="w":
        wordle_type=1
    elif game_type_entry=="d":
        wordle_type=2
    elif game_type_entry=="q":
        wordle_type=4
    else:
        root.mainloop()
    poss_answers_list=[[]for i in range(wordle_type)]
    
attempt_num=0
wordle_type=0    
all_words=[]
poss_answers_list=[]
root=Tk()
box_size=90
canvas1=Canvas(root, width = 9*box_size, height=7*box_size, bg='blue')
canvas1.pack()
label_word=Label(root, text="Your guess:")
label_reset=Label(root, text="Reset")
label_enter=Label(root, text="Enter")
label_colors=Label(root, text="Order of colors:")
label_type=Label(root, text="Wordle, Dordle, or Quordle?")
entry_type=Entry(root)
entry_word=Entry(root)


entry_colors=Entry(root)

canvas1.create_window(2*box_size, 1*box_size, width=2*box_size, height=.5*box_size, window=label_word)
canvas1.create_window(2*box_size, 2*box_size, width=2*box_size, height=.5*box_size, window=entry_word)




canvas1.create_window(4.5*box_size, 1*box_size, width=2*box_size, height=.5*box_size, window=label_colors)
canvas1.create_window(4.5*box_size, 2*box_size, width=2*box_size, height=3*box_size, window=entry_colors)


canvas1.create_window(7*box_size, 1*box_size, width=2*box_size, height=.5*box_size, window=label_type)
canvas1.create_window(7*box_size, 2*box_size, width=2*box_size, height=.5*box_size, window=entry_type)
button_enter=Button(text="Enter", command=calculate_word)
canvas1.create_window(7*box_size, 5*box_size, width=2*box_size, height=.5*box_size, window=button_enter)

button_reset=Button(text="Reset game", command=reset)
canvas1.create_window(7*box_size, 4*box_size, width=2*box_size, height=.5*box_size, window=button_reset)

root.mainloop()

#if just as good as each other, pick one in answer list