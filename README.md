# Qtile Window Manager Configuration

Qtile is a tiling window manager that use python as the basis configuration file. The default configuration may vary depending on your distro, in my case the configuration file is on /usr/share/doc/qtile/default_config.py
You can the info about Qtile on their [website](qtile.org) or the [documentation](http://docs.qtile.org/en/latest/).
if you're using the default config from the /usr/ folder then you need to change owenership of that file using the command below:

```bash
sudo chown owner.group folder/file
```
you can check owner and group by using the command:
```bash
ls -lart
```
in the folder (the owner is on column 3 and the group is on column 4).
(For more information about change ownership you can see [this article](https://www.howtoforge.com/linux-chown-command/))

```bash
for example:
sudo chown bruhtus.bruhtus .config/qtile/config.py
```

File [projector.sh](projector.sh) is for setting up dual monitor with xrandr.
