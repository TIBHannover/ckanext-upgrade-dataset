# encoding: utf-8

from flask import redirect, request
from sqlalchemy.sql.expression import false
import ckan.lib.helpers as h
import ckan.plugins.toolkit as toolkit
from ckanext.upgrade_dataset.model import PackagePublicationLink
from datetime import datetime as _time
from ckanext.upgrade_dataset.libs.link_publication import Helper



class LinkPublicationController():

    def save_doi():
        package_id = request.form.get('package_id')       
        doi = request.form.get('doi')       
        Helper.check_access_edit_package(package_id)

        if package_id and doi and Helper.check_doi_validity(doi) == True:
            package = toolkit.get_action('package_show')({}, {'name_or_id': package_id})
            try:
                record = PackagePublicationLink(package_name=package['name'], doi=doi, create_at = _time.now())
                record.save()
                return  redirect(h.url_for('dataset.read', id=str(package_id) ,  _external=True))   
            except:
                return toolkit.abort(403, "bad request")
            
        else:
            return toolkit.abort(403, "bad request")
    


    def get_publication(name):        
        res_object = PackagePublicationLink(package_name=name)
        result = res_object.get_by_package(name=name)
        return_rows = ""
        if result == false:
            return '0'
        for source in result:
            meta_data = Helper.process_doi_link(source.doi)
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
