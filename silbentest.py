import re

def split_into_syllables(sentence):
    # Entferne alle Sonderzeichen und Zahlen
    sentence = re.sub('[^a-zA-ZäöüÄÖÜß]', '', sentence)

    # Liste von Vokalen
    vowels = ['a', 'e', 'i', 'o', 'u', 'ä', 'ö', 'ü']

    # Liste von Diphthongs
    diphthongs = ['ai', 'au', 'ei', 'eu', 'ie', 'äu', 'öu', 'ui']

    # Füge nach jedem Vokal ein Leerzeichen ein
    for vowel in vowels:
        sentence = sentence.replace(vowel, vowel + ' ')

    # Füge nach jedem Diphthong ein Leerzeichen ein
    for diphthong in diphthongs:
        sentence = sentence.replace(diphthong, diphthong + ' ')

    # Entferne doppelte Leerzeichen
    sentence = re.sub(' +', ' ', sentence)

    # Teile den Satz in Silben auf
    syllables = sentence.split()

    return syllables

def split_into_sections(sentence):
    # Teile den Satz in Abschnitte auf
    sections = re.split(r'[,.!?;:]', sentence)

    # Entferne Leerzeichen am Anfang und Ende der Abschnitte
    sections = [section.strip() for section in sections if section.strip()]

    return sections

# Beispielaufruf
sentence = "1. The highest mountain in our solar system is Olympus Mons on Mars, reaching a height of about 13.6 miles (22 kilometers)."
sections = split_into_sections(sentence)

for section in sections:
    syllables = split_into_syllables(section)
    print(section)
    print(syllables)
    print()
