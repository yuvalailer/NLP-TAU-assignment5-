from PCFG import PCFG
import math
import numpy as np

def load_sents_to_parse(filename):
    sents = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line:
                sents.append(line)
    return sents

def cky(pcfg, sent):
    ### YOUR CODE HERE
    n = len(sent)
    idx2nonterminals = dict(enumerate(pcfg._rules.keys()))
    nonterminals2idx = {v: k for k,v in idx2nonterminals.items()}
    pi = np.zeros((n, n, len(pcfg._rules.keys())))

    # Initialization
    for i in range(n):
        for j, nonterminal in idx2nonterminals.items():
            pi[i,i,j] = pcfg.get_prob(nonterminal, sent[i])

    
    ### END YOUR CODE
    return "FAILED TO PARSE!"

if __name__ == '__main__':
    import sys
    pcfg = PCFG.from_file_assert_cnf(sys.argv[1])
    sents_to_parse = load_sents_to_parse(sys.argv[2])
    for sent in sents_to_parse:
        print cky(pcfg, sent)
