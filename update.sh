#!/bin/bash -x

errCode=1

function incErrCode()
{
  errCode=$(( errCode++ ))
}

function error()
{
  [[ $# -eq 1 ]] && msg=${1}
  if [[ -n ${msg} ]]
  then
    echo "${msg}" >> /tmp/ap-err.txt
  fi
  exit ${errCode}
}


cd /opt/utils
[[ $? -eq 0 ]] || error
incErrCode

rm -rf ProjectComm
[[ $? -eq 0 ]] || error
incErrCode

git clone https://github.com/mrasamny/ProjectComm.git
[[ $? -eq 0 ]] || error
incErrCode

sleep 1

cd ProjectComm
[[ $? -eq 0 ]] || error
incErrCode

chmod go-x *
[[ $? -eq 0 ]] || error
incErrCode

chmod u-x *
[[ $? -eq 0 ]] || error
incErrCode

chmod u+x broadcast.py server.py
[[ $? -eq 0 ]] || error
incErrCode

cp proj-*.service /usr/lib/systemd/system/.
[[ $? -eq 0 ]] || error
incErrCode


echo "*********************************************"
echo "*                                           *"
echo "*     Update complete.  Please reboot       *"
echo "*                                           *"
echo "*********************************************"
