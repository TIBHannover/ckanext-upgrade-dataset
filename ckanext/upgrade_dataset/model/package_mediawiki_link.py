# encoding: utf-8

import datetime
from sqlalchemy import Column, Table, ForeignKey, orm
from sqlalchemy import types as _types
from ckan.model import meta, Resource, DomainObject


__all__ = [u"ResourceMediawikiLink", u"resource_mediawiki_link_table"]

resource_mediawiki_link_table = Table(
    u"resource_mediawiki_link",
    meta.metadata,
    Column(u"id", _types.Integer, primary_key=True, nullable=False),
    Column(u"resource_id", _types.UnicodeText, ForeignKey(u"resource.id"), nullable=False),
    Column(u"url", _types.UnicodeText, nullable=False),
    Column(u"link_name", _types.UnicodeText),
    Column(u"create_at", _types.DateTime, default=datetime.datetime.utcnow, nullable=False),
    Column(u"updated_at", _types.DateTime, default=datetime.datetime.utcnow, nullable=False),
)

class ResourceMediawikiLink(DomainObject):
    def __init__(self, resource_id=None, url=None, link_name=None, create_at=None, updated_at=None):
        self.resource_id = resource_id
        self.url = url
        self.link_name = link_name
        self.create_at = create_at
        self.updated_at = updated_at
    
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







