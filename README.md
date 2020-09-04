# Terminal Quest

This is the source code for the Terminal Quest app available for Kano OS.
It is an introduction to terminal commands in the style of a text adventure game.

# How to install it

## Kano OS
linux-story is installed by default on Kano OS, and is provided as a debian package in our repositories. As it has a lot of dependencies from other packages in Kano OS, it is recommended you run it on Kano OS.
 - Package name: linux-story
 - Executable: /usr/bin/linux-story-gui

## Raspberry Pi OS
### Kano Repositories
This method allows you to run Terminal Quest without Kano OS, but requires installing many (stale and unnecessary) packages, and relies on Python 2.  Be sure to answer "no" if asked to replace any configuration files.
```
sudo apt-mark hold lxmenu-data
wget -qO - http://repo.kano.me/archive-stretch/repo.gpg.key | sudo apt-key add -
echo "deb http://repo.kano.me/archive-stretch/ release main" | sudo tee /etc/apt/sources.list.d/kano.list
sudo apt update
sudo apt upgrade
wget http://security.debian.org/debian-security/pool/updates/main/p/pillow/python-imaging_4.0.0-4+deb9u2_all.deb
sudo dpkg -i python-imaging_4.0.0-4+deb9u2_all.deb
sudo apt install --no-install-recommends linux-story python-docopt python-mercury python2-mercury
linux-story-gui
```

### Standalone
This fork adapted the original repository to run as a standalone application (no dependency on any Kano repositories/packages or Python 2), but should still run on Kano OS.
```
sudo apt update
sudo apt upgrade
sudo apt install gettext gir1.2-vte-2.90 python3-gi python3-pip
git clone https://github.com/bggardner/terminal-quest.git
cd terminal-quest
cd po
make
cd ..
pip3 install -e .
bin/linux-story-gui
```

# How Terminal Quest works
For a more detailed breakdown, read the [development wiki page](https://github.com/KanoComputing/linux-tutorial/wiki/Development).

# Options

```
linux-story-gui launches the application Terminal Quest at different points in the story.

Usage:
  linux-story-gui [-d | --debug]
  linux-story-gui challenge <challenge> <step> [-d | --debug]

Options:
   -h, --help       Show this message.
   -d, --debug      Debug mode, don't hide the terminal and spellbook widgets by default at the start.
```

Make sure your environment exposes `PYTHONIOENCODING=UTF-8` for correct i18n translations throughout the adventure.

# See Also
* [flappy-judoka](https://github.com/bggardner/flappy-judoka)
* [kano-draw](https://github.com/bggardner/kano-draw)
* [kano-pong](https://github.com/bggardner/kano-pong)
* [make-minecraft](https://github.com/bggardner/make-minecraft)
* [make-pong](https://github.com/bggardner/make-pong)
* [make-snake](https://github.com/bggardner/make-snake)
* [terminal-quest](https://github.com/bggardner/terminal-quest)

