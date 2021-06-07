# encoding: utf-8

from sqlalchemy.sql.expression import false, true
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