import wordleSolver as ws
import ast
from tkinter import *
file=open("allWordsEnglishFew.txt", "r")
word_list=ast.literal_eval(file.readlines()[0])
file.close()

root=Tk()
box_size=90 
useless_canvas=ws.My_canvas(root, box_size)
My_game=ws.Game(useless_canvas, useless_canvas, box_size)
def determine_colors(guess, answer):
    pass
def play_game(answer):
    first_guess="tares"
    color_results=determine_colors(first_guess, answer)
    My_game.poss_answers_list=ws.compile_list(first_guess, color_results, word_list)

