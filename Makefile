ACTIVATE=. venv/bin/activate

define run
	podman-compose --file databases/$(1).yml up -d
	$(ACTIVATE) && python3 run.py $(1)
	podman stop $(1)
endef

venv:
	python3 -m venv venv
	$(ACTIVATE) && pip3 install -r requirements.txt

run-mongo:
	$(call run,mongo)

run-influx:
	$(call run,influx)

run-cassandra:
	$(call run,cassandra)

run-neo4j:
	$(call run,neo4j)