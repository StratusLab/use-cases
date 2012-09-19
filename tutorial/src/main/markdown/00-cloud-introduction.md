
Cloud Marketing
===============

"Cloud" is currently a very trendy term and used everywhere.
Unfortunately, there are many different definitions that are often
imcompatible.  Moreover, it is often used to market pre-existing
(non-cloud) software further muddying the waters.  However, there are
interesting and useful concepts coming from the "cloud" sector for
research and engineering. 

NOTES: Add image for trend of cloud computing searches from google.

"The" Cloud
===========

Over the last 10-15 years, there have been many cloud or cloud-like
initiatives, although most took place before the term "cloud
technology" was coined.  There was the Commodity Computing effort from
Sun in 2005, followed by Utility Computing from IBM, HP, Microsoft,
and others.  These, however, were hampered the difficult interfaces
(APIs) and high costs.  It wasn't until 2006 with Amazon's EC2 compute
offering that cloud became a popular and cost-effective computing
model.  Amazon extended its offering to storage in 2008 with its
Elastic Block Store (EBS).

The reason for this success, was the convergence of several concepts: 
  * Mature virtualization technology with little performance
  degradation compared to "bare metal".
  * Appearance of simplified APIs (REST, XMLRPC, etc.) making use of
  the resources easy.
  * Excess of commercial computing capacity (Amazon, Google, etc.)
  making the offerings cost effective. 
These together make the cloud an interesting tool for scientific and
engineering computing. 

Virtualization
==============

NOTE: Insert diagram comparing direction installation on physical
machines vs. installation on virtual machines.   The point is just
that the procedure looks very similar except that there is a
"hypervisor" that provides "virtual" hardware.  Should provide a list
of commonly used hypervisors ("kvm", "xen", "esxi", etc.).  Also
provide a description of "full virtualization"
vs. "para-virtualization". 

What is a Cloud?
================

Best definitions can be found in the NIST document.  (Provide a link
to this document.)  Provides both "deployment models"--public,
community, private--and service models--SaaS, PaaS, and IaaS.

NOTE: Insert diagram for cloud taxonomy.

Software as a Service (SaaS)
============================

  * Architecture
    - Essentially web-hosting
  * Advantages
    - Very simple use: web interface with no software installation 
    - Very accessible: laptop, smartphone, etc.
  * Disadvantages
    - Questions about data: access, ownership, reliability, etc.
    - Integration of different services is often difficult

Platform as a Service (PaaS)
============================

  * Architecture
    - Platform and infrastructure for creating web applications
  * Advantages
    - Load balancing, automatic failover, etc. 
    - Programmers can forget about the low-level plumbing
  * Disadvantages
    - Restricted number of languages
    - Applications are not portable between difference providers 

Infrastructure as a Service (PaaS)
==================================

  * Architecture
    - Access to remote virtual machines
  * Advantages
    - Customized environment
    - Simple and rapid access
    - Access as "root"
    - Pay-as-you-go model (opex vs. capex)
  * Disadvantages
    - Non-standard interfaces (vendor lock-in)
    - Virtual machine creation is difficult and time-consuming

Summary of the Service Models
=============================

NOTE: Provide an overall summary of the service models.  Vendor
lock-in and flexibility as competing features.

Deployment Models
=================

  * Private
    - Single administrative domain, limited number of users
    - E.g. site uses cloud for standard site services, managed by
    system administrator
  * Community
    - Different administrative domains but with common
    interests/procedures 
    - E.g. high-energy physics community
  * Public
    - People outside of institute's administrative domain, general
    public 
    - E.g. Amazon Web Services (EC2, S3, etc.)

Using an IaaS Cloud
===================

NOTE: Provide figure for standard IaaS workflow.  Provide a
description of the various stages. 

  1. Find virtual macihine image to run on the cloud.
  2. Launch machine instance via the cloud front-end.
  3. Obtain machine's network address. 
  4. Use and control the virtual machine as usual.  (E.g. SSH to
  machine as root. 
  5. Shutdown or kill virtual machine. 

Why use an IaaS cloud?
======================

Customized Environment
  * Deployment of software with a large number or difficult
  dependencies
  * Use an environment that has already been validated

Development and Testing of Software
  * Easy access to many different operating systems
  * Change computing environment without impacting other developers 
  * Test software systems that consist of several machines

Service Deployment
  * Deploy services without the intervention of the local site
  administrator
  * Create platforms (PaaS) for scientific communities

Dynamic access to very significant computing resources.

Hybrid Clouds and "Sky" Computing
=================================

Peer Federation or Bursting

NOTE: Add the diagram and the description.

Brokered Federation

NOTE: Add teh diagram and the description.


Exercise: Your Interest in Clouds
=================================

Researchers and Engineers (End-users)
  * Use existing academic and/or commercial software on the cloud 
  * What scientific domains?

Developers
  * Modify existing software to use cloud resources
  * Create new software for the cloud
  * What types of software? 

Administrators
  * Provide cloud resources to researchers, engineers, and/or
  developers 
  * What types of users? Local, multi-institute, etc.?

