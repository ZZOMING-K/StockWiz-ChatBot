import pymongo
from pymongo import MongoClient 
from get_data import NewsData 
from pytz import utc
import logging
import pandas as pd 
import os 
from dotenv import load_dotenv
from pymongo.server_api import ServerApi

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

load_dotenv() #.env 파일 로드 

mongo_url = os.getenv("MONGO_URL") #환경변수에서 MONGO_URL 가져오기 
client = MongoClient(mongo_url , server_api=ServerApi('1')) #MongoDB 연결 
db = client["news_database"] #데이터 베이스 이름 설정 

#수집할 기업 리스트 정의
company_df = pd.read_csv('./data/nasdaq_100.csv')
company_name_list = company_df ['Symbol'].tolist()
companies = [company.strip() for company in company_name_list]

    
for company in companies :
    try : 
        news_data = NewsData(company_name=company)
        
        if news_data : 
            collection_name = f"{company}_news"
            collection = db[collection_name]
            collection.create_index("url" , unique = True) #url 필드에 대해서 고유 인덱스 생성 
            
            try : 
                collection.insert_many(news_data , ordered=False) #중복된 문서가 있어도 계속해서 삽입
                logging.info(f"Inserted {len(news_data)} documents into {collection_name}")
            
            except pymongo.errors.BulkWriteError as e:
                logging.info(f"All documents skipped for {company} due to duplication.")
        
        else : 
            logging.info(f"No news data found for {company}")
            
    except Exception as e:
        logging.error(f"Error processing {company}: {e}")