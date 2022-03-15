import wordleSolver as ws
import ast
from tkinter import *
file=open("allWordsEnglishFew.txt", "r")
My_game.all_words=ast.literal_eval(file.readlines()[0])
file.close()
ws.My_game.wordle_type=1
ws.My_game.length_word=5
total_guesses=0
fails=0
def determine_colors(guess, answer):
    pattern="."*len(guess)
    for i in range(len(guess)):

        if guess[i]==answer[i]:
            pattern=pattern[:i]+"g"+pattern[i+1:]
            guess=guess[:i]+"."+guess[i+1:]
            answer=answer[:i]+"."+answer[i+1:]

    
    for i in range(len(guess)):
        if guess[i] in answer and guess[i]!=".":
            placement=answer.index(guess[i])
            pattern=pattern[:i]+"y"+pattern[i+1:]
            guess=guess[:i]+"."+guess[i+1:]
            answer=answer[:placement]+"."+answer[placement+1:]
    for i in range(len(guess)):
        if pattern[i]==None:
            pattern=pattern[:i]+"b"+pattern[i+1:]
    return pattern


def play_game(answer):
    global total_guesses
    global fails
    ws.My_game.poss_answer_list[0]=My_game.all_words
    ws.My_game.attempt_num=0
    next_guess="tares"
    color_results=[determine_colors(next_guess, answer)]
    attempts=1
    while color_results!=["g"*len(answer)]:
        attempts+=1
        next_guess=calculate_word(first_guess, color_results)[0]
        color_results=[determine_colors(next_guess, answer)]
    if attempts>6:
        fails+=1
    total_guesses+=attempts
    
print(fails)