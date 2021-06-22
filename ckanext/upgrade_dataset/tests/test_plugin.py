# encoding: utf-8
'''Tests for the ckanext.upgrade_dataset extension.

'''

import pytest
import ckan.tests.factories as factories
import ckan.lib.helpers as h
import ckan.model as model
import ckan.lib.create_test_data as ctd
from ckanext.upgrade_dataset.api import API
from os import path

@pytest.mark.usefixtures('with_plugins', 'with_request_context')
class TestMediaWiki(object):

    username = None
    password = None
    query = "[[Category:Equipment]]|?hasManufacturer|?hasModel"  # all Equipments (machines and tools)


    def test_APIcredential_exist(self):
        '''
            The api needs username and password which has to be 
            in /etc/ckan/default/credentials/smw1368.txt
        '''
        assert path.isdir('/etc/ckan/default/credentials/') == True  ## the directory exists
        assert path.isfile('/etc/ckan/default/credentials/smw1368.txt') == True  ## the file exists
        try:
            credentials = open('/etc/ckan/default/credentials/smw1368.txt', 'r').read()
            credentials = credentials.split('\n')
            self.username = credentials[0].split('=')[1]
            self.password = credentials[1].split('=')[1]
           
        except:
            print("The credential file structure is wrong.")
            assert False
        
        assert True
    

    def test_media_wiki_API_call(self):
        '''
            Test the mediaWiki API call 
        '''

        try:
            credentials = open('/etc/ckan/default/credentials/smw1368.txt', 'r').read()
            credentials = credentials.split('\n')
            self.username = credentials[0].split('=')[1]
            self.password = credentials[1].split('=')[1]
           
        except:
            print("The credentials do not exist.")
            assert False
        
        try:
            api_call = API(username=self.username, password=self.password, query=self.query)
            results = api_call.pipeline()
        except:
            print("API call failed.")
            assert False
        
        if not results or len(results) == 0:
            print("API returns nothing.")
            assert False

        assert True

