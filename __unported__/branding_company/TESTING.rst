Testing this module
===================

Testing this module with automated unittests is difficult, because what we
need to test is what we view on the screen or in a report.

At least the following use-cases should be tested:

1. It should be possible to select a branding company on a sales order;
2. An invoice created from a sales order should by default get the branding
   company from the sales order.
3. An invoice created from a delivery for a sales order, should by default
    take the branding company from the sales order.
4. It should be possible to select a branding company on an invoice, wether it
   already has a branding company from a sales order, or wether the invoice is
   created manually.

