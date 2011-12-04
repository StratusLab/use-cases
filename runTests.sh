#!/bin/sh

nosetests --with-xunit \
  usecases.testAAACopyMetadataEntries \
  usecases.testBasicPersistentDiskLifecycle \
  usecases.testBasicVmLifecycle \
  usecases.testClientHelpOption \
  usecases.testClientVersionOption \
  usecases.testMetadataSignAndValidate \
  usecases.testMetadataUploadAndDeprecate \
  usecases.testVmIsAccessibleViaSsh 
#  usecases.testPersistentDiskRetainsData \
#  usecases.testRunVmFromPersistentDisk \
#  usecases.testVmStateNotification

