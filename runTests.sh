#!/bin/sh

nosetests -v --with-xunit \
  usecases.testAAACopyMetadataEntries \
  usecases.testClientHelpOption \
  usecases.testClientVersionOption \
  usecases.testMetadataSignAndValidate \
  usecases.testMetadataUploadAndDeprecate \
  usecases.testPrepareContext \
  usecases.testBasicPersistentDiskLifecycle \
  usecases.testBasicPersistentDiskLifecycleWithTag \
  usecases.testUploadImage \
  usecases.testDownloadImageFromMarketplace \
  usecases.testBasicVmLifecycleTtylinux \
  usecases.testBasicVmLifecycleUbuntu \
  usecases.testBasicVmLifecycleCentOS \
  usecases.testVmIsAccessibleViaSsh \
  usecases.testVmStateNotification \
  usecases.testAttachAndDetachDisk \
  usecases.testKillReleasesAttachedDisk \
  usecases.testPersistentDiskRetainsData \
  usecases.testRunVmFromPersistentDisk \
  usecases.testCloudInitCentOS \
  usecases.testReadonlyDataDisk \
  usecases.testBasicVmLifecycleCernVM \
  usecases.testCernVmIsAccessibleViaSsh

#  usecases.testCreateImage

# Currently not working because additional work on server is needed.
# See storage issue #19
#  usecases.testUploadAndDownloadImage

