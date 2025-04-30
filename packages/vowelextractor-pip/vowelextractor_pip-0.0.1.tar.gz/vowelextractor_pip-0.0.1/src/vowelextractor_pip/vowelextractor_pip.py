def vowel_extractor(st):
    """
    Extract all vowels from the input string.
    """
    vowels = 'aeiouAEIOU'
    vow = ''
    for i in st:
        if i in vowels:
            vow += i
    return vow

