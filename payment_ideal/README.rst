.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

======================
iDeal payment acquirer
======================

This module allows you to use iDeal as a payment acquirer within Odoo.

============
Installation
============

For the installation to run flawlessly, you probably need a few extra
dependendies on your server:

======== ===================================================== ========
name     debian/ubuntu                                         windows
======== ===================================================== ========
xmlsec   sudo apt-get install python-pkgconfig libxmlsec1-dev  untested
         pip install xmlsec
======== ===================================================== ========

Then just install as usual.

=============
Configuration
=============

After installation, you will be prompted to fill in your merchant ID,
your certificates and the other values your bank provided. If you don't
have those at hand, this module is not for you.

In case you accidentally closed this wizard, go to Settings / Payments /
Payment Acquirers, create a new one and select `iDeal` in the Provider field.

================
Acknowledgements
================

* iDeal icons are (c) https://www.ideal.nl/ontvangen/logos-banners
* ideal.py adapted from https://github.com/thegreatnew/python-ideal
