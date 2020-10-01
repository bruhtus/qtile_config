# Qtile Window Manager Configuration

Qtile is a tling window manager that use python as the basis configuration file. The default configuration may vary depending on your distro, in my case the default configuration file is on /usr/share/doc/qtile/default_config.py (you can search using `locate qtile` but don't forget to do `sudo updatedb` first).
You can find the info about qtile on [their website](https://qtile.org) or [the documentation](http://docs.qtile.org/en/latest/).

If you're using the default config from /usr/ folder then you need to change ownership of that file using the command below:
```bash
sudo chown owner.group folder/file
```
you can check owner and group by using `ls -lart` in the folder (the owner is on column 3 and the group on column 4).
(For more information about change ownership you can see [this article](https://www.howtoforge.com/linux-chown-command/).

#### Change Ownership Example
```bash
sudo chown bruhtus.bruhtus .config/qtile/config.py
```

File [projector.sh](projector.sh) is for setting up dual monitor with xrandr.
