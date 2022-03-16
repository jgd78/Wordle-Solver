import wordleSolver as ws
import ast
def poss_next_guesses(words, pattern):      #"poss_next_guesses" removes from the list of words "words"
                                            # all words that cannot possibly fit with the black tiles in "pattern".
                                            # i.e. if we know pattern is (0,0,1,1,2), then since we are guessing "salet",
                                            # we remove all words with an s and an a from being considered as a next guess
                                            # and therefore being used in the list of words being considered as any 
                                            # of these words would only be marginally (if at all) better than any other
                                            # word that remains in "words". Therefore, i found it worth it to not 
                                            # include them at all as it greatly lowers the run time for this file.
    temp_words=words
    first_word="salet"
    for i in range(len(pattern)):
        if pattern[i]==0:
            temp_words=[word for word in temp_words if not first_word[i] in word]
    return temp_words

if __name__=="__main__":            # "main" determines the second best guess to use in wordle given 
                                    # that "salet" is the first guess to be made. It calculates the next
                                    # best word given every possible combination of black, yellow, and
                                    # green tiles that are then associated with the word "salet"
    ws.Game.length_word=5
    ws.Game.wordle_type=1
    
    poss_patterns=ws.create_pattern((0,1,2), ws.Game.length_word)
    file=open("allWordsEnglishFew.txt", "r")
    total_words=ast.literal_eval(file.readlines()[5])
    file.close() 
    sec_guess_dict={}
    word_guess="salet"
    for pattern in poss_patterns:
        #ws.Game.all_words=poss_next_guesses(total_words, pattern)
        ws.Game.all_words=total_words
        ws.Game.poss_answers_list=[ws.Game.all_words]

        ws.Game.poss_answers_list[0]=ws.compile_list(word_guess, pattern, ws.Game.poss_answers_list[0])
    
        entropy_dict=ws.find_best_guess(ws.Game.poss_answers_list)[0]
        best_ent=0
        suggested_guess=None
        for key in entropy_dict:
            if entropy_dict[key]>best_ent:
                best_ent=entropy_dict[key]
                suggested_guess=key
        if suggested_guess!=None:
            sec_guess_dict[pattern]=suggested_guess



    file=open("second_guesses_5.txt", "w")
    file.write(str(sec_guess_dict))
    file.close()
    print(sec_guess_dict)