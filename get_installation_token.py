import requests
   from datetime import datetime, timedelta

   # Your GitHub App's private key (replace with your multi-line string private key)
   PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
   SHA256:w16NaUYnv/SCcOj84/CnlRkGtXX1vSSJVFGPvNwtHGI=
   -----END RSA PRIVATE KEY-----"""

   # App ID and installation ID (replace with your actual app ID and installation ID)
   APP_ID = '1863337'  # Your App ID
   INSTALLATION_ID = 'Iv23likhz0wIOms1YAt7'  # Replace with your actual Installation ID

   def generate_jwt():
       """Generate a JWT for GitHub App authentication."""
       payload = {
           'iat': datetime.utcnow(),
           'exp': datetime.utcnow() + timedelta(minutes=10),
           'iss': APP_ID
       }
       return jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')

   def get_installation_token():
       """Exchange JWT for an installation token."""
       jwt_token = generate_jwt()
       headers = {
           'Authorization': f'Bearer {jwt_token}',
           'Accept': 'application/vnd.github.v3+json'
       }

       # Get installation token
       url = f'https://api.github.com/app/installations/{INSTALLATION_ID}/access_tokens'                        
       response = requests.post(url, headers=headers)

       if response.status_code == 201:                                                                                     return response.json()['token']
       else:
           raise Exception(f"Failed to get installation token: {response.content}")
   # Get and print the installation token
   installation_token = get_installation_token()
   print(f"Installation Token: {installation_token}"
