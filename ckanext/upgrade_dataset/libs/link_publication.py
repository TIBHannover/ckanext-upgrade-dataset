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
            toolkit.abort(403, 'You are not authorized to access this function')


    def parse_doi_id(url):
        if 'doi.org/' not in url:
            return None

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
        # material_type = {
        #     'books' : 'Book in print',
        #     'booklet' : 'Book in print',
        #     'inbook' : 'Chapter in book',
        #     'incollection': 'Chapter in book',
        #     'article' : 'Journal article', 
        #     'conference': 'Conference paper',
        #     'inproceedings': 'Conference paper',
        #     'proceedings': 'Conference paper',
        #     'techreport': 'Technical report',
        #     'masterthesis': 'Thesis',
        #     'phdthesis': 'Thesis',
        #     'misc': 'dataset',
        # }

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



        return citation_text
    

    def none_type_checker(arg):
        if not arg:
            return ''
        return arg


    def create_table_row(meta_data, object_id):
        row = '<tr>'
        row = row +  '<td>' +  meta_data['cite'] + '</td>'        
        row = row +  '<td><a href="' +  meta_data['link'] + '" target="_blank">Link</a></td>'
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