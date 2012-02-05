# Makefile for aur2ccr
manpages = aur2ccr.8.gz
binfiles = aur2ccr
configs = names.conf
others = aur2ccr.8 Makefile
allfiles = $(binfiles) $(configs) $(manpages) $(others)

all: man $(allfiles)

man: aur2ccr.8.gz $(others)

install: $(allfiles) install-man
	install -d -m755 "$(DESTDIR)/usr/local/bin"
	install -d -m755 "$(DESTDIR)/etc/aur2ccr"
	install -D -m755 $(binfiles) "$(DESTDIR)/usr/local/bin/"
	install -D -m644 $(configs) "$(DESTDIR)/etc/aur2ccr/"

install-man: # 'make install' calls this, so only do 'make install-man' if all you want is the man page.
	install -d -m755 "$(DESTDIR)/usr/local/man/man8"
	install -D -m644 $(manpages) "$(DESTDIR)/usr/local/man/man8/"

aur2ccr.8.gz : $(others)
	gzip -c aur2ccr.8 > aur2ccr.8.gz

bundle: aur2ccr.txz.sh # This is for the distributer ONLY, you need my 'bundle>=0.9.1' to use it.

aur2ccr.txz.sh : $(allfiles)
	bundle -s -x * > aur2ccr.txz.sh
