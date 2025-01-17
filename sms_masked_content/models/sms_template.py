# Copyright 2024 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import api, models

mask_sentinel = object()


class MaskedString(str):
    unmasked_content = ""

    def __new__(cls, masked_content, unmasked_content):
        result = super().__new__(cls, masked_content)
        result.unmasked_content = unmasked_content
        return result


class SmsTemplate(models.Model):
    _inherit = "sms.template"

    @api.model
    def _render_template(
        self,
        template_src,
        model,
        res_ids,
        engine="inline_template",
        add_context=None,
        options=None,
        post_process=False,
    ):
        """
        Add masking function to context, attach unmasked version to result if masking was used
        """
        masking_used = False

        def mask_content(content, replacement="XXX"):
            nonlocal masking_used
            if self.env.context.get("sms_masked_content_unmask") == mask_sentinel:
                return content
            else:
                masking_used = True
                return replacement

        result = super()._render_template(
            template_src,
            model,
            res_ids,
            engine=engine,
            add_context=dict(add_context or {}, mask_content=mask_content),
            options=options,
            post_process=post_process,
        )

        if not masking_used:
            return result
        else:
            unmasked_result = self.with_context(
                sms_masked_content_unmask=mask_sentinel
            )._render_template(
                template_src,
                model,
                res_ids,
                engine=engine,
                add_context=dict(add_context or {}, mask_content=mask_content),
                options=options,
                post_process=post_process,
            )
            return {
                res_id: MaskedString(result[res_id], unmasked_result[res_id])
                for res_id in result
            }
