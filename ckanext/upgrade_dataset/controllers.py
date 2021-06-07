# encoding: utf-8

from sqlalchemy.sql.expression import false
import ckan.plugins.toolkit as toolkit
from flask import render_template, request, redirect
import ckan.lib.helpers as h
from ckanext.upgrade_dataset.lib import Helper


class MediaWikiController():

    def machines_view(id):
        package = toolkit.get_action('package_show')({}, {'name_or_id': id})
        stages = ['complete', 'complete', 'active']
        test_link = "https://service.tib.eu/sfb1368/wiki/Test2"
        machines_dict = [
            {'value': '0', 'text':'Not selected'},
            {'value': test_link, 'text':'Machine1'},
            {'value': test_link, 'text':'Machine2'},
            {'value': test_link, 'text':'Machine3'}
        ]
        return render_template('add_machines.html', pkg_dict=package, custom_stage=stages, machines_list=machines_dict)
    
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
            if result:
                return redirect(h.url_for('dataset.read', id=str(package_name) ,  _external=True))    

            return toolkit.abort(500, "Server issue")    

        return toolkit.abort(403, "bad request")
    

    def edit_machines_view(id):
        package = toolkit.get_action('package_show')({}, {'name_or_id': id})        
        return render_template('edit_machines.html', pkg_dict=package)
    
    def get_machine_link(id):
        if not toolkit.g.user: 
            return toolkit.abort(403, "You need to authenticate before accessing this function" )
        link = Helper.get_machine_link(id)
        if link == false:
            return '0'
        return link
