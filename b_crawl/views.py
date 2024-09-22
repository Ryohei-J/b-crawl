import requests
from bs4 import BeautifulSoup as bs4
from b_crawl.forms import ScrapingForm
from django.views.decorators.csrf import csrf_exempt
from .models import History
from django.shortcuts import redirect, render

@csrf_exempt

# ホスラブのスクレイピング
def scrape_hostlove(url):
    scraped_data = []
    try:
        while url:
            response = requests.get(url)
            response.raise_for_status()

            soup = bs4(response.content, 'html.parser')
            title = soup.find('h1').text if soup.find('h1') else ""

            posts = soup.select('article[id^=cmt_]')
            for post in posts:
                postID = post.find(class_='fancybox_com').text if post.find(class_='fancybox_com') else ""
                text = post.find(class_='res').text if post.find(class_='res') else ""
                date = post.find(class_='date').text if post.find(class_='date') else ""

                scraped_data.append({'postID': postID, 'text': text, 'date': date})

            next_page_button = soup.find(class_='gt_bt')
            next_page_num = next_page_button['href'] if next_page_button and 'href' in next_page_button.attrs else None

            if next_page_num:
                split_url = url.rsplit('/', 1)
                base_url = split_url[0]
                url = f"{base_url}/{next_page_num}"
            else:
                url = None

        return title, scraped_data

    except Exception as e:
        return "", []

# 爆サイのスクレイピング
def scrape_bakusai(url):
    scraped_data = []
    try:
        while url:
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'referer': 'https://bakusai.com/'
            }
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()

            soup = bs4(response.content, 'html.parser')
            title_element = soup.select_one('#title_thr strong')
            title = title_element.get_text() if title_element else ""

            posts = soup.select(".article.res_list_article")
            for post in posts:
                postID = post.find(class_='resnumb').text if post.find(class_='resnumb') else ""
                text = post.find(class_='resbody').text if post.find(class_='resbody') else ""
                date = post.find('span', itemprop='commentTime').text if post.find('span', itemprop='commentTime') else ""

                scraped_data.append({'postID': postID, 'text': text, 'date': date})

            next_page_button = soup.find(class_='paging_nextlink_btn')
            if next_page_button:
                next_page_url = next_page_button.find('a')['href']
                url = f"https://bakusai.com{next_page_url}"
            else:
                url = None

        return title, scraped_data

    except Exception as e:
        return "", []

# ホーム画面
def home(request):
    form = ScrapingForm()
    if request.method == 'POST':
        form = ScrapingForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            title = ""
            scraped_data = []
            # ホスラブの場合
            if 'hostlove.com' in url:
                title, scraped_data = scrape_hostlove(url)
            # 爆サイの場合
            elif 'bakusai.com' in url:
                title, scraped_data = scrape_bakusai(url)
            
            # create
            History.objects.create(url=url, title=title)

            request.session['title'] = title
            request.session['scraped_data'] = scraped_data

            return redirect('result')

    return render(request, 'b_crawl/home.html', {'form': form})

# 結果画面
def result(request):
    if 'title' not in request.session or 'scraped_data' not in request.session:
        return redirect('/')
    
    title = request.session.get('title', '')
    scraped_data = request.session.get('scraped_data', [])

    # セッションを削除
    request.session.flush()

    return render(request, 'b_crawl/result.html', {'title': title, 'scraped_data': scraped_data})

# 履歴
def history(request):
    # get
    history_data = History.objects.all()
    if not history_data.exists():
        history_data = ""
    
    # post
    # if request.method == 'POST':

    return render(request, 'b_crawl/history.html', {'history_data': history_data})
