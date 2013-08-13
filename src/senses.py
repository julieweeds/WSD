from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic as wn_ic

#path_similarity
#lch_similarity

#pos=wn.NOUN

posmap={'N':wn.NOUN,'V':wn.VERB,'J':wn.ADJ,'R':wn.ADV}
ic = wn_ic.ic('ic-semcor.dat')

def untag(wordpos):
    parts=wordpos.split('/')
    return(parts[0],posmap.get(parts[1],"unknown"))

def wnss(wsi,neigh,metric):
    #wn sim between word sense and neighbour (maximised over all senses of neighbour)
    (neighbour,pos)=untag(neigh)
    neighbour_senses=wn.synsets(neighbour,pos=pos)
    maxsim=0
    for neighsense in neighbour_senses:
        sim = wnsim(wsi,neighsense,metric)

        if sim > maxsim:
            maxsim=sim
            #print "wnss", wsi, wsi.definition, neighsense, neighsense.definition, maxsim


    return maxsim

def wnsim(wsi,neigh,metric="wup"):
    if metric=="lch":
        return wsi.lch_similarity(neigh)
    elif metric=="path":
        return wsi.path_similarity(neigh)
    elif metric=="wup":
        return wsi.wup_similarity(neigh)
    elif metric=="res":
        return wsi.res_similarity(neigh,ic)
    elif metric=="jcn":
        return wsi.jcn_similarity(neigh,ic)
    else:
        print "Error: unknown wn similarity metric "+metric
        exit(1)
def prevalences(neighbours,candidates,metric):
    #compute prevalence of each sense of word according to neighbour list
    #candidates=wn.synsets(word,pos=pos)
    simtotals={}
    dstotal=0
    for (neigh,ds) in neighbours:
        wn_sim_total=0
        for cand in candidates:
            wn_sim=wnss(cand,neigh,metric)
            wn_sim_total+=wn_sim
        simtotals[neigh]=wn_sim_total
        dstotal+=ds
    prevs=[]
    for cand in candidates:
        p=0
        for (neigh,ds) in neighbours:
            #print cand, neigh, ds, wnss(cand,neigh),simtotals[neigh]
            if simtotals[neigh]*dstotal == 0:
                p+=0
            else:
                p += (ds/dstotal) * (wnss(cand,neigh,metric)/simtotals[neigh])
        prevs.append((cand,p))
    return prevs

def prevalent_sense(w,neighbours,metric):
    (word,pos)=untag(w)
    prevs = prevalences(neighbours,wn.synsets(word,pos=pos),metric)
    maxp =-1
    sense =""
    for (cand,prev) in prevs:
        if prev>maxp:
            sense=cand
            maxp=prev

    return (sense,maxp)

def allpairings(w,senseneighbours,metric):
    (word,pos)=untag(w)
    candidates = wn.synsets(word,pos=pos) #may want to filter these so not all synsets are candidates
    wnsenses=len(candidates)
    prevmatrix=[]
    for senseneighbour in senseneighbours:
        prevmatrix.append(prevalences(senseneighbour,candidates,metric))
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


    myword="chicken/N"
   # senseneighbours=[[("cockerel",0.5),("hen",0.45),("meat",0.4),("cheese",0.38),("duck",0.37),("cow",0.35)]]
   # senseneighbours=[[("cockerel",0.5),("hen",0.45),("cow",0.35)],[("meat",0.4),("cheese",0.38),("duck",0.37)]]
   # senseneighbours=[[("cockerel",0.5),("hen",0.45),("cow",0.35)],[("cockerel",0.5),("hen",0.45),("cow",0.35)],[("meat",0.4),("cheese",0.38),("duck",0.37)]]
    senseneighbours=[[("cockerel/N",0.5),("hen/N",0.45),("cow/N",0.35)],[("cockerel/N",0.5),("hen/N",0.45),("cow/N",0.35)],[("meat/N",0.4),("cheese/N",0.38),("duck/N",0.37)],[("cockerel/N",0.5),("hen/N",0.45),("cow/N",0.35)],[("meat/N",0.4),("cheese/N",0.38),("duck/N",0.37)]]
    metric = "wup"
    for senseneighbour in senseneighbours:
        (ps,sc)=prevalent_sense(myword,senseneighbour,metric)
        print myword,ps,ps.definition,sc
    allpairings(myword,senseneighbours,metric)


