import unicodedata
import re
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

def basic_clean(s):
    '''
    Takes a string and returns a normalized lowercase string 
    with special characters removed
    '''
    #
    s = s.lower()
    # normalize
    s = unicodedata.normalize('NFKD', s)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    # remove special characters and lowercase
    s = re.sub(r"[^a-z0-9'\s]", '', s)
    return s

def tokenize(s):
    '''
    Takes a string and returns a tokenized version of the string
    '''
    # create tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()
    # return tokenized string
    return tokenizer.tokenize(s, return_str=True)

def stem(s):
    '''
    Takes a string and returns a stemmed version of the string
    '''
    # create porter stemmer
    ps = nltk.porter.PorterStemmer()
    # apply stemmer
    stems = [ps.stem(word) for word in s.split()]
    # join list of words
    stemmed_s = ' '.join(stems)
    # return list of stemmed strings
    return stemmed_s

def lemmatize(s):
    '''
    Takes a string and returns a lemmatized version of the string
    '''
    # create lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()
    # lemmatize split string
    lemmas = [wnl.lemmatize(word) for word in s.split()]
    # join words
    lemmatized_s = ' '.join(lemmas)
    # return lemmatized string
    return lemmatized_s

def remove_stopwords(s, extra_words = [], exclude_words = []):
    '''
    Takes a string and removes stopwords.
    Optional arguments: 
    extra_words adds words to stopword list
    exclude_words words to keep
    '''
    # create stopword list
    stopword_list = stopwords.words('english')
    # remove excluded words
    stopword_list = set(stopword_list) - set(exclude_words)
    # add extra words
    stopword_list = stopword_list.union(set(extra_words))

    #### old version
    # if len(extra_words) > 0:
    #     stopword_list.append(word for word in extra_words)
    # if len(exclude_words) > 0:
    #     stopword_list.remove(word for word in exclude_words)
    
    # split string into word list
    words = s.split()

    # add word to list if it's not in the stopword_list
    filtered_words = [w for w in words if w not in stopword_list]
    # join the filtered words into a string
    s_without_stopwords = ' '.join(filtered_words)
    # return list with removed stopwords
    return s_without_stopwords

def prep_article_data(df, column, extra_words=[], exclude_words=[]):
    '''
    Takes in a dataframe, original string column, with optional lists of words to
    add to and remove from the stopword_list. Returns a dataframe with the title,
    original column, and clean, stemmed, and lemmatized versions of the column.
    '''
    df['clean'] = df[column].apply(basic_clean).apply(tokenize).apply(remove_stopwords, extra_words=extra_words, exclude_words=exclude_words)
    
    df['stemmed'] = df['clean'].apply(tokenize).apply(stem)

    df['lemmatized'] = df['clean'].apply(tokenize).apply(lemmatize)

    
    return df[['title', column,'clean', 'stemmed', 'lemmatized']]