TARGET:=/opt/autosuspend
IF:=$(shell route | egrep "^default" | head -n 1 | awk '{print $$8}')
SERVICE_NAME:=autosuspend
SERVICE_FILE:=$(TARGET)/$(SERVICE_NAME).service

define SERVICE_FILE_CONTENT
[Unit]
Description=suspend automatically when machine is idle
After=network.target

[Service]
ExecStart=$(TARGET)/autosuspend.py $(IF)

[Install]
WantedBy=multi-user.target
endef
export SERVICE_FILE_CONTENT

install:
	mkdir -p $(TARGET)
	cp -ar * $(TARGET)

install_systemd_service:
	echo "$$SERVICE_FILE_CONTENT" > $(SERVICE_FILE)
	systemctl enable $(SERVICE_FILE)
	systemctl start $(SERVICE_NAME)

uninstall:
	@- systemctl disable $(SERVICE_NAME)
	rm -Ir $(TARGET)
