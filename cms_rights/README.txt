Open ERP System :- Odoo 9 Community

Installation 
============
Install the Application => Apps -> CMS Rights(Technical Name:cms_rights)

Module Configration Guideline
=============================
	1. Create Users and give rights of Webshop-Manager and Marketing-Manager to access website:
	   Settings -> Users -> Users -> Website

	2. Configure outgoing mail server to send email-notification on proposal and approval:
	   Settings -> General Settings -> Configure outgoing email servers

Roles
=====
1. Webshop-Manager(WM)

	=> WMs have access to edit all pages available in the website with full rights
	=> WM receives approval requests of content-change proposals and page creation proposal by Marketing-Managers
	=> WM can preview the request before approving it
	=> WMs are able to approve or reject a proposal
	=> WM can save templates from 'Content->Save as Template'
	=> WM can create new page by using saved templates of all users(WMs and MMs)
	=> Until approval, proposed changes remain unpublished​
	=> WM can re-set the main page template by discarding all content changes after MM requests
	=> WM will get notify by email on proposal request
	=> WM can redirect page url from 'Website Admin->SEO Redirections'

2. Marketing-Manager(MM)
 
 	=> MMs have limited access to font-properties and snippet functionalities
 	=> MMs can access a limited set of snippets
 	=> MMs can use pictures that have already been uploaded to the system
	=> MM can save or propose content changes to pages
	=> MM can save templates from 'Content->Save as Template'
	=> MM can create new page request from 'Content->New Page Templates'
	=> MM will get notify by email on approval by WM
	=> MMs have access to their own proposal-requests from backend(Website Admin menu)
