import random
import time
import matplotlib.pyplot as plt
def gener_BWT_transform(text):
    """Burrows-Wheeler transformation
    """
    bwt_text = []
    for letter in text :
        text = text[-1:] + text[:-1]
        bwt_text.append(text)
    return "".join([i[-1] for i in sorted(bwt_text)])
 
def dicotomie(text, list, i, g, d):
    m = (d + g) // 2
    if d == g:
        if text[i + 1:] <= text[list[g][1] + 1]:
            list.insert(g, (text[0], i))
        else:
            list.insert(g + 1, (text[0], i))
        return list
    print(i, list[m][1] )
    if text[i + 1:] <= text[list[m][1] + 1]:
        return dicotomie(text, list, i, g, m)
    elif d - g == 1:
        return dicotomie(text, list, i, d, d)
    else:
       return dicotomie(text, list, i, m, d)


def bwt_dicotomie(text):
    list = [("$", 0)]
    i = 0
    while text[i] != "$":
        list = dicotomie(text[i:], list, 1, 0, len(list) - 1)
        i += 1
    return "".join([value[0] for value in list])
 
def gener_P_N(transform):
    """N & P matrices for Burrows-Wheeler transformation
    """
    P = []
    dico = {"$" : 0, "A" : 0, "C" : 0, "G" : 0, "T" : 0}
    for lettre in transform :
        P.append(dico[lettre])
        dico[lettre] += 1
    N = {}
    count = 0
    for k in dico.keys() :
        N[k] = count
        count += dico[k]
    return P, N
 
def gener_retro_bwt(transform, P, N) :
    i = len(transform) - 1
    origin = "$"
    j = 0
    while i >= 1 :
        origin = transform[j] + origin
        j = N[transform[j]] + P[j]
        i -= 1
    return origin
 
def pos_BWT(transform, P, N):
    i = len(transform) - 2
    pos = [-1] * len(transform)
    j = 0
    while transform[j] != "$" :
        pos[j] = i
        j = N[transform[j]] + P[j]
        i -= 1
    return pos
 
def FM_index(M):
    dic = {'$':0,'A':0,'C':0,'G':0,'T':0}
    fm = [dic.copy()]
    for el in list(M):
        dic[el]+=1
        fm.append(dic.copy())
    return fm
 
def match(read, N, FM):
    nt = read[-1]
    d = N[nt] #debut
    f = N[nt] + FM[-1][nt] -1
    for nt in read[-2::-1]:
        d = N[nt] + FM[d][nt]
        f = N[nt] + FM[f+1][nt] -1
        if f < d :
            return (-1, -1)
    return d, f

def pos(start, end,  pos_list):
    position = []
    for i in range(start, end+1):
        position.append(str(pos_list[i] + 1))
    return position

def read_file(fil_ref, fil_reads):
    ref = ""
    with open(fil_ref) as filin:
        for line in filin:
            if line.startswith(">"):
                continue
            ref += line[:-1]
    l_read = []
    with open(fil_reads) as filin:
        seq = ""
        for line in filin:
            if line.startswith(">"):
                l_read.append(seq)
                seq = ""
                continue
            seq += line[:-1]
    l_read.append(seq )

    return l_read[1:], ref
                
def main():
    print(bwt_dicotomie("ATATCGT$"))
    # l = []
    # for i in range(0, 10):
    #     l.append ("".join(random.choices(["A", "T", "C", "G"], k = (i+1) * 10000)) + "$")
    # l_time = [0]
    # for i in range(0, 10):
    #     start = time.time()
    #     bwt_dicotomie(l[i])
    #     end = time.time()
    #     l_time. append( end - start )
    # print(l_time)
    # plt.plot(list(range(0, 11)), l_time)

    # l = []
    # for i in range(0, 10):
    #     l.append ("".join(random.choices(["A", "T", "C", "G"], k = (i+1) * 10000)) + "$")
    # l_time = [0]
    # for i in range(0, 10):
    #     start = time.time()
    #     gener_BWT_transform(l[i])
    #     end = time.time()
    #     l_time. append( end - start )
    # print(l_time)
    # plt.plot(list(range(0,11)), l_time)
    # plt.show()
    # l_read, ref = read_file("NC_045512-N.fna", "reads_1000_10_patient_6.fna") 
    # print(l_read)
    # print(ref)
    # ref_bwt = bwt_dicotomie(ref + "$")
    # p, n = gener_P_N(ref_bwt)
    # index = FM_index(ref_bwt)
    # l_pos = pos_BWT(ref_bwt, p, n)
    # print(ref_bwt)
    # l = [0, 0, 0]
    # l_pos_read = -1
    # with open("sortie.fasta", "w") as filout:
    #     for read in l_read:
    #         math = match(read, n, index)
    #         if math == (-1, -1):
    #              l_pos_read = ["-1"]
    #         else:
    #             l_pos_read = pos(math[0],  math[1],  l_pos)
    #         if  l_pos_read[0] == "-1":
    #             l[0] +=1
    #         elif len( l_pos_read) == 1:
    #             l[1] += 1
    #         else:
    #             l[2] += 1
    #         filout.write("> read:" + " ".join(l_pos_read) + "\n")
    #         filout.write(read + "\n")


    # print(l)





main()
