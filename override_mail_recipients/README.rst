Override mail recipients
========================

This module allows you to override all outgoing messages' `to`, `cc`, and `bcc`
values for testing purposes.

After installation, set the config parameter
`override_mail_recipients.override_to` to the email address you want
to send the testmails to.

After installing this module the parameter will contain text, but not a valid
mail address. This will cause emails not to be send out at all.

If you fill in a valid email address, this address will receive all emails
send from the system.

To resume normal mail processing, set this parameter to 'disable'
(litterally).
