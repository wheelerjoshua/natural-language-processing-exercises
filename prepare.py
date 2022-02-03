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
    # lowercase
    s = s.lower()
    # normalize
    s = unicodedata.normalize('NFKD', s)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    # remove special characters
    s = re.sub(r"[^a-z0-9'\s]", '', s)
    return s

def tokenize(s):
    '''
    Takes a string and returns a tokenized version of the string
    '''
    tokenizer = nltk.tokenize.ToktokTokenizer()
    return tokenizer.tokenize(s, return_str=True)

def stem(s):
    '''
    Takes a string and returns a stemmed version of the string
    '''
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in s.split()]
    stemmed_s = ' '.join(stems)
    return stemmed_s

def lemmatize(s):
    '''
    Takes a string and returns a lemmatized version of the string
    '''
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in s.split()]
    lemmatized_s = ' '.join(lemmas)

    return lemmatized_s

def remove_stopwords(s, extra_words = [], exclude_words = []):
    '''
    Takes a string and removes stopwords.
    Optional arguments: 
    extra_words adds words to stopword list
    exclude_words words to keep
    '''
    stopword_list = stopwords.words('english')
    if len(extra_words) > 0:
        stopword_list.append(word for word in extra_words)
    if len(exclude_words) > 0:
        stopword_list.remove(word for word in exclude_words)
    
    words = s.split()
    filtered_words = [w for w in words if w not in stopword_list]
    s_without_stopwords = ' '.join(filtered_words)
    return s_without_stopwords

