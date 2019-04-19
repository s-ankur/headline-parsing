Rules:



IS:
Due to lack of verbs in sentences, some nouns or adjectives are marked as verbs. We can insert a dummy verb as is/ are/ was etc wherever a Noun Phrase is given so as to disambiguate the sentence. Implemantations:
Infinitive -> is + infinitive
Unmanned level crossing gates to go ‘smart’ soon
Unmanned level crossing gates are to go ‘smart’ soon
Passive Verb -> is + passive verb
Varun Dhawan captured on the wrong side of the law
Varun Dhawan was captured on the wrong side of the law

Unsafe practice in spraying pesticide killing farmers
(ROOT (S (VP (VB Unsafe) (NP (NN practice)) (PP (IN in) (S (VP (VBG spraying) (NP (NN pesticide) (NN killing) (NNS farmers))))))))

(ROOT (S (NP (NP (JJ Unsafe) (NN practice)) (PP (IN in) (S (VP (VBG spraying) (NP (NN pesticide)))))) (VP (VBZ is) (VP (VBG killing) (NP (NNS farmers))))))

(NP+S (NP (NP (JJ unsafe) (NN practice)) (PP (IN in) (NP (VBG spraying) (NN pesticide)))) (VP (VBG killing) (NP (NNS farmers))))





THEREIS: Similar to above, but here we need to insert There is instead of is.
Implementations:

VMA annual festival from tomorrow

(ROOT (S (VP (VB VMA) (NP (JJ annual) (NN festival)) (PP (IN from) (NP (NN tomorrow))))))

(ROOT (S (NP (EX There)) (VP (VBZ is) (NP (NP (NNP VMA) (JJ annual) (NN festival)) (PP (IN from) (NP (NN tomorrow)))))))




QUOTE: Remove all quotations as they are easily mistaken for POS

‘Waterbodies being filled up with sand’
(ROOT (FRAG (VP (`` `) (VBZ Waterbodies) (S (VP (VBG being) (VP (VBN filled) (PRT (RP up)) (PP (IN with)
(NP (NN sand) (POS ')))))))))




COMMA: Comma is used as a substitute for and. All such commas need to be replaced by and as the second argument to the comma easily mistaken for VB


COLON1: 
A :B  -> A said B
U.N. to Israel: Withdraw from Arab territory


COLON2: 
A: B   -> B said A
Unite to fight dark forces in digital space: PM


COLON3:
A: B   -> regarding A,B
Bhiwandi collapse: death toll rises to 4




CAPITALIZATION: Remove all CAPS words not in corpus of abbreviations

(ROOT (NP (NP (NNP View)) (PP (IN from) (NP (DT the) (NNP CUPBOARD)))))
(ROOT (S (NP (DT This)) (VP (VBZ is) (NP (NP (NN view)) (PP (IN from) (NP (DT the) (NN cupboard)))))))

