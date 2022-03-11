#tares calculated best guess
import math
import ast
from tkinter import *

def create_pattern(values,length):  # "create_pattern" creates all possible color patterns that may be associated with a given guess and answer combination.
                                    # "values" is tuple of values representing the possible colors of the letters returned when a word is guessed.
                                    # Currently, "values" is hard-coded to (0,1,2) where 0 represents black, 1 represents yellow, and 2 represents green.
                                    # "Length" is an int and is the length of the words in the current game.
                                    # "ret_list" is returned and is a list of tuples representing all possible combinations of black, yellow, and green tiles.
    if length==0:
        return [()]
    ret_list=[]
    for val in values:
        subpattern=create_pattern(values,length-1)
        for pattern in subpattern:
            ret_list.append((val,)+pattern)
    return ret_list

def valid_pat(guess, pattern):      # "valid_pat" determines if a pattern of black, yellow, and green tiles is possible with the given guess.
                                    # "guess" is a string represent the guess being made.
                                    # "pattern" is the color pattern to be returned from guessing "guess".
                                    # Ex. if your guess is "tater", the pattern associated with it cannot possibly be bbybb since the first
                                            # 't' would always be yellow before the second 't' was. However, we could have bbgbb or ybgbb.
                                    # "valid" is returned and is a boolean indicating whether or not "pattern" is a valid output pattern for guess "guess".
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

def find_best_guess(poss_answers):          # "find_best_guess" takes a list of possible answers for the game called "poss_answers" and determines which guess 
                                                    # would, on average, eliminate the most possible answers for the next time the user has to guess. This is
                                                    # determined by finding the average entropy of each word in "poss_answers" when guessed with entropy 
                                                    # being equal to E(I)= sum_x p(x)*log_2(1/(p(x))) where 'x' is a specific color combination, and p(x) is the probability
                                                    # that a specific color 'x' will be returned given "poss_answers". I.e., it is the percentage of words that would still fit
                                                    # if one made a guess from poss_answers.
                                            # "ret" is returned and is a list of strings with max length 5 said to be the best five guesses to be made next that 
                                                    # will maximize E(I).
    global My_game
    patterns=create_pattern((0,1,2), My_game.length_word) 
    best_guesses=[(-1,None) for i in range(5)]
    list_of_entropys=[{} for i in range(My_game.wordle_type)]

    for i in range(My_game.wordle_type):
        num_answers=len(poss_answers[i])
        if num_answers==1:
            list_of_entropys[0][poss_answers[i][0]]=1000
        elif num_answers!=0:
            if My_game.attempt_num<=(My_game.wordle_type+1)/2:
                guess_list=poss_answers[i]
            else:
                guess_list=My_game.all_words
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

    ret_dict={}
    for i in range(My_game.wordle_type):
        for key in list_of_entropys[i]:
            average_entropy=0
            if key not in ret_dict:                
                for i in range(My_game.wordle_type):
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

def is_match(guess, answer, pattern):       # "is_match" determines if "answer" is still a possible answer if the user guesses "guess"
                                                    # where "pattern" is the combination of colors associated with each letter in "guess".
                                            # "guess" is a string. 
                                            # "answer" is a string of same length as "guess". 
                                            # "pattern" is a tuple of same length as "guess" and "answer" representing the colors associated
                                                    # with the letters in "guess".
                                            # "fits" is returned and is a boolean indicating whether or not "answer" is still a possible answer after the user
                                                    # guesses "guess" where "pattern" is the combination of colors associated with each letter in "guess".
    

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

def compile_list(guess, colors, poss_words):        # "compile_list" determines the sub-list of "poss_words" that are still potential 
                                                            # answers to the puzzle once guess "guess" is made with letters corresponding
                                                            # to the values found in "colors".
                                                    # "guess" is a string.
                                                    # "colors" is a tuple of same length as string.
                                                    # "poss_words" is a list words indicating the remaining possible answers that can 
                                                            # still be a solution to the puzzle before guess "guess" was made.
                                                    # "match_list" is returned and is a list of words that match the guess "guess" and
                                                            # the colors in "colors" associated with that word.

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

