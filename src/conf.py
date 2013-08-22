__author__ = 'juliewe'


def configure(args):

    parameters={}
    parameters["datadir"]="/Volumes/LocalScratchHD/juliewe/Documents/workspace/ThesEval/data/"
    parameters["thesdirs"]=["wiki_t100f100_nouns_conj/","wiki_t100f100_nouns_dobj/","wiki_t100f100_nouns_nsubj/","wiki_t100f100_nouns_amodDEP/","wiki_t100f100_nouns_nnHEAD/","wiki_t100f100_nouns_wins/"]
    parameters["thesdirs"]=["wiki_t100f100_nouns_conj/","wiki_t100f100_nouns_dobj/"]
    #parameters["thesdirs"]=["wiki_t100f100_nouns_wins/"]
    parameters["thesfile"]="neighbours.strings"
    parameters["words_of_interest"]=['chicken/N','star/N','squash/N','chair/N','table/N','birch/N',"cricket/N"]
    #parameters["words_of_interest"]=['chicken/N']
    parameters["k"]=5
    parameters["metric"]="wup"
    parameters["options"]=["pairwise"]

    return parameters