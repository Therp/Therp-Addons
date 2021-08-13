External users
==============

Define a group 'External Users' that only have access to selected partners,
usually their own organizations. These partners are indicated on the user's user
form. By default, this module only grants read access to these partners.

On a permission level, it seems necessary that the partners also need read access
to the database company partner, which this module also allows. Keep this in mind
when building functionality on top of this module that allows interaction with
the partner model. By means of precaution, this module does define separate
records for reading and writing so as to prevent modifications of the company
partner (even if global write access on partners are not granted to the external
users group in this module).

This module also disables the default assignment of the 'user' and 'partner manager'
groups to new users.