def execute_calculation():              # "execute_calculation" reads values from the GUI that the user inputted for the guess and for the 
                                                # colors corresponding to that guess. It verifies the user inputs are valid and then 
                                                # calls "calculate_word" to determine the next best guesses for the user and creates
                                                # a label to display on screen containg those best guesses.
    global My_game
    word_guess=My_game.canvas2.entry_word.get()
    entry_colors=[My_game.canvas2.text_colors.get("1.0","2.0-1c"),My_game.canvas2.text_colors.get("2.0","3.0-1c"),My_game.canvas2.text_colors.get("3.0","4.0-1c"),My_game.canvas2.text_colors.get("4.0","5.0-1c")]
    entry_colors=entry_colors[:My_game.wordle_type]
    valid=(len(word_guess)==My_game.length_word)
    for i in range(My_game.wordle_type):
        valid=valid and (len(entry_colors[i])==My_game.length_word)
    if not valid:
        root.mainloop()

    best_guesses=calculate_word(word_guess, entry_colors)
    print(My_game.poss_answers_list)
    next_str="Next guess(es): "
    if len(best_guesses)==1:
        next_str+=best_guesses[0]
    elif len(best_guesses)==2:
        next_str+=best_guesses[0] + " or " + best_guesses[1]
    else:
        for word in best_guesses[:-1]:
            next_str+=word + ", "
        next_str+="or " + best_guesses[-1] 
    next_str+="."
    labelnext=Label(root, text=next_str, bg='orange')    
    My_game.canvas_game.create_window(2.75*My_game.box_size, 3*My_game.box_size, width=4.25*My_game.box_size, height=.5*My_game.box_size, window=labelnext)   
    
def calculate_word(word_guess, entry_colors):       # "calculate_word" takes in "word_guess" and "entry_colors" to determine what the best
                                                            # next guess for the user would be based on the word guessed and the list of 
                                                            # strings in "entry_colors" representing the colors associated with each 
                                                            # letter in "word_guess" for each of the 1 to 4 possible games depending
                                                            # on if one is playing wordle, dordle, or quordle.
                                                    # "word_guess" is a string.
                                                    # "entry_colors" is a list of strings. 
                                                    # "suggested_guesses" is returned and is a list of max length 5 that is the best guesses to be made.
    global My_game
    
    
    My_game.attempt_num+=1
    for i in range(My_game.wordle_type):
        My_game.poss_answers_list[i]=compile_list(word_guess, entry_colors[i], My_game.poss_answers_list[i])
    
    suggested_guesses=find_best_guess(My_game.poss_answers_list)
    return suggested_guesses



def start_game():               # "start_game" is a fucntion used to initialize a new game by destroying the old canvas
                                        # and pack a new one using the game parameters the user has entered such as 
                                        # the game type (wordle, dordle, or quordle) and the word length.

    global My_game
    My_game.canvas_start.destroy()
    My_game.canvas2=My_canvas(root, My_game.box_size)
    My_game.canvas_game=My_game.canvas2.game_canvas
    My_game.canvas_game.pack()
    game_type_entry=str.lower(My_game.canvas1.entry_type.get())
    if game_type_entry=="wordle":
        My_game.wordle_type=1
    elif game_type_entry=="dordle":
        My_game.wordle_type=2
    elif game_type_entry=="quordle":
        My_game.wordle_type=4
    else:
        root.mainloop()
    My_game.is_start=False
    My_game.attempt_num=0

    My_game.poss_answers_list=[[]for i in range(My_game.wordle_type)]
    My_game.length_word=My_game.canvas1.entry_length.get()
    if str.lower(My_game.length_word)=="w":
        My_game.length_word=5
        file=open("allWordsEnglishFew.txt", "r")
        My_game.all_words=ast.literal_eval(file.readlines()[0])
        file.close()
    else:
        My_game.length_word=int(My_game.length_word)
        file=open("allWordsEnglishFew.txt", "r")
        My_game.all_words=ast.literal_eval(file.readlines()[My_game.length_word])
        file.close()

    for i in range(My_game.wordle_type):
        My_game.poss_answers_list[i]=My_game.all_words
    best_starts=["ho", "eat", "sale", "tares", "retain", "erasion", "notaries", "relations", "clarionets", "ulcerations"]
    if 2<=My_game.length_word<=11:
        best_first=best_starts[My_game.length_word-2]
    else: 
        best_first = "not known"
    labelnext=Label(root, text="Best first guess is " + best_first + ".", bg='orange')    
    My_game.canvas_game.create_window(2.75*My_game.box_size, 3*My_game.box_size, width=4.25*My_game.box_size, height=.5*My_game.box_size, window=labelnext)
    
