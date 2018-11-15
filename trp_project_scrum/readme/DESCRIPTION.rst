Extra security for projects.

Depends on trp_external_user module.
Creates a new collaborator group for all those users who are collaborating
to Therp projects and sprints.
This module depends on project_scrum, the user will see:  sprints,
stories, tests, meetings that are connected to projects  he is a member of.

The "collaborators" will have only read access to all these models, except for
the tasks where they will have also write access.

A user that belongs to collaborator will have read access to:

- Projects
- Sprints
- Stories
- Tests
- Meetings

that are connected to a project he is "MEMBER" of

and read/write access to:

- tasks assigned to him


Group can read and create attachments.
