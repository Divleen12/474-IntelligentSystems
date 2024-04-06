import spacy
import en_core_web_sm

text = open("./COMP474/Worksheets/worksheet01.txt", "r", encoding="utf8")
readText = text.read()
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('entityfishing')
doc = nlp(readText)

outputPath = f'COMP474/Worksheets/worksheet01_LinkedEntities.txt'

file = open(outputPath, "w", encoding = "utf8")

for span in doc.ents:
    if (span.label_ != 'CARDINAL' and span.label_ != 'ORDINAL' and span.label_ != 'PRODUCT' and span.label_ != 'LOC'):
        file.write(str((span.text, span.label_, span._.kb_qid, span._.url_wikidata, span._.nerd_score)) + "\n")
