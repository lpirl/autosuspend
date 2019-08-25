TARGET:=/opt/autosuspend
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

all: help
help:
	@echo "help"
	@echo "----"
	@echo
	@echo "variables:"
	@echo "	TARGET"
	@echo "		directory to install to (default: $(TARGET))"
	@echo
	@echo "targets:"
	@echo "	service_file"
	@echo "		generate service file for systemd"
	@echo "	install"
	@echo "		install to \$$(TARGET)"
	@echo "	install_systemd_service"
	@echo "		also install (and enable) systemd service"
	@echo "	uninstall"
	@echo "		remove \$$(TARGET)"

service_file: $(SERVICE_FILE)
.PHONY: $(SERVICE_FILE)
$(SERVICE_FILE):
	echo "$$SERVICE_FILE_CONTENT" > $@
	@# prevents systemd from warning about world-inaccessible files
	chmod a+r $@

install: $(SERVICE_FILE)
	mkdir -p $(TARGET)
	cp -ar * $(TARGET)

install_systemd_service: $(SERVICE_FILE)
	systemctl enable $(TARGET)/$(SERVICE_FILE)
	systemctl start $(SERVICE_NAME)

uninstall:
	@- systemctl disable $(SERVICE_NAME)
	rm -Ir $(TARGET)
