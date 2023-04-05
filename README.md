# oidc-python-client

Example OIDC RP using https://github.com/zamzterz/Flask-pyoidc

## Testing

Create a settings.cfg, for example:

```bash
# For Flask App
SECRET_KEY='secret123'
DEBUG='True'

# OIDC specific settings
OIDC_REDIRECT_URI='http://localhost:5000/redirect_uri'
OIDC_ISSUER='https://localhost:8443/cas/oidc'
OIDC_CLIENT_ID='client'
OIDC_CLIENT_SECRET='secret'
OIDC_SCOPES=['openid', 'profile', 'berkeley_edu_default']
```

No easy way to bypass cert checking if we are authenticating against
an OIDC OP with a self-signed cert.  When using a mkcert CA we can
export the CA to an ENV var that the Python requests library will check:

```bash
CERT_PATH=$(mkcert -CAROOT)/rootCA.pem
export SSL_CERT_FILE=${CERT_PATH}
export REQUESTS_CA_BUNDLE=${CERT_PATH}
```

## Notes

- CAS as an OIDC-OP will try to HTTP encode any data coming in from the client including the clientID.  So characters like '@' will cause an authentication failure unless encoded in the CAS service registration