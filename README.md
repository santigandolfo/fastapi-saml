# fastapi-saml

Example FastAPI backend that implements SAML2 authentication.

## Setup

To set up the project, follow these steps:

1. Ensure you have `uv` installed. You can find the installation instructions on
   the [uv installation page](https://docs.astral.sh/uv/getting-started/installation/).

2. Install the project dependencies using `uv`:

    ```bash
    uv sync
    ```

3. Install `xmlsec1` on your macOS machine using Homebrew:

    ```bash
    brew install libxmlsec1
    ```

## Preconditions

Before running the FastAPI startup command locally, you need to create `key.pem` and `cert.pem`
files for local HTTPS setup. Follow the steps below:

1. Open your terminal.

2. Run the following command to generate a private key (`key.pem`) and a self-signed certificate (
   `cert.pem`):

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
```

This command will prompt you to enter a passphrase and some information for the certificate. If you
want to avoid entering a passphrase on every restart, you can add `-nodes`:

```bash
openssl req -x509 -nodes -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
```

3. After running this command, `key.pem` and `cert.pem` files will be created in your current
   directory.

4. Now, you can run your FastAPI application with HTTPS locally.

Please ensure these files are kept secure, and remember to include `key.pem` and `cert.pem` in your
`.gitignore` file to prevent them from being committed to your repository.

## Environment Setup

To set up your environment variables, copy the contents of the `.env.example` file to a new file
named `.env`. You can do this using the following command:

```bash
cp .env.example .env
```

Then, update the values in the `.env` file as needed for your setup.

## Run

To start the service locally you should execute the command:

```bash
uv run uvicorn src.main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem --host=0.0.0.0 --port=8000 --reload
```

You could also use the `local_starter.sh` file:

```bash
source local_starter.sh
```