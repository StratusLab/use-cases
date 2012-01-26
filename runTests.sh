#!/bin/sh

nosetests -v --with-xunit \
  usecases.testAAACopyMetadataEntries \
  usecases.testBasicPersistentDiskLifecycle \
  usecases.testBasicPersistentDiskLifecycleWithTag \
  usecases.testBasicVmLifecycle \
  usecases.testClientHelpOption \
  usecases.testClientVersionOption \
  usecases.testMetadataSignAndValidate \
  usecases.testMetadataUploadAndDeprecate \
  usecases.testVmIsAccessibleViaSsh \
  usecases.testCernVmIsAccessibleViaSsh \
  usecases.testPersistentDiskRetainsData \
  usecases.testRunVmFromPersistentDisk \
  usecases.testVmStateNotification

