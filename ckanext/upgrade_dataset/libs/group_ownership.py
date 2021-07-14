# encoding: utf-8

from sqlalchemy.sql.expression import false, null, true
import ckan.plugins.toolkit as toolkit


class Helper():

    def get_groups_list():
        groups = toolkit.get_action('group_list')({}, {'all_fields':true})
        group_list = []
        temp = {}
        temp['value'] = '0'
        temp['text'] = 'No group'
        group_list.append(temp)
        for group in groups:
            temp = {}
            temp['value'] = group['id']
            temp['text'] = group['name']
            group_list.append(temp)
        
        return group_list
    
    def get_organizations_list():
        orgs = toolkit.get_action('organization_list')({}, {'all_fields':true})
        org_list = []
        temp = {}
        temp['value'] = '0'
        temp['text'] = 'No organization'
        org_list.append(temp)
        for org in orgs:
            temp = {}
            temp['value'] = org['id']
            temp['text'] = org['name']
            org_list.append(temp)
        
        return org_list



