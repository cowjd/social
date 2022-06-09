from django.shortcuts import get_object_or_404, render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Choice, Question


import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

import pandas as pd
from konlpy.tag import Hannanum

import requests
from bs4 import BeautifulSoup
import json
import re
import sys
import time
import random
import pandas as pd
import pymysql


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class WordCloudView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def wordcloud(request):
    context = {}
    return render(request, 'polls/wordcloud.html', context)


def showwordcloud(request):
    query = request.POST['query']


        # wordcloud 그리기
    hannanum = Hannanum()

    f = open('news_text.txt', 'r', encoding='UTF8')
    lines = f.readlines()
    f.close()

    # 한나눔 형태소 분석기로 명사만 추출
    # 한국어 분석을 할 때는 명사 추출 분석이 가장 일반적임
    temp = []
    for i in range(len(lines)):
        temp.append(hannanum.nouns(lines[i]))
    
    word_list = flatten(temp)
    word_list = pd.Series([x for x in word_list if len(x) > 1])
    # word_list.value_counts().head(10)

    font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'

    wordcloud = WordCloud(
        font_path = font_path,
        width=800,
        height=800,
        background_color="white")

    count = Counter(word_list)
    wordcloud = wordcloud.generate_from_frequencies(count)
    array = wordcloud.to_array()

    fig = plt.figure(figsize=(10,10))
    plt.imshow(array, interpolation="bilinear")
    fig.savefig('wordcloud.png')

    
    context = {"query": query}
    return render(request, 'polls/showwordcloud.html', context)


def get_news(n_url):
    news_detail = []
    print(n_url)
    breq = requests.get(n_url, headers={'User-Agent':'Mozilla/5.0'})
    bsoup = BeautifulSoup(breq.content, 'html.parser')

    # news text
    _text = bsoup.select('#newsct_article')[0].get_text().replace('\n', " ")
    btext = _text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "")
    news_detail.append(btext.strip())


    return news_detail

def get_newsdetail():
    columns = ['내용']
    df = pd.DataFrame(columns=columns)

    query = '코로나'   # url 인코딩 에러는 encoding parse.quote(query)
    s_date = "2022.06.01"
    e_date = "2022.06.04"
    s_from = s_date.replace(".", "")
    e_to = e_date.replace(".", "")
    page = 1


    while True:
        time.sleep(random.sample(range(3), 1)[0])
        print(page)

        url = "https://search.naver.com/search.naver?where=news&query=" + query + \
            "&sort=1&field=1&ds=" + s_date + "&de=" + e_date + \
            "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + \
            "%2Ca%3A&start=" + str(page)
    
    
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        req = requests.get(url, headers=header)
        print(url)
        cont = req.content
        soup = BeautifulSoup(cont, 'html.parser')


        naver_news = soup.find_all("a", {"class": "info"})
        if naver_news == []:
            break


        for a_tag in naver_news:
            try:
                news_url = a_tag.attrs["href"]
                if news_url.startswith("https://news.naver.com"):
                    print(news_url)
                    news_detail = get_news(news_url)
                    print(news_detail)
                    df = df.append(pd.DataFrame(
                        [[news_detail[0]]], columns=columns))
            except Exception as e:
                print(e)
                continue
        break
    
        page += 10

    df.to_csv('news_text.txt')




def flatten(l):
            flatList = []
            for elem in l:
                if type(elem) == list:
                    for e in elem:
                        flatList.append(e)
                else:
                    flatList.append(elem)
            return flatList



# def wordcloud():
#     # wordcloud 그리기
#     hannanum = Hannanum()

#     f = open('news_text.txt', 'r', encoding='UTF8')
#     lines = f.readlines()
#     f.close()

#     # 한나눔 형태소 분석기로 명사만 추출
#     # 한국어 분석을 할 때는 명사 추출 분석이 가장 일반적임
#     temp = []
#     for i in range(len(lines)):
#         temp.append(hannanum.nouns(lines[i]))
    
#     word_list = flatten(temp)
#     word_list = pd.Series([x for x in word_list if len(x) > 1])
#     # word_list.value_counts().head(10)

#     font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'

#     wordcloud = WordCloud(
#         font_path = font_path,
#         width=800,
#         height=800,
#         background_color="white")

#     count = Counter(word_list)
#     wordcloud = wordcloud.generate_from_frequencies(count)
#     array = wordcloud.to_array()

#     fig = plt.figure(figsize=(10,10))
#     plt.imshow(array, interpolation="bilinear")
#     fig.savefig('wordcloud.png')







