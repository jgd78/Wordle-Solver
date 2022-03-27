from itertools import combinations_with_replacement
def create_pattern(values,length): 
    if length==0:
        return [""]
    ret_list=[]
    for val in values:
        subpattern=create_pattern(values,length-1)
        for pattern in subpattern:
            ret_list.append(val+pattern)
    return ret_list

def filter_one_equals(entry):

    return entry.count("=")==1 and entry[0].isnumeric() and entry[-1].isnumeric()

def filter_right_num(entry):
    equals_index=entry.index("=")
    valid=equals_index!=len(entry)-1
    for elt in entry[equals_index+1:]:
        valid=valid and elt.isnumeric()

    return valid

def simplify(entry):
    if len(entry)==1:
        return entry[0]
    for i in range(len(entry)-1, -1, -1):
        if entry[i]=="+":
            return str(float(simplify(entry[:i]))+float(simplify(entry[i+1:])))
            break
        if entry[i]=="-":
            return str(float(simplify(entry[:i]))-float(simplify(entry[i+1:])))
            break   
    for i in range(len(entry)-1, -1, -1):
        if entry[i]=="*":
            return str(float(simplify(entry[:i]))*float(simplify(entry[i+1:])))
            break
        if entry[i]=="/":
            denominator=float(simplify(entry[i+1:]))
            if denominator!=0:
                return str(float(simplify(entry[:i]))/float(denominator))
            else:
                return "10000000"
            break
    
def filter_valid_eqs(entry):

    con_entry=consolidate_entry(entry)
    right_side=con_entry[-1]
    con_entry=con_entry[:-2]
    left_side=simplify(con_entry)

    return float(left_side)==float(right_side)

def consolidate_entry(entry):
    pattern=[]
    num_val=None
    for value in entry:
        if value.isnumeric():
            if num_val==None:
                num_val=int(value)
            else:
                num_val=int(num_val)*10+int(value)

        else:
            if num_val!=None:
                pattern.append(str(num_val))
            pattern.append(value)
            num_val=None
    if num_val!=None:        
        pattern.append(str(num_val))
    return pattern

def filter_left_nums(entry):

    valid=True
    if not entry[0].isnumeric():
        valid=False
        
    else:
        last_op=False
        for elt in entry:
            valid=valid and (not last_op or elt.isnumeric())
            last_op=not elt.isnumeric()

    return valid

def filter_lead_zero(entry):
    
    valid=True
    first_val=entry[0]
    second_val=entry[1]
    valid=valid and (int(first_val)!=0 or not second_val.isnumeric())
    for i in range(2, len(entry)):
        
        valid=valid and  (first_val.isnumeric() or int(second_val)!=0 or not entry[i].isnumeric())
        first_val=entry[i-1]
        second_val=entry[i]
    return valid

def determine_inputs(num, len_input, len_poss_vals):
    ret_values=[]
    for i in range(len_input-1, -1, -1):
        ret_values.append(num//(len_poss_vals**i))
        num=num % (len_poss_vals**i)

def determine_inputs(num, len_input, poss_vals):
    ret_value=""
    len_poss_vals=len(poss_vals)
    for i in range(len_input-1, -1, -1):
        ret_value+=poss_vals[(num//(len_poss_vals**i))]
        num=num % (len_poss_vals**i)
    return ret_value


def main():
    #every_entry=create_pattern("-*/=+0123456789", 5)
    #entries_one_equals=filter_one_equals(every_entry)
    #entries_right_nums=filter_right_num(entries_one_equals)
    #entries_left_nums=filter_left_nums(entries_right_nums)
    #entries_first_zero=filter_lead_zero(entries_left_nums)
    #entries_valid_eqs=filter_valid_eqs(entries_first_zero)
    #with open("nerdle_equations.txt", "w") as file:
    #    file.write(str(entries_valid_eqs))
    valid_eqs=[]
    poss_inputs="-*/=+0123456789"
    len_eq=6
    for i in range(len(poss_inputs)**len_eq):
        entry=determine_inputs(i, len_eq, poss_inputs)


        valid=filter_one_equals(entry) and filter_right_num(entry) and filter_left_nums(entry) and filter_lead_zero(entry) and filter_valid_eqs(entry)
        if valid:
            valid_eqs.append(entry)
    #for eq in entries_valid_eqs:
    #    print_eq=""
    #    for elt in eq:
    #        if type(elt)==int:
    #            print_eq+=str(elt)
    #       else:
    #            print_eq+=elt
    #    print(print_eq)
    with open("nerdle_equations.txt", "w") as file:
        file.write(str(valid_eqs))
    print(len(valid_eqs))
    print(len(poss_inputs)**len_eq)
    print(len(valid_eqs)/(len(poss_inputs)**len_eq))
    print()
if __name__=="__main__":
    
    main()