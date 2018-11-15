# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import SingleTransactionCase
from odoo.exceptions import AccessError


class TestProjectScrum(SingleTransactionCase):

    post_install = True

    def setUp(self):
        super(TestProjectScrum, self).setUp()
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
