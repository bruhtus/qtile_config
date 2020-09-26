# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import socket
import subprocess

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = 'mod1'
terminal = 'alacritty'

keys = [
    # Switch between windows in current layout
    Key([mod], "h", lazy.layout.left(),
        desc="Move focus left in stack pane"
        ),
    Key([mod], "j", lazy.layout.down(),
        desc="Move focus down in stack pane"
        ),
    Key([mod], "k", lazy.layout.up(),
        desc="Move focus up in stack pane"
        ),
    Key([mod], "l", lazy.layout.right(),
        desc="Move focus right in stack pane"
        ),

    # Move windows up or down in current stack
    Key([mod, "control"], "j", lazy.layout.shuffle_down(),
        desc="Move window down in current stack "
        ),
    Key([mod, "control"], "k", lazy.layout.shuffle_up(),
        desc="Move window up in current stack "
        ),

    # Launch  dmenu launcher
    Key([mod], "a", lazy.spawn("dmenu_run -p 'Run: '"),
        desc="Dmenu Run Launcher"
        ),

    # Launch terminal
    Key([mod], "d", lazy.spawn(terminal),
        desc="Launch terminal"
        ),

    # Toggle between different layouts as defined below
    Key([mod], "s", lazy.next_layout(),
        desc="Toggle between layouts"
        ),

    # Close window
    Key([mod], "q", lazy.window.kill(),
        desc="Kill focused window"
        ),

    # Restart qtile
    Key([mod, "control"], "w", lazy.restart(),
        desc="Restart qtile"
        ),

    # Shutdown qtile
    Key([mod, "control"], "q", lazy.shutdown(),
        desc="Shutdown qtile"
        ),

    ### Switch focus to specific monitor
    Key([mod, "control"], "z", lazy.to_screen(0),
        desc="Focus to monitor 1"
        ),
    Key([mod, "control"], "x", lazy.to_screen(0.1),
        desc="Focus to monitor 2"
        ),

    ### Switch focus of monitors
    Key([mod, "control"], "s", lazy.next_screen(),
        desc="Move focus to next monitor"
        ),
    Key([mod, "control"], "a", lazy.prev_screen(),
        desc="Move focus to prev monitor"
        ),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layout_theme = {
        "border_width": 2,
        "margin": 6,
        "border_focus": "ffffff"
        }

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Columns(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.Clock(format='%A, %B %d | [%H:%M] '),
                widget.Spacer(length=10),
                widget.WindowName(),
                #widget.Chord(
                    #chords_colors={
                        #'launch': ("#ff0000", "ffffff"),
                    #},
                    #name_transform=lambda name: name.upper(),
                #),
                widget.CPU(),
                widget.Sep(),
                widget.TextBox(
                    text = 'Battery:'
                    ),
                widget.Battery(format='{char} {hour:d}:{min:02d}'),
                widget.TextBox(
                    text = 'Volume:'
                    ),
                widget.Volume(),
                widget.TextBox(
                    text = 'Mem:'
                    ),
                widget.MemoryGraph(),
                widget.Sep(),
                widget.TextBox(
                    text = 'Net Graph:'
                    ),
                widget.NetGraph(interface='auto'),
                widget.TextBox(
                    text = 'HDD:'
                    ),
                widget.HDDGraph(),
                widget.Systray(),
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
