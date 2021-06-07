# encoding: utf-8

import datetime
from sqlalchemy import types, Column, Table, ForeignKey, orm
from ckan.model import meta, Resource, DomainObject


__all__ = [u"ResourceMediawikiLink", u"resource_mediawiki_link_table"]

resource_mediawiki_link_table = Table(
    u"resource_mediawiki_link",
    meta.metadata,
    Column(u"id", types.Integer, primary_key=True, nullable=False, default=types.make_uuid),
    Column(u"resource_id", types.UnicodeText, ForeignKey(u"resource.id"), nullable=False),
    Column(u"url", types.UnicodeText, nullable=False),
    Column(u"link_name", types.UnicodeText),
    Column(u"create_at", types.DateTime, default=datetime.datetime.utcnow, nullable=False),
    Column(u"updated_at", types.DateTime, default=datetime.datetime.utcnow, nullable=False),
)

class ResourceMediawikiLink(DomainObject):
    def __init__(self, resource_id=None):
        self.resource_id = resource_id
    
    @classmethod
    def get(cls, id):
        if not id:
            return None
        return meta.Session.query(cls).get(id)
    
    def get_resource(self):
        return self.resource



meta.mapper(
    ResourceMediawikiLink,
    resource_mediawiki_link_table,
    properties={
        u"resource": orm.relation(
            Resource, backref=orm.backref(u"resource_mediawiki_links", cascade=u"all, delete, delete-orphan")
        )
    },
)







