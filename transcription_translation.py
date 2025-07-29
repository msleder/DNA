import time
from easygui import *

def transcription(sequence):
    mrna = ""
    sequence = sequence.upper()

    for nucleobase in sequence:
        if nucleobase not in "ATCG":
            print("Impossible nucleotide base entered.")
            quit()
        if nucleobase == "T":
            mrna += "A"
        elif nucleobase == "A":
            mrna += "U"
        elif nucleobase == "G":
            mrna += "C"
        elif nucleobase == "C":
            mrna += "G"
    return mrna


def findStart(mrna):
    for i in range(len(mrna)):
        if mrna[i-2] == "A" and mrna[i-1] == "U" and mrna[i] == "G":
            return i-2, True
        
    msgbox("Error, Met (start) not found. Proceeding with translation from start.")
    return 0, False


def findEnd(mrna, start):
    mrna = mrna[start:]
    for i in range (start+6, len(mrna)):
        if mrna[i-2] == "U":

            if mrna[i-1] == "A":
                if mrna[i] == "G" or mrna[i] == "A":
                    return i+2, True
                
            if mrna[i-1] == "G" and mrna[i] == "A":
                    return i+2, True
            
    msgbox("Error, Stop not found. Proceeding with translation without it.")
    return len(mrna), False


def cutToLength(mrna, start_present, end_present):
    if len(mrna)%3 == 0:
        return mrna
    if len(mrna) != 0 and start_present and end_present:
        msgbox("Impossible to translate, wrong length of sequence.")
        quit()
    if len(mrna) != 0 and start_present and not end_present:
        return mrna[:len(mrna)-len(mrna)%3]
    if len(mrna) != 0 and not start_present and end_present:
        return mrna[len(mrna)%3:]
    if len(mrna)%3 != 0 and not start_present and not end_present:
        return mrna[:len(mrna)-len(mrna)%3]


def translate(mrna, start_present, end_present):
    codon_string = ""
    start_num = 0
    end_num = len(mrna)+1
    if start_present:
        codon_string += "Met, "
        start_num += 3
    if end_present:
        end_num -= 3

    for i in range(start_num + 2,end_num, 3):
        if mrna[i-2] == "U":
            if mrna[i-1] == "C":
                codon_string += "Ser"
            elif mrna[i-1] == "U":
                if mrna[i] == "U" or mrna[i] == "C":
                    codon_string += "Phe"
                else:
                    codon_string += "Leu"
            elif mrna[i-1] == "A":
                codon_string += "Tyr"
            elif mrna[i-1] == "G":
                if mrna[i] == "G":
                    codon_string += "Trp"
                else:
                    codon_string += "Cys"
        elif mrna[i-2] == "C":
            if mrna[i-1] == "U":
                codon_string += "Leu"
            elif mrna[i-1] == "C":
                codon_string += "Pro"
            elif mrna[i-1] == "G":
                codon_string += "Arg"
            elif mrna[i-1] == "A":
                if mrna[i] == "U" or mrna[i] == "C":
                    codon_string += "Hist"
                else:
                    codon_string += "Gln"
        elif mrna[i-2] == "A":
            if mrna[i-1] == "U":
                codon_string += "Ile"
            elif mrna[i-1] == "C":
                codon_string += "Thr"
            elif mrna[i-1] == "A":
                if mrna[i] == "U" or mrna[i] == "C":
                    codon_string += "Asn"
                else:
                    codon_string += "Lys"
            elif mrna[i-1] == "G":
                if mrna[i] == "U" or mrna[i] == "C":
                    codon_string += "Ser"
                else:
                    codon_string += "Arg"
        else:
            if mrna[i-1] == "U":
                codon_string += "Val"
            elif mrna[i-1] == "C":
                codon_string += "Ala"
            elif mrna[i-1] == "G":
                codon_string += "Gly"
            elif mrna[i-1] == "A":
                if mrna[i] == "U" or mrna[i] == "C":
                    codon_string += "Asp"
                else:
                    codon_string += "Glu"

        if end_present or i <= end_num - 3:
            codon_string += ", "
 
    if end_present:
        codon_string += "Stop"
    return codon_string


def runSequence():
    img = "/home/melani/Documents/projects/DNA/Transcribe_Translate.png"
    msgbox(msg="Welcome to the DNA transcriber and translator!", image=img)
    sequence = enterbox("Enter DNA sequence here: ")
    mrna = transcription(sequence)
    msgbox("Transcribing DNA to mRNA...")
    msgbox(f"mRNA sequence: {mrna}")
    start, start_present = findStart(mrna)
    end, end_present = findEnd(mrna,start)
    msgbox("Trimming mRNA if needed...")
    mrna = mrna[start:end+1]
    mrna = cutToLength(mrna, start_present, end_present)
    msgbox(f"mRNA to be translated: {mrna}")
    msgbox("Translating mRNA to amino acids to be created using codons...")
    amino_acids = translate(mrna, start_present, end_present)
    msgbox(f"Amino acids: {amino_acids}")


runSequence()