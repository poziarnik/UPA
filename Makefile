ACTIVATE=. venv/bin/activate

define run
	podman-compose --file $(1)/$(1).yml up -d
	$(ACTIVATE) && python3 $(1)/run.py
	podman stop $(1)
endef

venv:
	python3 -m venv venv
	$(ACTIVATE) && pip3 install -r requirements.txt

run-mongo:
	$(call run,"mongo")