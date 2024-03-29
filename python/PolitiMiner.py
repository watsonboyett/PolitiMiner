
import urllib2, re
from bs4 import BeautifulSoup



# get main people page
url_base = "http://www.politifact.com"
url_add = "/personalities/"
page_url = url_base + url_add
page = []
while len(page)<1:
    page = urllib2.urlopen(page_url).read()

                   
# parse list for available people
soup = BeautifulSoup(page,from_encoding="UTF-8")
tags = soup.find_all('a',href=re.compile('/personalities/'))


# minimize the set (unique hits only)
urls = set()
for tag in tags:
        urls.add(tag.attrs['href'])

# convert to list (for indexing)
urls = list(urls)
x = len(urls)
print "found " + str(x) + " entities! \n"


d_attrs = ['True','Mostly-True','Half-True','Mostly-False','False','Pants-on-Fire']
d_type = ['c','c','c','c','c','c']
# skip, if there are no people (not sure why this error occurs..)
if x>0:

    # write attributes to file
    f = open('../data/data.tab','w')
    f.write('name\t')
    f.write('assoc\t')
    for j in range(len(d_attrs)):
        f.write(d_attrs[j] + '\t')
    f.write('\n')
    # write data-type to file
    f.write('d\t')
    f.write('d\t')
    for j in range(len(d_type)):
        f.write(d_type[j] + '\t')
    f.write('\n')
    # write class to file
    f.write('\tclass\n')

    # iterate over all urls, extracting page data
    i = 0
    while i<x:
        # get page
        page_url = url_base + urls[i]
        page = urllib2.urlopen(page_url).read()
        print str(i) + ": " + page_url

        # repeat, if page didn't load properly
        if len(page)<1:
            continue
        
        # parse page
        soup = BeautifulSoup(page, from_encoding="UTF-8")
        if soup.contains_replacement_characters:
            continue

        # get entity name
        tags = soup.find('div',attrs={'class' : "pfhead"})
        name = tags.text[0:-8].strip().encode('ascii','ignore')

        # get entity assoc
        tags = soup.find_all('h6',limit=1)
        if len(tags)>0:
            assoc = tags[0].text.strip().split(' ')[0].encode('ascii','ignore')
        else:
            assoc = "undef"

        # get entity meter data
        vals = []
        tags = soup.find_all('span',attrs={'class':'count'})
        for tag in tags:
            val = tag.text.strip().split('(')[0].encode('ascii','ignore')
            vals.append(val)
        
        
        # display entity info
        print name + ", " + assoc
        print str(vals) + "\n"        

        # write info to file
        f.write(name + '\t')
        f.write(assoc + '\t')
        for j in range(len(vals)):
            f.write(vals[j] + '\t')
        f.write('\n')
        

        i = i + 1


    f.close()
