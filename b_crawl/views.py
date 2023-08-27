from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as bs4
from b_crawl.forms import ScrapingForm
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def home(request):
    form = ScrapingForm()
    # スクレイピング処理
    if request.method == 'POST':
        form = ScrapingForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            scraped_data = []
            try:
                while url:
                    print(url)
                    response = requests.get(url)
                    response.raise_for_status()

                    soup = bs4(response.content, 'html.parser')
                    title = soup.find('h1').text if soup.find('h1') else ""

                    posts = soup.select('article[id^=cmt_]')
                    for post in posts:
                        postID = post.find(class_='fancybox_com').text if post.find(class_='fancybox_com') else ""
                        print(postID)
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
                return render(request, 'b_crawl/result.html', {'title': title, 'scraped_data': scraped_data})
            except Exception as e:
                return render(request,'b_crawl/result.html')
    
    return render(request, 'b_crawl/home.html', {'form': form})

def result(request, user_input):
    return render(request, 'b_crawl/result.html', {'user_input': user_input})