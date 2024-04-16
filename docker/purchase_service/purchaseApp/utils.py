import requests

def get_username(request):
    if isAuthenticated(request):

        user_token = request.authorization.__str__()[7:-1]

        request_url = 'http://127.0.0.1:8000/api/account/authenticate'
        request_headers = {'Authorization': 'Bearer ' + user_token}
        response = requests.post(request_url, headers=request_headers)

        return response.json()['username']
    else:
        return None

def isAuthenticated(request):
    auth = request.authorization.__str__()[0:6]
    print(auth)
    if auth is None or auth != 'Bearer':
        return False
    else:
        return True
    
def get_cart(username):
    ...