
Exercises: Storage
==================

Volatile Disks
  * Create a VM with volaile disk
  * Verify that the disk space is present and usable
  * Need to format the space to use it
  * Commands: fdisk -l; mkfs -t ext4

Persistent Disk Lifecycle
  * Run through entire lifecycle without using a VM
  * Do this both via the CLI and the browser

Use persistent disk with a VM
  * Verify that disk can be created and populated on one machine, then
  be mounted and used on another.
  * Verify that data on disk is preserved
  * Verify that disk can be mounted/unmounted from running VM
  * NOTE: Need to use Ubuntu or CentOS.  Ensure acpiphp module is
  loaded before hot mounting or dismounting of disks. 

