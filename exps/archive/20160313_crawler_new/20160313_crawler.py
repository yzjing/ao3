
# coding: utf-8

# In[1]:

from bs4 import BeautifulSoup as bs
import urllib2
import re
import csv
from collections import OrderedDict, Counter
import cookielib
import time


# In[2]:

start = 'http://archiveofourown.org/tags/Sherlock%20(TV)/works'
outfile = './sherlock_0_1000.csv'
start_page = 0
max_page = 1000


# In[3]:

cookie_file = './cookie'


# In[77]:

def save_cookie(cookie_file):
    cookie = cookielib.MozillaCookieJar(cookie_file)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    response = opener.open('http://archiveofourown.org/works/5051548?view_adult=true')
    cookie.save(ignore_discard=True, ignore_expires=True)


# In[78]:

def load_cookie(cookie_file):
    cookie = cookielib.MozillaCookieJar()
    cookie.load(cookie_file, ignore_discard=True, ignore_expires=True)
    return cookie


# In[79]:

# save_cookie(cookie_file)
cookie = load_cookie(cookie_file)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))


# In[80]:

def find_page(base_url, page_number):
    #go to any page number.
    return base_url+'?page=' +str(page_number)


# In[81]:

def find_works(page):
    #Find all works from a works list page.
    works_page = bs(urllib2.urlopen(page))
    links = []
    for link in works_page.find_all('a'):
        try:
            url = link.get('href')
            url_s = [i for i in url.split('/') if i != '']
            if 'work' in url and len(url_s) == 2 and str(url_s[1]).isdigit():
                    links.append('http://archiveofourown.org'+link.get('href'))
        except:
            pass
    return links


# In[82]:

def show_full_contents(url):
    #go through adult contents filtering.
    base = bs(urllib2.urlopen(url))
    full_url = url
    for link in base.find_all('a'):
        if 'Proceed' in link.text:
            full_url = url +'?view_adult=true'
    return full_url


# In[83]:

def get_contents(url, opener=opener):
#     get work metadata and contents from the work page.
    try:
        req = urllib2.Request(url)
        page = bs(opener.open(req))
        contents = str(page.body.text.encode('utf-8'))
    except:
        contents = ''
        pass
    return url, contents


# In[84]:

