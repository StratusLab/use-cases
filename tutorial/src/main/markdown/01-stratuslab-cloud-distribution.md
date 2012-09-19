
StratusLab History
==================

Collaboration, EU-funded project, collaboration, etc. 

Project Principles
==================

Grid and cloud technologies are complementary
  * Uniform security model (grid)
  * Sharing of resources, algorithms, and expertise (grid)
  * Dynamic allocation of resources (cloud)
  * Customized environments (cloud) 

Only develop new software when necessary
  * Integrate existing solutions if possible
  * Practical development -> real needs of users

Maintain production quality with rapid evolution
  * Use agile and scrum methodologies
  * Iterative integration: always maintain working distribution
  * Public releases approximately every 6 weeks

Infrastructure as a Service (IaaS)
==================================

NOTE: Reiterate the goal, advantage, and disadvantages of IaaS service
model.

StratusLab Architecture
=======================

NOTE: Provide the updated architecuture diagram.  Emphasize the
features that are unique for StratusLab. 

Compute Services
================

OpenNebula (opennebula.org)
  * Provides core of virtual machine management (start, stop, kill)
  * Plug-in architecture allows use of multiple hypervisors (kvm, …)

Enhancements
  * Quarantine of stopped images for forensic analysis
  * Improved logging of user and resource information
  * Ability to pass error messages from plug-ins to user
  * Improved fault tolerance
  * Improved management of network addresses
  * Support for users, groups, and roles (post-1.0)

Storage Services
================

Persistent (Read-Write) Disks
  * Allows the storage of service state or user data
  * Mounted as a disk on VMs
  * Disks are persistent and have a lifecycle independent of a single VM
  * Can be mounted by single VM at any time
  * Only available within a single cloud instance

Static (Read-Only) Disks
  * Useful for distribution of quasi-static databases
  * Handled and shared like VM images via Marketplace

Volatile (Read-Write) Disks
  * Useful for temporary (!) data storage
  * Data will disappear when VM instance is destroyed

Other Storage Types
===================

File-based Storage
  * Normal client tools can be installed in VMs
  * Access services normally from VM (e.g. tools for SRM)
  * Unlikely to be implemented by StratusLab, although will provide
  CDMI interface to persistent storage service 

Object Storage
  * Simple object storage, usually minimal hierarchy and chunked data
  * Won’t implement this in StratusLab, could take implementations
  from elsewhere, e.g. OpenStack

Key-value Pair Database
  * Exposes simple API for “database” of key-value pairs
  (e.g. Cassandra)
  * Can deploy VM with persistent disk to provide this service

Networking Services
===================

IP Address Classes & Selection
  * Public: Internet-accessible services
  * Local: Batch systems or parallel calculations
  * Private: Slaves in pilot job systems

Future Services
  * IP address reservation
  * User specified firewalls
  * Dynamic VLANs
  * IPv6 use/validation

Marketplace
===========

Machine image creation is a barrier to cloud adoption
  * Creating virtual machine images is time-consuming 
  * Ensuring that machines are secure and correct is difficult
  * Sharing existing machines lowers this barrier

Marketplace facilitates sharing of images
  * Registry of metadata for machine & disk images
  * Image contents are kept in cloud, grid, or web storage
  * Supports trust between creators, users, and administrators

Benefits
  * End-users: browse and use existing images for their analyses
  * Creators: publicize their work and attract larger user base
  * Cloud Admins.: Use metadata to evaluate trustworthiness of images

Other Services
==============

Authn/Authz
  * Authentication done through common proxy service
  * Allows username/password from LDAP or from file
  * Allows use of grid certificates and VOMS proxies
  * Authorization done in individual services
  * Delegation currently not needed/used (will change if machine or
  disk images are protected)

Other Services
==============

Registration Service
  * Web service for user registration
  * LDAP DB for easy integration with cloud and other services

Accounting/Monitoring
  * Ganglia for monitoring of physical and virtual infrastructure
  * Simple scripts to extract accounting information for reports
  * No publication of the information for the moment


Accessing Services
==================

StratusLab Client
  * Command line scripts in python/java with few dependencies
  * Works on Mac OSX, Linux, and Windows

Programming Interfaces
  * Most services provide REST interfaces
  * Easy to program from any language
  * Straightforward resource <-> URL mapping
  * Standard interfaces will be implemented (OCCI, CMDI, …)

Libraries
  * None currently provided
  * jclouds (java, clojure) will be implemented shortly

Appliances
==========

Appliances
  * Provide pre-configured, pre-installed software and services
  * Makes it easier to get started quickly using cloud resources
  * Can make and publish your own appliances

StratusLab-Provided Appliances
  * Base images: ttylinux, CentOS 5.5, Ubuntu 10.04, OpenSuSE (soon)
  * Grid: CE, SE, WN, APEL/BDII, UI
  * Bioinformatics: Data server and analysis images


Grid and Cloud Together
=======================

NOTE: Add diagram about grid and cloud layering.  Just drop this whole
section? 

Architecture & Roadmap
======================

NOTE: Add diagram of the overall architecture again and a road map of
where the developments are going. 

Federative Services
===================

Hybrid and sky computing.  

NOTE: Add diagram of the hybrid cloud methods.  Provide aspects of
StratusLab that allows federation (mainly authentication and
Marketplace). 


