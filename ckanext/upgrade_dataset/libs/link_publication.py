# encoding: utf-8

from werkzeug.datastructures import Headers
from ckanext.upgrade_dataset import model
from flask.globals import request
import ckan.plugins.toolkit as toolkit
import urllib.request, json 
import ckan.lib.helpers as h
import bibtexparser


Base_doi_api_url = "http://dx.doi.org/"

class Helper():

    def check_access_edit_package(package_id):
        context = {'user': toolkit.g.user, 'auth_user_obj': toolkit.g.userobj}
        data_dict = {'id':package_id}
        try:
            toolkit.check_access('package_update', context, data_dict)
            return True

        except toolkit.NotAuthorized:
            return False
            # toolkit.abort(403, 'You are not authorized to access this function')


    def parse_doi_id(url):
        if 'doi.org/' not in url:  # url has to be a doi ID
            return url  

        temp = url.split('doi.org/')
        doi_id = temp[len(temp) - 1]
        return doi_id
    

    def call_api(api_url):
        response = None
        request_header = {'Accept': 'application/x-bibtex'}                
        try:
            req_obj = urllib.request.Request(api_url, headers=request_header)
            with urllib.request.urlopen(req_obj) as url:            
                if url.code == 200:                    
                    response = bibtexparser.load(url).entries[0]
        
            return response
        
        except:
            return None


    def process_doi_link(doi_link):
               
        try:            
            doi_id = Helper.parse_doi_id(doi_link)
            dest_url = Base_doi_api_url + doi_id
            response = Helper.call_api(dest_url)
            if response:                        
                processed_result = {}
                processed_result['cite'] = Helper.create_citation(response)
                return processed_result
            
            else:
                return None
        
        except:
            return None
    
    
    def create_citation(response):
        citation_text = ""

        if response['ENTRYTYPE'] in ['article']:
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('title'):
                citation_text += ('"<i>' + response.get('title') + '</i>," ')
            if response.get('publisher'):
                citation_text += (response.get('publisher') + '. ')
            if response.get('journal'):
                citation_text += (response.get('journal') + '., ')
            if response.get('volume'):
                citation_text += ('vol. ' + response.get('volume') + ', ')
            if response.get('pages'):
                citation_text += ('pp. ' + response.get('pages') + ', ')
            if response.get('month'):
                citation_text += (response.get('month') + ' ')
            if response.get('year'):
                citation_text += (response.get('year') + '.')
  
        elif response['ENTRYTYPE'] in ['misc']: 
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('title'):
                citation_text += ('"<i>' + response.get('title') + '</i>." ')
            if response.get('publisher'):
                citation_text += (response.get('publisher') + ', ')
            if response.get('year'):
                citation_text += (response.get('year') + ', ')
            if response.get('doi'):
                citation_text += ( 'doi: ' + response.get('doi') + '.')
        
        elif response['ENTRYTYPE'] in ['conference', 'inproceedings', 'proceedings']:
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('title'):
                citation_text += ('"<i>' + response.get('title') + '</i>," ')
            if response.get('booktitle'):
                citation_text += (response.get('booktitle') + ', ')
            if response.get('series'):
                citation_text += (response.get('series') + ', ')
            if response.get('address'):
                citation_text += (response.get('address') + ', ')
            if response.get('pages'):
                citation_text += ('pp. ' + response.get('pages') + ', ')
            if response.get('publisher'):
                citation_text += (response.get('publisher') + ', ')
            if response.get('year'):
                citation_text += (response.get('year') + '.')

        elif response['ENTRYTYPE'] in ['inbook']:
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('title'):
                citation_text += ('"<i>' + response.get('title') + '</i>," ')
            if response.get('pages'):
                citation_text += ('pp. ' + response.get('pages') + ', ')
            if response.get('address'):
                citation_text += (response.get('address') + ', ')
            if response.get('publisher'):
                citation_text += (response.get('publisher') + ', ')
            if response.get('year'):
                citation_text += (response.get('year') + '.')
        
        elif response['ENTRYTYPE'] in ['incollection']:
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('title'):
                citation_text += ('"<i>' + response.get('title') + '</i>," ')
            if response.get('editor'):
                citation_text += ('In ' + response.get('editor') + ', editors, ')
            if response.get('booktitle'):
                citation_text += (response.get('booktitle') + ', ')
            if response.get('pages'):
                citation_text += ('pp. ' + response.get('pages') + ', ')
            if response.get('publisher'):
                citation_text += (response.get('publisher') + ', ')            
            if response.get('address'):
                citation_text += (response.get('address') + ', ')            
            if response.get('year'):
                citation_text += (response.get('year') + '.')
        
        elif response['ENTRYTYPE'] in ['book']:
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('title'):
                citation_text += ('"<i>' + response.get('title') + '</i>," ')
            if response.get('address'):
                citation_text += (response.get('address') + ', ')
            if response.get('publisher'):
                citation_text += (response.get('publisher') + ', ')
            if response.get('year'):
                citation_text += (response.get('year') + '.')
        
        elif response['ENTRYTYPE'] in ['masterthesis']:
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('title'):
                citation_text += ('"<i>' + response.get('title') + '</i>," Master Thesis, ')
            if response.get('school'):
                citation_text += (response.get('school') + ', ')
            if response.get('address'):
                citation_text += (response.get('address') + ', ')
            if response.get('month'):
                citation_text += (response.get('month') + '. ')
            if response.get('year'):
                citation_text += (response.get('year') + '.')
        
        elif response['ENTRYTYPE'] in ['phdthesis']:
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('title'):
                citation_text += ('"<i>' + response.get('title') + '</i>," PhD Thesis, ')
            if response.get('school'):
                citation_text += (response.get('school') + ', ')
            if response.get('address'):
                citation_text += (response.get('address') + ', ')
            if response.get('month'):
                citation_text += (response.get('month') + '. ')
            if response.get('year'):
                citation_text += (response.get('year') + '.')
        
        elif response['ENTRYTYPE'] in ['techreport']:
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('title'):
                citation_text += ('"<i>' + response.get('title') + '</i>," Tech.Rep. ')
            if response.get('number'):
                citation_text += (response.get('number') + ', ')
            if response.get('institution'):
                citation_text += (response.get('institution') + ', ')
            if response.get('address'):
                citation_text += (response.get('address') + ', ')
            if response.get('month'):
                citation_text += (response.get('month') + '. ')
            if response.get('year'):
                citation_text += (response.get('year') + '.')

        citation_text = citation_text.replace('{', '')
        citation_text = citation_text.replace('}', '')
        return citation_text
    


    def create_table_row(meta_data, object_id, is_auth_to_delete):
        row = '<tr>'
        row = row +  '<td>' +  meta_data['cite'] + '</td>'        
        row = row +  '<td><a href="' +  meta_data['link'] + '" target="_blank">Link</a></td>'
        if is_auth_to_delete:
            row = row +  '<td>' +  Helper.create_delete_modal(object_id) + '</td>'  
        row = row +  '</tr>'
        return row
    

    def check_doi_validity(doi_url):        
        doi = Helper.parse_doi_id(doi_url)
        if not doi:
            return 'url not vaid'
        dest_url = Base_doi_api_url + doi
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