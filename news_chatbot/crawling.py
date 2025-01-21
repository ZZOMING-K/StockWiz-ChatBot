import requests 
from bs4 import BeautifulSoup as bs

def get_html(url) : 
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://finance.yahoo.com/",
        "Origin": "https://finance.yahoo.com"
    }
    
    response = requests.get(url , headers = headers) # 페이지 접속 
    
    if response.status_code != 200 : 
        print("f 요청 실패 : {response.status_code}")
        
    html_text = response.text 
    soup = bs(html_text , 'html.parser') # html파싱 
    return soup 

# 언론사에 따라 다르게 크롤링 
def get_news_contents(soup , publisher) :
    
    news_contents = soup.find(attrs = {"class" : "body-wrap yf-i23rhs"}) 
    
    if (news_contents is None)  and (publisher == "Investor's Business Daily") :
        new_url = soup.select_one("a.link.caas-button.readmore-button-finance").attrs['href']
        soup = get_html(new_url)
        news_contents = soup.find(attrs = {"class" : "main-content-column" })

    if news_contents is None :
        news_contents = soup.find(attrs = {'class' : 'caas-body'})

    if news_contents is None :
        print("내용을 확인할 수 없습니다.")
        
    news_detail = news_contents.get_text(separator=" " , strip = True)
    
    return news_detail

