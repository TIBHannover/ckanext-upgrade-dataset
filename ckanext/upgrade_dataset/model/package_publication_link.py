# encoding: utf-8

import datetime
from sqlalchemy import Column, Table, ForeignKey, orm
from sqlalchemy import types as _types
from sqlalchemy.sql.expression import false
from ckan.model import meta, Package, domain_object


__all__ = [u"PackagePublicationLink", u"package_publication_link_table"]

package_publication_link_table = Table(
    u"package_publication_link",
    meta.metadata,
    Column(u"id", _types.Integer, primary_key=True, nullable=False),
    Column(u"package_name", _types.UnicodeText, ForeignKey(u"package.name"), nullable=False),
    Column(u"doi", _types.UnicodeText, nullable=False),    
    Column(u"create_at", _types.DateTime, default=datetime.datetime.utcnow, nullable=False),
)

class PackagePublicationLink(domain_object.DomainObject):
    def __init__(self, package_name=None, doi=None, create_at=None):
        self.package_name = package_name
        self.doi = doi        
        self.create_at = create_at

    
    @classmethod
    def get_by_package(cls, name, autoflush=True):
        if not name:
            return None

        exists = meta.Session.query(cls).filter(cls.package_name==name).first() is not None
        if not exists:
            return false
        query = meta.Session.query(cls).filter(cls.package_name==name)
        query = query.autoflush(autoflush)
        record = query.all()
        return record
    

    @classmethod
    def get_by_id(cls, id, autoflush=True):
        if not id:
            return None

        exists = meta.Session.query(cls).filter(cls.id==id).first() is not None
        if not exists:
            return false
        query = meta.Session.query(cls).filter(cls.id==id)
        query = query.autoflush(autoflush)
        record = query.first()
        return record

    
    def get_package(self):
        return self.package



meta.mapper(
    PackagePublicationLink,
    package_publication_link_table,
    properties={
        u"package": orm.relation(
            Package, backref=orm.backref(u"package_publication_link", cascade=u"all, delete, delete-orphan")
        )
    },
)







