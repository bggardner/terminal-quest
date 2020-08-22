
# Terminal Quest

This is the source code for the Terminal Quest app available for Kano OS.
It is an introduction to terminal commands in the style of a text adventure game.

# How to install it

## Kano OS
linux-story is installed by default on Kano OS, and is provided as a debian package in our repositories. As it has a lot of dependencies from other packages in Kano OS, it is recommended you run it on Kano OS.
 - Package name: linux-story
 - Executable: /usr/bin/linux-story-gui

## Standalone on Raspberry Pi (2 or later)
This fork adapted the original repository to run as a standalone application (no dependency on any Kano repositories/packages or Python 2), but should still run on Kano OS.
```
sudo apt update
sudo apt upgrade
sudo apt install gettext gir1.2-vte-2.90 python3 python3-gi python3-pip
git clone https://github.com/bggardner/terminal-quest.git
cd terminal-quest
cd po
make
cd ..
pip3 install .
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
