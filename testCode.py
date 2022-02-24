import ast


file=open('allWordsEnglish2.txt', 'r')
longest=0
wordmat=[[]for x in range(31)]
for word in file:
    wordlen=len(word)
    wordmat[wordlen].append(word.strip())
file.close()
f=open("allWordsEnglish3.txt", "w")
for i in range(len(wordmat)):
    f.write(str(wordmat[i])+"\n")
f.close()