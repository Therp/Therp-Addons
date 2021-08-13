# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "External users",
    "summary": "Allow external users on your system",
    "version": "13.0.1.0.0",
    "author": "Therp BV, Sunflower IT",
    "category": "External users",
    "website": "https://therp.nl",
    "depends": ["base", "portal"],
    "demo": ["demo/res_users.xml"],
    "data": [
        "data/ir_module_category.xml",
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "views/res_users.xml",
    ],
    "license": "AGPL-3",
}
