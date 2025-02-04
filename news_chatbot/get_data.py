from crawling import get_html, get_news_contents
import datetime
from types import SimpleNamespace
import yfinance as yf
import pandas as pd


def Timestamp(unixtime) :
    dt = datetime.datetime.utcfromtimestamp(unixtime)
    return dt

def NewsData(company_name = 'IONQ') :
    
    news_list = yf.Search(company_name, news_count=5).news
    current_utc_date = datetime.datetime.utcnow().date() #현재 UTC 기준 날짜 
    
    news_data = []

    for news in news_list:
        
        news = SimpleNamespace(**news)
        news_publishtime = Timestamp(news.providerPublishTime)
        news_publishdate = news_publishtime.date() 
        
        if (news_publishdate == current_utc_date) and (news.publisher not in ['Barrons.com', 'MT Newswires']): 
            
            soup = get_html(news.link)
            news_detail = get_news_contents(soup , news.publisher) 
        

            news_data.append({'title' : news.title , # 뉴스제목 
                            'url' : news.link , # 뉴스 url 
                            'publisher' : news.publisher , #언론사
                            'publishtime' : news_publishtime, #언론 날짜 및 시간
                            'news_detail' : news_detail}) #뉴스 상세 내용 
    
    return news_data