# encoding: utf-8

import ckan.plugins.toolkit as toolkit
from flask import render_template, request, redirect
import ckan.lib.helpers as h
from ckanext.upgrade_dataset.lib import Helper


class GroupOwnershipController():

    def add_ownership_view(id):
        package = toolkit.get_action('package_show')({}, {'name_or_id': id})
        group_list = Helper.get_groups_list()
        organizations = Helper.get_organizations_list()
        stages = ['complete', 'complete', 'active', 'uncomplete']
        return render_template('add_owner.html', pkg_dict=package, custom_stage=stages, group_list=group_list, org_list=organizations)
    

    def save_ownership():
        if not toolkit.g.user: 
            return toolkit.abort(403, "You need to authenticate before accessing this function" )

        package_name = request.form.get('package')        
        if package_name == None:
            return toolkit.abort(403, "bad request")
        
        try:
            package = toolkit.get_action('package_show')({}, {'name_or_id': package_name})            
        except:
            return toolkit.abort(400, "Package not found") 
               
        action = request.form.get('save_btn')
        if action == 'finish_ownership':
            org = request.form.get('owner_org')
            group = request.form.get('owner_group')
            if org != '0' and group != '0' and group and org:
                package['owner_org'] = org
                toolkit.get_action('package_update')({}, package)
                member = {
                    'id' : group,
                    'object': package['id'],
                    'object_type': 'package',
                    'capacity' : 'public'
                }
                toolkit.get_action('member_create')({}, member)

                return redirect(h.url_for('media_wiki.machines_view', id=str(package_name) ,  _external=True))    

            return toolkit.abort(403, "bad request")    

        return toolkit.abort(403, "bad request")