from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class meterreader(HTMLParser):
    def reset(self):                              
        HTMLParser.reset(self)

        self.iscontent = 0
        self.isdone = 0
        
        self.isname = 0
        self.name = []
        self.isinfo = 0
        self.info = []
        self.isbio = 0
        self.bio = []
        
        self.ischart = 0
        self.ischart_attr = 0
        self.chart_attr = []
        self.ischart_val = 0
        self.chart_val = []

    def handle_starttag(self, tag, attrs):
        # handle start of content pane
        if tag=="div":
            for attr in attrs:
                if "class" in attr and "pfcontentleft" in attr:
                    self.iscontent = 1
                    return
        if tag=="div":
                    for attr in attrs:
                        if "class" in attr and "pfcontentmid" in attr:
                            self.iscontent = 0
                            self.isdone = 1
                            return
                        
        if tag=="div" and self.iscontent==1:
            for attr in attrs:
                if "class" in attr and "pfhead" in attr:
                    self.isname = 1
                    return

        # handle bio tags          
        if tag=="h6":
            self.isinfo = 1
            return
        if tag=="p" and self.isinfo==2:
            self.isbio = 1
            return

        # handle meter tags    
        if tag=="ul":
            for attr in attrs:
                if "class" in attr and "chartlist" in attr:
                    self.ischart = 1
                    return
        if tag=="a" and self.ischart==1:
            self.ischart_attr = 1
            return
        if tag=="span" and self.ischart==1:
            for attr in attrs:
                if "class" in attr and ("count" in attr or "count nocount" in attr):
                    self.ischart_val = 1
                    return

    def handle_endtag(self, tag):
        if tag=="div" and self.iscontent==1 and self.isdone==1:
            self.iscontent = 0
            return
        
        # handle bio tags
        if tag=="div" and self.isname==1:
            self.isname = 0
            return
        if tag=="h6":
            self.isinfo = 2
            return
        if tag=="p" and self.isinfo>0:
            self.isbio = 0
            self.isinfo = 0
            self.isdone = 1
            return
        
        # handle meter tags
        if tag=="ul":
            self.ischart = 0
            self.ischart_attr = 0
            self.ischart_val = 0
            return
        if tag=="a" and self.ischart==1:
            self.ischart_attr = 0
            return
        if tag=="span" and self.ischart==1:
            self.ischart_val = 0
            return
        
    def handle_data(self, data):
        # handle bio data
        if self.isname==1:
            self.name = data
            return
        if self.isinfo==1:
            self.info = data
            return
        if self.isbio==1:
            self.bio = data
            return
        
        # handle meter data
        if self.ischart == 1:
            if self.ischart_attr == 1:
                self.chart_attr.append(data)
                return
            if self.ischart_val == 1:
                self.chart_val.append(data)
                return

            
        
