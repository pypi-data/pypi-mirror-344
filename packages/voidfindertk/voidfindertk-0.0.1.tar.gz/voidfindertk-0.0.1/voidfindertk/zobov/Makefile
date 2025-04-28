.PHONY : loader

CFLAGS = -fPIC -std=c99
LDFLAGS = -shared

loader:
	gcc $(CFLAGS) $(LDFLAGS) -o zobov_loader.so zobov_loader.c
	gcc $(CFLAGS) $(LDFLAGS) -o zones_in_void.so zones_in_void.c
	gcc $(CFLAGS) $(LDFLAGS) -o tracers_in_zones.so tracers_in_zones.c

clean:
	rm -f *.so
