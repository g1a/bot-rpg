
install-service-account:
	useradd -m bot-rpg
	sudo -u bot-rpg bash && \
		cd /home/bot-rpg && \
		git clone https://github.com/g1a/bot-rpg.git && \
		cd bot-rpg && \
		python3 -m pip install virtualenv && \
		python3 -m venv env && \
		python3 -m pip install -r requirements.txt

/etc/systemd/system:
	@echo "install-service only works on a system that uses systemd"
	exit 1

install-service: /etc/systemd/system
	cp devops/systemd/bot-rpg.service /etc/systemd/system

install: install-service-account install-service
