#!/usr/bin/env python

import unittest

import usecases.testCopyMetadataEntries

import usecases.testBasicPersistentDiskLifecycle
import usecases.testBasicVmLifecycle
import usecases.testClientHelpOption
import usecases.testClientVersionOption
import usecases.testMetadataSignAndValidate
import usecases.testMetadataUploadAndDeprecate
import usecases.testPersistentDiskRetainsData
import usecases.testRunVmFromPersistentDisk
import usecases.testVmIsAccessibleViaSsh
import usecases.testVmStateNotification

suite = unittest.TestSuite()

# Do this first to copy image entries used in tests.
suite.addTest(usecases.testCopyMetadataEntries.suite())

suite.addTest(usecases.testBasicPersistentDiskLifecycle.suite())
suite.addTest(usecases.testBasicVmLifecycle.suite())
suite.addTest(usecases.testClientHelpOption.suite())
suite.addTest(usecases.testClientVersionOption.suite())
suite.addTest(usecases.testMetadataSignAndValidate.suite())
suite.addTest(usecases.testMetadataUploadAndDeprecate.suite())
suite.addTest(usecases.testPersistentDiskRetainsData.suite())
suite.addTest(usecases.testRunVmFromPersistentDisk.suite())
suite.addTest(usecases.testVmIsAccessibleViaSsh.suite())
suite.addTest(usecases.testVmStateNotification.suite())

result = unittest.TextTestRunner(verbosity=0).run(suite)

message = '''
Errors:               %d
Failures:             %d
Skipped:              %d
Expected Failures:    %d
Unexpected Successes: %d
Tests Run:            %d
''' % (len(result.errors),
       len(result.failures),
       len(result.skipped),
       len(result.expectedFailures),
       len(result.unexpectedSuccesses),
       result.testsRun)

print message

if result.wasSuccessful():
    sys.exit(0)
else:
    sys.exit(1)


