#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface
from collective.objectentry import MessageFactory as _
from ..utils.vocabularies import _createPriorityVocabulary, _createInsuranceTypeVocabulary
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

priority_vocabulary = SimpleVocabulary(list(_createPriorityVocabulary()))
insurance_type_vocabulary = SimpleVocabulary(list(_createInsuranceTypeVocabulary()))

class ListField(schema.List):
    """We need to have a unique class for the field list so that we
    can apply a custom adapter."""
    pass

# # # # # # # # # # # # #
# Widget interface      #
# # # # # # # # # # # # #

class IFormWidget(Interface):
    pass


# # # # # # # # # # # # # #
# DataGrid interfaces     # 
# # # # # # # # # # # # # #

# General
class IDepositor(Interface):
    name = schema.TextLine(title=_(u'Depositor'), required=False)
    contact = schema.TextLine(title=_(u'Contact'), required=False)

class IDestination(Interface):
    term = schema.TextLine(title=_(u'Destination'), required=False)
    contact = schema.TextLine(title=_(u'Contact'), required=False)

class IShipper(Interface):
    term = schema.TextLine(title=_(u'Shipper'), required=False)
    contact = schema.TextLine(title=_(u'Contact'), required=False)

class IRequirements(Interface):
    term = schema.TextLine(title=_(u'Requirements'), required=False)

class IPackingNotes(Interface):
    term = schema.TextLine(title=_(u'Packing notes'), required=False)

class IDigitalReferences(Interface):
    type = schema.TextLine(title=_(u'Type'), required=False)
    reference = schema.TextLine(title=_(u'Reference'), required=False)

class INotes(Interface):
    notes = schema.Text(title=_(u'Notes'), required=False)

class IObjectName(Interface):
    term = schema.TextLine(title=_(u'Object name'), required=False)

class ITitle(Interface):
    title = schema.TextLine(title=_(u'Title'), required=False)

class IDate(Interface):
    dateEarly = schema.TextLine(title=_(u'Date early'), required=False)
    dateLate = schema.TextLine(title=_(u'Date late'), required=False)

class ICreator(Interface):
    creator = schema.TextLine(title=_(u'Creator'), required=False)
    productionPlace = schema.TextLine(title=_(u'Production place'), required=False)

class IMaterial(Interface):
    term = schema.TextLine(title=_(u'Material'), required=False)

class ITechnique(Interface):
    term = schema.TextLine(title=_(u'Technique'), required=False)

class ILinkedObjects(Interface):
    recordNumber = schema.TextLine(title=_(u'Record number'), required=False)
    objectNumber = schema.TextLine(title=_(u'Object number'), required=False)
    maker = schema.TextLine(title=_(u'Maker'), required=False)
    objectName = schema.TextLine(title=_(u'Object name'), required=False)
    title = schema.TextLine(title=_(u'Title'), required=False)
    status = schema.TextLine(title=_(u'Status'), required=False)
    conditionChecked = schema.TextLine(title=_(u'Condition checked'), required=False)
    transportReason = schema.TextLine(title=_(u'Transport reason'), required=False)
    packing = schema.TextLine(title=_(u'Packing'), required=False)
    insuranceValue = schema.TextLine(title=_(u'Insurance value'), required=False)
    curr = schema.TextLine(title=_(u'Curr.'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)


