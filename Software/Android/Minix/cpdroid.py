# -*- coding: utf-8 -*-
import logging
# The multiprocessing package isn't
# part of the ASE installation so
# we must disable multiprocessing logging
logging.logMultiprocessing = 0
 
import android
import cherrypy
import time
import goslate
#from translate import Translator
import urllib2
import urllib
import httplib
import sys
from xml.etree import ElementTree as etree

class wolfram(object):
    def __init__(self, appid):
        self.appid = 'G4XT2U-QP8W45HRTX'
        self.base_url = 'http://api.wolframalpha.com/v2/query?'
        self.headers = {'User-Agent':None}
 
    def _get_xml(self, ip):
        url_params = {'input':ip, 'appid':self.appid}
        data = urllib.urlencode(url_params)
        req = urllib2.Request(self.base_url, data, self.headers)
        xml = urllib2.urlopen(req).read()
        print xml
        return xml
 
    def _xmlparser(self, xml):
        data_dics = {}
        tree = etree.fromstring(xml)
        #retrieving every tag with label 'plaintext'
        for e in tree.findall('pod'):
            for item in [ef for ef in list(e) if ef.tag=='subpod']:
                for it in [i for i in list(item) if i.tag=='plaintext']:
                    if it.tag=='plaintext':
                        data_dics[e.get('title')] = it.text
        return data_dics
 
    def search(self, ip):
        xml = self._get_xml(ip)
        result_dics = self._xmlparser(xml)
        #return result_dics
        print result_dics
        if result_dics.has_key('Current result'):  
            return result_dics['Current result'] 
        elif result_dics.has_key('Result'): 
            return result_dics['Result'] 
        elif result_dics.has_key('Response'): 
            return result_dics['Response'] 
        else:
            return "i dont know"


    
    
class Root(object):
    def __init__(self):
        self.droid = android.Android()
 
    @cherrypy.expose
    def index(self):
        self.droid.vibrate()
        message = """
            location <br>
            speak/"what" <br>
            getQuestion (start the voice recognition)<br> 
        """
        return message
 
    @cherrypy.expose
    def location(self):
        location = self.droid.getLastKnownLocation().result
        location = location.get('network', location.get('gps'))
        return "LAT: %s, LON: %s" % (location['latitude'],
                                     location['longitude'])
    @cherrypy.expose
    def speak(self,what):
        droid = android.Android()
        droid.ttsSpeak(what)
        return "ok"

    @cherrypy.expose
    def getQuestion(self):
        "Voice recognitiion STT (Speech to text)"
        droid = android.Android()
        translation = ""
        results = droid.recognizeSpeech("Ask Ziri",None,None)
        if( results.error != None ) :   #If speech dialogue box is cancelled, use text entry mode
            speech = ""
            print "Hide Text Recognization Dialogue"
        else:
            speech =  results.result.encode('ascii', 'ignore') #fix the sì error but now "si" is "s" 
            print speech
            #goslate to english
            gs = goslate.Goslate()
            translation = gs.translate(speech, 'en')
            print translation
            #wolframalpha
            appid = 'G4XT2U-QP8W45HRTX'
            #query = 'distance moon'
            w = wolfram(appid)
            response = w.search(translation)
            print response
            #goslate to italian
            gs = goslate.Goslate()
            translation = gs.translate(response, 'it')
            droid = android.Android()
            clean_translation = translation.replace("|","")
            clean_translation = clean_translation.replace("(","")
            clean_translation = clean_translation.replace(")","")
            droid.ttsSpeak(clean_translation)
        return translation

def run():
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(Root(), '/')
 
if __name__ == '__main__':
    run()