# Njal.la Python

![Njal.la Logo](njalla.svg)

## Description

This Python library provides a convenient interface for interacting with the Njal.la API, allowing users to seamlessly integrate Njal.la services into their Python applications.

## Installation

To install the library, use the following command:

```
pip install Njalla
```

## Usage

```python
from Njalla import Njalla

# Initialize the Njal.la client
client = Njalla(api_key="your_api_key")
```

## API Key

To use the library, you need to obtain an API key from Njal.la.
You can sign up for an account on [Njal.la website](https://njal.la/) and generate an API key in your account settings.

## Pronunciation

The library is named after "/ˈɲalla/" (Sami),
which refers to a small hut in the Sápmi forest, built to protect against predators.
This concept aligns with Njal.la's commitment to providing a secure and protective environment for online activities.

## License

This library is licensed under the `CC BY-NC-SA 4.0` License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions!
If you find any issues or have suggestions for improvement,
please open an [issue](https://github.com/DevCa-IO/Njalla/issues)
or submit a [pull request](https://github.com/DevCa-IO/Njalla/pulls).


## Classes

Njalla provides six different API classes.
You can use these simply by adding the class name on top of your Instance.\
Those are:
- API
- Domain
- Server
- User (used for Cookie Authentication, deprecated and not suggested to use by Njalla)
- VPN
- Wallet


```python
from Njalla import Njalla

# Initialize the Njal.la client
client = Njalla("your_api_key")

# API

print(client.API.add_token("comment", "from", "allowed_domains", "allowed_servers", "allowed_methods", "allowed_types", "acme")

# Domain

print(client.Domain.register_domain("domain", "years"))

# Server

print(client.Server.add_traffic("id", "amount", "months",  "starts_today"))

# User

print(client.User.logout())

# VPN

print(client.VPN.add_vpn("name", "autorenew"))

# Wallet

print(client.Wallet.get_balance())
```

All the methods are also available in our (not yet existing) ReadTheDocs Documentation.\