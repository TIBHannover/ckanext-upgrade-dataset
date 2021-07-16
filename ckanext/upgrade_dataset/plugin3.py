import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint
from ckanext.upgrade_dataset.controllers.link_publication import LinkPublicationController


class LinkPublicationPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'themes/link_publication')
        toolkit.add_public_directory(config_, 'statics/link_publication')       
        toolkit.add_resource('statics/link_publication', 'ckanext-upgrade-dataset-link-publication')
    

    def get_blueprint(self):

        blueprint = Blueprint(self.name, self.__module__)        
       
        blueprint.add_url_rule(
            u'/upgrade_dataset/save_doi',
            u'save_doi',
            LinkPublicationController.save_doi,
            methods=['POST']
            )
        
        blueprint.add_url_rule(
            u'/upgrade_dataset/get_publication/<name>',
            u'get_publication',
            LinkPublicationController.get_publication,
            methods=['GET']
        )

        blueprint.add_url_rule(
            u'/upgrade_dataset/doi_is_valid',
            u'doi_is_valid',
            LinkPublicationController.doi_is_valid,
            methods=['POST']
        )

        blueprint.add_url_rule(
            u'/upgrade_dataset/delete_doi/<doi_id>',
            u'delete_doi',
            LinkPublicationController.delete_doi,
            methods=['GET']
        )

        return blueprint