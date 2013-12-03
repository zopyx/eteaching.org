# -*- coding: utf-8 -*-

################################################################
# eteaching.policy
# (C) 2013, ZOPYX Ltd.
################################################################

import os
import glob
import shutil
import urllib2
import random
import loremipsum

import zope.event
from plone.i18n.normalizer.de import Normalizer
from zope.component import getUtility

from App.config import getConfiguration
from DateTime.DateTime import DateTime
from Products.Five.browser import BrowserView
from Products.CMFPlone.factory import addPloneSite
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.event import ObjectInitializedEvent


def gen_paragraphs(num=3):
    return u'/'.join([p[2] for p in loremipsum.Generator().generate_paragraphs(num)])

def gen_sentence(max_words=None):
    text = loremipsum.Generator().generate_sentence()[-1]
    if max_words:
        return u' '.join(text.split(' ')[:max_words])
    return text

def gen_sentences(length=80):
    return u' '.join([s[2] for s in loremipsum.Generator().generate_sentences(length)])

def random_image(width, height):
    url = 'http://lorempixel.com/%d/%d/' % (width, height)
    return urllib2.urlopen(url).read()

def normalizeString(title):

    if isinstance(title, unicode):
        s = Normalizer().normalize(title.lower())
    else:
        s = Normalizer().normalize(unicode(title, 'utf-8').lower())
    s = s.replace(' ', '-')
    s = s.replace('%20', '-')
    if s.endswith('.'):
        s = s[:-1]
    return s

def setText(obj, fieldname, text):
    field = obj.Schema().getField(fieldname)
    field.set(obj, text)
    field.setContentType(obj, 'text/html')

def publish(obj):
    wf_tool = getToolByName(obj, 'portal_workflow')
    try:
        wf_tool.doActionFor(obj, 'publish')
    except:
        pass

def createFolderHierarchy(site, path):
    current = site
    for p in path.split('/'):
        if not p in current.objectIds():
            if 'ressourcen' in path:
                current.invokeFactory('ResourcesFolder', id=p, title=p)
            else:
                current.invokeFactory('Folder', id=p, title=p)

            publish(current[p])
            current[p].reindexObject()
        current = current[p]
    return current                        

def invokeFactory(folder, portal_type, title=None):
    obj_title = title
    if not obj_title:
        obj_title = gen_sentence()
    obj_id = normalizeString(obj_title)
    if obj_id in folder.objectIds():
        obj_id += str(random.randint(0,100))
    if isinstance(obj_title, unicode):
        obj_title = obj_title.encode('utf-8')
#    else:
#        obj_title = unicode(obj_title, 'iso-8859-15').encode('utf-8')
    folder.invokeFactory(portal_type, id=obj_id, title=obj_title)
    folder[obj_id].setDescription(gen_sentence(25))
    folder[obj_id].reindexObject()
    obj = folder[obj_id]
    publish(obj)
    return obj

class Setup(BrowserView):

    def setupSite(self, with_content=False):
        portal_id = 'et-%s' % DateTime().strftime('%d.%m.%y-%H%M%S')
        profiles = ['plonetheme.sunburst:default', 'eteaching.policy:default']
        addPloneSite(self.context, portal_id, create_userfolder=True, extension_ids=profiles)
        site = self.context[portal_id]
        self.request.response.redirect(self.context.getId() + '/' + portal_id)

