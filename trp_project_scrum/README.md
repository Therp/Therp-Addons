trp_project_scrum
=================


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


Option 2:

The Collaborator group is based on all the members of a project , if we prefer
to give access to all the project one is following in the same way there is
also the collaborator_follower group.

A user that belongs to collaborator_follower will have read access to:

- Projects
- Sprints
- Stories
- Tests
- Meetings

he is following. and read/write access to:

- tasks assigned to him

Both groups can read and create attachments.
