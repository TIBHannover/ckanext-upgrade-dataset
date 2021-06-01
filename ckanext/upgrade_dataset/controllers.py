# encoding: utf-8

import ckan.plugins.toolkit as toolkit
from flask import render_template

class MediaWikiController():

    def machines_view(id):
        package = toolkit.get_action('package_show')({}, {'name_or_id': id})
        stages = ['complete', 'complete', 'active']
        return render_template('add_machines.html', pkg_dict=package, custom_stage=stages)