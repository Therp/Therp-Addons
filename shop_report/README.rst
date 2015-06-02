Shop report
===========

Provide each shop within a company with its own logo.

A shop can be linked with a logo. This shop can be set both on sales orders
and invoices. And reports printed (sales order or customer invoice) will
use the shop logo, instead of the company logo.

For the moment, like in the original module, a shop will be linked to a
company record created for this purpose. The disadvantage is that companies
need to be created that are neither juridical entities, nor have their own
bookkeeping. I intend to update the module to use res.partner, instead of
res.company.

Also, for the moment, we just use the alternative logo. It would be logical
to also use the name and address of the "logo" company, to provide a
completely separate branding.

Further, it would be nice if the replacement of the normal company logo (and
other information) on reports could be completely automatic for objects linked
to a shop. As it is, we need to customize the reports.

You can use the shop logo in the header of your reports that use the standard
header by adding the following definition to the rml header of the main
company:

[[ (company.logo if not 'shop_id' in objects[0] else objects[0].shop_id.logo_company_id.logo) or removeParentNode('image') ]]

Or you can use this in your custom reports:
<image x="5.25cm" y="3.75cm" width="150.0" height="100.0"
    >[[ o.shop_id and o.shop_id.logo_company_id.logo or company.logo]]</image>

You could try to change all your qweb based reports by changing the
external_layout view (Settings==>User Interface==>Views):
(NOT TESTED YET)

<?xml version="1.0"?>
<t t-name="report.external_layout">
    <!-- Multicompany -->
    <t t-if="o and 'company_id' in o">
        <t t-set="company" t-value="o.company_id"/>
    </t>
    <t t-if="not o or not 'company_id' in o">
        <t t-set="company" t-value="res_company"/>
    </t>
     <t t-if="o and 'shop_id' in o">
          <t t-set="company" t-value="o.shop_id.logo_company_id"/>
     </t>

    <t t-call="report.external_layout_header"/>
    <t t-raw="0"/>
    <t t-call="report.external_layout_footer"/>
</t>

