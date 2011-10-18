#!/bin/sh -e

PING_LIMIT=20
PING_SLEEP=5
PING_ADDR=127.0.0.1

SSH_LIMIT=20
SSH_SLEEP=5
SSH_ADDR=127.0.0.1

#
# Try to ping address until success.
# Args: 1-IP Address, 2-Max. number of tries, 3-Sleep in seconds
#
ping_address () {
  ping_ok=1
  ping_limit=${2-$PING_LIMIT}

  for ((i=0; i<=${ping_limit}; i++)); do
    ping -q -c 1 ${1-$PING_ADDR} 2>&1 >/dev/null && ping_ok=0 && break
    sleep ${3-$PING_SLEEP}
  done

  return ${ping_ok}
}

#
# Try to ssh to address until success.
# Args: 1-IP Address, 2-Max. number of tries, 3-Sleep in seconds
#
ssh_address () {
  ssh_ok=1
  ssh_limit=${2-$SSH_LIMIT}

  ssh_id=""
  if [ "x$STRATUSLAB_KEY" != "x" ]; then
    ssh_id="-i $STRATUSLAB_KEY"
  fi

  for ((i=0; i<=${ssh_limit}; i++)); do
    ssh -q $ssh_id -o 'StrictHostKeyChecking=false' root@${1-$SSH_ADDR} /bin/true && ssh_ok=0 && break
    sleep ${3-$SSH_SLEEP}
  done

  return ${ssh_ok}
}
