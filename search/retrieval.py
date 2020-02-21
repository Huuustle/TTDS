import os
import math
import operator
import re
import sqlite3
import configparser
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from datetime import *

class SearchModel:
    config_path = ''
    config_encoding = ''

    k1 = 0
    b = 0
    data_len = 0
    average_len = 0

    conn = None

    def __init__(self,config_path,config_encoding):
        config_path = os.path.dirname(os.path.abspath(__file__)) + '/' + config_path
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        self.k1 = float(config['DEFAULT']['k1'])
        self.b = float(config['DEFAULT']['b'])
        self.data_len = int(config['DEFAULT']['n'])
        self.average_len = float(config['DEFAULT']['avg_len'])
        self.conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__))+'/'+config['DEFAULT']['db_path'])

    def __del__(self):
        self.conn.close()

    def process_news(self, news):
        term_count_dict = {}

        for term in news:
            if term in term_count_dict:
                term_count_dict[term] = term_count_dict[term]+1
            else:
                term_count_dict[term] = 1

        return len(news), term_count_dict
    def preprocessing(self, text):
        # token and case folding
        lower_text = text.lower().strip('\n')
        pre = r"https?(\S*)?"
        new_text = re.sub(pre, ' ', lower_text)
        pre1 = r"[^\w@ _]"
        new_text = re.sub(pre1, ' ', new_text)
        new_text = re.split(' ', new_text)
        token_list = [i for i in new_text if '' != i]

        # stop words
        stop_list = set(stopwords.words('english'))
        stop_list.update(['“', '‘', '”', '’'])
        stop_filtered = [w for w in token_list if w not in stop_list]

        # stemming
        stem_list = SnowballStemmer('english')
        stem_filtered = [stem_list.stem(w) for w in stop_filtered]
        # stem_string = ' '.join(stem_filtered)
        return stem_filtered
    def small_preprocessing(self, text):
        # token and case folding
        lower_text = text.lower().strip('\n')
        pre = r"https?(\S*)?"
        new_text = re.sub(pre, ' ', lower_text)
        pre1 = r"[^\w@ _]"
        new_text = re.sub(pre1, ' ', new_text)
        new_text = re.split(' ', new_text)
        token_list = [i for i in new_text if '' != i]

        # stemming
        stem_list = SnowballStemmer('english')
        stem_filtered = [stem_list.stem(w) for w in token_list]
        # stem_string = ' '.join(stem_filtered)
        return stem_filtered
    def fetch_from_db(self, term):
        c = self.conn.cursor()
        c.execute('SELECT * FROM postings WHERE term=?', (term,))
        return(c.fetchone())
    def BM25(self,sentence):
        news_list = self.small_preprocessing(sentence)
        doc_len, term_count_dict = self.process_news(news_list)
        BM25_scores = {}
        for term in term_count_dict.keys():
            r = self.fetch_from_db(term)
            if r is None:
                continue
            df = r[1]
            w1 = math.log2((self.data_len - df + 0.5) / (df + 0.5))
            docs = r[2].split('\n')
            for doc in docs:
                docid, doc_len, date, tf = doc.split('\t')
                docid = int(docid)
                tf = float(tf)
                doc_len = int(doc_len)
                s = (self.k1 * tf * w1) / (tf + self.k1 * (1 - self.b + self.b * doc_len / self.average_len))
                if docid in BM25_scores:
                    BM25_scores[docid] = BM25_scores[docid] + s
                else:
                    BM25_scores[docid] = s
        BM25_scores = sorted(BM25_scores.items(), key=operator.itemgetter(1))
        BM25_scores.reverse()
        if len(BM25_scores) == 0:
            return 0, []
        else:
            return 1, BM25_scores

    def time_sort(self, sentence):
        news_list = self.small_preprocessing(sentence)
        doc_len, term_count_dict = self.process_news(news_list)
        time_scores = {}
        for term in term_count_dict.keys():
            r = self.fetch_from_db(term)
            if r is None:
                continue
            docs = r[2].split('\n')
            for doc in docs:
                docid, doc_len, date, tf = doc.split('\t')
                if docid in time_scores:
                    continue
                news_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S ')
                now_time = datetime.now()
                time_interval = now_time - news_time
                docid = int(docid)
                time_interval = (timedelta.total_seconds(time_interval / 3600))
                time_scores[docid] = time_interval
        time_scores = sorted(time_scores.items(), key=operator.itemgetter(1))
        if len(time_scores) == 0:
            return 0, []
        else:
            return 1, time_scores
    def hot_sort(self,sentence):
        news_list = self.small_preprocessing(sentence)
        doc_len, term_count_dict = self.process_news(news_list)
        hot_scores={}
        for term in term_count_dict.keys():
            r = self.fetch_from_db(term)
            if r is None:
                continue
            df = r[1]
            w = math.log2((self.data_len - df + 0.5) / (df + 0.5))
            docs = r[2].split('\n')
            for doc in docs:
                docid, doc_len, date, tf = doc.split('\t')
                docid = int(docid)
                tf = float(tf)
                doc_len = int(doc_len)
                news_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S ')
                now_time = datetime.now()
                time_interval = now_time - news_time
                BM25_score = (self.k1 * tf * w) / (tf + self.k1 * (1 - self.b + self.b * doc_len / self.average_len))
                time_interval = (timedelta.total_seconds(time_interval / 3600))
                hot_score = math.log(BM25_score) + 1 / time_interval
                if docid in hot_scores:
                    hot_scores[docid] = hot_scores[docid] + hot_score
                else:
                    hot_scores[docid] = hot_score
        hot_scores = sorted(hot_scores.items(), key=operator.itemgetter(1))
        hot_scores.reverse()
        if len(hot_scores) ==0:
            return 0,[]
        else:
            return 1,hot_scores

    def search(self,sentence,sort_type):
        if sort_type == 1:
            return self.BM25(sentence)
        elif sort_type == 2:
            return self.time_sort(sentence)
        elif sort_type == 3:
            return self.hot_sort(sentence)

if __name__ == "__main__":
    se = SearchModel('config.ini','utf-8')
    flag,rs = se.search('BBC',0)
    print(rs[:100])
