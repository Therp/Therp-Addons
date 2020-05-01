"""Make sure no unwanted mail leaves the server."""
# Copyright 2015-2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from email.utils import COMMASPACE

from odoo import api, models
from odoo.addons.base.models.ir_mail_server import extract_rfc2822_addresses


ADDRESS_REPLACEMENTS = str.maketrans(
    {
        "\\": "",  # Remove backslash
        '"': '\\"',  # escape double quote
        "<": "[",  # open actual address part
        ">": "]",  # close actual address part
        "@": "(at)",
    }
)


class IrMailServer(models.Model):
    """Make sure no unwanted mail leaves the server."""
    _inherit = 'ir.mail_server'

    @api.model
    def send_email(self, message, *args, **kwargs):
        """Override email recipients if requested, then send mail.

        Or throw Exception when no valid recipients.
        """
        self.patch_message(message)
        return super().send_email(message, *args, **kwargs)

    @api.model
    def patch_message(self, message):
        """Override message recipients.

        Result is dependent on what is specified in the configuration:
        1. Message is not changed (no configuration or 'disabled');
        2. Message recipients are replaced;
        3. There is no valid recipient in the override configuration.

        If there is no valid recipient, an Exception will be thrown. This
        will be an AssertionException, in line with what is done by standard
        Odoo. Most likely this message will be catched and an appropiate
        reason for non delivery registered.
        """
        override_email_to = self.env.ref(
            'override_mail_recipients.override_email_to',
            raise_if_not_found=False)
        override = override_email_to.value if override_email_to else 'disable'
        domain_whitelist = self.env.ref(
            'override_mail_recipients.domain_whitelist',
            raise_if_not_found=False)
        whitelisted_domains = [
            '@' + domain for domain in domain_whitelist.value.split(',')
            if '.' in domain] if domain_whitelist else []
        if override == 'disable' and not whitelisted_domains:
            return
        override_recipients = \
            extract_rfc2822_addresses(override) \
            if override != 'disable' else []
        assert override_recipients or whitelisted_domains, \
            'No valid override_email_to'
        any_mail = False
        for field in ['to', 'cc', 'bcc']:
            if not message[field]:
                continue
            any_mail = self._patch_field(
                message, field, override_recipients, whitelisted_domains
            ) or any_mail
        assert any_mail, 'Attempt to send mail outside of allowed domain'

    def _patch_field(
            self, message, field, override_recipients, whitelisted_domains):
        """Patch where needed email recipients.

        - if in whitelisted or defined recipient: do not touch;
        - if no override recipients and not whitelisted: ignore;
        - if override recipients and not whitelisted, add textual
          representation of email address to address of actual recipients.

        return True if any address used, else False.
        """
        def check_recipient(recipient, valid_strings):
            """Check wether domain, or email address in recipient."""
            for test_string in valid_strings:
                if test_string in recipient:
                    return True
            return False

        actual_recipients = []
        replaced_recipients = []
        original_recipients = message.get_all(field, [])
        for recipient in original_recipients:
            in_override = check_recipient(recipient, override_recipients)
            whitelisted = not in_override and check_recipient(
                recipient, whitelisted_domains)
            if whitelisted:
                actual_recipients.append(recipient)
            if not whitelisted and not in_override:
                replaced_recipients.append(self._do_replacement(recipient))
        actual_recipients += override_recipients
        if not actual_recipients:
            del message[field]
            return False
        if not replaced_recipients:
            # Message field can be used unchanged.
            return True
        # Add information on replaced recipients to actual recipients.
        del message[field]
        replaced_string = COMMASPACE.join(replaced_recipients)
        message[field] = COMMASPACE.join(
            '"%s" <%s>' % (replaced_string, email)
            for email in actual_recipients)
        return True

    def _do_replacement(self, recipient):
        """Make recipient address into a simple string."""
        # pylint: disable=no-self-use
        return recipient.translate(ADDRESS_REPLACEMENTS)
