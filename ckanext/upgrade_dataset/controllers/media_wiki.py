# encoding: utf-8

import ckan.plugins.toolkit as toolkit
from flask import render_template, request, redirect
from ckanext.upgrade_dataset.libs.media_wiki import Helper
from sqlalchemy.sql.expression import false, true
import json
import ckan.lib.helpers as h



class MediaWikiController():

    def machines_view(id):
        package = toolkit.get_action('package_show')({}, {'name_or_id': id})
        stages = ['complete', 'complete','complete', 'active']
        machines, machine_imageUrl = Helper.get_machines_list()
        return render_template('add_machines.html', 
            pkg_dict=package, 
            custom_stage=stages, 
            machines_list=machines,
            machine_imageUrl=machine_imageUrl
            )
    
    def save_machines():
        if not toolkit.g.user: 
            return toolkit.abort(403, "You need to authenticate before accessing this function" )

        package_name = request.form.get('package')
        resources_len = 0
        if package_name == None:
            return toolkit.abort(403, "bad request")
        
        try:
            package = toolkit.get_action('package_show')({}, {'name_or_id': package_name})
            resources_len = len(package['resources'])

        except:
            return toolkit.abort(400, "Package not found") 
               
        action = request.form.get('save_btn')
        if action == 'go-dataset-veiw': # I will add it later button
            return redirect(h.url_for('dataset.read', id=str(package_name) ,  _external=True)) 
        
        if action == 'finish_machine':
            result = Helper.add_machine_links(request, resources_len)
            if result != false:
                return redirect(h.url_for('dataset.read', id=str(package_name) ,  _external=True))    

            return toolkit.abort(500, "Server issue")    

        return toolkit.abort(403, "bad request")
    

    def edit_machines_view(id):
        package = toolkit.get_action('package_show')({}, {'name_or_id': id})        
        machines, machine_imageUrl = Helper.get_machines_list()
        resource_machine_data = []
        for resource in package['resources']:
            temp = {}
            temp['name'] = resource['name']            
            temp['id'] = resource['id']
            record = Helper.get_machine_link(resource['id'])
            temp['machine'] =  record.url if record != false else '0'
            resource_machine_data.append(temp)

        return render_template('edit_machines.html', 
            pkg_dict=package, 
            machines_list=machines, 
            resource_data=resource_machine_data,
            machine_imageUrl=machine_imageUrl
            )
    

    def edit_save():
        if not toolkit.g.user: 
            return toolkit.abort(403, "You need to authenticate before accessing this function" )
        
        package_name = request.form.get('package')
        resources_len = int(request.form.get('resources_length'))
        action = request.form.get('save_btn')
        if action == 'go-dataset-veiw': # cancel button
            return redirect(h.url_for('dataset.read', id=str(package_name) ,  _external=True)) 
        
        if action == 'update_machine':
            result = Helper.update_resource_machine(request, resources_len)
            if result != false:
                return redirect(h.url_for('dataset.read', id=str(package_name) ,  _external=True))    

            return toolkit.abort(500, "Server issue")    

        return toolkit.abort(403, "bad request")
    
    

    def get_machine_link(id):
        if not toolkit.g.user: 
            return toolkit.abort(403, "You need to authenticate before accessing this function" )
        record = Helper.get_machine_link(id)
        if record == false or record.url == '0':
            return '0'
        return json.dumps([record.url, record.link_name])
    
    
    def cancel_dataset_plugin_is_enabled():
        if Helper.check_plugin_enabled('cancel_dataset_creation'):
            return True
        return False

