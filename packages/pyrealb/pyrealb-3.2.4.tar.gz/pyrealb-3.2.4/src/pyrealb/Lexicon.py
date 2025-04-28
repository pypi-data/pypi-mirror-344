import json,sys, os

datadir=os.path.abspath(os.path.join(os.path.dirname(__file__),'data')) 

class Lexicon(object):
    """ Keep information about English and French lexica and rules  """
    
    def __init__(self):
        """ load English and French lexica and rules"""
        
        self.lexicon={
            "en":json.load(open(os.path.join(datadir,"lexicon-en.json"),encoding="utf-8")),
            "fr":json.load(open(os.path.join(datadir,"lexicon-fr.json"),encoding="utf-8")),
        }
        self.rules={
            "en":json.load(open(os.path.join(datadir,"rules-en.json"),encoding="utf-8")),
            "fr":json.load(open(os.path.join(datadir,"rules-fr.json"),encoding="utf-8")),
        }
        self.lang="en"
        
    def getLexicalInfo(self,lemma):
        the_lexicon=self.getLexicon()
        if lemma in the_lexicon:
            return the_lexicon[lemma]
        else:
            return None
    
    def getLexicon(self):
        return self.lexicon[self.lang]
    
    def getRules(self):
        return self.rules[self.lang]
        
__lexicon = Lexicon()

def getLanguage():
    return __lexicon.lang

def loadEn(trace=False):
    __lexicon.lang="en"
    if trace: print("English lexicon and rules loaded",file=sys.stderr)

def loadFr(trace=False):
    __lexicon.lang="fr"
    if trace: print("Règles et lexique français chargés",file=sys.stderr)

def load(lang,trace=False):
    from .utils import Q
    if lang=="en": loadEn(trace)
    elif lang=="fr": loadFr(trace)
    else:
        Q(lang).warn("bad language",lang)

# add to lexicon and return the updated object
#     to remove from lexicon (give None as newInfos)
def addToLexicon(lemma,newInfos=None,lang=None):
    lexicon=getLexicon(lang)
    if isinstance(lemma,dict): # convenient when called with a single JSON object as shown in the IDE
        item=list(lemma.items())[0]
        newInfos=item[1]
        lemma=item[0]
    elif newInfos is None: # remove entry
        if lemma in lexicon:
            del lexicon[lemma]
        return
    if lemma in lexicon:
        lexicon[lemma].update(newInfos)
    else:
        lexicon[lemma]=newInfos
    return lexicon[lemma]

# update current lexicon by "merging" the pyrealb lexicon with the current one
#     i.e. adding pyrealb key-value pairs and replacing existing key-value pairs with the pyrealb one
#     newLexicon is a single object with the "correct" structure
def updateLexicon(newLexicon,lang=None):
    lexicon = getLexicon(lang)
    lexicon.update(newLexicon)

# get lemma from lexicon (useful for debugging )
def getLemma(lemma,lang=None):
    lexicon=getLexicon(lang)
    return lexicon[lemma] if lemma in lexicon else None

# return the current lexicon or the one specified
def getLexicon(lang=None):
    if lang is not None:
        return __lexicon.lexicon[lang]
    return __lexicon.getLexicon()

# return the current rules or the ones specified
def getRules(lang=None):
    if lang is not None:
        return __lexicon.rules[lang]
    return __lexicon.getRules()
