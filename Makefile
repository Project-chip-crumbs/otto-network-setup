all: setup.tpl otto-network-setup.py
#	scp setup.tpl otto-network-setup.py cam0:/mnt/otto-network-setup/
	scp setup.tpl cam0:/usr/lib/otto-network-setup/
	scp images.tpl cam0:/usr/lib/otto-network-setup/
	scp otto-network-setup.py cam0:/usr/bin
	scp otto-network-setup.service cam0:/usr/lib/systemd/system/otto-network-setup.service
	ssh cam0 "/bin/rm -f /etc/systemd/system/multi-user.target.wants/otto-network-setup.service"
	ssh cam0 "/bin/ln -s /usr/lib/systemd/system/otto-network-setup.service /etc/systemd/system/multi-user.target.wants/otto-network-setup.service"
#	ssh cam0 'killall -9 python'
#	ssh cam0 'cd /mnt/ott-network-setup; ./otto-network-setup.py
