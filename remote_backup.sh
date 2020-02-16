#!/usr/bin/env bash

SSL_PATH='/etc/apache/passl'
QMAIL_PATH='/var/qmail/control'

mkdir $SSL_PATH/backup-$(date +'%F') 2>/dev/null
if [ -e $SSL_PATH/pa.cert.intermediate ]; then
  cp $SSL_PATH/{pa.cert.cert,pa.cert.key,pa.cert.intermediate} $SSL_PATH/backup-$(date +'%F')/ 2>>/root/debug
  cat $SSL_PATH/{pa.cert.cert,pa.cert.key,pa.cert.intermediate} > $QMAIL_PATH/clientcert.pem 2>/dev/null
else
  cp $SSL_PATH/{pa.cert.cert,pa.cert.key} $SSL_PATH/backup-$(date +'%F')/ 2>/dev/null
  cat $SSL_PATH/{pa.cert.cert,pa.cert.key} > $QMAIL_PATH/clientcert.pem 2>/dev/null
fi
cp -p $QMAIL_PATH/clientcert.pem $QMAIL_PATH/clientcert.pem.back
cp -p $QMAIL_PATH/servercert.pem $QMAIL_PATH/servercert.pem.back
cat '' >> $QMAIL_PATH/clientcert.pem
cp $QMAIL_PATH/clientcert.pem $QMAIL_PATH/servercert.pem
for i in {1..3}; do qmail stop; done; qmail start
qmail start
apachectl -k restart
rm -rf /root/remote_backup.sh
