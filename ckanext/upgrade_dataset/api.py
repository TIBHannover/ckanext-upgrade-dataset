from pprint import pprint
from mwclient import Site
from datetime import datetime

class API():
    
    username = None
    password = None
    site = None
    host = "service.tib.eu/sfb1368"
    path = "/wiki/"
    scheme = "https"
    query = ""


    def __init__(self, username, password, query):
        self.username = username
        self.password = password
        self.query = query
    

    def pipeline(self):
        results = []
        try:
            self.login(self.host, self.path, self.scheme)
            raw_results = self.site.ask(self.query)
            for answer in raw_results:
                results.append( self.unpack_ask_response(answer))
        except:
            return None

        return results


    def login(self, host: str, path: str, scheme: str):
        site_ = Site(host=host, path=path, scheme=scheme)
        if self.username and self.password:
            site_.login(username=self.username, password=self.password)        
        self.site = site_
        return True
    

    def unpack_ask_response(self, response):
        results = {}
        printouts = response['printouts']
        page = response['fulltext']
        results['page'] = page
        for prop in printouts:
            p_item = response['printouts'][prop]
            for prop_val in p_item:
                if isinstance(prop_val, dict) is False:
                    results[prop] = prop_val
                else:                   
                    props = list(prop_val.keys())
                    if 'fulltext' in props:
                        val = prop_val.get('fulltext')
                    elif 'timestamp' in props:
                        val = datetime.fromtimestamp(
                            int(prop_val.get('timestamp')))
                    else:
                        val = list(prop_val.values())[0]
                    results[prop] = val
        return results