def get_comments_time(url, opener=opener):
    req = urllib2.Request(url)
    page = bs(opener.open(req))
    times = []
    month_dict = {'Jan':'01', 'Feb':'02','Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
    for line in str(page).split('<span class="posted datetime">'):
        month = re.findall('Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec', line)[0]
        year = re.findall('<span class="year">([0-9]*)</span>', line)
        if month != [] and year != []:
            times.append(str(year[0]) + '-' + month_dict.get(month))
    c = Counter(times)
    times_dict = {time:c[time] for time in times}
    return times_dict


# In[85]:

def get_bookmarks_time(url, opener=opener):
    req = urllib2.Request(url)
    page = bs(opener.open(req))
    page_list = [i for i in re.findall('<a href="(.*?)>', str(page)) if 'bookmarks?' in i]
    page_list = sorted(list(set([i.split()[0].replace('\"', '') for i in page_list])))       
        
    dt = re.findall('<p class="datetime">(.*?)</p>', str(page))
    times = []
    month_dict = {'Jan':'01', 'Feb':'02','Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
    for time in dt:
        times.append(time.split()[2] + '-' + month_dict.get(time.split()[1]))
    times = times[1:]
    if page_list != []:
        for page in page_list:
            times += get_bookmarks_time_subpages('http://archiveofourown.org'+page, opener=opener)
        
        
    c = Counter(times)
    times_dict = {time:c[time] for time in times}
    return times_dict


# In[86]:

def get_bookmarks_time_subpages(url, opener=opener):
    req = urllib2.Request(url)
    page = bs(opener.open(req))
    dt = re.findall('<p class="datetime">(.*?)</p>', str(page))
    times = []
    month_dict = {'Jan':'01', 'Feb':'02','Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
    for time in dt:
        times.append(time.split()[2] + '-' + month_dict.get(time.split()[1]))
    times = times[1:]
    return times


# In[87]:

def write_header(outfile):
    f = open(outfile, 'a')
    writer = csv.writer(f, delimiter=',')
    keys = ['Additional_Tags', 'Archive_Warnings', 'Author', 'Bookmarks', 'Category', 'Chapters', 'Characters',             'Comments', 'CompleteDate', 'Fandoms', 'Hits', 'Kudos', 'Language', 'Notes', 'PublishDate', 'Rating',             'Relationship', 'Summary', 'Text', 'Title', 'UpdateDate', 'Words']
    writer.writerow(keys)
    f.close()


# In[88]:

def write_work_content(work_dict,outfile):
    #write work metadata and contents as values of a sorted dictionary.
    f = open(outfile, 'a')
    writer = csv.writer(f, delimiter=',')
    try:
        writer.writerow(OrderedDict(sorted(work_dict.items())).values())
    except:
        pass
    f.close()


# In[89]:

#creates dictionary for information in a single work.
def create_work_dict(url, contents):
#     get work metadata and contents into a dictionary.

    work = {}
    
    try:
        rating = re.findall('Rating:(.*?)<br />',contents) 
        warning = re.findall('Warnings:(.*?)<br />',contents)
        fandom = re.findall(r'Fandoms:\\n          \\n\\n\\n(.*?)\\n\\n\\n\\n|Fandom:\\n          \\n\\n\\n(.*?)\\n\\n\\n\\n',contents)
        category = re.findall(r'Categories:\\n          \\n\\n\\n(.*?)\\n\\n\\n\\n|Category:\\n          \\n\\n\\n(.*?)\\n\\n\\n\\n',contents)
        relationship = re.findall('Relationships:(.*?)<br />',contents)
        characters = re.findall('Characters:(.*?)<br />',contents)
        additional = re.findall('Additional Tags:(.*?)<br />',contents)
        language = re.findall(r'Language:\\n      \\n\\n        (.*?)\\n      \\n',contents)
        author = re.findall(r'<strong>(.*?)</strong>',contents)[1]
        text = re.findall(r'Work Text:(.*?)\\n\\n\\n\\n\\n\\n\\n\\n|Chapter Text\\n(.*?)\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n|Chapter Text\\n\\n\\n\\n\\n\\n(.*?)',contents)
        text = [i for i in text[0] if i != ''] if text != [] else []
        title = re.findall(r'<strong>(.*?)</strong>',contents)[0]
        summary = re.findall('>Summary: <p>(.*?)</p>',contents)
        notes = re.findall(r'Notes:\\n\\n(.*?)\\n\\n',contents)
        publishdate = re.findall('Published:([0-9]*-[0-9]*-[0-9]*)',contents)
        completedate = re.findall('Completed:([0-9]*-[0-9]*-[0-9]*)',contents)
        updatedate = re.findall('Updated:([0-9]*-[0-9]*-[0-9]*)',contents)
        words = re.findall('Words:([0-9]*)',contents)
        chapters = re.findall('Chapters:([0-9]*/[0-9]*)',contents)
        kudos = re.findall('Kudos:([0-9]*)',contents)
        hits = re.findall('Hits:([0-9]*)',contents)  
        comments = re.findall('Comments:([0-9]*)',contents)
        bookmarks = re.findall('Bookmarks:([0-9]*)',contents)


        work['Rating'] = rating[0] if rating != [] else ''
        work['Archive_Warnings'] = warning[0] if warning != [] else ''
        work['Fandoms'] = [i for i in fandom[0] if i != ''][0] if fandom != [] else ''
        work['Category'] = [i for i in category[0] if i != ''][0] if category != [] else ''
        work['Relationship'] = relationship[0] if relationship != [] else '' 
        work['Characters'] = characters[0] if characters != [] else ''
        work['Additional_Tags'] = additional[0] if additional != [] else ''
        work['Language'] = language[0] if language != [] else ''
        work['Author'] = author
        work['Text']= text[0] if text != [] else ''
        work['Title']  = title
        work['Summary'] = summary[0] if summary != [] else ''
        work['Notes'] = notes[0] if notes != [] else ''
        work['PublishDate'] = publishdate[0] if publishdate != [] else ''
        work['CompleteDate'] = completedate[0] if completedate != [] else ''
        work['UpdateDate'] = updatedate[0] if updatedate != [] else ''
        work['Words'] = words[0] if words != [] else ''
        work['Chapters'] = chapters[0] if chapters != [] else ''
        work['Kudos'] = kudos[0] if kudos != [] else ''
        work['Hits'] = hits[0] if hits != [] else ''
        work['Comments'] = comments[0] if comments != [] else ''
        work['Bookmarks'] = bookmarks[0] if bookmarks != [] else ''

        if len(work['Chapters']) > 2:
            if work['Chapters'][2]== '1':
                work['CompleteDate'] = work['PublishDate']


        if work['Comments'] > 0 and 'works' in url:
            id = [i for i in re.findall('[0-9]*', url) if i != ''][0]
            comments_url = 'http://archiveofourown.org/comments/show_comments?work_id=' + str(id) 
            work['Comments'] = get_comments_time(comments_url, opener=opener)
            if work['Comments'] == {}:
                work['Comments'] = ''

        if work['Comments'] > 0 and 'chapters' in url:
            id = [i for i in re.findall('[0-9]*', url) if i != ''][1]
            comments_url = 'http://archiveofourown.org/comments/show_comments?chapter_id=' + str(id) 
            work['Comments'] = get_comments_time(comments_url, opener=opener)
            if work['Comments'] == {}:
                work['Comments'] = ''

        if work['Bookmarks'] > 0:
            id = [i for i in re.findall('[0-9]*', url) if i != ''][0]        
            bookmarks_url = 'http://archiveofourown.org/works/' + id + '/bookmarks'
            work['Bookmarks'] = get_bookmarks_time(bookmarks_url)
            if work['Bookmarks'] == {}:
                work['Bookmarks'] = ''

    except:
        pass
    return work


# In[91]:

content = get_contents('http://archiveofourown.org/works/6242977')
w =  create_work_dict('http://archiveofourown.org/works/6242977', str(content))
for i in w:
    print i, w[i]


# In[92]:

def get_chapters_list(url,opener=opener):
    url_full = show_full_contents(url)
    chapters_list = []
    navigate = ''
    
    req = urllib2.Request(url_full)
    page = bs(opener.open(req))
    for link in page.find_all('a'):
        if 'Chapter Index' in link.text and len(link.get('href')) > 1:
            navigate = 'http://archiveofourown.org' + link.get('href')
    
    if navigate != '':
        req2 = urllib2.Request(navigate)
        page2 = bs(opener.open(req2))
        for link in page2.find_all('a'):
            if 'chapters' in link.get('href'):
                chapters_list.append('http://archiveofourown.org' + link.get('href'))
    return chapters_list


# In[93]:

def read_single_work(url):
    url_full = show_full_contents(url)
    c = get_contents(url_full)
    work = create_work_dict(url_full, str(c))
    write_work_content(work,outfile)

#main loop
write_header(outfile)
start_time = time.clock()
count = 0

for i in range(start_page, max_page+1):
    try:
        page = find_page(start, i)
        worklist = find_works(page)
        for w in worklist:
            ch_list = get_chapters_list(w)
            if ch_list != []:
                read_single_work(w)
                for ch in ch_list:
                    read_single_work(ch)
            else:
                read_single_work(w)
            count += 1
        # print 'crawling page:', i
    except:
        pass

print 'Saved %s works from %s pages of tag %s in %s seconds .' %(count, i, 'Sherlock Holmes', str(time.clock() - start_time))        




