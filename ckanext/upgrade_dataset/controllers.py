# encoding: utf-8

import ckan.plugins.toolkit as toolkit
from flask import render_template

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
        return "OK"