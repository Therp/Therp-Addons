# coding: utf-8
# Copyright (C) 2014 Therp BV (<http://therp.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Fetch mail into inbox (invoice specific)",
    "version": "8.0.1.0",
    "author": "Therp BV",
    "complexity": "normal",
    "description": """
Fetch emails from a mail server to attach to existing invoices. The emails are
kept in a dedicated inbox for a user to review the mails manually.

Usage
=====

Create a fetchmail configuration for the model "Fetchmail inbox for
invoices". The mails fetched from this server will be put into
Accounting / Suppliers / Fetchmail inbox for further processing.
    """,
    "category": "Accounting & Finance",
    "depends": [
        'account',
        'fetchmail_inbox',
    ],
    "data": [
        'view/mail_message.xml',
        'view/menu.xml',
        'security/ir.model.access.csv',
    ],
    "js": [
    ],
    "css": [
    ],
    "qweb": [
    ],
    "auto_install": False,
    "installable": True,
    "external_dependencies": {
        'python': [],
    },
}
