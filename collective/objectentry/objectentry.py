#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Zope dependencies
#
from zope import schema
from zope.interface import invariant, Invalid, Interface, implements
from zope.interface import alsoProvides
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.fieldproperty import FieldProperty
from zope.component import getMultiAdapter

#
# Plone dependencies
#
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

#
# z3c.forms dependencies
#
from z3c.form import group, field
from z3c.form.form import extends
from z3c.form.browser.textlines import TextLinesFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList

#
# DataGridFields dependencies
#
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from collective.z3cform.datagridfield.blockdatagridfield import BlockDataGridFieldFactory


# # # # # # # # # # # # # # # 
# Dexterity imports         # 
# # # # # # # # # # # # # # # 
from five import grok
from collective import dexteritytextindexer
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.content import Container
from plone.dexterity.browser import add, edit

# # # # # # # # # # # # # # # # 
# !Object specific imports!   #
# # # # # # # # # # # # # # # #
from collective.objectentry import MessageFactory as _
from .utils.vocabularies import *
from .utils.interfaces import *
from .utils.views import *
from .utils.source import ObjPathSourceBinder


# # # # # # # # # #
# # # # # # # # # #
# Object schema   #
# # # # # # # # # #
# # # # # # # # # #

class IObjectEntry(form.Schema):
    text = RichText(
        title=_(u"Body"),
        required=False
    )

    priref = schema.TextLine(
        title=_(u'priref'),
        required=False
    )
    dexteritytextindexer.searchable('priref')

    # # # # # # # # # # # # # # 
    # Identification fieldset #
    # # # # # # # # # # # # # # 
    
    model.fieldset('general', label=_(u'General'), 
        fields=['general_entry_transportNumber',
                'general_entry_dateExpected', 'general_entry_entryDate',
                'general_entry_transportMethod', 'general_entry_reason',
                'general_entry_currentOwner', 'general_entry_depositor',
                'general_entry_destination', 'general_transport_shipper',
                'general_transport_courier', 'general_numberOfObjects_numberInFreightLetter',
                'general_numberOfObjects_numberDelivered', 'general_freightLetter_template',
                'general_freightLetter_digRef', 'general_totalInsuranceValue_insuranceValue',
                'general_totalInsuranceValue_currency', 'general_requirements_requirements',
                'general_requirements_packingNotes', 'general_requirements_digitalReferences',
                'general_notes_notes']
    )

    #
    # Entry
    #
    general_entry_transportNumber =  schema.TextLine(
        title=_(u'Transport number'),
        required=False
    )
    dexteritytextindexer.searchable('general_entry_transportNumber')

    general_entry_dateExpected =  schema.TextLine(
        title=_(u'Date (expected)'),
        required=False
    )
    dexteritytextindexer.searchable('general_entry_dateExpected')

    general_entry_entryDate =  schema.TextLine(
        title=_(u'Entry date'),
        required=False
    )
    dexteritytextindexer.searchable('general_entry_entryDate')

    general_entry_transportMethod = schema.TextLine(
        title=_(u'Transport method'),
        required=False
    )
    dexteritytextindexer.searchable('general_entry_transportMethod')

    general_entry_reason = schema.TextLine(
        title=_(u'Reason'),
        required=False
    )
    dexteritytextindexer.searchable('general_entry_reason')

    general_entry_currentOwner = schema.TextLine(
        title=_(u'Current owner'),
        required=False
    )
    dexteritytextindexer.searchable('general_entry_reason')

    general_entry_depositor = ListField(title=_(u'Depositor'),
        value_type=DictRow(title=_(u'Depositor'), schema=IDepositor),
        required=False)
    form.widget(general_entry_depositor=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('general_entry_depositor')

    general_entry_destination = ListField(title=_(u'Destination'),
        value_type=DictRow(title=_(u'Destination'), schema=IDestination),
        required=False)
    form.widget(general_entry_destination=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('general_entry_destination')

    #
    # Transport
    #
    general_transport_shipper = ListField(title=_(u'Shipper'),
        value_type=DictRow(title=_(u'Shipper'), schema=IShipper),
        required=False)
    form.widget(general_transport_shipper=DataGridFieldFactory)
    dexteritytextindexer.searchable('general_transport_shipper')

    general_transport_courier = schema.TextLine(
        title=_(u'Courier'),
        required=False
    )
    dexteritytextindexer.searchable('general_transport_courier')

    #
    # Number of objects
    #
    general_numberOfObjects_numberInFreightLetter = schema.TextLine(
        title=_(u'Number in freight letter'),
        required=False
    )
    dexteritytextindexer.searchable('general_numberOfObjects_numberInFreightLetter')

    general_numberOfObjects_numberDelivered = schema.TextLine(
        title=_(u'Number delivered'),
        required=False
    )
    dexteritytextindexer.searchable('general_numberOfObjects_numberDelivered')

    #
    # Freight letter
    #
    general_freightLetter_template = schema.TextLine(
        title=_(u'Template'),
        required=False
    )
    dexteritytextindexer.searchable('general_freightLetter_template')

    general_freightLetter_digRef = schema.TextLine(
        title=_(u'(Dig.) ref.'),
        required=False
    )
    dexteritytextindexer.searchable('general_freightLetter_digRef')

    #
    # Total insurance value
    #
    general_totalInsuranceValue_insuranceValue = schema.TextLine(
        title=_(u'Insurance value'),
        required=False
    )
    dexteritytextindexer.searchable('general_totalInsuranceValue_insuranceValue')

    general_totalInsuranceValue_currency = schema.TextLine(
        title=_(u'Currency'),
        required=False
    )
    dexteritytextindexer.searchable('general_totalInsuranceValue_currency')

    #
    # Requirements
    #
    general_requirements_requirements = ListField(title=_(u'Requirements'),
        value_type=DictRow(title=_(u'Requirements'), schema=IRequirements),
        required=False)
    form.widget(general_requirements_requirements=DataGridFieldFactory)
    dexteritytextindexer.searchable('general_requirements_requirements')

    general_requirements_packingNotes = ListField(title=_(u'Packing notes'),
        value_type=DictRow(title=_(u'Packing notes'), schema=IPackingNotes),
        required=False)
    form.widget(general_requirements_packingNotes=DataGridFieldFactory)
    dexteritytextindexer.searchable('general_requirements_packingNotes')

    general_requirements_digitalReferences = ListField(title=_(u'Digital references'),
        value_type=DictRow(title=_(u'Digital references'), schema=IDigitalReferences),
        required=False)
    form.widget(general_requirements_digitalReferences=DataGridFieldFactory)
    dexteritytextindexer.searchable('general_requirements_digitalReferences')

    #
    # Notes
    #
    general_notes_notes = ListField(title=_(u'Notes'),
        value_type=DictRow(title=_(u'Notes'), schema=INotes),
        required=False)
    form.widget(general_notes_notes=DataGridFieldFactory)
    dexteritytextindexer.searchable('general_notes_notes')

    
    model.fieldset('template_for_object_data', label=_(u'Template for object data'), 
        fields=['templateForObjectData_objectName', 'templateForObjectData_title',
                'templateForObjectData_description', 'templateForObjectData_date',
                'templateForObjectData_creator', 'templateForObjectData_material',
                'templateForObjectData_technique', 'templateForObjectData_location',
                'templateForObjectData_currentOwner', 'templateForObjectData_notes',
                'templateForObjectData_createLinkedObjectRecords']
    )

    templateForObjectData_objectName = ListField(title=_(u'Object name'),
        value_type=DictRow(title=_(u'Object name'), schema=IObjectName),
        required=False)
    form.widget(templateForObjectData_objectName=DataGridFieldFactory)
    dexteritytextindexer.searchable('templateForObjectData_objectName')


    templateForObjectData_title = ListField(title=_(u'Title'),
        value_type=DictRow(title=_(u'Title'), schema=ITitle),
        required=False)
    form.widget(templateForObjectData_title=DataGridFieldFactory)
    dexteritytextindexer.searchable('templateForObjectData_title')

    templateForObjectData_description = schema.TextLine(
        title=_(u'Description'),
        required=False
    )
    dexteritytextindexer.searchable('templateForObjectData_description')

    templateForObjectData_date = ListField(title=_(u'Date'),
        value_type=DictRow(title=_(u'Date'), schema=IDate),
        required=False)
    form.widget(templateForObjectData_date=DataGridFieldFactory)
    dexteritytextindexer.searchable('templateForObjectData_date')

    templateForObjectData_creator = ListField(title=_(u'Creator'),
        value_type=DictRow(title=_(u'Creator'), schema=ICreator),
        required=False)
    form.widget(templateForObjectData_creator=DataGridFieldFactory)
    dexteritytextindexer.searchable('templateForObjectData_creator')

    templateForObjectData_material = ListField(title=_(u'Material'),
        value_type=DictRow(title=_(u'Material'), schema=IMaterial),
        required=False)
    form.widget(templateForObjectData_material=DataGridFieldFactory)
    dexteritytextindexer.searchable('templateForObjectData_material')

    templateForObjectData_technique = ListField(title=_(u'Technique'),
        value_type=DictRow(title=_(u'Technique'), schema=ITechnique),
        required=False)
    form.widget(templateForObjectData_technique=DataGridFieldFactory)
    dexteritytextindexer.searchable('templateForObjectData_technique')

    templateForObjectData_location = schema.TextLine(
        title=_(u'Location'),
        required=False
    )
    dexteritytextindexer.searchable('templateForObjectData_location')

    templateForObjectData_currentOwner = schema.TextLine(
        title=_(u'Current owner'),
        required=False
    )
    dexteritytextindexer.searchable('templateForObjectData_currentOwner')

    templateForObjectData_notes = ListField(title=_(u'Notes'),
        value_type=DictRow(title=_(u'Notes'), schema=INotes),
        required=False)
    form.widget(templateForObjectData_notes=DataGridFieldFactory)
    dexteritytextindexer.searchable('templateForObjectData_notes')

    templateForObjectData_createLinkedObjectRecords = schema.TextLine(
        title=_(u'Create linked object records'),
        required=False
    )
    dexteritytextindexer.searchable('templateForObjectData_createLinkedObjectRecords')


    model.fieldset('list_with_linked_objects', label=_(u'List with linked objects'), 
        fields=['listWithLinkedObjects_transportContentNote', 'listWithLinkedObjects_linkedObjects']
    )

    listWithLinkedObjects_transportContentNote = schema.TextLine(
        title=_(u'Transport content note'),
        required=False
    )
    dexteritytextindexer.searchable('listWithLinkedObjects_transportContentNote')

    listWithLinkedObjects_linkedObjects = ListField(title=_(u'Linked objects'),
        value_type=DictRow(title=_(u'Linked objects'), schema=ILinkedObjects),
        required=False)
    form.widget(listWithLinkedObjects_linkedObjects=DataGridFieldFactory)
    dexteritytextindexer.searchable('listWithLinkedObjects_linkedObjects')



# # # # # # # # # # # # #
# Object declaration    #
# # # # # # # # # # # # #

class ObjectEntry(Container):
    grok.implements(IObjectEntry)
    pass

# # # # # # # # # # # # # #
# Object add/edit views   # 
# # # # # # # # # # # # # #

class AddForm(add.DefaultAddForm):
    template = ViewPageTemplateFile('objectentry_templates/add.pt')
    def update(self):
        super(AddForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                alsoProvides(widget, IFormWidget)

class AddView(add.DefaultAddView):
    form = AddForm
    

class EditForm(edit.DefaultEditForm):
    template = ViewPageTemplateFile('objectentry_templates/edit.pt')
    
    def update(self):
        super(EditForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                alsoProvides(widget, IFormWidget)

