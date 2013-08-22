__author__ = 'juliewe'

import sys,conf
from operator import itemgetter

class Byblo:

    def __init__(self,filename,k):

        self.filename=filename
        self.updated=0
        self.k=k
        self.entrydict={}

    def readsomesims(self,entrylist):

        print"Reading sim file "+self.filename
        linesread=0
        instream=open(self.filename,'r')
        for line in instream:
            if line.split('\t')[0] in entrylist:
                self.processsimline(line.rstrip())
            linesread+=1
            if self.updated==len(entrylist):
                #all found
                break
            if (linesread%1000 == 0):
                #print "Read "+str(linesread)+" lines and updated "+str(self.updated)+" similarity vectors"
                sys.stdout.flush()
                #return
        print "Read "+str(linesread)+" lines and updated "+str(self.updated)+" vectors"
        instream.close()

    def processsimline(self,line):
        featurelist=line.split('\t')

        entry=featurelist[0]

        #print entry
        featurelist.reverse() #reverse list so can pop features and scores off
        featurelist.pop() #take off last item which is word itself

        thisentry=self.updatesimvector(featurelist)
        self.entrydict[entry]=self.topk(thisentry)
        self.updated+=1

    def updatesimvector(self,featurelist):
        thisentry=[]
        while(len(featurelist)>0):
            f=featurelist.pop()
            sc=featurelist.pop()
            thisentry.append((f,float(sc)))
        return thisentry

    def topk(self,thisentry):

        #only retain top k neighbours
        #print thisentry
        thisentry = sorted(thisentry,key=itemgetter(1),reverse=True)
        k=min(self.k,len(thisentry))
        topkentry=thisentry[:k]
        return topkentry

    def displayneighs(self,word,k):
        kdisplay=min(self.entrydict[word],k)
        print word, self.entrydict[word][:kdisplay]

    def getneighs(self,word,k):
        kdisplay=min(self.entrydict[word],k)
        return self.entrydict[word][:kdisplay]



if __name__=="__main__":

    parameters=conf.configure(sys.argv)
    print parameters

    words=parameters["words_of_interest"]
    myThes={}
    count=0
    for thesdir in parameters["thesdirs"]:
        byblofile=parameters["datadir"]+thesdir+parameters["thesfile"]
        myThes[count] = Byblo(byblofile,parameters["k"])


        myThes[count].readsomesims(words)
        count+=1
    for word in words:
        for thes in myThes.keys():
            myThes[thes].displayneighs(word,parameters["k"])
