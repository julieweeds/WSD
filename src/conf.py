__author__ = 'juliewe'


def configure(args):

    parameters={}
    parameters["datadir"]="/Volumes/LocalScratchHD/juliewe/Documents/workspace/ThesEval/data/"
    parameters["thesdirs"]=["wiki_t100f100_nouns_conj/","wiki_t100f100_nouns_dobj/","wiki_t100f100_nouns_nsubj/"]
    #parameters["thesdirs"]=["wiki_t100f100_nouns_wins/"]
    parameters["thesfile"]="neighbours.strings"
    parameters["words_of_interest"]=['chicken/N','star/N','squash/N','chair/N','table/N','birch/N']
    parameters["k"]=5
    parameters["metric"]="wup"

    return parameters