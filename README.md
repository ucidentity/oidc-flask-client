# oidc-flask-client

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
# At minimum the 'openid' scope must be included
OIDC_SCOPES=['openid', 'profile', 'berkeley_edu_default']
```

No easy way to bypass cert checking if we are authenticating against
an OIDC OP with a self-signed cert.  When using a mkcert CA we can
export the CA to an ENV var that the Python requests library will check:

```bash
CERT_PATH=$(mkcert -CAROOT)/rootCA.pem && export SSL_CERT_FILE=${CERT_PATH} && export REQUESTS_CA_BUNDLE=${CERT_PATH}
```

Local testing in a container

```bash
docker build --tag oidc-flask-client .
export CERT_PATH=$(mkcert -CAROOT)/rootCA.pem
docker run --rm -it -p 5000:5000 --name oidc-client --network cas-test -e SSL_CERT_FILE=/rootCA.pem -e REQUESTS_CA_BUNDLE=/rootCA.pem --volume ${PWD}/settings.cfg:/settings.cfg --volume $CERT_PATH:/rootCA.pem oidc-flask-client
```

or

```bash
export CERT_PATH=$(mkcert -CAROOT)/rootCA.pem
docker compose --env-file /dev/null up
```

## Notes

- CAS as an OIDC-OP will try to HTTP encode any data coming in from the client including the clientID.  So characters like '@' will cause an authentication failure unless encoded in the CAS service registration