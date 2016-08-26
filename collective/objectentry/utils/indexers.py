#!/usr/bin/python
# -*- coding: utf-8 -*-

from plone.indexer.decorator import indexer
from ..objectentry import IObjectEntry

@indexer(IObjectEntry)
def templateForObjectData_creator_productionPlace(object, **kw):
    try:
        if hasattr(object, 'templateForObjectData_creator'):
            terms = []
            items = object.templateForObjectData_creator
            if items:
                for item in items:
                    if item['productionPlace']:
                        for term in item['productionPlace']:
                            if term:
                                terms.append(term)

            return terms
        else:
            return []
    except:
        return []



@indexer(IObjectEntry)
def listWithLinkedObjects_linkedObjects_curr(object, **kw):
    try:
        if hasattr(object, 'listWithLinkedObjects_linkedObjects'):
            terms = []
            items = object.listWithLinkedObjects_linkedObjects
            if items:
                for item in items:
                    if item['curr']:
                        for term in item['curr']:
                            if term:
                                terms.append(term)

            return terms
        else:
            return []
    except:
        return []

