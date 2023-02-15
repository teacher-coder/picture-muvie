def isHangeul(ch) -> bool:
    JAMO_START_LETTER = 44032
    JAMO_END_LETTER = 55203
    return ord(ch) >= JAMO_START_LETTER and ord(ch) <= JAMO_END_LETTER

def isAlphabet(ch) -> bool:
    UPPER_A_LETTER = 65
    UPPER_Z_LETTER = 90
    LOWER_A_LETTER = 97
    LOWER_Z_LETTER = 122
    return (ord(ch) >= UPPER_A_LETTER and ord(ch) <= UPPER_Z_LETTER) or (ord(ch) >= LOWER_A_LETTER and ord(ch) <= LOWER_Z_LETTER)

def isSpace(ch) -> bool:
    return ord(ch) == 32

def count_lyric_type(lyric: str) -> dict:
    chr_dict = {'alphabet':0, 'hangeul':0, 'space':0, 'special':0}
    for c in lyric:
        if isAlphabet(c):
            chr_dict['alphabet'] += 1
        elif isHangeul(c):
            chr_dict['hangeul'] += 1
        elif isSpace(c):
            chr_dict['space'] += 1
        else:
            chr_dict['special'] += 1
    return chr_dict

def get_unit_length(lyric: str) -> int:
    chr_dict = count_lyric_type(lyric)
    return int(chr_dict['alphabet'] * 0.5 + chr_dict['hangeul'] + chr_dict['space'] + chr_dict['special'] * 0.3)
