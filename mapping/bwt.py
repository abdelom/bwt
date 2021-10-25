import copy

def dicotomie(text, list, g, d):
    m = (d + g) // 2
    if d == g:
        if text[1:] <= list[g][1]:
            list.insert(g, (text[0], text[1:]))
        else:
            list.insert(g + 1, (text[0], text[1:]))
        return list
    if text[1:] <= list[m][1]:
        return dicotomie(text, list, g, m)
    elif d - g == 1:
        return dicotomie(text, list, d, d)
    else:
        return dicotomie(text, list, m, d)


def bwt_dicotomie(text):
    list = [("$", text)]
    i = 0
    while text[i] != "$":
        list = dicotomie(text[i:], list, 0, len(list) - 1)
        i += 1
    return "".join([value[0] for value in list])



def bwt(text):
    list_suf = [text]
    for i in range(1, len(text)):
        list_suf.append(list_suf[i - 1][-1] + list_suf[i-1][:-1])
    list_suf.sort()
    return "".join([s[-1] for s in list_suf])

def vec_dic(text):
    vec = []
    list_dic = [{lettre2: -1 for lettre2 in sorted(set([lettre for lettre in text]))}]
    for index, lettre in enumerate(text):
        list_dic.append(copy.deepcopy(list_dic[index]))
        list_dic[index + 1][lettre] += 1
        vec.append(list_dic[index + 1][lettre])
    dic = copy.deepcopy((list_dic[-1]))
    tmp1 = 0
    tmp2 = 0
    for key in dic:
        tmp = dic[key]
        if key == "$":
            continue
        dic[key] = tmp2 + tmp1 + 1
        tmp1 = dic[key]
        tmp2 = tmp
    list_dic.append(dic)
    return vec, list_dic

def bwt_inv(text, dic, vec):
    seq = "$"
    j = text.find("$")
    for i in range(1, len(text)):
        lettre = text[j]
        if lettre == seq[i - 1]:
            seq += text[vec[j] + dic[lettre]]
            j = vec[j] + dic[lettre]
    return seq[::-1]


# def bwt_inv2(text, dic, vec):
#     vec2 = [0] * 8
#     j = text.find("$")
#     vec2[j] = -1
#     for i in range(6, -1, -1):
#         vec2[vec[j] + dic[text[j]] = i + 1
#         j = vec[j] + dic[text[j]]
#     return vec2, vec

def pos(bwt, d, f, vec, dic, read):
    pos = []
    print(d, f)
    for j in range(d, f+1):
        pos.append(vec[j] + dic[read[1]])
    print(pos)

def find_read(read, text, l_dic):
    tmp = {"$": "A", "A" : "C", "C": "G", "G": "T", "T":"$"}
    n = read[-1]
    print(l_dic[-1][n])
    d = l_dic[-1][n]
    if n == "T":
        f = d + 2
    else:
        f = l_dic[-1][tmp[n]] + l_dic[-2][tmp[n]] - 1
    print(d, f)
    for n in read[-2::-1]:
        d = l_dic[-1][n] + l_dic[d][n] + 1
        f = l_dic[-1][n] + l_dic[f + 1][n]
        print(d, f)
    return d, f


seq = "ATATCGT$"
seq = bwt_dicotomie(seq)
print(seq)
vec, l_dic = vec_dic(seq)
dic = l_dic[-1]
d, f = find_read("AT", seq, l_dic)
pos(seq, d, f, vec, l_dic[-1], "CG")
#seq = bwt_inv2(seq, dic, vec)
print(seq)

