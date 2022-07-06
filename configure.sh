#!/bin/sh
yum update -y
wget https://package.perforce.com/perforce.pubkey
gpg --with-fingerprint perforce.pubkey
rpm --import https://package.perforce.com/perforce.pubkey
touch /etc/yum.repos.d/perforce.repo
echo '[perforce]' >> /etc/yum.repos.d/perforce.repo
echo 'name=Perforce' >> /etc/yum.repos.d/perforce.repo
echo 'baseurl=http://package.perforce.com/yum/rhel/7/x86_64' >> /etc/yum.repos.d/perforce.repo
echo 'enabled=1' >> /etc/yum.repos.d/perforce.repo
echo 'gpgcheck=1' >> /etc/yum.repos.d/perforce.repo
yum -y install helix-p4d
mkfs -t xfs /dev/sdb
mkdir /mnt/project
mount /dev/sdb /mnt/project
echo '/dev/sdb       /mnt/project   xfs    defaults,nofail        0       2' >> /etc/fstab
export p4root="/mnt/project"
export pwd=$(curl --silent http://169.254.169.254/latest/meta-data/instance-id)
export p4address="ssl:1666"
/opt/perforce/sbin/configure-helix-p4d.sh main -p $p4address -r $p4root -u super -P $pwd --case 0 -n
sed -i '16i\        P4PORT    =     ssl:1666' /etc/perforce/p4dctl.conf.d/main.conf