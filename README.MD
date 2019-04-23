# HeadLine Parsing (HID334 Project)

## What is Headline Parsing?
Headlines in newspapers do not follow normal grammatical rules of the English Language. Instead, headlines have a distinct yet coherent syntax that incorporates brevity of speech while emphasizing the important part of the document. However, this means that while extracting a parse from headlines, many statistical parsers such as Stanford Parser will fail. One solution to this problem can be to create a seperate parser just for headlines. Alternatively, headlines can be preprocessed to work with normal parser. <br>
For more info about the differences between normal English and headline English, see [this](https://www.chronicle.com/blogs/linguafranca/2013/02/18/the-grammar-of-newspaper-headlines/).

## What is "Canonicalization"?
A solution to the problem of an explosion of syntactic parses of headlines is to  assign canonical forms to the headlines. In order for parsers to understand headlines, certain changes to them have to be made so that the original meaning of the headline is preserved as far as possible while at the same time, the headline has to be made to conform to normal grammar. THe process of canonicalization is hard, as headlines come in many formats and there are few universal forms of headlines. Moreover, there are several irregularities in how they are formatted. Certain general rules can be formulated that apply to most headlines, however it is very difficult to get the correct parse on each and every sentence. The purpose of a canonical form is to ensure a correct parse by conversion or approximation of the headline to a normal english sentence so as to remove ambiguity and reduce errors. 

## Prerequisites and Install Process:
The project depends on several external libraries
* newspaper3k -> Downloading Headlines automatically<br>
`pip install newspaper3k`
* requests, bs4 -> Using the online stanford parser<br>
`pip install requests beautifulsoup4`
* pyStatParser -> Python Statistical Parser alternative to Stanford Parser<br>
`Download https://github.com/emilmont/pyStatParser, Run setup.py`
* allennlp (Optional) -> allennlp parser<br>
`pip install allennlp`
* wiktionaryparser -> searching for abbreviations online corpus<br>
`pip install wiktionaryparser`

## Structure of Project:
* README.MD -> Explanation and Main Analysis.
* data -> directory containing the example headlines for the project
  * 5_Ankur.csv -> Original Headlines provided
  * 5_Ankur_canonical.csv -> manually canonicalized sentences
  * 5_Ankur.ods -> contains orignial and canonical sentences along with the rules identified for each parse

* `download.py` -> code for downloading
```
  usage: download.py [-h] NEWSPAPER

  Download News Headlines from popular Newspapers. The output format is one
  headline per line which can be stored in a file using the command python
  download.py>headlines.txt Note: Certain headlines may be malformed so as an
  error their urls are printed.

  positional arguments:
    NEWSPAPER   website of the newspaper from which to download the headlines
                from www.cnbc.com zeenews.india.com www.business-standard.com
                www.bloombergquint.com www.indiatoday.in www.news18.com

  optional arguments:
    -h, --help  show this help message and exit
```
* `parse.py` -> code for parsing using a given parser
```
  usage: parse.py [-h] [-p {pystat,stanford,allen}] file

  Parse the given sentence using a parser such as Stanford Parser, PyStatParser
  or AllenNlp Parser Takes input in the form of a file of newline seperated
  sentences and outputs the parse in a similar format. The parse notation of
  various parsers may be significantly different.

  positional arguments:
    file                  input file

  optional arguments:
    -h, --help            show this help message and exit
    -p {pystat,stanford,allen}, --parser {pystat,stanford,allen}
                          parser to be used
```
* `rules.py` -> code for applying rules to automatically canonicalize sentences
```
usage: rules.py [-h] [-e EXCLUDE] file

Apply all the rules to a file in the same format as generted by headlines.py.
Currently Implemented Rule: Capitalization(C) Quote(Q) Is(I)

positional arguments:
  file                  input file

optional arguments:
  -h, --help            show this help message and exit
  -e EXCLUDE, --exclude EXCLUDE
                        rule to exclude ['Q', 'C', 'I']

```
## Rules:
Certain rules can be formulated for automatic conversion of headlines into canonical forms.

### Implemented:
#### 1. CAPITALIZATION: 
Headlines often have spurious and random capitalization of words in the middle of sentences just for thematic effect or for emphasis. Confusingly, headlines also contain a host of acronyms and abbreivations the are already capitalized correctly. This leads to random words being labelled as Proper Nouns (NNP) by the parser.
**Solution**:
Remove all CAPS words not in corpus of abbreviations. 
**Implementation**:
For the implementation of this rule in rules.py, for every all caps word, I search the online dictionary [Wikictionary](https://www.wiktionary.org/) for the word having that exact capitalization. If it does exist then it is most likely an acronym. Otherwise convert it to lowercase.
```
Original: View from the CUPBOARD
Stanford:
(ROOT 
  (NP (NP (NNP View)) (PP (IN from) (NP (DT the) (NNP CUPBOARD))))
)
Canonical: This is the view from the cupboard
Stanford:
(ROOT 
  (S (NP (DT This)) (VP (VBZ is) (NP (NP (NN view)) (PP (IN from) (NP (DT the) (NN cupboard))))))
)
```
### Unimplemented:

#### 1. IS:
Due to lack of verbs in sentences, some nouns or adjectives are marked as verbs especially for stanford parser. This is specifically due to the fact that headlines avoid generally the types of words that are obvious such as "is, are, were" etc which show existance and can therefore be inferred from context. Due to lack of verb-ish words in the sentence, the parser mistakenly identifies other words as verbs and vice versa.
```
Original: Unsafe practice in spraying pesticide killing farmers
Stanford:
(ROOT
  (S (VP (VB Unsafe) (NP (NN practice)) (PP (IN in) 
  (S (VP (VBG spraying) (NP (NN pesticide) (NN killing) (NNS farmers)))))))
 )
PyStatParser:
(NP+S 
  (NP (NP (JJ unsafe) (NN practice)) (PP (IN in) 
  (NP (VBG spraying) (NN pesticide)))) (VP (VBG killing) (NP (NNS farmers)))
)
```
**Solution**:
We can insert a dummy verb as is/ are/ was etc wherever a Noun Phrase is given so as to disambiguate the sentence. 
```
Original:  Unsafe practice in spraying pesticide killing farmers
Canonical: Unsafe practice in spraying pesticide is killing farmers
Stanford:
(ROOT 
  (S (NP (NP (JJ Unsafe) (NN practice)) (PP (IN in) 
  (S (VP (VBG spraying) (NP (NN pesticide)))))) (VP (VBZ is) (VP (VBG killing) (NP (NNS farmers)))))
)
```

**Possible Implementations**:
1. Infinitive -> is + infinitive
```
Original: Unmanned level crossing gates to go ‘smart’ soon
Canonical: Unmanned level crossing gates are to go ‘smart’ soon
```
2. Passive Verb -> is + passive verb
```
Original: Varun Dhawan captured on the wrong side of the law
Canonical: Varun Dhawan was captured on the wrong side of the law
```

#### 2.THEREIS: 
Similar to above, but here we need to insert There is instead of is.
**Possible Implementations**:
```
Original: VMA annual festival from tomorrow
Stanford:
(ROOT 
  (S (VP (VB VMA) (NP (JJ annual) (NN festival)) (PP (IN from) (NP (NN tomorrow)))))
)
Canonical: There is VMA annual festival from tomorrow.
Stanford:
(ROOT 
  (S (NP (EX There)) (VP (VBZ is) (NP (NP (NNP VMA) (JJ annual) 
  (NN festival)) (PP (IN from) (NP (NN tomorrow))))))
)
```

#### 3.QUOTE:
Remove all quotations as they are easily mistaken for possessives.
```
Original : ‘Waterbodies being filled up with sand’
Stanford:
(ROOT (FRAG (VP (`` `) (VBZ Waterbodies) (S (VP (VBG being) (VP (VBN filled) (PRT (RP up)) (PP (IN with)
  (NP (NN sand) (POS '))))))))
)
```

#### 4.COMMA:
Comma is used as a substitute for and. All such commas need to be replaced by and as the second argument to the comma easily mistaken for VB

#### 5.COLON
Colon in a headline can mean  3 things:
1. A :B  -> A said B
```
U.N. to Israel: Withdraw from Arab territory
```
2. A: B   -> B said A
```
Unite to fight dark forces in digital space: PM
```
3. A: B   -> regarding A,B
```
Bhiwandi collapse: death toll rises to 4
```
