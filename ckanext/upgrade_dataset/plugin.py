import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint
from ckanext.upgrade_dataset.controllers import MediaWikiController


class MediaWikiLinkPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic','upgrade_dataset')
        toolkit.add_resource('public/statics', 'ckanext-upgrade-dataset')


    #plugin Blueprint

    def get_blueprint(self):

        blueprint = Blueprint(self.name, self.__module__)
        blueprint.template_folder = u'templates'
        blueprint.add_url_rule(
            u'/upgrade_dataset/machines_view/<id>',
            u'machines_view',
            MediaWikiController.machines_view,
            methods=['GET']
            )

        return blueprint