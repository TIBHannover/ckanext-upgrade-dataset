import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint



class LinkPublicationPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'themes/link_publication')
        toolkit.add_public_directory(config_, 'statics/link_publication')       
        toolkit.add_resource('statics/link_publication', 'ckanext-upgrade-dataset-link-publication')