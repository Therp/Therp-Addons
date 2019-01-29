# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from random import random
from odoo.tests.common import SingleTransactionCase
from odoo.exceptions import AccessError
from odoo import fields


class TestProjectScrum(SingleTransactionCase):

    post_install = True
    at_install = False

    def setUp(self):
        super(TestProjectScrum, self).setUp()
        self.external_scrum_user = self.env.ref(
            'trp_project_scrum.external_scrum_user')
        self.collaborator_follower = self.env.ref(
            'trp_project_scrum.collaborator_follower')
        self.scrumproject_alpha = self.env.ref(
            'trp_project_scrum.scrum_project_alpha')
        self.scrumproject_beta = self.env.ref(
            'trp_project_scrum.scrum_project_beta')
        self.scrumproject_gamma = self.env.ref(
            'trp_project_scrum.scrum_project_gamma')
        self.not_scrum_project = self.env.ref(
            'trp_project_scrum.not_scrum_project')
        self.task1 = self.env.ref(
            'trp_project_scrum.alpha_1')
        self.task2 = self.env.ref(
            'trp_project_scrum.alpha_2')
        self.task3 = self.env.ref(
            'trp_project_scrum.beta_1')
        self.task4 = self.env.ref(
            'trp_project_scrum.beta_2')
        self.task5 = self.env.ref(
            'trp_project_scrum.not_scrum_1')

    def test_project_scrum_permissions(self):
        all_projects = \
            self.scrumproject_alpha + \
            self.scrumproject_beta + \
            self.scrumproject_gamma + \
            self.not_scrum_project
        all_tasks = \
            self.task1 + \
            self.task2 + \
            self.task3 + \
            self.task4 + \
            self.task5
        #  check if other groups are assigned
        self.assertEqual(self.collaborator_follower.has_group(
            'trp_external_user.group_external_user'
            ),
            True,
            'Group External User was not triggered after assigning'
            ' collaborator group'
        )
        self.assertEqual(self.collaborator_follower.has_group(
            'trp_project_scrum.collaborators_followers'),
            True,
            'Collaborator follower group was not triggered after assigning'
        )
        self.scrumproject_alpha.message_subscribe_users(
            self.external_scrum_user.ids +
            self.collaborator_follower.ids,
        )
        # verify it cannot see any element of other projects
        projects = self.env['project.project'].sudo(
            self.collaborator_follower.id
        ).search([('id', 'in', all_projects.ids)])
        # should see only 1 project
        self.assertEqual(
            len(projects), 1,
            'a collaborator follower sees too many projects'
        )
        # verify admin can see all still all
        projects2 = self.env['project.project'].sudo().search(
            [('id', 'in', [x.id for x in all_projects])]
        )
        # should see all  projects we made
        self.assertEqual(
            len(projects2), 4, 'admin does not see all prgs'
        )
        # verify user cannot modify projects or scrum elements he can see
        # collaborator can see no tasks:
        tasks = self.env['project.task'].sudo(
            self.collaborator_follower.id
            ).search([('id', 'in', [x.id for x in all_tasks])])

        # should see only the task of the project
        self.assertEqual(
            len(tasks), 2,
            'Collaborator can see some tasks when should see none'
        )

        # verify that he can modify tasks of his project
        self.assertEqual(
            self.task2.sudo(
                self.collaborator_follower.id
            ).with_context(mail_notrack=True).write({'name': 'this is ok'}),
            True,
            'Collaborator could not write on a task where has permissions'
        )
        self.assertRaises(
            AccessError,
            self.task5.sudo(
                self.collaborator_follower.id
            ).with_context(mail_notrack=True).write, {'name': 'this is not ok'}
        )
        # try deleting a project as both users
        self.assertRaises(
            AccessError,
            self.scrumproject_gamma.sudo(self.external_scrum_user.id).unlink
        )
        self.assertRaises(
            AccessError,
            self.scrumproject_gamma.sudo(self.collaborator_follower.id).unlink
        )
        # try create/write/delete on project_scrum_meeting
        vals_scrum_meeting = {
            'project_id': self.scrumproject_alpha.id,
            'datetime_meeting': fields.Datetime.now(),
            'user_id_meeting': None,
            'question_yesterday': 'test',
            'question_today': 'test',
            'question_blocks': 'test',
            'question_backlog': 'no',
            }
        with self.assertRaises(AccessError):
            self.do_operation(
                self.external_scrum_user.id,
                'project.scrum.meeting',
                'create',
                vals_scrum_meeting,
            )
        with self.assertRaises(AccessError):
            self.do_operation(
                self.collaborator_follower.id,
                'project.scrum.meeting',
                'create',
                vals_scrum_meeting,
            )
        with self.assertRaises(AccessError):
            self.do_operation(
                self.external_scrum_user.id,
                'project.scrum.meeting',
                'write',
                vals_scrum_meeting,
            )
        with self.assertRaises(AccessError):
            self.do_operation(
                self.collaborator_follower.id,
                'project.scrum.meeting',
                'write',
                vals_scrum_meeting,
            )
        with self.assertRaises(AccessError):
            self.do_operation(
                self.external_scrum_user.id,
                'project.scrum.meeting',
                'unlink',
                vals_scrum_meeting,
            )
        with self.assertRaises(AccessError):
            self.do_operation(
                self.collaborator_follower.id,
                'project.scrum.meeting',
                'unlink',
                vals_scrum_meeting,
            )
        # try create/write/delete on project_scrum_sprint
        vals_scrum_sprint = {
            'name': 'test',
            'project_id': self.scrumproject_alpha.id,
            'product_owner_id': None,
            'scrum_master_id': None,
            'state': 'draft',
            }
        with self.assertRaises(AccessError):
            self.do_operation(
                self.external_scrum_user.id,
                'project.scrum.sprint',
                'create',
                vals_scrum_sprint,
            )
        with self.assertRaises(AccessError):
            self.do_operation(
                self.collaborator_follower.id,
                'project.scrum.sprint',
                'create',
                vals_scrum_sprint,
            )
        with self.assertRaises(AccessError):
            self.do_operation(
                self.external_scrum_user.id,
                'project.scrum.sprint',
                'write',
                vals_scrum_sprint,
            )
        with self.assertRaises(AccessError):
            self.do_operation(
                self.collaborator_follower.id,
                'project.scrum.sprint',
                'write',
                vals_scrum_sprint,
            )
        with self.assertRaises(AccessError):
            self.do_operation(
                self.external_scrum_user.id,
                'project.scrum.sprint',
                'unlink',
                vals_scrum_sprint,
            )
        with self.assertRaises(AccessError):
            self.do_operation(
                self.collaborator_follower.id,
                'project.scrum.sprint',
                'unlink',
                vals_scrum_sprint,
            )
        # try create/write/delete on project_scrum_test
        vals_scrum_test = {
            'name': 'name',
            'project_id': self.scrumproject_alpha.id,
        }
        self.do_operation(
            self.external_scrum_user.id,
            'project.scrum.test',
            'create',
            vals_scrum_test,
        )
        self.do_operation(
            self.collaborator_follower.id,
            'project.scrum.test',
            'create',
            vals_scrum_test,
        )
        self.do_operation(
            self.external_scrum_user.id,
            'project.scrum.test',
            'write',
            vals_scrum_test,
        )
        self.do_operation(
            self.collaborator_follower.id,
            'project.scrum.test',
            'write',
            vals_scrum_test,
        )
        with self.assertRaises(AccessError):
            self.do_operation(
                self.external_scrum_user.id,
                'project.scrum.test',
                'unlink',
                vals_scrum_test,
            )
        with self.assertRaises(AccessError):
            self.do_operation(
                self.collaborator_follower.id,
                'project.scrum.test',
                'unlink',
                vals_scrum_test,
            )
        vals_scrum_us = {
            'name': 'name',
            'project_id': self.scrumproject_alpha.id,
        }
        # try create/write/delete on project_scrum_us
        self.do_operation(
            self.external_scrum_user.id,
            'project.scrum.us',
            'create',
            vals_scrum_us,
        )
        self.do_operation(
            self.collaborator_follower.id,
            'project.scrum.us',
            'create',
            vals_scrum_us,
        )
        self.do_operation(
            self.external_scrum_user.id,
            'project.scrum.us',
            'write',
            vals_scrum_us,
        )
        self.do_operation(
            self.collaborator_follower.id,
            'project.scrum.us',
            'write',
            vals_scrum_us,
        )
        with self.assertRaises(AccessError):
            self.do_operation(
                self.external_scrum_user.id,
                'project.scrum.us',
                'unlink',
                vals_scrum_us,
            )
        with self.assertRaises(AccessError):
            self.do_operation(
                self.collaborator_follower.id,
                'project.scrum.us',
                'unlink',
                vals_scrum_us,
            )
        vals_project_task = {
            'name': 'name',
            'kanban_state': 'normal',
            'project_id': self.scrumproject_alpha.id,
        }
        # try create/write/delete on project_task
        task = self.do_operation(
            self.external_scrum_user.id,
            'project.task',
            'create',
            vals_project_task,
        )
        self.do_operation(
            self.collaborator_follower.id,
            'project.task',
            'create',
            vals_project_task,
        )
        self.do_operation(
            self.external_scrum_user.id,
            'project.task',
            'write',
            vals_project_task,
        )
        self.do_operation(
            self.collaborator_follower.id,
            'project.task',
            'write',
            vals_project_task,
        )
        with self.assertRaises(AccessError):
            self.do_operation(
                self.external_scrum_user.id,
                'project.task',
                'unlink',
                vals_project_task,
            )
        with self.assertRaises(AccessError):
            self.do_operation(
                self.collaborator_follower.id,
                'project.task',
                'unlink',
                vals_project_task,
            )
        # try create/write/delete on account.analytic.line
        vals_timesheet = {
            'date': fields.Date.today(),
            'user_id': None,
            'name': 'test',
            'project_id': self.scrumproject_alpha.id,
            'task_id': task.id,
        }
        with self.assertRaises(AccessError):
            self.do_operation(
                self.external_scrum_user.id,
                'account.analytic.line',
                'create',
                vals_timesheet,
            )
        self.do_operation(
            self.collaborator_follower.id,
            'account.analytic.line',
            'create',
            vals_timesheet,
        )
        with self.assertRaises(AccessError):
            self.do_operation(
                self.external_scrum_user.id,
                'account.analytic.line',
                'write',
                vals_timesheet,
            )
        res = self.do_operation(
            self.collaborator_follower.id,
            'account.analytic.line',
            'write',
            vals_timesheet,
        )
        self.assertEquals(res.date, vals_timesheet['date'])
        self.assertEquals(res.user_id.id, self.collaborator_follower.id)
        self.assertEquals(res.name, vals_timesheet['name'])
        self.assertEquals(res.project_id.id, vals_timesheet['project_id'])
        self.assertEquals(res.task_id.id, vals_timesheet['task_id'])
        with self.assertRaises(AccessError):
            self.do_operation(
                self.external_scrum_user.id,
                'account.analytic.line',
                'unlink',
                vals_timesheet,
            )
        with self.assertRaises(AccessError):
            self.do_operation(
                self.collaborator_follower.id,
                'account.analytic.line',
                'unlink',
                vals_timesheet,
            )

    def do_operation(self, user_id, model, operation, vals):
        model = self.env[model].sudo(user_id).with_context(
            mail_create_nosubscribe=True)
        # keep a rec in hand for write/unlink
        if 'product_owner_id' in vals:
            vals['product_owner_id'] = user_id
        if 'user_id_meeting' in vals:
            vals['user_id_meeting'] = user_id
        if 'scrum_master_id' in vals:
            vals['scrum_master_id'] = user_id
        if 'user_id' in vals:
            vals['user_id'] = user_id
        if model._name == 'project.task':
            vals['name'] = random()
            vals['code'] = random()
        # on write/read/unlink you need to have a record to work with
        rec = model.create(vals)
        if operation == 'read':
            rec.read(vals.keys())
        elif operation == 'write':
            rec.write(vals)
        elif operation == 'unlink':
            rec.unlink()
        return rec
