# encoding: utf-8

from flask import redirect, request
from sqlalchemy.sql.expression import false
import ckan.lib.helpers as h
import ckan.plugins.toolkit as toolkit
from ckanext.upgrade_dataset.model import PackagePublicationLink



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

            return  redirect(h.url_for('dataset.read', id=str(package_id) ,  _external=True))   

        else:
            return toolkit.abort(403, "bad request")
    

    def get_publication(name):        
        res_object = PackagePublicationLink(package_name=name)
        result = res_object.get_by_package(name=name)
        if result != false:
            return '0'

        return '0'