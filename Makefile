
install-bin:
	./devops/scripts/install-bin.sh

/etc/systemd/system:
	@echo "install-service only works on a system that uses systemd"
	exit 1

install-service: /etc/systemd/system
	cp devops/systemd/bot-rpg.service /etc/systemd/system
	useradd bot-rpg

install: install-bin install-service
