import base64
import simplejson as json
import hashlib
import hmac
import httplib2
import time
import urllib.request
from modules.Logger import *

ACCESS_TOKEN = 'd85cd8f6-9fce-4c5f-9901-8c43fc580a76'
SECRET_KEY = 'e6a6f4f5-bdf4-4f0a-a284-46daa10abc25'

#API_URL = 'https://api.coinone.co.kr/v2'

def get_encoded_payload(payload):
    payload[u'nonce'] = int(time.time()*1000)

    dumped_json = json.dumps(payload)  
    LOG.info( str(json.dumps(payload, sort_keys=True, indent=4) ) )

    #encoded_json = base64.b64encode(dumped_json.encode('utf-8'))
    encoded_json = base64.b64encode(dumped_json.encode())
    return encoded_json

def get_signature(encoded_payload, secret_key):
    #signature = hmac.new(str(secret_key).upper(), str(encoded_payload), hashlib.sha512);  
    key = str(secret_key).upper().encode('utf-8')
    signature = hmac.new( bytes(key), bytes(encoded_payload), hashlib.sha512);  
    return signature.hexdigest()

def post(url, payload):        
    LOG.info("url=>" + url )    
    try:
        encoded_payload = get_encoded_payload(payload)
        headers = {
            'Content-type': 'application/json',
            'X-COINONE-PAYLOAD': encoded_payload,
            'X-COINONE-SIGNATURE': get_signature(encoded_payload, SECRET_KEY)
        }        
        http = httplib2.Http()
        response, content = http.request(url, 'POST', headers=headers, body=encoded_payload)
        content = json.loads(content)
        LOG.info( "Response=>"+ str(json.dumps(content, sort_keys=True, indent=4) ) )
    except Exception as e:
        LOG.error("exception=>" + str(e)    )
        return None
    LOG.info("end")    
    return content

def get( url ):    
    LOG.info("url=>" + url )    
    try:
        session = urllib.request.urlopen(url, timeout=1 ) 
        content = session.read()    
        content = json.loads(content)
        #LOG.debug( "Response=>"+ str(json.dumps(content, sort_keys=True, indent=4) ) )
    except Exception as e:
        LOG.error("exception=>" + str(e)    )
        return None
    LOG.info("end")    
    return content

'''
def get_result( url, method, payload ):
    #full_url = API_URL + url
    
    content = post(url, payload)          
    content = json.loads(content)
    LOG.info( "Response=>"+ str(json.dumps(content, sort_keys=True, indent=4) ) )
    return content
'''
