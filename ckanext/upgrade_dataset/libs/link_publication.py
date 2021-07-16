# encoding: utf-8

from ckanext.upgrade_dataset import model
from flask.globals import request
import ckan.plugins.toolkit as toolkit
import urllib.request, json 
import ckan.lib.helpers as h


Base_crossref_url = "https://api.crossref.org/works/"

class Helper():

    def parse_doi_id(url):
        if 'doi.org/' not in url:
            return None

        temp = url.split('doi.org/')
        doi_id = temp[len(temp) - 1]
        return doi_id
    

    def call_api(api_url):
        response = None
        try:
            with urllib.request.urlopen(api_url) as url:            
                if url.code == 200:
                    response = json.loads(url.read().decode())
        
            return response
        
        except:
            return None


    def process_doi_link(doi_link):
        try:            
            doi_id = Helper.parse_doi_id(doi_link)
            dest_url = Base_crossref_url + doi_id
            response = Helper.call_api(dest_url)
            if response:
                processed_result = {}
                processed_result['type'] = response.get('message').get('type')
                processed_result['title'] = response.get('message').get('title')[0]
                processed_result['year'] = response.get('message').get('created').get('date-parts')[0][0]
                processed_result['authors'] = Helper.extract_authors(response.get('message').get('author'))

                return processed_result
            
            else:
                return None
        
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
    
    def create_table_row(meta_data, object_id):
        row = '<tr>'
        row = row +  '<td>' +  meta_data['type'] + '</td>'
        row = row +  '<td>' +  meta_data['title'] + '</td>'
        row = row +  '<td>' +  str(meta_data['year']) + '</td>'
        row = row +  '<td>' +  meta_data['authors'] + '</td>'
        row = row +  '<td><a href="' +  meta_data['link'] + '" target="_blank">Link</a></td>'
        row = row +  '<td>' +  Helper.create_delete_modal(object_id) + '</td>'  
        row = row +  '</tr>'
        return row
    

    def check_doi_validity(doi_url):        
        doi = Helper.parse_doi_id(doi_url)
        if not doi:
            return 'url not vaid'
        dest_url = Base_crossref_url + doi
        response = Helper.call_api(dest_url)
        if response:
            return True

        return None


    def create_delete_modal(object_id):
        delete_url = h.url_for('link_publication.delete_doi', doi_id=str(object_id) ,  _external=True)
        modal = '<a href="#" type="button" data-toggle="modal" data-target="#deleteModal' + str(object_id) +  '"><i class="fa fa-trash-o"></i></a>'
        modal += '<div id="deleteModal' + str(object_id)  + '" class="modal fade" role="dialog">'
        modal += '<div class="modal-dialog">'
        modal += '<div class="modal-content">'
        modal += '<div class="modal-header">'
        modal += '<button type="button" class="close" data-dismiss="modal">&times;</button>'
        modal += '</div>'
        modal += '<div class="modal-body">'
        modal += '<p><h3>Are you sure about deleting this material?</h3></p>'
        modal += '</div>'
        modal += '<div class="modal-footer">'
        modal += '<a href="' + delete_url + '" type="button" class="btn btn-danger">Delete</a>'
        modal += '<button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>'
        modal += '</div>'
        modal += '</div>'
        modal += '</div>'
        modal += '</div>'
                
        return modal