#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from collective.objectentry import MessageFactory as _
from collective.object.utils.vocabularies import ATVMVocabulary, ObjectVocabulary


# # # # # # # # # # # # # #
# Vocabularies            #
# # # # # # # # # # # # # #

def _createInsuranceTypeVocabulary():
    insurance_types = {
        "commercial": _(u"Commercial"),
        "indemnity": _(u"Indemnity"),
    }

    for key, name in insurance_types.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        yield term

def _createPriorityVocabulary():
    priorities = {
        "low": _(u"low"),
        "medium": _(u"medium"),
        "high": _(u"high"),
        "urgent": _(u"urgent")
    }

    for key, name in priorities.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        yield term

def _createTemplateVocabulary():
    templates = {
        "English": _(u"English"),
        "Dutch": _(u"Dutch"),
        "German": _(u"German")
    }

    terms = []
    terms.append(SimpleTerm(value="No value", token=str("No value"), title=_(u" ")))
    for key, name in templates.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        terms.append(term)
    
    return terms


priority_vocabulary = SimpleVocabulary(list(_createPriorityVocabulary()))
insurance_type_vocabulary = SimpleVocabulary(list(_createInsuranceTypeVocabulary()))
template_vocabulary = SimpleVocabulary(list(_createTemplateVocabulary()))


TransportMethodVocabularyFactory = ObjectVocabulary('general_entry_transportMethod')
ReasonVocabularyFactory = ATVMVocabulary('ObjectEntryReason')
ObjectnameVocabularyFactory = ObjectVocabulary('templateForObjectData_objectName')
ProductionPlaceVocabularyFactory = ObjectVocabulary('templateForObjectData_creator_productionPlace')
MaterialVocabularyFactory = ObjectVocabulary('templateForObjectData_material')
TechniqueVocabularyFactory = ObjectVocabulary('templateForObjectData_technique')
LocationVocabularyFactory = ObjectVocabulary('templateForObjectData_location')
CurrencyVocabularyFactory = ObjectVocabulary('listWithLinkedObjects_linkedObjects_curr')

