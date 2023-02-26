# botjam - anti-bruteforce for OpenBSD
# See LICENSE file for copyright and license details.
#
# botjam version
VERSION = 0.1

# Customize below to fit your system
# paths
PREFIX = /usr/local

install:
	@echo installing executable file to ${DESTDIR}${PREFIX}/bin
	@mkdir -p ${DESTDIR}${PREFIX}/bin
	@cp -f botjam ${DESTDIR}${PREFIX}/bin
	@echo installing script file to ${DESTDIR}${PREFIX}/sbin
	@cp -f botjam.py ${DESTDIR}${PREFIX}/sbin
	@chmod 755 ${DESTDIR}${PREFIX}/bin/botjam
	@chmod 644 ${DESTDIR}${PREFIX}/sbin/botjam.py
	@echo installing sample config file
	@cp -f botjam.json /etc/botjam.json
	@chmod 644 /etc/botjam.json
	@echo installing init script in /etc/rc.d
	@cp -f botjam.rc /etc/rc.d/botjam
	@chmod 755 /etc/rc.d/botjam
	@echo installing crontab as root 
	@crontab -u ${USER} botjam.crontab

uninstall:
	@echo removing executable file from ${DESTDIR}${PREFIX}/bin
	@rm -f ${DESTDIR}${PREFIX}/bin/botjam
	@rm -f ${DESTDIR}${PREFIX}/bin/botjamreport
	@rm -f ${DESTDIR}${PREFIX}/sbin/botjam.py
	@rm -f ${DESTDIR}${PREFIX}/sbin/botjamreport.py
	@echo Remove configuration file manually if you want, located at /etc/botjam.json
	@echo Also remove the running crontab with \`crontab -u $$USER -e\` if you want

.PHONY: install uninstall
