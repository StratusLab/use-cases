Client Installation
===================

Tutorial Infrastructure
=======================

Reference Cloud Infrastructure
  * Allow users to test a StratusLab cloud without having to install one
  * Your accounts from the Registration Service will work there soon...
  * Problems, ask questions via support@stratuslab.eu 

In this tutorial we will be using:
  * Registration: https://register.stratuslab.eu:8444/ 
  * Endpoint: cloud.lal.stratuslab.eu
  * Persistent Disk Endpoint: pdisk.lal.stratuslab.eu
  * Public Marketplace: http://marketplace.stratuslab.eu/ 
  * Test Marketplace: http://cloud.lal.stratuslab.eu:8081/  
  * Account (username/password) you created when registering

Prerequisites
=============

Client allows remote access and control of VMs in cloud.

Client has minimal prerequisites:
  * Python 2.6+ (but not Python 3.x)
  * Java 1.6+ (for metadata signatures/validation)
  * SSH client with user keypair
  * Certificate (grid is OK) for signing image metadata entries

Support for multiple platforms:
  * Fedora 14 (tarball and RPM package)
  * Other linux systems (tarball)
  * Mac OSX (tarball)
  * Windows (tarball) – version 1.9 is buggy, corrected in next release 

Tarball Download
================

Install client via OS-independent tarball/zip:
  * Create the directory: $HOME/stratuslab
  * “Get Started” button on http://stratuslab.eu/, use version 1.9
  * Download the tarball/zip (stratuslab-cli-user-zip-*.{tar.gz|zip})
  * Extract files from archive: tar zxf mytarball $HOME/stratuslab

Adjust for other OSes/packages/shells as necessary.


Configure Environment
=====================

Configure path variables:
  * Define: PATH=$HOME/stratuslab/bin:$PATH
  * Define: PYTHONPATH=$HOME/stratuslab/lib/stratuslab/python/
  * Test: stratus-run-instance –help

Ensure that you have an SSH keypair:
  * Look in $HOME/.ssh/ for id_rsa, id_rsa.pub files (or similar)
  * Use ssh-keygen to create keys if necessary (remember password!)


StratusLab Client Configuration
===============================

Multiple ways to provide parameter values
  * Configuration file: ~/.stratuslab/stratuslab-user.cfg
  * Environmental variables: STRATUSLAB_*
  * Command line options: --endpoint=XXX

Client configuration file:
  * Create: $HOME/.stratuslab
  * Copy: $HOME/stratuslab/conf/stratuslab-user.cfg.ref  to
    $HOME/.stratuslab/stratuslab-user.cfg
  * Verify: filename name ends with *.cfg and NOT *.ref!
  * Provide values: endpoint, username, password, key
    - Change ‘key =‘ to ‘user_public_key_file =‘ for public ssh key!
    - Default value is $HOME/.ssh/id_rsa.pub

Test Client Configuration
=========================

Run a command to list your VMs on the infrastructure.
Run: stratus-describe-instance
If working:

~~~bash
$ stratus-describe-instance
id  state     vcpu memory    cpu% ip              name
~~~

If not working, ask a StratusLab person for help!


Exercises
=========

Explore CLI Options
-------------------

All commands:
  * Start with stratus-*
  * Support the --help option

Explore the commands and look at options
