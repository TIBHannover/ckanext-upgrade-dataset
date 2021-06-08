# encoding: utf-8

from sqlalchemy.sql.expression import false, null, true
from ckanext.upgrade_dataset.model import ResourceMediawikiLink
from datetime import datetime as _time


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
        base_link = "https://service.tib.eu/sfb1368/wiki/"
        machines_dict = [
            {'value': '0', 'text':'Not selected'},
            {'value': base_link + 'Test1', 'text':'Machine1'},
            {'value': base_link + 'Test2', 'text':'Machine2'},
            {'value': base_link + 'Test3', 'text':'Machine3'}
        ]

        return machines_dict



