#!/bin/sh

# create server and samba account:

read -p "Enter new user name: " ACCOUNT
read -p "Enter new user passwd: " PASSWD

echo "1. Create account"

useradd -d /home/$ACCOUNT -m $ACCOUNT -s /bin/bash
(echo $PASSWD;echo $PASSWD) | passwd $ACCOUNT

echo "2. Create samba account"

(echo $PASSWD;echo $PASSWD) | smbpasswd -a $ACCOUNT

echo "3. Add config to /etc/samba/smb.conf"

USER_SMB_CONFIG="\n[$ACCOUNT]\ncomment = $ACCOUNT share directory\npath = /home/$ACCOUNT\nbrowseable = yes\nwriteable = yes\nvalid users = $ACCOUNT\n"

echo $USER_SMB_CONFIG >> /etc/samba/smb.conf

echo "4. Restart samba service"

service smbd restart

SERVER_IP=`/sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v 0.0.0.0|grep -v inet6|awk '{print $2}'|tr -d "addr:"`

echo "+++++++++++++++++++++++++++++++"
echo Server：$SERVER_IP
echo Account: $ACCOUNT
echo Passwd: $PASSWD
echo "+++++++++++++++++++++++++++++++"


#echo "5. Create /mnt/sdc directory"
#mkdir /mnt/sdc/$ACCOUNT
#chown -R $ACCOUNT:$ACCOUNT /mnt/sdc/$ACCOUNT

#echo "6. Create /opt directory"
#mkdir /opt/$ACCOUNT
#chown -R $ACCOUNT:$ACCOUNT /opt/$ACCOUNT
