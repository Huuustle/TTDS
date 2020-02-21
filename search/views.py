from django.shortcuts import render,get_object_or_404
from .retrieval import SearchModel
from .models import News, Knearest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from time import *
from .spell_checker import sp
import re

def home(request):
    return render(request, 'home.html')

def search(request):
    begin_time = time()
    str = request.GET.get('oq')
    relevancy = request.GET.get('relevancy') if request.GET.get('relevancy') != None else "1"
    relevancy = int(relevancy)
    test_list = []
    spell_bol = True
    if str != None:
        list = str.split('+')
        query = ''
        for i in list:
            query = query + i + ' '

        #spell check
        query_list, spell_bol = sp(query)
        if spell_bol == False:
            query_check = ''
            for one in query_list:
                query_check = query_check + one + ' '

        se = SearchModel('config.ini', 'utf-8')
        flag, rs = se.search(query, relevancy)
        items = []
        length = len(rs) if len(rs) <= 100 else 100
        rs = rs[:100] if len(rs)>100 else rs
        for news in rs:
            doc_id = news[0]
            item = News.objects.get(id=doc_id)
            item_list = []
            q_list = query.lower().strip().split(' ')
            for each_word in q_list:
                content = item.content.replace('\\n', ' ').lower()
                pattern = re.compile('[,.][^,.]*' + each_word + '[^,.]*[,.]')
                if len(item_list) > 5:
                    continue
                for i in pattern.findall(content)[:5]:
                    item_list.append(i)

            n = '...'.join(item_list).replace(',', '').strip('.')
            item.content = n + '...'
            items.append(item)

        paginator = Paginator(items, 10)
        current_page = int(request.GET.get("page", 1))
        page = paginator.page(current_page)

        max_page_count = 5
        max_page_count_half = int(max_page_count / 2)
        # 判断页数是否大于max_page_count
        if paginator.num_pages >= max_page_count:
            # 得出start位置
            if current_page <= max_page_count_half:
                page_start = 1
                page_end = max_page_count + 1
            else:
                if current_page + max_page_count_half + 1 > paginator.num_pages:
                    page_start = paginator.num_pages - max_page_count
                    page_end = paginator.num_pages + 1
                else:
                    page_start = current_page - max_page_count_half
                    page_end = current_page + max_page_count_half + 1
            page_range = range(page_start, page_end)
        else:
            page_range = paginator.page_range
    else:
        str = ""
    end_time = time()
    run_time = round((end_time - begin_time),2)

    return render(request, 'search.html',locals())

def result(request):
    id = request.GET.get('id')
    news = get_object_or_404(News, pk=id)
    knearest = get_object_or_404(Knearest, pk=id)
    first = get_object_or_404(News, pk=knearest.first)
    second = get_object_or_404(News, pk=knearest.second)
    third = get_object_or_404(News, pk=knearest.third)
    fourth = get_object_or_404(News, pk=knearest.fourth)
    fifth = get_object_or_404(News, pk=knearest.fifth)
    return render(request, 'result.html',locals())