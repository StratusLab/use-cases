
Exercises: Create an Account
============================

NOTE: There may be other mechanisms for registering with a StratusLab
cloud service.  This exercise concentrates on the mechanism used by
the reference cloud infrastructure.  (LDAP as a user database with
either username/password or certificate authentication.)

Navigate to Registration Service
  * https://register.stratuslab.eu:8444/
  * Read and understand the policies

Provide information
  * Read policies
  * Complete registration form: Provide some context for your use of
    cloud.
  * Be sure to use a valid email address (it will be verified) 

NOTE: For the X509 DN you must use the RFC2253 format.  Use the
openssl command to get the correct option and format.

Final Step: Validation
  * This is a manual process to avoid "bots" or people outside of our
  community. 
  * Wait for approval
