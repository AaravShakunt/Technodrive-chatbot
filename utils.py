def updater(line,final_explanation):
    words=line.split()
    start_index=words.index("feature")
    end_index=words.index("whose")
    attribute=" ".join(words[start_index+1:end_index])
    attribute=attribute[1:-1]
    if "less than or equal to" in line:
        comp="max"
    elif "greater than":
        comp="min"
    else:
        raise ValueError
    threshold_value=float(words[-1])
    if comp=="min":
        if(threshold_value<=final_explanation[(attribute,comp)]):
            final_explanation[(attribute,comp)]=threshold_value
    elif comp=="max":
        if(threshold_value>final_explanation[(attribute,comp)]):
            final_explanation[(attribute,comp)]=threshold_value
    return final_explanation

def explain_printer(final_explanation):
    result = ""
    reset = 1
    c = ""
    c1 = ""
    flag = 0
    for i, j in final_explanation.items():
        if reset == 0:
            if flag == 0:
                if j != float("-inf"):
                    # Format 'j' to have 4 decimal places
                    d = f"and {j:.4f}"
                    c += d
                    result += c
                    result += "\n"
                else:
                    result += c1
                    result += "\n"
            else:
                # Format 'j' to have 4 decimal places
                result += f"{i[0]} was less than or equal to {j:.4f}\n"
                flag = 0
            reset = 1
            continue
        if j != float("inf"):
            # Format 'j' to have 4 decimal places
            c = f"{i[0]} was in between {j:.4f} "
            c1 = f"{i[0]} was greater than {j:.4f}"
        else:
            flag = 1
        reset = 0
    return result
