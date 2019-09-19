all:
	gcc -o ./bin/dns dns.c
run:
	./bin/dns

clean:
	rm -rf ./bin/*
