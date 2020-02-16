#!/usr/bin/env bash

#cd /etc/apache/passl
mkdir /etc/apache/passl/backup-$(date +'%F') 2>/dev/null
if [ -e /etc/apache/passl/pa.cert.intermediate ]; then
  cp /etc/apache/passl/{pa.cert.cert,pa.cert.key,pa.cert.intermediate} backup-$(date +'%F')/ 2>/dev/null
  cat /etc/apache/passl/{pa.cert.cert,pa.cert.key,pa.cert.intermediate} > /var/qmail/control/clientcert.pem 2>/dev/null
else
  cp /etc/apache/passl/{pa.cert.cert,pa.cert.key} backup-$(date +'%F')/ 2>/dev/null
  cat /etc/apache/passl/{pa.cert.cert,pa.cert.key} > /var/qmail/control/clientcert.pem 2>/dev/null
fi
cp -p /var/qmail/control/clientcert.pem /var/qmail/control/clientcert.pem.back
cp -p /var/qmail/control/servercert.pem /var/qmail/control/servercert.pem.back
cat '' >> /var/qmail/control/clientcert.pem
cp /var/qmail/control/clientcert.pem /var/qmail/control/servercert.pem
for i in {1..3}; do qmail stop; done; qmail start
qmail start
apachectl -k restart
rm -rf /root/remote_backup.sh
