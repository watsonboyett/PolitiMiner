
from sgmllib import SGMLParser

class URLLister(SGMLParser):
    def reset(self):                              
        SGMLParser.reset(self)
        self.urls = []
        self.cls = []

    def start_a(self, attrs):                     
        href = [v for k, v in attrs if k=='href']  
        if href:
            self.urls.extend(href)
                    
        cls = [v for k, v in attrs if k=='class']  
        if cls:
            self.cls.extend(cls)
