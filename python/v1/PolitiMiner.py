
import urllib2, urllister, MeterReader

timeout = 60

# get main people page
url_base = "http://www.politifact.com"
req = urllib2.Request(url_base+"/personalities/")
usock = urllib2.urlopen(req,None,timeout)
                   
# parse list of available people
parser = urllister.URLLister()
parser.feed(usock.read())
usock.close()
parser.close()                    


# remove non-person links
urls = set()
for url in parser.urls:
    if (url.find("/personalities/")>=0) and (len(url)>=15):
        urls.add(url)

# convert to list (for indexing)
urls = list(urls)
x = len(urls)
print "found " + str(x) + " entities! \n"

# skip, if there are no people
if x>0:
    # get meter data for every person
    mparser = meterreader.meterreader()
    f = open('./data.tab','w')
    i = 0
    while i<x:
        page_url = url_base + urls[i]
        print str(i) + ": " + page_url
        
        # get page (html) and parse desired attributes
        mparser.reset()
        usock = urllib2.urlopen(page_url,None,timeout)
        mparser.feed(usock.read())
        usock.close()
        mparser.close()

        # repeat, if page didn't load properly
        if len(mparser.name)<1:
            continue

        
        # get person info
        name = mparser.name[0:-8]
        name = name.strip()
        info = mparser.info
        if len(info)>0:
            info = info.split(' ')
            assoc = info[0]
        else:
            assoc = "undef"

        # debug 
        print name + ", ",
        print assoc
        print str(mparser.chart_val) + "\n"

        
        if i==0:
            # write attributes to file
            f.write('name\t')
            f.write('assoc\t')
            for j in range(len(mparser.chart_attr)):
                f.write(mparser.chart_attr[j] + '\t')
            f.write('\n')
            # write data-type to file
            f.write('d\t')
            f.write('d\t')
            for j in range(len(mparser.chart_attr)):
                f.write('c\t')
            f.write('\n')
            # write class to file
            f.write('\tclass\n')


        # write data to file
        f.write(name + '\t')
        f.write(assoc + '\t')
        for j in range(len(mparser.chart_val)):
            f.write(str(mparser.chart_val[j]) + '\t')
        f.write('\n')
        
        i = i+1

        
    f.close()        
    


