generate:
	wireviz engine-100.yaml --prepend-file engine-100-connectors.yaml -o out/engine-100

clean:
	@rm out/*
