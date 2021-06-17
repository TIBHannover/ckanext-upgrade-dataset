import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint
from ckanext.upgrade_dataset.controllers import GroupOwnershipController



class GroupOwnershipPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'themes/group_ownership')
        toolkit.add_public_directory(config_, 'statics/group_ownership')
        toolkit.add_resource('statics/group_ownership', 'ckanext-upgrade-dataset-group-ownership')

    def get_blueprint(self):

        blueprint = Blueprint(self.name, self.__module__)        
        blueprint.add_url_rule(
            u'/upgrade_dataset/add_ownership_view/<id>',
            u'add_ownership_view',
            GroupOwnershipController.add_ownership_view,
            methods=['GET']
            )
        
        blueprint.add_url_rule(
            u'/upgrade_dataset/save_ownership',
            u'save_ownership',
            GroupOwnershipController.save_ownership,
            methods=['POST']
            )

        return blueprint