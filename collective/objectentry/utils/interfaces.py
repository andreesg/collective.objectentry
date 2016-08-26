#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface
from collective.objectentry import MessageFactory as _
from ..utils.vocabularies import _createPriorityVocabulary, _createInsuranceTypeVocabulary
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from collective.object.utils.widgets import SimpleRelatedItemsFieldWidget, AjaxSingleSelectFieldWidget
from collective.object.utils.source import ObjPathSourceBinder
from plone.directives import dexterity, form

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
    shipper = RelationList(
        title=_(u'Shipper'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            vocabulary='collective.object.relateditems'
        ),
        required=False
    )
    form.widget('shipper', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')
    contact = schema.TextLine(title=_(u'Contact'), required=False)

class IRequirements(Interface):
    term = schema.Text(title=_(u'Requirements'), required=False)

class IPackingNotes(Interface):
    term = schema.Text(title=_(u'Packing notes'), required=False)

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
    creator = RelationList(
        title=_(u'Creator'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            vocabulary='collective.object.relateditems'
        ),
        required=False
    )
    form.widget('creator', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    productionPlace = schema.List(
        title=_(u'Production place'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[],
        default=[]
    )
    form.widget('productionPlace', AjaxSingleSelectFieldWidget, vocabulary="collective.objectentry.productionPlace")

class IMaterial(Interface):
    term = schema.TextLine(title=_(u'Material'), required=False)

class ITechnique(Interface):
    term = schema.TextLine(title=_(u'Technique'), required=False)

class ILinkedObjects(Interface):
    objectNumber = RelationList(
        title=_(u'Object number'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            vocabulary='collective.object.relateditems'
        ),
        required=False
    )
    form.widget('objectNumber', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')
    status = schema.TextLine(title=_(u'Status'), required=False)
    conditionChecked = schema.Bool(title=_(u'Condition checked'), required=False, default=False, missing_value=False)
    transportReason = schema.TextLine(title=_(u'Transport reason'), required=False)
    packing = schema.TextLine(title=_(u'Packing'), required=False)
    insuranceValue = schema.TextLine(title=_(u'Insurance value'), required=False)
    curr = schema.List(
        title=_(u'Curr.'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[],
        default=[]
    )
    form.widget('curr', AjaxSingleSelectFieldWidget, vocabulary="collective.objectentry.currency")
    date = schema.TextLine(title=_(u'Date'), required=False)
    notes = schema.Text(title=_(u'label_notes', default=u'Notes'), required=False)


