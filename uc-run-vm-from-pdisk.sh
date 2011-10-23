#!/bin/sh -e

. ./uc-utils.sh

export TTYLINUX_URL=http://appliances.stratuslab.eu/images/base/ttylinux-9.7-i486-base/1.3/ttylinux-9.7-i486-base-1.3.img.gz
export UBUNTU_ID=OWojA0YDjya7Uhzf7fDRulB3pz3

TAG=`date`

echo "Creating persistent disk..."
uuid=`stratus-create-volume -s 1 --tag "$TAG" | cut -d ' ' -f 2`
echo "Disk UUID: ${uuid}"

echo "Starting machine instance..."
output=`stratus-run-instance --quiet $UBUNTU_ID --persistent-disk=$uuid`
vmid=`echo $output | cut -d ',' -f 1 | sed 's/ //'`
ipaddr=`echo $output | cut -d ',' -f 2 | sed 's/ //'`

echo "Machine instance: VM ID=${vmid}, IP ADDR=${ipaddr}"

echo "Trying to ping machine..."
ping_address ${ipaddr} || echo "ping failed" || exit 1

echo "ping succeeded"

echo "Trying to ssh into machine..."
`ssh_address ${ipaddr}` || echo "ssh failed" || exit 1

echo "ssh succeeded"

echo "Add curl to machine..."
ssh -t -t -q -o 'StrictHostKeyChecking=false' root@${ipaddr} apt-get install -y curl

echo "List disks..."
ssh -t -t -q -o 'StrictHostKeyChecking=false' root@${ipaddr} fdisk -l 

echo "Dump TTYLINUX image into disk"
ssh -t -t -q -o 'StrictHostKeyChecking=false' root@${ipaddr} curl $TTYLINUX_URL \| gunzip \> /dev/sdc  

echo "List disks..."
ssh -t -t -q -o 'StrictHostKeyChecking=false' root@${ipaddr} fdisk -l 

echo "Killing machine..."
stratus-kill-instance ${vmid}

echo "Starting machine instance from persistent disk..."
output=`stratus-run-instance --quiet $uuid`
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

echo "Deleting persistent volume..."
sleep 5
stratus-delete-volume ${uuid}
