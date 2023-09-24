# UPA

## Implementation informtation
- container name, compose file name and directory name for the database must be the same!

## Usage
If you don't want to install requirements to your global ones, run:
```console
$ make venv
```

To run specific database within the venv:
```console
$ make run-{mongo,influx,cassandra,neo4j}
```
