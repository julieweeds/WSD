__author__ = 'juliewe'


import senses,sys,conf
from byblo import Byblo


if __name__=="__main__":
    parameters=conf.configure(sys.argv)
    print parameters



    words=parameters.get("words_of_interest",["chicken/N"])
    metric=parameters.get("metric","wup")
    myThes={}
    count=0
    for thesdir in parameters["thesdirs"]:
        byblofile=parameters["datadir"]+thesdir+parameters["thesfile"]
        myThes[count] = Byblo(byblofile,parameters.get("k",10))


        myThes[count].readsomesims(words)
        count+=1
    for word in words:
        senseneighbours=[]
        for thes in myThes.keys():
            #myThes[thes].displayneighs(word,parameters["k"])
            senseneighbours.append(myThes[thes].getneighs(word,parameters.get("k",10)))

        #print senseneighbours


        for senseneighbour in senseneighbours:
            (ps,sc)=senses.prevalent_sense(word,senseneighbour,metric)
            print word,ps,ps.definition,sc, senseneighbour
        #senses.allpairings(word,senseneighbours,metric)

