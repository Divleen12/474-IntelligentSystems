import spacy
import en_core_web_sm

j=2

while (j<5):
    i = 1

    while (i<7):
        inputPath = f"./COMP47{j}/Worksheets/worksheet0{i}.txt"
        text = open(inputPath, "r", encoding="utf8")
        readText = text.read()
        nlp = spacy.load('en_core_web_sm')
        nlp.add_pipe('entityfishing')
        doc = nlp(readText)

        outputPath = f'COMP47{j}/Worksheets/worksheet0{i}_LinkedEntities.txt'

        file = open(outputPath, "w", encoding = "utf8")
        
        for span in doc.ents:
            if (span.label_ != 'CARDINAL' and span.label_ != 'ORDINAL' and span.label_ != 'PRODUCT' and span.label_ != 'LOC' and span._.kb_qid != None):
                file.write(str((span.text, span.label_, span._.kb_qid, span._.url_wikidata, span._.nerd_score)) + "\n")
        i+= 1

    i=1

    while (i<8):
        inputPath = f"./COMP47{j}/Slides/Slide_0{i}.txt"
        text = open(inputPath, "r", encoding="utf8")
        readText = text.read()
        nlp = spacy.load('en_core_web_sm')
        nlp.add_pipe('entityfishing')
        doc = nlp(readText)

        outputPath = f'COMP47{j}/Slides/Slide_0{i}_LinkedEntities.txt'

        file = open(outputPath, "w", encoding = "utf8")
        
        for span in doc.ents:
            if (span.label_ != 'CARDINAL' and span.label_ != 'ORDINAL' and span.label_ != 'PRODUCT' and span.label_ != 'LOC' and span._.kb_qid != None):
                file.write(str((span.text, span.label_, span._.kb_qid, span._.url_wikidata, span._.nerd_score)) + "\n")
        i+= 1
    j+=2