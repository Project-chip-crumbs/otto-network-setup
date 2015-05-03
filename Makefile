SERVER=root@192.168.1.135

py: otto-network-setup.py
	scp otto-network-setup.py $(SERVER):/usr/bin

views_: views
	scp -r views $(SERVER):/usr/lib/otto-network-setup/

assets_: assets
	scp -r assets $(SERVER):/usr/lib/otto-network-setup/

all: views_ assets_ py

#	scp setup.tpl otto-network-setup.py cam0:/mnt/otto-network-setup/
#	scp otto-network-setup.service $(SERVER):/usr/lib/systemd/system/otto-network-setup.service
#	ssh cam0 "/bin/rm -f /etc/systemd/system/multi-user.target.wants/otto-network-setup.service"
#	ssh cam0 "/bin/ln -s /usr/lib/systemd/system/otto-network-setup.service /etc/systemd/system/multi-user.target.wants/otto-network-setup.service"
#	ssh cam0 'killall -9 python'
#	ssh cam0 'cd /mnt/ott-network-setup; ./otto-network-setup.py
