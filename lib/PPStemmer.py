# russian && english pure-Python stemming module (snowball algorithm)
# coding: utf-8

import re
from stemming import porter2 # see http://pypi.python.org/pypi/stemming/1.0


stem_caching = 0
stem_cache = {}

vowel = re.compile(u'аеиоуыэюя')
perfectiveground = re.compile(u'((ив|ивши|ившись|ыв|ывши|ывшись)|((?<=[ая])(в|вши|вшись)))$')
reflexive = re.compile(u'(с[яь])$')
adjective = re.compile(u'(ее|ие|ые|ое|ими|ыми|ей|ий|ый|ой|ем|им|ым|ом|его|ого|ему|ому|их|ых|ую|юю|ая|яя|ою|ею)$')
participle = re.compile(u'((ивш|ывш|ующ)|((?<=[ая])(ем|нн|вш|ющ|щ)))$')
verb = re.compile(u'((ила|ыла|ена|ейте|уйте|ите|или|ыли|ей|уй|ил|ыл|им|ым|ен|ило|ыло|ено|ят|ует|уют|ит|ыт|ены|ить|ыть|ишь|ую|ю)|((?<=[ая])(ла|на|ете|йте|ли|й|л|ем|н|ло|но|ет|ют|ны|ть|ешь|нно)))$')
noun = re.compile(u'(а|ев|ов|ие|ье|е|иями|ями|ами|еи|ии|и|ией|ей|ой|ий|й|иям|ям|ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я)$')
rvre = re.compile(u'^(.*?[аеиоуыэюя])(.*)')
derivational = re.compile(u'[^аеиоуыэюя][аеиоуыэюя]+[^аеиоуыэюя]+[аеиоуыэюя].*(?<=о)сть?$')

yoe = re.compile(u'ё')

is_pattern = re.compile('Pattern$')

russian_alphabet = re.compile(u'[а-я]')
english_alphabet = re.compile(u'[a-z]')


def s(string_wrapper, search_re, replace):
    """
    Strings are immutable, so to return boolean value and change string
    in-place we must wrap string to mutable type - say, List.
    """

    orig = string_wrapper[0]
    if is_pattern.match( type(search_re).__name__ ):
        string_wrapper[0] = search_re.sub(replace, orig)
    else:
        string_wrapper[0] = re.sub(search_re, replace, orig)

    return orig != string_wrapper[0]


def stem(word):
    """
    Take russian or english unicode word and return its stem using snowball
    algorithm
    """

    word, wlen, stem = word.lower(), len(word), ''

    if wlen <= 2:
        return word

    # check cache
    if stem_caching and stem_cache[word]:
        return stem_cache[word]

    # check if it english or russian
    eng_len = len( russian_alphabet.sub('', word) )
    rus_len = len( english_alphabet.sub('', word) )
    if rus_len > eng_len:
        stem = _stem_rus(word)
    else:
        stem = _stem_eng(word)

    if stem_caching:
        stem_cache[word] = stem

    return stem


def _stem_rus(word):
    """
    Since it is a private function, it should be called from stem(), and thus
    word will be already lowercased
    """

    word = yoe.sub(u'е', word);

    stem = word
    # `while` used like block of code. Executed only once.
    # Can be replaced with (private) subroutine.
    while True:
        m = rvre.match(word)
        if m is None:
            break

        start = m.group(1)
        rv = m.group(2)
        if not rv:
            break

        rv = [rv]

        # step 1
        if not s(rv, perfectiveground, ''):
            s(rv, reflexive, '')

            if s(rv, adjective, ''):
                s(rv, participle, '')
            else:
                if not s(rv, verb, ''):
                    s(rv, noun, '')

        # step 2
        s(rv, u'/и/', '')

        # step 3
        if derivational.match(rv[0]):
            s(rv, u'/ость?/', '')

        # step 4
        if not s(rv, u'/ь/', ''):
            s(rv, u'/ейше?/', '')
            s(rv, u'/нн/', u'н')

        stem = start + rv[0]

        break


    return stem


def _stem_eng(word):
    return porter2.stem(word)


def set_caching(on):
    stem_caching = 1 if on else 0


def clear_cache():
    stem_cache = {}

