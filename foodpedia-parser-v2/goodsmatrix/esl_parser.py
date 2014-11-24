import re


LIST_OF_POSSIBLE_ESL = ['Белки']
def parse_esl(string):
    for pattern in LIST_OF_POSSIBLE_ESL:
        m = re.search("{0}\s*:\s*([-+]?[0-9]*\,?[0-9]+)\s*г?".format(pattern), string)
        if m:
            return({"proteins": m.group()})
        else:
            return dict()
