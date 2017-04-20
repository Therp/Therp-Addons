# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests.common import TransactionCase
from openerp.exceptions import AccessError
import random
import string

class TestTrpProjectScrum(TransactionCase):
    def setUp(self):
        super(TestTrpProjectScrum, self).setUp()
        # will trigger implied IDS of other groups
        # let's make believe we are logged in by passing 'login' in data
        # create a random login just in case we get one that already exists
        login1 = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for _ in range(8))
        password1 = ''.join(random.choice(
                string.ascii_uppercase + string.digits
            ) for _ in range(8)
        )
        self.collaborator_follower = self.env['res.users'].create({
            'name' : 'collaborator_follower',
            'groups_id': [(
                4,
                self.env.ref('trp_project_scrum.collaborators_followers').id,
                0
            )],
            'login': login1,
            'password': password1
        })
        self.scrumproject_alpha = self.env['project.project'].with_context(
            mail_create_nolog=False).create(
            {
             'privacy_visibility': 'followers',
             'alias_name': 'aliasalpha',
             'name': 'alpha',
             'use_scrum': True,
             'state': 'open',
            }
        )
        self.scrumproject_beta = self.env['project.project'].create(
            {
             'privacy_visibility': 'followers',
             'alias_name': 'aliasbeta',
             'name': 'beta',
             'use_scrum': True,
             'state': 'open',
            }
        )
        self.scrumproject_gamma = self.env['project.project'].create(
            {
             'privacy_visibility': 'followers',
             'alias_name': 'aliasgamma',
             'name': 'gamma',
             'use_scrum': True,
             'state': 'open',
            }
        )
        self.not_scrum_project = self.env['project.project'].create(
            {
             'privacy_visibility': 'followers',
             'alias_name': 'alianotscrm',
             'name': 'noscrum',
             'use_scrum': True,
             'state': 'open',
            }
        )
        # Add tasks to projects
        self.task1 = self.env['project.task'].create({
           'name' : 'task_alpha_1',
           'project_id' : self.scrumproject_alpha.id
        })

        self.task2 = self.env['project.task'].create({
           'name' : 'task_alpha_2',
           'project_id' : self.scrumproject_alpha.id
        })
        self.task3 = self.env['project.task'].create({
           'name' : 'task_beta_1',
           'project_id' : self.scrumproject_beta.id
        })

        self.task4 = self.env['project.task'].create({
           'name' : 'task_beta_2',
           'project_id' : self.scrumproject_beta.id
        })
        self.task5 = self.env['project.task'].create({
           'name' : 'task_noscrum',
           'project_id' : self.not_scrum_project.id
        })


    def test_trp_project_scrum_permissions(self):
        all_projects = [
             self.scrumproject_alpha,
             self.scrumproject_beta,
             self.scrumproject_gamma,
             self.not_scrum_project
        ]
        all_tasks = [
            self.task1,
            self.task2,
            self.task3,
            self.task4,
            self.task5
        ]
        #check if other groups are assigned
        self.assertEqual(self.collaborator_follower.has_group(
            'trp_external_user.group_external_user'
        ), True,
        'Group External User was not triggered after assigning'
        ' collaborator group'
        )

        self.assertEqual(self.collaborator_follower.has_group(
            'trp_project_scrum.collaborators_followers')
        , True,
        'Collaborator follower group was not triggered after assigning'
        )
        self.scrumproject_alpha.write({
            'message_follower_ids' : [
                (6, 0, [self.collaborator_follower.partner_id.id])
            ]
        })
        # verify it cannot see any element of other projects
        projects = self.env['project.project'].sudo(
           self.collaborator_follower.id
        ).search([('id', 'in', [x.id for x in all_projects])])
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
        #collaborator can see no tasks:
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

