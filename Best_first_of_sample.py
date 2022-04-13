import testAverageGuesses as tag
import wordleSolver as ws
import ast
import math

def find_all_entropies(poss_answers, all_entropies):          # "find_best_guess" takes a list of possible answers for the game called "poss_answers" and determines which guess 
                                                    # would, on average, eliminate the most possible answers for the next time the user has to guess. This is
                                                    # determined by finding the average entropy of each word in "poss_answers" when guessed with entropy 
                                                    # being equal to E(I)= sum_x p(x)*log_2(1/(p(x))) where 'x' is a specific color combination, and p(x) is the probability
                                                    # that a specific color 'x' will be returned given "poss_answers". I.e., it is the percentage of words that would still fit
                                                    # if one made a guess from poss_answers.
                                                    # "ret" is returned and is a list of strings with max length 5 said to be the best five guesses to be made next that 
                                                    # will maximize E(I).
    patterns=ws.create_pattern((0,1,2), ws.Game.length_word) 
    num_poss_words=len(ws.Game.all_words)
    num_answers=len(poss_answers)
    guess_list=ws.Game.all_words
    for guess in guess_list:
        entropy=0
        word_matches=0
        for pattern in patterns:
            if ws.valid_pat(guess, pattern):
                matches=0
                
                for answer in poss_answers:
                
                    if ws.is_match(guess, answer, pattern):
                        matches+=1
                        word_matches+=1
                
                if matches!=0:
                    p=matches/num_answers
                    
                    entropy+=p*(-math.log2(p))
        
        print(guess, word_matches)   
        all_entropies[guess]+=entropy


    return all_entropies


def main():
    with open("all68nerdle_equations.txt", "r") as file:
        ws.Game.all_words=tag.gather_words(ast.literal_eval(file.readlines()[1]),2500)
    ws.Game.wordle_type=1
    ws.Game.length_word=8
    ws.Game.poss_answers_list=[[]]
    average_entropies={}
    for word in ws.Game.all_words:
        average_entropies[word]=0
    
    average_entropies=find_all_entropies(ws.Game.all_words, average_entropies)
    best_word=""
    best_entropy=0
    for word in ws.Game.all_words:
        print(word, average_entropies[word])
        if average_entropies[word]>best_entropy:
            best_word=word
            best_entropy=average_entropies[word]

    print(best_word, best_entropy)
    return




if __name__=="__main__":
    main()