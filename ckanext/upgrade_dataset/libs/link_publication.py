# encoding: utf-8

import ckan.plugins.toolkit as toolkit
import urllib.request, json 

Base_crossref_url = "https://api.crossref.org/works/"

class Helper():

    def process_doi_link(doi_link):
        try:
            temp = doi_link.split('doi.org/')
            doi_id = temp[len(temp) - 1]
            dest_url = Base_crossref_url + doi_id
            with urllib.request.urlopen(dest_url) as url:
                response = json.loads(url.read().decode())
            
            processed_result = {}
            processed_result['type'] = response.get('message').get('type')
            processed_result['title'] = response.get('message').get('title')[0]
            processed_result['year'] = response.get('message').get('created').get('date-parts')[0][0]
            processed_result['authors'] = Helper.extract_authors(response.get('message').get('author'))

            return processed_result
        
        except:
            return None

    

    def extract_authors(authors_list):
        result = ""
        for au in authors_list:
            if au['sequence'] == 'first' and result == "":
                result = au['given'] 
            elif au['sequence'] == 'first' and result != "":
                result = au['given'] + ', ' + result
            else:
                result = result + ', ' + au['given']
        
        return result  
