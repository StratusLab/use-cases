
Registration
============

Authentication and Authorization
================================

Common Proxy Service
  * All authentication is done through common service
  * Relies on JAAS implementation in Jetty web service container
  * Flexible mechanism that takes advantage of existing software

Authentication Mechanisms
  * Username/password (password file or LDAP)
  * Grid certificates and VOMS proxies (DN file or LDAP)
  * Shibboleth, SLCS, etc. are currently being worked on

Authorization
  * Done by individual cloud services and rights may differ between them
  * Policies based on groups and roles will be available soon

Home
====

NOTE: Add screenshot and address of the registration link. 


Policies
========

NOTE: Screenshot for policy page.

Statement of policies and guarantees.

Register
========

What information needs to be supplied.  How to extract the DN in the
RFC2252 format?

NOTE: Add screenshot.

Profile
=======

Show what a user profile looks like.  

NOTE: Add screenshot. 

Exercises
=========

Register with StratusLab
------------------------

Navigate to Registration Service
  * https://register.stratuslab.eu:8444/
  * Click through warnings about self-signed certificate

Provide information
  * Read policies
  * Complete registration form
  * Be sure to use a valid email address (it will be verified) 

Wait for approval 

