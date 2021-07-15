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
        context = {'user': toolkit.g.user, 'auth_user_obj': toolkit.g.userobj}
        data_dict = {'id':package_id}
        try:
            toolkit.check_access('package_update', context, data_dict)
        except toolkit.NotAuthorized:
            toolkit.abort(403, 'You are not authorized to access this function')

        if package_id and doi:
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
                return_rows += Helper.create_table_row(meta_data)
        
        if return_rows != "":
            return return_rows
        
        return '0'
