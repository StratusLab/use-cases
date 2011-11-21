#!/usr/bin/env python

import sys
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

def formatResult(title, results):
    if results:
        print "\n----------\n%s\n----------\n" % title
        for result in results:
            testCase, traceback = result
            print testCase.id()
    
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

formatResult('ERRORS', result.errors)
formatResult('FAILURES', result.failures)
formatResult('SKIPPED', result.skipped)
formatResult('EXPECTED FAILURES', result.expectedFailures)
formatResult('UNEXPECTED SUCCESSES', result.unexpectedSuccesses)

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
