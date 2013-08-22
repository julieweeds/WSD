__author__ = 'juliewe'


import senses,sys,conf
from byblo import Byblo


class SenseEval:

    def __init__(self,parameters):

        self.parameters=parameters
        self.words=parameters.get("words_of_interest",["chicken/N"])
        self.metric=parameters.get("metric","wup")
        self.myThes={}
        self.count=0
        #load
        for thesdir in parameters["thesdirs"]:
            byblofile=parameters["datadir"]+thesdir+parameters["thesfile"]
            self.myThes[self.count] = Byblo(byblofile,parameters.get("k",10))


            self.myThes[self.count].readsomesims(self.words)
            self.count+=1


    def computeall(self):

        for word in self.words:
            senseneighbours=[]
            for thes in self.myThes.keys():
                #myThes[thes].displayneighs(word,parameters["k"])
                senseneighbours.append(self.myThes[thes].getneighs(word,self.parameters.get("k",10)))

            #print senseneighbours


            for senseneighbour in senseneighbours:
                (ps,sc)=senses.prevalent_sense(word,senseneighbour,self.metric)
                print word,ps,ps.definition,sc, senseneighbour
                senses.display_prevalences(word,senseneighbour,self.metric)
                #senses.allpairings(word,senseneighbours,metric)

    def pairwise(self):

        for word in self.words:

            for thesA in self.myThes.keys():
                senseneighbourA = self.myThes[thesA].getneighs(word,self.parameters.get("k",10))
                for thesB in self.myThes.keys():
                    if thesA != thesB:
                        senseneighbourB=self.myThes[thesB].getneighs(word,self.parameters.get("k",10))
                        senses.compare_prevalences(word,senseneighbourA,senseneighbourB,self.metric)




if __name__=="__main__":
    parameters=conf.configure(sys.argv)
    print parameters

    mySenseEval=SenseEval(parameters)



    #computation
    if "computeall" in parameters["options"]:
        mySenseEval.computeall()
    if "pairwise" in parameters["options"]:
        mySenseEval.pairwise()
