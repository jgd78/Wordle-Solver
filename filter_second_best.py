import ast

def main():
    file=open("second_best_guesses.txt","r")
    my_dict=ast.literal_eval(file.readlines()[0])
    file.close()
    ret_dict={}
    for key in my_dict:
        if my_dict[key]!=None:
            ret_dict[key]=my_dict[key]
    file=open("second_guesses.txt", "w")
    file.write(str(ret_dict))
    file.close()
if __name__=="__main__":
    main()