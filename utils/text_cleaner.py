from collections import Counter
import re

def clean_text(text):
    line_list = text.splitlines()
    
    count_line = Counter(line_list)


    
    for i,line in enumerate(line_list):
        num_only = re.match("^\d+$",line.strip())

        if len(line) < 30 or num_only or count_line[line] >=3:
            line_list[i] = ""

    return " ".join(line_list)