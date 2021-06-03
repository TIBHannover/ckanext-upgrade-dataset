# encoding: utf-8

import ckan.plugins.toolkit as toolkit
from flask import render_template, request, redirect
import ckan.lib.helpers as h


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
        package_name = request.form.get('package')
        is_manually = request.form.get('notFind')
        link = request.form.get('machine_link')
        action = request.form.get('save_btn')
        if is_manually != None :
            link = request.form.get('machine_link_manually')
        
        if action == 'go-dataset-veiw':
            return redirect(h.url_for('dataset.read', id=str(package_name) ,  _external=True)) 
        
        if action == 'finish_machine':
            ## add to the table
            return redirect(h.url_for('dataset.read', id=str(package_name) ,  _external=True))

        return toolkit.abort(403, "bad request")
    

    def edit_machines_view(id):
        package = toolkit.get_action('package_show')({}, {'name_or_id': id})        
        return render_template('edit_machines.html', pkg_dict=package)
