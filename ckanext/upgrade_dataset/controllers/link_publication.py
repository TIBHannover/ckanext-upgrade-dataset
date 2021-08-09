# encoding: utf-8

from flask import redirect, request, render_template
from sqlalchemy.sql.expression import false, null
import ckan.lib.helpers as h
import ckan.plugins.toolkit as toolkit
from ckanext.upgrade_dataset.model import PackagePublicationLink
from datetime import datetime as _time
from ckanext.upgrade_dataset.libs.link_publication import Helper
import json



class LinkPublicationController():

    def save_doi():
        package_id = request.form.get('package_id')       
        doi = request.form.get('doi')       
        Helper.check_access_edit_package(package_id)

        if package_id and doi and Helper.check_doi_validity(doi) == True:
            package = toolkit.get_action('package_show')({}, {'name_or_id': package_id})
            try:
                citation = Helper.process_doi_link(doi)
                if citation:
                    record = PackagePublicationLink(package_name=package['name'], doi=doi, create_at = _time.now(), citation=citation.get('cite'))
                    record.save()
                return  redirect(h.url_for('dataset.read', id=str(package_id) ,  _external=True))   
            except:
                return toolkit.abort(403, "bad request")
            
        else:
            return toolkit.abort(403, "bad request")
    


    def get_publication(name):        
        Helper.fill_null_citation(name)
        res_object = PackagePublicationLink(package_name=name)
        result = res_object.get_by_package(name=name)
        return_rows = ""
        if result == false:
            return '0'
        for source in result:
            if not source.citation:
                continue
            meta_data = {}
            meta_data['cite'] = source.citation
            if meta_data:
                meta_data['link'] = source.doi
                return_rows += Helper.create_table_row(meta_data, source.id)
        
        if return_rows != "":
            return return_rows
        
        return '0'
    

    def doi_is_valid():
        doi_url = request.form.get('doi_url')
        response = Helper.check_doi_validity(doi_url)
        if not response:
            return 'There is no information about this doi url'
        
        elif response == 'url not vaid':
            return 'Please enter a valid doi url. Ex: https://www.doi.org/DOI_ID'
        
        return '1'
    

    def delete_doi(doi_id):
        res_object = PackagePublicationLink()
        doi_obj = res_object.get_by_id(id=doi_id)
        package_name = doi_obj.package_name
        package = toolkit.get_action('package_show')({}, {'name_or_id': package_name})
        Helper.check_access_edit_package(package['id'])
        try:            
            doi_obj.delete()
            doi_obj.commit()
            return  redirect(h.url_for('dataset.read', id=str(package_name) ,  _external=True)) 

        except:
            return toolkit.abort(403, "bad request")
    

    def add_publication_manually(package_name):
        package = toolkit.get_action('package_show')({}, {'name_or_id': package_name})
        publication_types = Helper.get_publication_types_dropdown_content()
        years = Helper.get_years_list()
        months = Helper.get_month_list()

        return render_template('add_manually.html', 
            pkg_dict=package, 
            publication_types=publication_types,
            years=years,
            months=months
            )
    

    def save_publication_manually():
        package_name = request.form.get('package')
        if package_name:
            package = toolkit.get_action('package_show')({}, {'name_or_id': package_name})
            Helper.check_access_edit_package(package['id'])
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
            

            citation = Helper.create_citation(reference)
            return citation
        


        else:
            toolkit.abort(403, "package not specefied")

        return '0'
