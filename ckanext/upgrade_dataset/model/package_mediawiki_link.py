# encoding: utf-8

import copy
import datetime

from sqlalchemy import types, Column, Table, ForeignKey, orm
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

import ckan.plugins.toolkit as tk
from ckan.model import meta, Package, DomainObject


__all__ = [u"PackageMediawikiLink", u"package_mediawiki_link_table"]

package_mediawiki_link_table = Table(
    u"package_mediawiki_link",
    meta.metadata,
    Column(u"id", types.Integer, primary_key=True, nullable=False, default=types.make_uuid),
    Column(u"package_name", types.UnicodeText, ForeignKey(u"package.name"), nullable=False),
    Column(u"url", types.UnicodeText, nullable=False),
    Column(u"link_name", types.UnicodeText),
    Column(u"create_at", types.DateTime, default=datetime.datetime.utcnow, nullable=False),
    Column(u"updated_at", types.DateTime, default=datetime.datetime.utcnow, nullable=False),
)

class PackageMediawikiLink(DomainObject):
    def __init__(self, package_name=None):
        self.package_name = package_name
    
    @classmethod
    def get(cls, id):
        if not id:
            return None
        return meta.Session.query(cls).get(id)
    
    def get_package(self):
        return [self.package]



meta.mapper(
    PackageMediawikiLink,
    package_mediawiki_link_table,
    properties={
        u"package": orm.relation(
            Package, backref=orm.backref(u"package_mediawiki_links", cascade=u"all, delete, delete-orphan")
        )
    },
)







