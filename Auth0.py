import requests
from requests import RequestException, URLRequired, HTTPError

domain = 'dev-348imcezrwd5f04u.us.auth0.com'
client_id = 'rlKmKUfSuynLjWo1wFE404D6qSD25nf9'
client_secret = '6J79ReXzkULbSEwLLDRJdrUUPQ-t0ZYJ0PnDPv7Jgvb2xtCjMCE5wmzIwqfBxdoc'
audience = 'https://dev-348imcezrwd5f04u.us.auth0.com/api/v2/'
grant_type = 'client_credentials'
connection = 'dump-db'
single_page_client_Id = 'a9tDsq10GLLBAQp8ksFZzizIvYcMeP8S'

# Get an Access Token from Auth0
base_url = f"https://{domain}"
payload =  {
  'grant_type': grant_type,
  'client_id': client_id,
  'client_secret': client_secret,
  'audience': audience
}
response = requests.post(f'{base_url}/oauth/token', data=payload)
oauth = response.json()
print(type(oauth))
access_token = oauth.get('access_token')
# print(access_token)

# Add the token to the Authorization header of the request
headers = {
  'Authorization': f'Bearer {access_token}',
  'Content-Type': 'application/json'
}

# Get all Applications using the token
try:
  res = requests.get(f'{base_url}/api/v2/clients', headers=headers)
  print(res.json())
except HTTPError as e:
  print(f'HTTPError: {str(e.code)} {str(e.reason)}')
except URLRequired as e:
  print(f'URLRequired: {str(e.reason)}')
except RequestException as e:
  print(f'RequestException: {e}')
except Exception as e:
  print(f'Generic Exception: {e}')

