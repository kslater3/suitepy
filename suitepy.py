
from urllib import response
import requests
from requests_oauthlib import OAuth1



class Response:
    def __init__(self, response):
        self.response = response
        
        self.ok = response.ok
        self.status_code = response.status_code
        self.headers = response.headers
        
        if not response.ok:
            self.error_title = response.json()['title']
            self.error_status = str(response.json()['status'])
            self.error_msg = response.json()['o:errorDetails'][0]['detail']
            
            self._print_error()
            
            #TODO: Throw Exception
    
    
    def _print_error(self):
        print('ERROR')
        print('error_title: ' + self.error_title)
        print('error_status: ' + str(self.error_status))
        print('error_msg: ' + self.error_msg)
        print('')
        



class QueryResponse(Response):
    def __init__(self, response):
        super().__init__(response)
        
        self.links = {}
        self.count = 0
        self.hasMore = False
        self.offset = 0
        self.totalResults = 0
        self.items = []
        
        if response.ok:
            if response.status_code != 204:
                jsonResults = response.json()
                
                for link in jsonResults['links']:
                    self.links[link['rel']] = link['href']
            
                self.count = jsonResults['count']
                
                self.hasMore = jsonResults['hasMore']
                
                self.offset = jsonResults['offset']
                
                self.totalResults = jsonResults['totalResults']
                
                self.items = jsonResults['items']
    



class RESTMaster:
    def __init__(self, credentials):
        self.credentials = credentials
        
        self.base_url = 'https://' + credentials['account_id'] + '.suitetalk.api.netsuite.com/services/rest/'
        
        # Note that "realm" in the sandbox requires underscore and capitalization
        self.oauth = OAuth1(credentials['consumer_key'], client_secret=credentials['consumer_secret'], resource_owner_key=credentials['token_id'], resource_owner_secret=credentials['token_secret'], signature_method='HMAC-SHA256', realm=credentials['account_id'].upper().replace('-', '_'))
    
    
    
    def _determine_all_fields(self, items):
        all_fields = set()
        
        for item in items:
            for field in item:
                if field != 'links':
                    all_fields.add(field)

        return list(all_fields)
    
    
    
    def _dict_from_results(self, items):
        item_dict = {}
        
        full_fields = self._determine_all_fields(items)
        
        for field in full_fields:
            item_dict[field] = []


        for item in items:
            for field in item:
                if field != 'links':
                    item_dict[field].append(item[field])
            
            for field in full_fields:
                if not field in item:
                    item_dict[field].append(None)

        return item_dict
        
    
    
    def query(self, url, queryString):
        body = '{"q": "' + queryString + '"}'
        
        return requests.post(url, auth=self.oauth, data=body, cookies={'NS_ROUTING_VERSION': 'LAGGING'}, headers={'prefer': 'transient'})
    
    
    
    def query_all(self, queryString):
        #TODO: Require Query String to be Select Statement for Query All to Run
        
        all_items = []
        
        moreQueries = True
        
        next_url = self.base_url + 'query/v1/suiteql'
        
        queryRun = 0
        
        while(moreQueries):
            moreQueries = False
            
            results = self.query(url=next_url, queryString=queryString)
            
            response = QueryResponse(results)
            
            if response.ok:
                moreQueries = response.hasMore
                
                if moreQueries:
                    next_url = response.links['next']
                
                all_items.extend(response.items)
                
                print("Running Query " + str(queryRun) + ' of ' + str(response.totalResults // 1000 + 1000 // response.totalResults), end='\r')
                queryRun += 1
            else:
                #TODO: Throw Exception
                return {}
        
        all_items = self._dict_from_results(all_items)
        
        return all_items
    
    
    def create(self, typeId, data):
        url = self.base_url + 'record/v1/' + typeId
        
        response = Response(requests.post(url, auth=self.oauth, data=data, cookies={'NS_ROUTING_VERSION': 'LAGGING'}, headers={'prefer': 'transient'}))
        
        return response
    
    
    #TODO: Make a "create_bulk" method and deal with an entire json 1 at a time
    
    
    def update(self, typeId, recordId, data):
        url = self.base_url + 'record/v1/' + typeId + '/' + str(recordId)
        
        response = Response(requests.patch(url, auth=self.oauth, data=data, cookies={'NS_ROUTING_VERSION': 'LAGGING'}, headers={'prefer': 'transient'}))
        
        return response
    
    
    #TODO: Make a "update_bulk" method and deal with an entire json 1 at a time
    
    
    #TODO: Make an Upsert
    
    
    def delete(self, typeId, recordId):
        url = self.base_url + 'record/v1/' + typeId + '/' + str(recordId)
        
        response = Response(requests.delete(url, auth=self.oauth, cookies={'NS_ROUTING_VERSION': 'LAGGING'}, headers={'prefer': 'transient'}))
        
        return response 


