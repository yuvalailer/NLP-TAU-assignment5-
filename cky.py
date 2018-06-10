from PCFG import PCFG
import math

def load_sents_to_parse(filename):
    sents = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line:
                sents.append(line)
    return sents


def find_root(pi, idx2nonterminals, sent_length):
    max_nonterm, score = -1, 0
    for x in idx2nonterminals.values():
        p = pi.get((0,sent_length-1,x), 0)
        if p > score:
            max_nonterm = x
            score = p
    return max_nonterm, score


def cky(pcfg, sent):
    ### YOUR CODE HERE
    sentence = sent.split()
    n = len(sentence)
    num_nonterms = len(pcfg._rules.keys())
    idx2nonterminals = dict(enumerate(pcfg._rules.keys()))
    nonterminals2idx = {v: k for k,v in idx2nonterminals.items()}
    pi = {}
    bp = {}

    valid_parsing_exists = False
    # Initialization
    for i in range(n):
        level_sum = 0
        for X, nonterminal in idx2nonterminals.items():
            prob = pcfg.get_prob(nonterminal, sentence[i])
            if prob > 0:
                pi[(i,i,nonterminal)] = prob
                bp[(i,i,nonterminal)] = [(i,i,sentence[i])]
                level_sum += prob

        if level_sum == 0:
            return "FAILED TO PARSE!"

    # dynamic programing
    for level in range(1,n):
        level_sum = 0
        for i in range(n-level):
            j = i+level
            for X, nonterminal in idx2nonterminals.items():
                for symbols, weight in pcfg._rules[nonterminal]:
                    if len(symbols) < 2:
                        continue

                    Y,Z = symbols
                    for s in range(i,j):
                        left_split, right_split = (i,s,Y),(s+1,j,Z)
                        if left_split not in pi or right_split not in pi:
                            continue
                        prob = pcfg.get_prob(nonterminal, symbols) * pi[(i,s,Y)] * pi[(s+1,j,Z)]
                        if prob > pi.get((i,j,nonterminal),0):
                            pi[(i,j,nonterminal)] = prob
                            bp[(i,j,nonterminal)] = ((i,s,Y),(s+1,j,Z))
                            level_sum += prob
    root = (0, n-1, 'ROOT')
    p = pi.get(root, 0)
    if p > 0:
        return pcfg.gen_cky_tree(bp, root)
    ### END YOUR CODE
    return "FAILED TO PARSE!"

if __name__ == '__main__':
    import sys
    pcfg = PCFG.from_file_assert_cnf(sys.argv[1])
    sents_to_parse = load_sents_to_parse(sys.argv[2])
    for sent in sents_to_parse:
        print cky(pcfg, sent)