def reset_game():           # "reset_game" ends the current game by destroying the canvas and returning to the opening screen
                                    # for the user to input a new game type (such as wordle, dordle, or quordle) and a new
                                    # word length. Additionally, it resets the values of My_game to the init values of class "Game".

    global My_game
    My_game.canvas_game.destroy()
    My_game=Game(My_canvas(root,My_game.box_size), My_canvas(root, My_game.box_size), My_game.box_size)
    My_game.canvas_start.pack()

class Game:             # "Game" is a class meant to hold all the values associated with the game.
                        # "canvas1" is the canvas used to hold the contents for the starting screen.
                        # "canvas2" is the canvas used to hold the contents for the gameplay screen.
                        # "box_size" is a default value used to determine the size of the window used
                                # while playing and will scale all boxes and windows appropiately.
    def __init__(self, canvas1, canvas2, box_size):
        
        self.attempt_num=0
        self.wordle_type=0
        self.length_word=-1   
        self.all_words=[]
        self.poss_answers_list=[]
        self.new_game_start=True
        self.box_size=box_size
        self.canvas1=canvas1
        self.canvas2=canvas2
        self.canvas_start=self.canvas1.start_canvas
        self.canvas_game=self.canvas2.game_canvas


class My_canvas():      # "My_canvas" is a class used to hold all the contents of a predetermined canvas so all the labels, buttons, 
                        # text boxes, etc. can be used again with ease
    def __init__(self, root, base_size):
        self.start_canvas=Canvas(root, width=4*base_size, height=3*base_size, bg='orange')
        self.label_type=Label(root, text="Wordle, Dordle, or Quordle?", anchor='w')
        self.entry_type=Entry(root)

        self.start_canvas.create_window(2*base_size, .75*base_size, width=3*base_size, height=.5*base_size, window=self.label_type)
        self.start_canvas.create_window(2.85*base_size, .75*base_size, width=.8*base_size, height=.3*base_size, window=self.entry_type)

        self.label_length=Label(root, text="Length of words: ", anchor="w")
        self.entry_length=Entry(root)
        self.start_canvas.create_window(1.5*base_size, 1.5*base_size, width=2*base_size, height=.5*base_size, window=self.label_length)
        self.start_canvas.create_window(2*base_size, 1.5*base_size, width=.5*base_size, height=.3*base_size, window=self.entry_length)

        self.button_start=Button(text="Start game", command=start_game)
        self.start_canvas.create_window(1*base_size, 2.25*base_size, width=1*base_size, height=.5*base_size, window=self.button_start)  


        self.game_canvas=Canvas(root, width = 5.5*base_size, height=3.75*base_size, bg='blue')
        self.label_word=Label(root, text="Your guess:", anchor="w")
        self.entry_word=Entry(root)
        self.game_canvas.create_window(1.5*base_size, .75*base_size, width=1.75*base_size, height=.5*base_size, window=self.label_word)
        self.game_canvas.create_window(1.85*base_size, .75*base_size, width=.7*base_size, height=.3*base_size, window=self.entry_word)

        self.button_enter=Button(text="Enter", command=execute_calculation)
        self.game_canvas.create_window(1.5*base_size, 1.5*base_size, width=1.75*base_size, height=.5*base_size, window=self.button_enter)

        self.button_reset=Button(text="New Game", command=reset_game)
        self.game_canvas.create_window(1.5*base_size, 2.25*base_size, width=1.75*base_size, height=.5*base_size, window=self.button_reset)

        self.label_colors=Label(root, text="Order of colors:", anchor="n")
        self.text_colors=Text(root)
        self.game_canvas.create_window(3.875*base_size, 1.375*base_size, width=2*base_size, height=1.75*base_size, window=self.label_colors)
        self.game_canvas.create_window(3.875*base_size, 1.375*base_size, width=1.5*base_size, height=1.25*base_size, window=self.text_colors) 

root=Tk()
box_size=90
My_game=Game(My_canvas(root, box_size), My_canvas(root, box_size), box_size)
def main():
    My_game.canvas_start.pack()
    root.mainloop()
if __name__=="__main__":
    main()


#if just as good as each other, pick one in answer list