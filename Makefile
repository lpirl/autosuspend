TARGET:=/opt/autosuspend
IF:=$(shell route | egrep "^default" | head -n 1 | awk '{print $$8}')
SERVICE_NAME:=autosuspend
SERVICE_FILE:=$(SERVICE_NAME).service

define SERVICE_FILE_CONTENT
[Unit]
Description=suspend automatically when machine is idle
After=network.target

[Service]
ExecStart=$(TARGET)/autosuspend

[Install]
WantedBy=multi-user.target
endef
export SERVICE_FILE_CONTENT

all: $(SERVICE_FILE)

.PHONY: $(SERVICE_FILE)
$(SERVICE_FILE):
	echo "$$SERVICE_FILE_CONTENT" > $@

install: all
	mkdir -p $(TARGET)
	cp -ar * $(TARGET)
	systemctl enable $(TARGET)/$(SERVICE_FILE)
	systemctl start $(SERVICE_NAME)

uninstall:
	@- systemctl disable $(SERVICE_NAME)
	rm -Ir $(TARGET)
