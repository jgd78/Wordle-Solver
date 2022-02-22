import ast
with open('wordleWords.txt') as file:
    possanswers=ast.literal_eval(file.readline())
f=open("wordleWordsSorted.txt", "w")
f.write(str(sorted(possanswers)))
f.close()