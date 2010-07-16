# heart of project

import re
import PPStemmer
from google.appengine.ext import db


split2words = re.compile(u'[^a-zA-Zа-яА-Я]+')
# stop_words taken from PostgreSQL 8.4 distribution. Thanks to Fedor and Oleg!
stop_words = set([
u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u'your',
u'yours', u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', u'her',
u'hers', u'herself', u'it', u'its', u'itself', u'they', u'them', u'their', u'theirs',
u'themselves', u'what', u'which', u'who', u'whom', u'this', u'that', u'these', u'those',
u'am', u'is', u'are', u'was', u'were', u'be', u'been', u'being', u'have', u'has', u'had',
u'having', u'do', u'does', u'did', u'doing', u'a', u'an', u'the', u'and', u'but', u'if',
u'or', u'because', u'as', u'until', u'while', u'of', u'at', u'by', u'for', u'with',
u'about', u'against', u'between', u'into', u'through', u'during', u'before', u'after',
u'above', u'below', u'to', u'from', u'up', u'down', u'in', u'out', u'on', u'off', u'over',
u'under', u'again', u'further', u'then', u'once', u'here', u'there', u'when', u'where',
u'why', u'how', u'all', u'any', u'both', u'each', u'few', u'more', u'most', u'other',
u'some', u'such', u'no', u'nor', u'not', u'only', u'own', u'same', u'so', u'than', u'too',
u'very', u's', u't', u'can', u'will', u'just', u'don', u'should', u'now',

u'и', u'в', u'во', u'не', u'что', u'он', u'на', u'я', u'с', u'со', u'как', u'а', u'то',
u'все', u'она', u'так', u'его', u'но', u'да', u'ты', u'к', u'у', u'же', u'вы', u'за', u'бы',
u'по', u'только', u'ее', u'мне', u'было', u'вот', u'от', u'меня', u'еще', u'нет', u'о',
u'из', u'ему', u'теперь', u'когда', u'даже', u'ну', u'вдруг', u'ли', u'если', u'уже',
u'или', u'ни', u'быть', u'был', u'него', u'до', u'вас', u'нибудь', u'опять', u'уж', u'вам',
u'ведь', u'там', u'потом', u'себя', u'ничего', u'ей', u'может', u'они', u'тут', u'где',
u'есть', u'надо', u'ней', u'для', u'мы', u'тебя', u'их', u'чем', u'была', u'сам', u'чтоб',
u'без', u'будто', u'чего', u'раз', u'тоже', u'себе', u'под', u'будет', u'ж', u'тогда',
u'кто', u'этот', u'того', u'потому', u'этого', u'какой', u'совсем', u'ним', u'здесь',
u'этом', u'один', u'почти', u'мой', u'тем', u'чтобы', u'нее', u'сейчас', u'были', u'куда',
u'зачем', u'всех', u'никогда', u'можно', u'при', u'наконец', u'два', u'об', u'другой',
u'хоть', u'после', u'над', u'больше', u'тот', u'через', u'эти', u'нас', u'про', u'всего',
u'них', u'какая', u'много', u'разве', u'три', u'эту', u'моя', u'впрочем', u'хорошо',
u'свою', u'этой', u'перед', u'иногда', u'лучше', u'чуть', u'том', u'нельзя', u'такой',
u'им', u'более', u'всегда', u'конечно', u'всю', u'между', u'сиськами'
])


class Word(db.Model):
    stem  = db.StringProperty(required = True)
    total = db.IntegerProperty(required = True)
    spam  = db.IntegerProperty(required = True)


def _filter_stop_words(word):
    return (word and word not in stop_words)


def mark_as_spam(text):
    _update_text(text, "spam")


def mark_not_spam(text):
    _update_text(text, "organic")


def _update_text(text, type):
    words = split2words.split(text)
    words = map(lambda x:x.lower(), words)

    words = filter(_filter_stop_words, words)
    words = map(PPStemmer.stem, words)

    uniq_words = {}
    for w in words:
        uniq_words[w] = (uniq_words[w] + 1 if w in uniq_words else 1) # very ugly

    # save data
    for w in uniq_words.keys():
        count = uniq_words[w]
        spam_count = (count if type == "spam" else 0)

        query = Word.gql("WHERE stem = :1", w)
        word  = query.get()
        if word is None:
            word = Word(stem = w, total = count, spam = spam_count)
            word.put()
        else:
            db.run_in_transaction(_update_word, word.key(), count, spam_count)

    return len(uniq_words.keys())


def _update_word(key, count, spam_count):
    word = db.get(key)
    word.total += count
    word.spam  += spam_count

    db.put(word)


def is_spam(text, spam_weight = 70):
    words = split2words.split(text)

    words = filter(_filter_stop_words, words)
    words = map(PPStemmer.stem, words)

    uniq_words = {}
    for w in words:
        uniq_words[w] = (uniq_words[w] + 1 if uniq_words[w] else 1) # very ugly

    weight = 0
    # hope I correctly get max portion size
    i, portion, wcount = 0, 30, len(words)
    while i < wcount:
        wportion = words[i:i+portion]
        i += portion

        ws = Word.gql("WHERE stem in :1", wportion).fetch()

        for word in ws:
            word_weight = float(word.spam)/word.total
            word_count  = uniq_words[word]
            validity    = float(word_count)/wcount

            weight += validity * word_weight


    weight *= 100

    return (1 if weight > spam_weight else 0)

