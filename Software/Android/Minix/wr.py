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
        #print result_dics
        if result_dics.has_key('Current result'):  
            print result_dics['Current result'] 
        else:
            print result_dics['Result'] 

if __name__ == "__main__":
    appid = 'G4XT2U-QP8W45HRTX'
    query = 'distance moon'
    w = wolfram(appid)
    w.search(query)
      
