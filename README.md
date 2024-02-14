# fastapi-saml

Example FastAPI backend that implements SAML2 authentication.

## Preconditions

Before running the FastAPI startup command locally, you need to create `key.pem` and `cert.pem` files for local HTTPS setup. Follow the steps below:

1. Open your terminal.

2. Run the following command to generate a private key (`key.pem`) and a self-signed certificate (`cert.pem`):

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
```

This command will prompt you to enter a passphrase and some information for the certificate. If you want to avoid entering a passphrase on every restart, you can add `-nodes`:

```bash
openssl req -x509 -nodes -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
```

3. After running this command, `key.pem` and `cert.pem` files will be created in your current directory.

4. Now, you can run your FastAPI application with HTTPS locally.

Please ensure these files are kept secure, and remember to include `key.pem` and `cert.pem` in your `.gitignore` file to prevent them from being committed to your repository.

## Run

To start the service locally you should execute the command:

```bash
uvicorn src.main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem --host=0.0.0.0 --port=8000 --reload
```

You could also use the `local_starter.sh` file:

```bash
source local_starter.sh
```