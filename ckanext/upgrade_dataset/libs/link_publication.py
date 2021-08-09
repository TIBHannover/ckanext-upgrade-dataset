# encoding: utf-8

from sqlalchemy.sql.expression import false, null
import ckan.plugins.toolkit as toolkit
import urllib.request
import ckan.lib.helpers as h
import bibtexparser
from ckanext.upgrade_dataset.model.package_publication_link import PackagePublicationLink
from datetime import datetime


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
    

    '''
        fill null citations for a dataset
    '''
    def fill_null_citation(package):
        try:
            res_object = PackagePublicationLink(package_name=package)
            result = res_object.get_by_package(name=package)
            if result == false:
                return False

            for source in result:                        
                if not source.citation or source.citation == null:
                    source.citation = Helper.process_doi_link(source.doi).get('cite')
                    source.commit()
        except:
            return False

        return True



    def check_doi_validity(doi_url):        
        doi = Helper.parse_doi_id(doi_url)
        if not doi:
            return 'url not vaid'
        dest_url = Base_doi_api_url + doi
        response = Helper.call_api(dest_url)
        if response:
            return True

        return None

    def process_publication_manual_metadata(request):
        reference = {}
        reference['ENTRYTYPE'] = request.form.get('type')
        reference['title'] = request.form.get('title')
        reference['author'] = request.form.get('author')
        reference['year'] = request.form.get('year')
        reference['publisher'] = request.form.get('publisher')

        if reference['ENTRYTYPE'] == 'article':
            reference['journal'] = request.form.get('journal')
            reference['volume'] = request.form.get('volume')
            reference['pages'] = request.form.get('page')
            reference['month'] = request.form.get('month')

        elif reference['ENTRYTYPE'] in ['conference', 'inproceedings', 'proceedings']:
            reference['booktitle'] = request.form.get('booktitle')
            reference['pages'] = request.form.get('pages')
            reference['address'] = request.form.get('address')
            reference['series'] = request.form.get('series')
        
        elif reference['ENTRYTYPE'] == 'techreport':
            reference['number'] = request.form.get('number')
            reference['institutaion'] = request.form.get('institutaion')
            reference['address'] = request.form.get('address')
            reference['month'] = request.form.get('month')
        
        elif reference['ENTRYTYPE'] == 'inbook':
            reference['pages'] = request.form.get('pages')                
            reference['address'] = request.form.get('address')

        elif reference['ENTRYTYPE'] == 'book':                           
            reference['address'] = request.form.get('address')
        
        elif reference['ENTRYTYPE'] == 'incollection':
            reference['booktitle'] = request.form.get('booktitle')
            reference['pages'] = request.form.get('pages')
            reference['address'] = request.form.get('address')
            reference['editor'] = request.form.get('editor')
        
        elif reference['ENTRYTYPE'] in ['masterthesis', 'phdthesis']:
            reference['school'] = request.form.get('institutaion')
            reference['address'] = request.form.get('address')
            reference['month'] = request.form.get('month')
        
        else:
            reference['ENTRYTYPE'] = 'misc'
            reference['doi'] = ''

        return reference

    

    def get_publication_types_dropdown_content():
        publication_types = []
        Types = ['',
            'article', 
            'conference', 
            'inproceedings', 
            'proceedings', 
            'inbook', 
            'incollection', 
            'book', 
            'masterthesis', 
            'phdthesis',
            'techreport',
            'Other'
            ]        
        for t in Types:
            temp = {}
            temp['value'] = t
            temp['text'] = t
            publication_types.append(temp)

        return publication_types

    
    def get_years_list():
        years = []        
        current_year = datetime.now().year
        for i in list(reversed(range(1900, current_year + 1))):
            temp = {}
            temp['value'] = i
            temp['text'] = i
            years.append(temp)
        return years

    
    def get_month_list():
        months = []
        texts = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        values = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        for i in range(0, 12):
            temp = {}
            temp['value'] = values[i]
            temp['text'] = texts[i]
            months.append(temp)

        return months



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
    


    def create_table_row(meta_data, object_id):
        row = '<tr>'
        row = row +  '<td>' +  meta_data['cite'] + '</td>'        
        row = row +  '<td><a href="' +  meta_data['link'] + '" target="_blank">Link</a></td>'
        row = row +  '<td>' +  Helper.create_delete_modal(object_id) + '</td>'  
        row = row +  '</tr>'
        return row
    


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