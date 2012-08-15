import urllib2,json,hmac,hashlib, time

#api_key = 'e3823ddf28759f6ddf420da207031a3c43c169d6'
#secret_key = '350a53b206c09bcda6aaa428b9944d04cf9c8f65'
api_key = 'c55f5dc59ee5d02fb9346aea07f154d89e17e9cd'
secret_key = 'f15621dfd5dac6e134ca9c878487392da814ceb1'
class Pictorria_client:
    def __init__(self,api_key=None,secret_key=None):
        if api_key:
            self.api_key=api_key
        if secret_key:
            self.secret_key=secret_key

    def process_request(self,pictorria_request):
        if pictorria_request.url:
            return self.process_url(pictorria_request)
        elif pictorria_request.local_file:
            return self.process_file(pictorria_request)

    def process_url(self,pictorria_request):
        # Submit Process to Pictorria
        response = self.submit_process(pictorria_request)
        # If in sync mode, wait and get results
        pictorria_request.db_key = response['db_key']
        while 'eta' in response:
            time.sleep(response['eta'])
            response = self.get_result(pictorria_request)

        return response

    def process_file(self,pictorria_request):
        # Upload Image to Pictorria and get URL

        # Send to process_url

        return

    def upload_image(self,pictorria_request):
        return

    def submit_process(self,pictorria_request):
        trequest = {'api_key' : self.api_key , 'url':pictorria_request.url , 'command':'submit', 'service':pictorria_request.service_id}
        thmac = self.calculate_hmac(self.api_key+pictorria_request.url,self.secret_key)
        trequest['hmac'] = thmac
        trequest_json = json.dumps(trequest)
        req = urllib2.Request('http://www.pictorria.com/api',trequest_json,{'content-type':'application/json'})
        #req = urllib2.Request('http://127.0.0.1:8080/api',treq_json,{'content-type':'application/json'})
        response_stream = urllib2.urlopen(req)
        response = response_stream.read()
        print response
        resp = json.loads(response)
        print (resp['t2'])-(resp['t1'])
        print (resp['t3'])-(resp['t2'])
        return resp


    def get_result(self,pictorria_request):
        trequest = {'api_key' : self.api_key , 'command':'result', 'db_key':pictorria_request.db_key}
        thmac = self.calculate_hmac(self.api_key+pictorria_request.db_key,secret_key)
        trequest['hmac'] = thmac
        trequest_json = json.dumps(trequest)
        print trequest_json
        req = urllib2.Request('http://www.pictorria.com/api',trequest_json,{'content-type':'application/json'})
        #req = urllib2.Request('http://127.0.0.1:8080/api',treq_json,{'content-type':'application/json'})
        res_stream = urllib2.urlopen(req)
        resp = res_stream.read()
        print resp
        resp = json.loads(resp)
        return resp



    def calculate_hmac(self,message,secret_key):
        return hmac.new(str(secret_key), str(message), hashlib.sha1).hexdigest()

class Pictorria_Request:
    def __init__(self):
        self.url = False
        self.local_file = False
        self.status = ''
        self.service_id = ''
        self.image_id = ''
        self.process_time = ''
        self.sync = False
        self.token = ''
        self.db_key=''

if __name__ == '__main__':
    resp = submit()
    db_key = resp['db_key']
    while 'eta' in resp:
        time.sleep(resp['eta'])
        resp = result(db_key)
