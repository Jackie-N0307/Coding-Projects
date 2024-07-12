
from newsapi import NewsApiClient
from KEY import API_KEY
from datetime import date, timedelta


# Get the current date
today = date.today()

# Calculate the date of yesterday
yesterday = today - timedelta(days=1)

newsapi = NewsApiClient(API_KEY)


def get_tophealindes():
    articles_json = newsapi.get_top_headlines(
                                    sources='abc-news-au,australian-financial-review,https://www.bloomberg.com/',
                                    language='en',
                                    page_size=10
                                    )


    result_list = []

    # print(articles_json)
    if 'articles' in articles_json:
        articles = articles_json['articles']
        for article in articles:
            # print("Title:", article.get('title'))
            # print("Date:" + article.get('publishedAt'))
            # print("Description:", article.get('description'))
            # print("URL:", article.get('url'))
            # print()  # Print a blank line between articles

            result_list.append({"title":article.get("title"),"author": article.get('author'),"link":article.get('url')})

    else:
        print("No articles found in the response.")
    
    return result_list


def esg_company_articles(company,stock):

    
    json = newsapi.get_everything(
        q= f"+{company} AND +{stock} AND ASX 200 bank stocks",
        qintitle='title',
        from_param=yesterday,
        language= 'en',
        page_size= 1,
        sort_by="popularity",
        
    )
    result= None
    if 'articles' in json:
        articles = json['articles']
        for article in articles:
            # print("Title:", article.get('title'))
            # print("Date:" + article.get('publishedAt'))
            # print("Description:", article.get('description'))
            # print("URL:", article.get('url'))
            # print()  # Print a blank line between articles
            result = {"title":article.get("title"),"author": article.get('author'),"link":article.get('url')}
            
    else:
        print("No articles found in the response.")
        return None
    
    return result
    