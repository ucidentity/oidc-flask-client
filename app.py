import flask
import logging
from flask import Flask, jsonify

from flask_pyoidc import OIDCAuthentication
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata
from flask_pyoidc.user_session import UserSession

import toml


app = Flask(__name__)
# See https://flask.palletsprojects.com/en/2.0.x/config/
app.config.from_file(filename='settings.cfg',load=toml.load)

# We support the authorization_code grant_type and code response_type
client_metadata = ClientMetadata(client_id=app.config['OIDC_CLIENT_ID'], 
                                 client_secret=app.config['OIDC_CLIENT_SECRET'],
                                 response_types=['code'],
                                 grant_types=['authorization_code']
                                 )
provider_name = 'calnet'
# If issuer supports auto-discovery (CAS does) we just need to 
# supply the base OIDC URL
issuer = app.config['OIDC_ISSUER']
auth_params = {'scope': app.config['OIDC_SCOPES']}
provider_config = ProviderConfiguration(issuer=issuer,
                                        auth_request_params=auth_params,
                                        client_metadata=client_metadata)

auth = OIDCAuthentication({provider_name: provider_config})

@app.route('/')
@auth.oidc_auth(provider_name)
def login():
    user_session = UserSession(flask.session)
    # userinfo will contain the attributes payload (if any)
    # including claims from scopes requested in auth_params
    return jsonify(access_token=user_session.access_token,
                   id_token=user_session.id_token,
                   userinfo=user_session.userinfo)

@app.route('/logout')
@auth.oidc_logout
def logout():
    return "You've been successfully logged out!"

@auth.error_view
def error(error=None, error_description=None):
    return jsonify({'error': error, 'message': error_description})

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    auth.init_app(app)
    app.run()
else:
    auth.init_app(app)