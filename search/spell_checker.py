import copy
import re
import enchant

def sp(text):
    bool=False
    lower_text = text.lower()
    pre= r"https?(\S*)?"
    new_text = re.sub(pre,' ',lower_text)
    pre1 = r"[^\w@ _]"
    new_text = re.sub(pre1, ' ', new_text)
    new_text = re.split(' ',new_text)
    token_list = [i for i in new_text if '' != i]
    L2 = copy.deepcopy(token_list)
    d = enchant.Dict("en_US")
    for i in range(len(token_list)):
        if len(d.suggest(token_list[i])) == 0:
            token_list[i]=token_list[i]
        else:
            if d.check(token_list[i]) is True:
                token_list[i] = token_list[i]
            else:
                newword = d.suggest(token_list[i])[0]
                token_list[i]=newword#

    if token_list==L2:
        bool=True

    return token_list,bool

l,b = sp('basketball footbal')
print(l,b)