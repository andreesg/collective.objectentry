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
from collective.z3cform.datagridfield.interfaces import IDataGridField

# # # # # # # # # # # # # # # 
# Dexterity imports         # 
# # # # # # # # # # # # # # # 
from five import grok
from collective import dexteritytextindexer
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.content import Container
from plone.dexterity.browser import add, edit
from plone.app.widgets.dx import AjaxSelectFieldWidget

# # # # # # # # # # # # # # # # 
# !Object specific imports!   #
# # # # # # # # # # # # # # # #
from collective.objectentry import MessageFactory as _
from .utils.vocabularies import *
from .utils.interfaces import *
from .utils.views import *

from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from collective.object.utils.widgets import SimpleRelatedItemsFieldWidget, AjaxSingleSelectFieldWidget
from collective.object.utils.source import ObjPathSourceBinder
from plone.directives import dexterity, form

# # # # # # # # # #
# # # # # # # # # #
# Object schema   #
# # # # # # # # # #
# # # # # # # # # #


from plone.app.content.interfaces import INameFromTitle
class INameFromTransportNumber(INameFromTitle):
    def title():
        """Return a processed title"""

class NameFromTransportNumber(object):
    implements(INameFromTransportNumber)
    
    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return self.context.title

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
        fields=['title',
                'general_entry_dateExpected', 'general_entry_entryDate',
                'general_entry_returnDate',
                'general_entry_transportMethod', 'general_entry_reason',
                'general_entry_currentOwner', 'general_entry_depositor',
                'general_entry_depositorContact',
                'general_entry_destination', 'general_entry_destinationContact',
                'general_transport_shipper',
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
    title =  schema.TextLine(
        title=_(u'Transport number'),
        required=True
    )
    dexteritytextindexer.searchable('title')

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

    general_entry_returnDate =  schema.TextLine(
        title=_(u'Return date'),
        required=False
    )
    dexteritytextindexer.searchable('general_entry_returnDate')

    general_entry_transportMethod = schema.List(
        title=_(u'Transport method'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[],
        default=[]
    )
    form.widget('general_entry_transportMethod', AjaxSingleSelectFieldWidget, vocabulary="collective.objectentry.transportmethod")

    general_entry_reason = schema.Choice(
        title=_(u'Reason'), 
        required=True,
        vocabulary="collective.objectentry.reason", 
        default="No value",
        missing_value=" "
    )

    general_entry_currentOwner = RelationList(
        title=_(u'Current owner'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('general_entry_currentOwner', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')


    general_entry_depositor = RelationList(
        title=_(u'Depositor'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('general_entry_depositor', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    general_entry_depositorContact = RelationList(
        title=_(u'Contact'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('general_entry_depositorContact', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    general_entry_destination = RelationList(
        title=_(u'Destination'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('general_entry_destination', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')


    general_entry_destinationContact = RelationList(
        title=_(u'Contact'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('general_entry_destinationContact', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    #
    # Transport
    #
    general_transport_shipper = ListField(title=_(u'Shipper'),
        value_type=DictRow(title=_(u'Shipper'), schema=IShipper),
        required=False)
    form.widget(general_transport_shipper=BlockDataGridFieldFactory)
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
    general_freightLetter_template = schema.Choice(
        title=_(u'Template'), 
        required=True,
        vocabulary=template_vocabulary, 
        default="No value",
        missing_value=" "
    )

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
    form.widget(general_requirements_digitalReferences=BlockDataGridFieldFactory)
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

    templateForObjectData_objectName = schema.List(
        title=_(u'Object name'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[],
        default=[]
    )
    form.widget('templateForObjectData_objectName', AjaxSelectFieldWidget, vocabulary="collective.objectentry.objectname")


    templateForObjectData_title = ListField(title=_(u'Title'),
        value_type=DictRow(title=_(u'Title'), schema=ITitle),
        required=False)
    form.widget(templateForObjectData_title=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('templateForObjectData_title')

    templateForObjectData_description = schema.TextLine(
        title=_(u'Description'),
        required=False
    )
    dexteritytextindexer.searchable('templateForObjectData_description')

    templateForObjectData_date = ListField(title=_(u'Date'),
        value_type=DictRow(title=_(u'Date'), schema=IDate),
        required=False)
    form.widget(templateForObjectData_date=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('templateForObjectData_date')

    templateForObjectData_creator = ListField(title=_(u'Creator'),
        value_type=DictRow(title=_(u'Creator'), schema=ICreator),
        required=False)
    form.widget(templateForObjectData_creator=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('templateForObjectData_creator')

    templateForObjectData_material = schema.List(
        title=_(u'Material'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[],
        default=[]
    )
    form.widget('templateForObjectData_material', AjaxSelectFieldWidget, vocabulary="collective.objectentry.material")

    templateForObjectData_technique = schema.List(
        title=_(u'Technique'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[],
        default=[]
    )
    form.widget('templateForObjectData_technique', AjaxSelectFieldWidget, vocabulary="collective.objectentry.technique")

    templateForObjectData_location = schema.List(
        title=_(u'Location'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[],
        default=[]
    )
    form.widget('templateForObjectData_location', AjaxSelectFieldWidget, vocabulary="collective.objectentry.location")

    templateForObjectData_currentOwner = RelationList(
        title=_(u'Current owner'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('templateForObjectData_currentOwner', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    templateForObjectData_notes = ListField(title=_(u'Notes'),
        value_type=DictRow(title=_(u'Notes'), schema=INotes),
        required=False)
    form.widget(templateForObjectData_notes=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('templateForObjectData_notes')

    templateForObjectData_createLinkedObjectRecords = schema.Bool(
        title=_(u'Create linked object records'),
        required=False,
        default=False,
        missing_value=False
    )


    model.fieldset('list_with_linked_objects', label=_(u'List with linked objects'), 
        fields=['listWithLinkedObjects_transportContentNote', 'listWithLinkedObjects_linkedObjects']
    )

    listWithLinkedObjects_transportContentNote = schema.Text(
        title=_(u'Transport content note'),
        required=False
    )
    dexteritytextindexer.searchable('listWithLinkedObjects_transportContentNote')

    listWithLinkedObjects_linkedObjects = ListField(title=_(u'Linked objects'),
        value_type=DictRow(title=_(u'Linked objects'), schema=ILinkedObjects),
        required=False)
    form.widget(listWithLinkedObjects_linkedObjects=BlockDataGridFieldFactory)
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
                if IDataGridField.providedBy(widget):
                    widget.auto_append = False
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

