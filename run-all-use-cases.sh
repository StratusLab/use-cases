#!/bin/bash

run_cmd () {
  $1
  rc=$?
  if [ $rc -eq 0 ]; then
    echo "OK: $1"
  else
    echo "FAILURE: $1"
  fi

  return $rc
}

failed=0

run_cmd ./stratus_tutorial_dist.py
rc=$?
if [ $rc -ne 0 ]; then
  failed=$rc
fi

run_cmd ./uc-vm-state-notification.py
rc=$?
if [ $rc -ne 0 ]; then
  failed=$rc
fi

exit $failed

