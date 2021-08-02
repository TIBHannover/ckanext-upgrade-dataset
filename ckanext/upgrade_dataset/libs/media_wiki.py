# encoding: utf-8

from sqlalchemy.sql.expression import false, null, true
from ckanext.upgrade_dataset.model import ResourceMediawikiLink
from datetime import datetime as _time
from ckanext.upgrade_dataset.libs.media_wiki_api import API
from urllib import parse
import ckan.plugins.toolkit as toolkit


class Helper():

    def add_machine_links(request, resources_len):
        try:
            for i in range(1, resources_len + 1):
                resource = request.form.get('resource_' + str(i))            
                link = request.form.get('machine_link' + str(i))
                if link == '0': # not specified
                    continue            
                machine_name = request.form.get('machine_name_' + str(i))
                create_at = _time.now()
                updated_at = create_at
                resource_object = ResourceMediawikiLink(resource, link, machine_name, create_at, updated_at)
                resource_object.save()
        except:
            return false

        return true
    

    def update_resource_machine(request, resources_len):
        try:
            for i in range(1, resources_len + 1):
                resource = request.form.get('resource_' + str(i))            
                link = request.form.get('machine_link' + str(i))            
                machine_name = request.form.get('machine_name_' + str(i))                
                if link == '0':
                    machine_name = None
                updated_at = _time.now()
                resource_object = ResourceMediawikiLink(resource_id=resource).get_by_resource(id=resource)                
                if resource_object == false:
                    # resource link does not exist --> add a new one
                    create_at = _time.now()
                    updated_at = create_at
                    resource_object = ResourceMediawikiLink(resource, link, machine_name, create_at, updated_at)
                    resource_object.save()
                    continue

                resource_object.url = link
                resource_object.link_name = machine_name
                resource_object.updated_at = updated_at
                resource_object.commit()
        except:
            return false

        return true

    
    def get_machine_link(resource_id):
        res_object = ResourceMediawikiLink(resource_id=resource_id)
        result = res_object.get_by_resource(id=resource_id)
        if result != false:
            return result
        return false
    

    def get_machines_list():
        machines_list = []
        username = None
        password = None
        credentials_path, smw_base_url, api_host = Helper.get_api_config()
        query = "[[Category:Equipment]]|?hasManufacturer|?hasModel|?depiction"  # all Equipments (machines and tools)
        try:
            credentials = open(credentials_path, 'r').read()
            credentials = credentials.split('\n')
            username = credentials[0].split('=')[1]
            password = credentials[1].split('=')[1]
           
        except:
            return []
        
        api_call = API(username=username, password=password, query=query, host=api_host)
        results, machine_imageUrl = api_call.pipeline()
        if results and len(results) > 0:
            temp = {}
            temp['value'] = '0'
            temp['text'] = 'Not selected'
            machines_list.append(temp)
            for machine in results:
                temp = {}
                temp['value'] = smw_base_url + parse.quote(machine['page'])
                temp['text'] = machine['page']
                temp['image'] = machine_imageUrl.get( machine['page'])
                machines_list.append(temp)
                        
            return [machines_list, machine_imageUrl]
        
        return []
    

    def get_api_config():
        credential_path = '/etc/ckan/default/credentials/smw1368.txt'
        smw_base_url = "https://service.tib.eu/sfb1368/wiki/"
        api_host = "service.tib.eu/sfb1368"
        ckan_root_path = toolkit.config.get('ckan.root_path')
        if 'sfb1153/ckan' in ckan_root_path:
            credential_path = '/etc/ckan/default/credentials/smw1153.txt'
            smw_base_url = "https://service.tib.eu/sfb1153/wiki/"
            api_host = "service.tib.eu/sfb1153"

        return [credential_path, smw_base_url, api_host]
    



