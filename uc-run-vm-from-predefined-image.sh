#!/bin/sh -e

. uc-utils.sh

export TTYLINUX_ID=LwcRbwCalYSysY1wftQdAj6Bwoi

echo "Starting machine instance..."
output=`stratus-run-instance --quiet $TTYLINUX_ID`
vmid=`echo $output | cut -d ',' -f 1 | sed 's/ //'`
ipaddr=`echo $output | cut -d ',' -f 2 | sed 's/ //'`

echo "Machine instance: VM ID=${vmid}, IP ADDR=${ipaddr}"

echo "Trying to ping machine..."
ping_address ${ipaddr} || echo "ping failed" || exit 1

echo "ping succeeded"

echo "Trying to ssh into machine..."
`ssh_address ${ipaddr}` || echo "ssh failed" || exit 1

echo "ssh succeeded"

echo "Killing machine..."
stratus-kill-instance ${vmid}
