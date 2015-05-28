Shop report
===========

Provide each shop within a company with its own logo.

A shop can be linked with a logo. This shop can be set both on sales orders
and invoices. And reports printed (sales order or customer invoice) will
use the shop logo, instead of the company logo.

You can use the shop logo in the header of all your reports by adding the
following definition to the rml header of the main company:

[[ (company.logo if not 'shop_id' in objects[0] else objects[0].shop_id.logo_company_id.logo) or removeParentNode('image') ]]
