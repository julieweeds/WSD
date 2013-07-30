from nltk.corpus import wordnet as wn


def wnss(wsi,neighbour):
    #wn sim between word sense and neighbour (maximised over all senses of neighbour)
    neighbour_senses=wn.synsets(neighbour,pos=pos)
    maxsim=0
    for neighsense in neighbour_senses:
        sim = wsi.lch_similarity(neighsense)
        if sim > maxsim:
            maxsim=sim
            #print "wnss", wsi, wsi.definition, neighsense, neighsense.definition, maxsim


    return maxsim

def prevalences(neighbours,candidates):
    #compute prevalence of each sense of word according to neighbour list
    #candidates=wn.synsets(word,pos=pos)
    simtotals={}
    dstotal=0
    for (neigh,ds) in neighbours:
        wn_sim_total=0
        for cand in candidates:
            wn_sim=wnss(cand,neigh)
            wn_sim_total+=wn_sim
        simtotals[neigh]=wn_sim_total
        dstotal+=ds
    prevs=[]
    for cand in candidates:
        p=0
        for (neigh,ds) in neighbours:
            #print cand, neigh, ds, wnss(cand,neigh),simtotals[neigh]
            p += (ds/dstotal) * (wnss(cand,neigh)/simtotals[neigh])
        prevs.append((cand,p))
    return prevs

def prevalent_sense(word,neighbours):
    prevs = prevalences(neighbours,wn.synsets(word,pos=pos))
    maxp =0
    sense =""
    for (cand,prev) in prevs:
        if prev>maxp:
            sense=cand
            maxp=prev

    return (sense,maxp)

def allpairings(word,senseneighbours):
    candidates = wn.synsets(word,pos=pos) #may want to filter these so not all synsets are candidates
    wnsenses=len(candidates)
    prevmatrix=[]
    for senseneighbour in senseneighbours:
        prevmatrix.append(prevalences(senseneighbour,candidates))
  #  print prevmatrix
    #permutations


    while len(candidates)<len(senseneighbours):
        #generate empty wordnet senses to pair extra distributional senses to
        candidates.append("nosense")
    perms=[[]]
    while(len(perms[0])<len(senseneighbours)): #each perm needs to have same number of items as senseneighbours
        newperms=[]
        for perm in perms: #extend each perm with all wn senses
            for i in range(len(candidates)):
                if i not in perm:
                    newperm=perm[:]
                    newperm.append(i)
                    newperms.append(newperm[:])
        perms=newperms[:]
#    print len(perms)
 #   print perms

    #score each permutation
    best_score=-1
    best_index=-1
    for permindex,perm in enumerate(perms):
        score=0
        for dsindex,wnindex in enumerate(perm):
            if wnindex<wnsenses: # range check as it may be an extra "nosense" sense
                (_,prev)=prevmatrix[dsindex][wnindex]
                score += prev
        score = score/len(perm)

        if score > best_score:
            best_score=score
            best_index=permindex

    print perms[best_index],best_score
    for dsindex,wnindex in enumerate(perms[best_index]):
        prev=0
        mydef = "none"
        if wnindex<wnsenses:
            (_,prev)=prevmatrix[dsindex][wnindex]
            mydef=candidates[wnindex].definition
        print senseneighbours[dsindex],candidates[wnindex],mydef,prev
    return best_score

if __name__=="__main__":

    pos=wn.NOUN
    myword="chicken"
   # senseneighbours=[[("cockerel",0.5),("hen",0.45),("meat",0.4),("cheese",0.38),("duck",0.37),("cow",0.35)]]
   # senseneighbours=[[("cockerel",0.5),("hen",0.45),("cow",0.35)],[("meat",0.4),("cheese",0.38),("duck",0.37)]]
   # senseneighbours=[[("cockerel",0.5),("hen",0.45),("cow",0.35)],[("cockerel",0.5),("hen",0.45),("cow",0.35)],[("meat",0.4),("cheese",0.38),("duck",0.37)]]
    senseneighbours=[[("cockerel",0.5),("hen",0.45),("cow",0.35)],[("cockerel",0.5),("hen",0.45),("cow",0.35)],[("meat",0.4),("cheese",0.38),("duck",0.37)],[("cockerel",0.5),("hen",0.45),("cow",0.35)],[("meat",0.4),("cheese",0.38),("duck",0.37)]]

    for senseneighbour in senseneighbours:
        (ps,sc)=prevalent_sense(myword,senseneighbour)
        print myword,ps,ps.definition,sc
    allpairings(myword,senseneighbours)

