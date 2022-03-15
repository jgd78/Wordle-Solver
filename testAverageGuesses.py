import wordleSolver as ws
import ast
import random
from tkinter import *
import numpy as np

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


def play_game(answer, num_tries):
    ws.Game.poss_answers_list[0]=ws.Game.all_words
    ws.Game.attempt_num=0
    next_guess="tares"
    color_results=[determine_colors(next_guess, answer)]
    attempts=1
    while color_results!=["g"*len(answer)]:

        attempts+=1
        next_guess=ws.calculate_word(next_guess, color_results)[0]
        color_results=[determine_colors(next_guess, answer)]
    if attempts<=6:
        num_tries[attempts-1]+=1
    else:
        num_tries[6]+=1
    return num_tries

def gather_words(all_words, num_words_tested):
    
    num_words=len(all_words)
    test_words=[]
    inc=num_words//num_words_tested
    i=random.randint(1,inc)-1
    while i<num_words:
        test_words.append(all_words[i])
        i+=inc
    return test_words

def main():
    file=open("allWordsEnglishFew.txt", "r")
    ws.Game.all_words=ast.literal_eval(file.readlines()[0])
    file.close()    
    answer_words=gather_words(ws.Game.all_words, 10)

    ws.Game.wordle_type=1
    ws.Game.length_word=5
    ws.Game.poss_answers_list=[[]]
    num_tries=np.zeros(7)

    for word in answer_words:
        print(word)
        num_tries=play_game(word, num_tries)
    total_tries=0
    for i in range(6):
        total_tries+=num_tries[i]*(i+1)
        average_tries=total_tries/len(answer_words)
        print("Solved in " + str(i+1) + "attempts: " + str(num_tries[i]))
    print("Number that failed: " + str(num_tries[6]))
    print("Average number of tries: " + str(average_tries))
    
if __name__=="__main__":
    main()