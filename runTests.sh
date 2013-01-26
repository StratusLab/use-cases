#!/bin/sh

nosetests -v --with-xunit \
  usecases.testAAACopyMetadataEntries \
  usecases.testClientHelpOption \
  usecases.testClientVersionOption \
  usecases.testMetadataSignAndValidate \
  usecases.testMetadataUploadAndDeprecate \
  usecases.testBasicPersistentDiskLifecycle \
  usecases.testBasicPersistentDiskLifecycleWithTag \
  usecases.testBasicVmLifecycleTtylinux \
  usecases.testBasicVmLifecycleUbuntu \
  usecases.testBasicVmLifecycleCentOS \
  usecases.testBasicVmLifecycleCernVM \
  usecases.testVmIsAccessibleViaSsh \
  usecases.testVmStateNotification \
  usecases.testCernVmIsAccessibleViaSsh \
  usecases.testAttachAndDetachDisk \
  usecases.testKillReleasesAttachedDisk \
  usecases.testPersistentDiskRetainsData \
  usecases.testRunVmFromPersistentDisk \
  usecases.testPrepareContext \
  usecases.testCloudInitCentOS \
  usecases.testCreateImage


