__author__ = 'juliewe'


def configure(args):

    parameters={}
    parameters["datadir"]="/Volumes/LocalScratchHD/juliewe/Documents/workspace/ThesEval/data/"
    parameters["thesdirs"]=["wiki_t100f100_nouns_conj/","wiki_t100f100_nouns_dobj/"]
    #parameters["thesdirs"]=["wiki_t100f100_nouns_deps/"]
    parameters["thesfile"]="neighbours.strings"
    parameters["words_of_interest"]=['chicken/N','birch/N','star/N']
    parameters["k"]=5
    parameters["metric"]="res"

    return parameters