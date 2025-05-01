# Copyright 2008-2015 Jose Fonseca
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import math
import os
import re
import subprocess
import sys
import time
import operator
import shutil
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('PangoCairo', '1.0')

from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Gdk

# See http://www.graphviz.org/pub/scm/graphviz-cairo/plugin/cairo/gvrender_cairo.c

# For pygtk inspiration and guidance see:
# - http://mirageiv.berlios.de/
# - http://comix.sourceforge.net/

from . import actions
from ..dot.lexer import ParseError
from ._xdotparser import XDotParser
from . import animation
from . import actions
from .elements import Graph


class DotWidget(Gtk.DrawingArea):
    """GTK widget that draws dot graphs."""

    # TODO GTK3: Second argument has to be of type Gdk.EventButton instead of object.
    __gsignals__ = {
        'clicked': (GObject.SignalFlags.RUN_LAST, None, (str, object)),
        'error': (GObject.SignalFlags.RUN_LAST, None, (str,)),
        'history': (GObject.SignalFlags.RUN_LAST, None, (bool, bool))
    }

    filter = 'dot'
    graphviz_version = None

    def __init__(self):
        Gtk.DrawingArea.__init__(self)

        self.graph = Graph()
        self.openfilename = None

        self.set_can_focus(True)

        self.connect("draw", self.on_draw)
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.connect("button-press-event", self.on_area_button_press)
        self.connect("button-release-event", self.on_area_button_release)
        self.add_events(Gdk.EventMask.POINTER_MOTION_MASK |
                        Gdk.EventMask.POINTER_MOTION_HINT_MASK |
                        Gdk.EventMask.BUTTON_RELEASE_MASK |
                        Gdk.EventMask.SCROLL_MASK |
                        Gdk.EventMask.SMOOTH_SCROLL_MASK)
        self.connect("motion-notify-event", self.on_area_motion_notify)
        self.connect("scroll-event", self.on_area_scroll_event)
        self.connect("size-allocate", self.on_area_size_allocate)

        self.connect('key-press-event', self.on_key_press_event)
        self.last_mtime = None
        self.mtime_changed = False

        GLib.timeout_add(1000, self.update)

        self.x, self.y = 0.0, 0.0
        self.zoom_ratio = 1.0
        self.zoom_to_fit_on_resize = False
        self.animation = animation.NoAnimation(self)
        self.drag_action = actions.NullAction(self)
        self.presstime = None
        self.highlight = None
        self.highlight_search = False
        self.history_back = []
        self.history_forward = []

        self.zoom_gesture = Gtk.GestureZoom.new(self)
        self.zoom_gesture.connect("scale-changed", self.on_scale_changed)

    def error_dialog(self, message):
        self.emit('error', message)

    def set_filter(self, filter):
        self.filter = filter
        self.graphviz_version = None

    def run_filter(self, dotcode):
        if not self.filter:
            return dotcode
        try:
            p = subprocess.Popen(
                [self.filter, '-Txdot'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False,
                universal_newlines=False
            )
        except OSError as exc:
            error = '%s: %s' % (self.filter, exc.strerror)
            p = subprocess.CalledProcessError(exc.errno, self.filter, exc.strerror)
        else:
            xdotcode, error = p.communicate(dotcode)
            error = error.decode()
        error = error.rstrip()
        if error:
            sys.stderr.write(error + '\n')
        if p.returncode != 0:
            self.error_dialog(error)
        return xdotcode

    def _set_dotcode(self, dotcode, filename=None, center=True):
        # By default DOT language is UTF-8, but it accepts other encodings
        assert isinstance(dotcode, bytes)
        xdotcode = self.run_filter(dotcode)
            
        if xdotcode is None:
            return False
        try:
            self.set_xdotcode(xdotcode, center=center)
        except ParseError as ex:
            self.error_dialog(str(ex))
            return False
        else:
            return True

    def set_dotcode(self, dotcode, filename=None, center=True):
        self.openfilename = None
        if self._set_dotcode(dotcode, filename, center=center):
            if filename is None:
                self.last_mtime = None
            else:
                self.last_mtime = os.stat(filename).st_mtime
            self.mtime_changed = False
            self.openfilename = filename
            return True

    def set_xdotcode(self, xdotcode, center=True):
        assert isinstance(xdotcode, bytes)

        if self.graphviz_version is None and self.filter is not None:
            stdout = subprocess.check_output([self.filter, '-V'], stderr=subprocess.STDOUT)
            stdout = stdout.rstrip()
            mo = re.match(br'^.* - .* version (?P<version>.*) \(.*\)$', stdout)
            assert mo
            self.graphviz_version = mo.group('version').decode('ascii')

        parser = XDotParser(xdotcode, graphviz_version=self.graphviz_version)
        self.graph = parser.parse()
        self.zoom_image(self.zoom_ratio, center=center)

    def reload(self):
        if self.openfilename is not None:
            try:
                fp = open(self.openfilename, 'rb')
                self._set_dotcode(fp.read(), self.openfilename, center=False)
                fp.close()
            except IOError:
                pass
            else:
                del self.history_back[:], self.history_forward[:]

    def update(self):
        if self.openfilename is not None:
            try:
                current_mtime = os.stat(self.openfilename).st_mtime
            except OSError:
                return True
            if current_mtime != self.last_mtime:
                self.last_mtime = current_mtime
                self.mtime_changed = True
            elif self.mtime_changed:
                self.mtime_changed = False
                self.reload()
        return True

    def _draw_graph(self, cr, rect):
        w, h = float(rect.width), float(rect.height)
        cx, cy = 0.5 * w, 0.5 * h
        x, y, ratio = self.x, self.y, self.zoom_ratio
        x0, y0 = x - cx / ratio, y - cy / ratio
        x1, y1 = x0 + w / ratio, y0 + h / ratio
        bounding = (x0, y0, x1, y1)

        cr.translate(cx, cy)
        cr.scale(ratio, ratio)
        cr.translate(-x, -y)
        self.graph.draw(cr, highlight_items=self.highlight, bounding=bounding)

    def on_draw(self, widget, cr):
        if self.highlight:
            for node in self.highlight:
                if hasattr(node, 'x') and hasattr(node, 'y'):
                    width = getattr(node, 'width', 20)
                    height = getattr(node, 'height', 20)
    
                    cr.set_source_rgba(1.0, 1.0, 0.0, 0.3)
                    cr.rectangle(node.x - 5, node.y - 5, width + 10, height + 10)
                    cr.fill()
    
        rect = self.get_allocation()
        Gtk.render_background(self.get_style_context(), cr, 0, 0, rect.width, rect.height)
    
        cr.save()
        self._draw_graph(cr, rect)
        cr.restore()
    
        self.drag_action.draw(cr)
    
        return False

    def get_current_pos(self):
        return self.x, self.y

    def set_current_pos(self, x, y):
        self.x = x
        self.y = y
        self.queue_draw()

    def set_highlight(self, items, search=False):
        # Enable or disable search highlight
        if search:
            self.highlight_search = items is not None
        # Ignore cursor highlight while searching
        if self.highlight_search and not search:
            return
        if self.highlight != items:
            self.highlight = items
            self.queue_draw()

    def zoom_image(self, zoom_ratio, center=False, pos=None):
        # Constrain zoom ratio to a sane range to prevent numeric instability.
        zoom_ratio = min(zoom_ratio, 1E4)
        zoom_ratio = max(zoom_ratio, 1E-6)

        if center:
            self.x = self.graph.width/2
            self.y = self.graph.height/2
        elif pos is not None:
            rect = self.get_allocation()
            x, y = pos
            x -= 0.5*rect.width
            y -= 0.5*rect.height
            self.x += x / self.zoom_ratio - x / zoom_ratio
            self.y += y / self.zoom_ratio - y / zoom_ratio
        self.zoom_ratio = zoom_ratio
        self.zoom_to_fit_on_resize = False
        self.queue_draw()

    def zoom_to_area(self, x1, y1, x2, y2):
        rect = self.get_allocation()
        width = abs(x1 - x2)
        height = abs(y1 - y2)
        if width == 0 and height == 0:
            self.zoom_ratio *= self.ZOOM_INCREMENT
        else:
            self.zoom_ratio = min(
                float(rect.width)/float(width),
                float(rect.height)/float(height)
            )
        self.zoom_to_fit_on_resize = False
        self.x = (x1 + x2) / 2
        self.y = (y1 + y2) / 2
        self.queue_draw()

    def zoom_to_fit(self):
        rect = self.get_allocation()
        rect.x += self.ZOOM_TO_FIT_MARGIN
        rect.y += self.ZOOM_TO_FIT_MARGIN
        rect.width -= 2 * self.ZOOM_TO_FIT_MARGIN
        rect.height -= 2 * self.ZOOM_TO_FIT_MARGIN
        zoom_ratio = min(
            float(rect.width)/float(self.graph.width),
            float(rect.height)/float(self.graph.height)
        )
        self.zoom_image(zoom_ratio, center=True)
        self.zoom_to_fit_on_resize = True

    ZOOM_INCREMENT = 1.25
    ZOOM_TO_FIT_MARGIN = 12

    def on_zoom_in(self, action):
        self.zoom_image(self.zoom_ratio * self.ZOOM_INCREMENT)

    def on_zoom_out(self, action):
        self.zoom_image(self.zoom_ratio / self.ZOOM_INCREMENT)

    def on_zoom_fit(self, action):
        self.zoom_to_fit()

    def on_zoom_100(self, action):
        self.zoom_image(1.0)

    POS_INCREMENT = 100

    def show_search_bar(self):
        if hasattr(self, "search_entry") and self.search_entry.get_parent():
            self.search_entry.set_visible(True)  # <- Ensure it becomes visible again
            self.search_entry.grab_focus()
            return
    
        # Create entry if it doesn't exist
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Search nodes, ports, signals...")
        self.search_entry.set_hexpand(True)
    
        # Get the top-level widget (usually the main window)
        win = self.get_toplevel()
        vbox = win.get_children()[0]  # assuming a Gtk.Box or Gtk.VBox
    
        # Add search bar at the top
        vbox.pack_start(self.search_entry, False, False, 0)
        self.search_entry.show()  # <- Show for the first time
        self.search_entry.grab_focus()
    
        # Connect search handling
        self.search_entry.connect("changed", self.on_search_text_changed)
        self.search_entry.connect("activate", self.on_search_entry_activate)
        self.search_entry.connect("key-press-event", self.on_search_entry_key_press)

    def exit_search_mode(self):
        if hasattr(self, "search_entry"):
            self.search_entry.set_visible(False)
        self.search_results = []
        self.highlight = None
        self.queue_draw()
        self.grab_focus()

    def on_search_text_changed(self, entry):
        query = entry.get_text().strip()
        if not query:
            self.highlight = None
            self.queue_draw()
            return
    
        try:
            pattern = re.compile(query, re.IGNORECASE)
        except re.error as err:
            return
    
        matches = []
        for element in self.graph.nodes + self.graph.edges + self.graph.shapes:
            if hasattr(element, "search_text") and element.search_text(pattern):
                matches.append(element)
                self.search_results = matches
                self.search_index = 0
    
        self.highlight = matches
        self.queue_draw()

    def on_search_entry_activate(self, entry):
        if not self.search_results:
            return
    
        self.search_entry.set_visible(False)
        self.grab_focus()
    
        match = self.search_results[self.search_index]
        self.animate_to(match.x, match.y)

    def on_search_entry_key_press(self, widget, event):
        if Gdk.keyval_name(event.keyval) == "Escape":
            self.exit_search_mode()
            return True
        return False

    def on_key_press_event(self, widget, event):
        if event.keyval == Gdk.KEY_Left:
            self.x -= self.POS_INCREMENT/self.zoom_ratio
            self.queue_draw()
            return True
        if event.keyval == Gdk.KEY_Right:
            self.x += self.POS_INCREMENT/self.zoom_ratio
            self.queue_draw()
            return True
        if event.keyval == Gdk.KEY_Up:
            self.y -= self.POS_INCREMENT/self.zoom_ratio
            self.queue_draw()
            return True
        if event.keyval == Gdk.KEY_Down:
            self.y += self.POS_INCREMENT/self.zoom_ratio
            self.queue_draw()
            return True
        if event.keyval in (Gdk.KEY_Page_Up,
                            Gdk.KEY_plus,
                            Gdk.KEY_equal,
                            Gdk.KEY_KP_Add):
            self.zoom_image(self.zoom_ratio * self.ZOOM_INCREMENT)
            self.queue_draw()
            return True
        if event.keyval in (Gdk.KEY_Page_Down,
                            Gdk.KEY_minus,
                            Gdk.KEY_KP_Subtract):
            self.zoom_image(self.zoom_ratio / self.ZOOM_INCREMENT)
            self.queue_draw()
            return True
        if event.keyval == Gdk.KEY_Escape:
            self.drag_action.abort()
            self.drag_action = actions.NullAction(self)
            return True
        if event.keyval == Gdk.KEY_r:
            self.reload()
            return True
        if event.keyval == Gdk.KEY_f:
            win = widget.get_toplevel()
            find_toolitem = win.uimanager.get_widget('/ToolBar/Find')
            textentry = find_toolitem.get_children()
            win.set_focus(textentry[0])
            return True
        if event.keyval == Gdk.KEY_q:
            Gtk.main_quit()
            return True
        if event.keyval == Gdk.KEY_p:
            self.on_print()
            return True
        if event.keyval == Gdk.KEY_t:
            # toggle toolbar visibility
            win = widget.get_toplevel()
            toolbar = win.uimanager.get_widget("/ToolBar")
            toolbar.set_visible(not toolbar.get_visible())
            return True
        if event.keyval == Gdk.KEY_w:
            self.zoom_to_fit()
            return True
        keyval = event.keyval 
        keyname = Gdk.keyval_name(keyval)
        if keyname == "slash":
            self.show_search_bar();
            return True
        if Gdk.keyval_name(event.keyval) == "Escape":
            if hasattr(self, "search_entry") and self.search_entry.get_visible():
                self.exit_search_mode()
                return True
        if keyname in ("n", "N") and self.search_results:
            if keyname == "n":
                self.search_index = (self.search_index + 1) % len(self.search_results)
            else:
                self.search_index = (self.search_index - 1) % len(self.search_results)
        
            match = self.search_results[self.search_index]
            self.set_highlight([match], search=True)
            self.animate_to(match.x, match.y)
            return True
        return False

    print_settings = None

    def on_print(self, action=None):
        print_op = Gtk.PrintOperation()

        if self.print_settings is not None:
            print_op.set_print_settings(self.print_settings)

        print_op.connect("begin_print", self.begin_print)
        print_op.connect("draw_page", self.draw_page)

        res = print_op.run(Gtk.PrintOperationAction.PRINT_DIALOG, self.get_toplevel())
        if res == Gtk.PrintOperationResult.APPLY:
            self.print_settings = print_op.get_print_settings()

    def begin_print(self, operation, context):
        operation.set_n_pages(1)
        return True

    def draw_page(self, operation, context, page_nr):
        cr = context.get_cairo_context()
        rect = self.get_allocation()
        self._draw_graph(cr, rect)

    def get_drag_action(self, event):
        state = event.state
        if event.button in (1, 2):  # left or middle button
            modifiers = Gtk.accelerator_get_default_mod_mask()
            if state & modifiers == Gdk.ModifierType.CONTROL_MASK:
                return actions.ZoomAction
            elif state & modifiers == Gdk.ModifierType.SHIFT_MASK:
                return actions.ZoomAreaAction
            else:
                return actions.PanAction
        return actions.NullAction

    def on_area_button_press(self, area, event):
        self.animation.stop()
        self.drag_action.abort()
        action_type = self.get_drag_action(event)
        self.drag_action = action_type(self)
        self.drag_action.on_button_press(event)
        self.presstime = time.time()
        self.pressx = event.x
        self.pressy = event.y
        return False

    def is_click(self, event, click_fuzz=4, click_timeout=1.0):
        assert event.type == Gdk.EventType.BUTTON_RELEASE
        if self.presstime is None:
            # got a button release without seeing the press?
            return False
        # XXX instead of doing this complicated logic, shouldn't we listen
        # for gtk's clicked event instead?
        deltax = self.pressx - event.x
        deltay = self.pressy - event.y
        return (time.time() < self.presstime + click_timeout and
                math.hypot(deltax, deltay) < click_fuzz)

    def on_url(self, url):
        import shutil
        import subprocess
        import os
        from pathlib import Path
    
        if not url:
            return
    
        # Keep existing file finding logic intact
        clean_url = url.split('#')[0].split(':')[0]
        url_components = clean_url.replace('\\', '/').split('/')
        
        project_root = Path(os.getenv("VIDOT_PROJECT_ROOT", ".")).resolve()
        max_search_depth = 6
        found_path = None
    
        direct_paths = [
            project_root / clean_url,
            Path(getattr(self, 'dot_file_path', '.')).resolve() / clean_url
        ]
    
        for path in direct_paths:
            if path.exists() and path.is_file():
                found_path = str(path)
                break
    
        if not found_path and len(url_components) > 1:
            try:
                search_depth = len(url_components) - 1
                for root, dirs, files in os.walk(str(project_root), followlinks=True):
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    
                    current_depth = Path(root).relative_to(project_root).parts.count(os.sep)
                    if current_depth > max_search_depth:
                        dirs[:] = []
                        continue
    
                    rel_path = Path(root).relative_to(project_root)
                    path_parts = rel_path.parts
                    
                    if len(path_parts) >= len(url_components)-1:
                        dirs_match = all(a == b for a, b in 
                                       zip(path_parts[-(len(url_components)-1):], 
                                       url_components[:-1]))
                        
                        if dirs_match and url_components[-1] in files:
                            found_path = str(Path(root) / url_components[-1])
                            break
            except Exception as e:
                print(f"Component search error: {e}")
    
        if not found_path:
            target_file = url_components[-1]
            try:
                for root, dirs, files in os.walk(str(project_root), followlinks=True):
                    if target_file in files:
                        found_path = str(Path(root) / target_file)
                        break
            except Exception as e:
                print(f"Fallback search error: {e}")
    
        # Improved editor handling section
        if found_path:
            # Determine editor with priority
            editor = os.environ.get("VIDOT_EDITOR") or os.environ.get("EDITOR")
            terminal_editor = False
            
            # Common editor detection
            if not editor:
                # Try to find a suitable GUI editor first
                gui_editors = ['code', 'subl', 'gedit', 'notepad.exe']
                for e in gui_editors:
                    editor_path = shutil.which(e)
                    if editor_path:
                        editor = editor_path
                        break
                
                # Fallback to terminal editors
                if not editor:
                    term_editors = ['vim', 'nvim', 'nano']
                    for e in term_editors:
                        editor_path = shutil.which(e)
                        if editor_path:
                            editor = editor_path
                            terminal_editor = True
                            break
    
            if not editor:
                print("No editor found. Set VIDOT_EDITOR/EDITOR environment variable.")
                return
    
            # Build command based on editor type
            cmd = [editor, found_path]
            terminal = os.environ.get("VIDOT_TERMINAL")
    
            try:
                if terminal_editor:
                    # Handle modern terminal syntax
                    terminal_commands = {
                        'gnome-terminal': ['--', 'bash', '-c'],
                        'konsole': ['-e'],
                        'xterm': ['-e'],
                        'alacritty': ['-e'],
                        'wt': ['-w', '0', '--']
                    }
                    
                    # Get base terminal name without path
                    term_base = os.path.basename(terminal) if terminal else ''
                    
                    if terminal and term_base in terminal_commands:
                        cmd = [terminal] + terminal_commands[term_base] + [' '.join(cmd)]
                    elif terminal:
                        # Fallback for unknown terminals
                        cmd = [terminal, '-e'] + cmd
                    else:
                        # Directly open terminal editor in current terminal
                        subprocess.Popen(cmd, start_new_session=True)
                else:
                    # GUI editor handling
                    if os.name == 'nt':
                        os.startfile(found_path)
                    else:
                        subprocess.Popen(cmd, start_new_session=True)
    
                print(f"Opening {found_path} with {editor}")
    
            except Exception as e:
                print(f"Failed to launch editor: {e}")
                print(f"Try running manually: {' '.join(cmd)}")
        else:
            print(f"File '{clean_url}' not found (searched up to {max_search_depth} levels deep)")

    def on_click(self, element, event):
        if element.url:
            self.on_url(element.url)

    def on_area_button_release(self, area, event):
        self.drag_action.on_button_release(event)
        self.drag_action = actions.NullAction(self)
        x, y = int(event.x), int(event.y)
        if self.is_click(event):
            el = self.get_element(x, y)
            if self.on_click(el, event):
                return True

            if event.button == 1:
                url = self.get_url(x, y)
                if url is not None:
                    self.emit('clicked', url.url, event)
                else:
                    ctrl_held = event.state & Gdk.ModifierType.CONTROL_MASK
                    jump = self.get_jump(x, y, to_dst=ctrl_held)
                    if jump is not None:
                        self.animate_to(jump.x, jump.y)

                return True

        if event.button == 1 or event.button == 2:
            return True
        return False

    def on_area_scroll_event(self, area, event):
        if event.direction == Gdk.ScrollDirection.UP:
            self.zoom_image(self.zoom_ratio * self.ZOOM_INCREMENT,
                            pos=(event.x, event.y))
            return True
        elif event.direction == Gdk.ScrollDirection.DOWN:
            self.zoom_image(self.zoom_ratio / self.ZOOM_INCREMENT,
                            pos=(event.x, event.y))
        else:
            deltas = event.get_scroll_deltas()
            self.zoom_image(self.zoom_ratio * (1 - deltas.delta_y / 10),
                            pos=(event.x, event.y))
            return True
        return False

    def on_area_motion_notify(self, area, event):
        self.drag_action.on_motion_notify(event)
        return True

    def on_area_size_allocate(self, area, allocation):
        if self.zoom_to_fit_on_resize:
            self.zoom_to_fit()

    def on_scale_changed(self, gesture, scale):
        point, x, y = gesture.get_point()
        if point:
            pos = (x, y)
        new_zoom_ratio = self.zoom_ratio * math.exp(math.log(scale) / 3)
        self.zoom_image(new_zoom_ratio, pos=pos)

    def animate_to(self, x, y):
        del self.history_forward[:]
        self.history_back.append(self.get_current_pos())
        self.history_changed()
        self._animate_to(x, y)

    def _animate_to(self, x, y):
        self.animation = animation.ZoomToAnimation(self, x, y)
        self.animation.start()

    def history_changed(self):
        self.emit(
            'history',
            bool(self.history_back),
            bool(self.history_forward))

    def on_go_back(self, action=None):
        try:
            item = self.history_back.pop()
        except LookupError:
            return
        self.history_forward.append(self.get_current_pos())
        self.history_changed()
        self._animate_to(*item)

    def on_go_forward(self, action=None):
        try:
            item = self.history_forward.pop()
        except LookupError:
            return
        self.history_back.append(self.get_current_pos())
        self.history_changed()
        self._animate_to(*item)

    def window2graph(self, x, y):
        rect = self.get_allocation()
        x -= 0.5*rect.width
        y -= 0.5*rect.height
        x /= self.zoom_ratio
        y /= self.zoom_ratio
        x += self.x
        y += self.y
        return x, y

    def get_element(self, x, y):
        x, y = self.window2graph(x, y)
        return self.graph.get_element(x, y)

    def get_url(self, x, y):
        x, y = self.window2graph(x, y)
        return self.graph.get_url(x, y)

    def get_jump(self, x, y, to_dst = False):
        x, y = self.window2graph(x, y)
        return self.graph.get_jump(x, y, to_dst)


class FindMenuToolAction(Gtk.Action):
    __gtype_name__ = "FindMenuToolAction"

    def do_create_tool_item(self):
        return Gtk.ToolItem()


class DotWindow(Gtk.Window):

    ui = '''
    <ui>
        <toolbar name="ToolBar">
            <toolitem action="Open"/>
            <toolitem action="Export"/>
            <toolitem action="Reload"/>
            <toolitem action="Print"/>
            <separator/>
            <toolitem action="Back"/>
            <toolitem action="Forward"/>
            <separator/>
            <toolitem action="ZoomIn"/>
            <toolitem action="ZoomOut"/>
            <toolitem action="ZoomFit"/>
            <toolitem action="Zoom100"/>
            <separator/>
            <toolitem name="Find" action="Find"/>
            <separator name="FindNextSeparator"/>
            <toolitem action="FindNext"/>
            <separator name="FindStatusSeparator"/>
            <toolitem name="FindStatus" action="FindStatus"/>
        </toolbar>
    </ui>
    '''

    base_title = 'Dot Viewer'

    def __init__(self, widget=None, width=512, height=512):
        Gtk.Window.__init__(self)

        self.graph = Graph()

        window = self

        window.set_title(self.base_title)
        window.set_default_size(width, height)
        window.set_wmclass("xdot", "xdot")
        vbox = Gtk.VBox()
        window.add(vbox)

        self.dotwidget = widget or DotWidget()
        self.dotwidget.connect("error", lambda e, m: self.error_dialog(m))
        self.dotwidget.connect("history", self.on_history)

        # Create a UIManager instance
        uimanager = self.uimanager = Gtk.UIManager()

        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        window.add_accel_group(accelgroup)

        # Create an ActionGroup
        actiongroup = Gtk.ActionGroup('Actions')
        self.actiongroup = actiongroup

        # Create actions
        actiongroup.add_actions((
            ('Open', Gtk.STOCK_OPEN, None, None, "Open dot-file", self.on_open),
            ('Export', Gtk.STOCK_SAVE_AS, None, None, "Export graph to other format", self.on_export),
            ('Reload', Gtk.STOCK_REFRESH, None, None, "Reload graph", self.on_reload),
            ('Print', Gtk.STOCK_PRINT, None, None,
             "Prints the currently visible part of the graph", self.dotwidget.on_print),
            ('ZoomIn', Gtk.STOCK_ZOOM_IN, None, None, "Zoom in", self.dotwidget.on_zoom_in),
            ('ZoomOut', Gtk.STOCK_ZOOM_OUT, None, None, "Zoom out", self.dotwidget.on_zoom_out),
            ('ZoomFit', Gtk.STOCK_ZOOM_FIT, None, None, "Fit zoom", self.dotwidget.on_zoom_fit),
            ('Zoom100', Gtk.STOCK_ZOOM_100, None, None, "Reset zoom level", self.dotwidget.on_zoom_100),
            ('FindNext', Gtk.STOCK_GO_FORWARD, 'Next Result', None, 'Move to the next search result', self.on_find_next),
        ))

        self.back_action = Gtk.Action('Back', None, None, Gtk.STOCK_GO_BACK)
        self.back_action.set_sensitive(False)
        self.back_action.connect("activate", self.dotwidget.on_go_back)
        actiongroup.add_action(self.back_action)

        self.forward_action = Gtk.Action('Forward', None, None, Gtk.STOCK_GO_FORWARD)
        self.forward_action.set_sensitive(False)
        self.forward_action.connect("activate", self.dotwidget.on_go_forward)
        actiongroup.add_action(self.forward_action)

        find_action = FindMenuToolAction("Find", None,
                                         "Find a node by name", None)
        actiongroup.add_action(find_action)

        findstatus_action = FindMenuToolAction("FindStatus", None,
                                               "Number of results found", None)
        actiongroup.add_action(findstatus_action)

        # Add the actiongroup to the uimanager
        uimanager.insert_action_group(actiongroup, 0)

        # Add a UI descrption
        uimanager.add_ui_from_string(self.ui)

        # Create a Toolbar
        toolbar = uimanager.get_widget('/ToolBar')
        vbox.pack_start(toolbar, False, False, 0)

        vbox.pack_start(self.dotwidget, True, True, 0)

        self.last_open_dir = "."

        self.set_focus(self.dotwidget)

        # Add Find text search
        find_toolitem = uimanager.get_widget('/ToolBar/Find')
        self.textentry = Gtk.Entry()
        self.textentry.set_icon_from_stock(0, Gtk.STOCK_FIND)
        find_toolitem.add(self.textentry)

        self.textentry.set_activates_default(True)
        self.textentry.connect("activate", self.textentry_activate, self.textentry);
        self.textentry.connect("changed", self.textentry_changed, self.textentry);

        uimanager.get_widget('/ToolBar/FindNextSeparator').set_draw(False)
        uimanager.get_widget('/ToolBar/FindStatusSeparator').set_draw(False)
        self.find_next_toolitem = uimanager.get_widget('/ToolBar/FindNext')
        self.find_next_toolitem.set_sensitive(False)

        self.find_count = Gtk.Label()
        findstatus_toolitem = uimanager.get_widget('/ToolBar/FindStatus')
        findstatus_toolitem.add(self.find_count)

        self.show_all()

    def find_text(self, entry_text):
        found_items = []
        dot_widget = self.dotwidget
        try:
            regexp = re.compile(entry_text)
        except re.error as err:
            sys.stderr.write('warning: re.compile() failed with error "%s"\n' % err)
            return []
        for element in dot_widget.graph.nodes + dot_widget.graph.edges + dot_widget.graph.shapes:
            if element.search_text(regexp):
                found_items.append(element)
        return sorted(found_items, key=operator.methodcaller('get_text'))

    def textentry_changed(self, widget, entry):
        self.find_count.set_label('')
        self.find_index = 0
        self.find_next_toolitem.set_sensitive(False)
        entry_text = entry.get_text()
        dot_widget = self.dotwidget
        if not entry_text:
            dot_widget.set_highlight(None, search=True)
            return

        found_items = self.find_text(entry_text)
        dot_widget.set_highlight(found_items, search=True)
        if found_items:
            self.find_count.set_label('%d nodes found' % len(found_items))

    def textentry_activate(self, widget, entry):
        self.find_index = 0
        self.find_next_toolitem.set_sensitive(False)
        entry_text = entry.get_text()
        dot_widget = self.dotwidget
        if not entry_text:
            dot_widget.set_highlight(None, search=True)
            self.set_focus(self.dotwidget)
            return

        found_items = self.find_text(entry_text)
        dot_widget.set_highlight(found_items, search=True)
        if found_items:
            dot_widget.animate_to(found_items[0].x, found_items[0].y)
        self.find_next_toolitem.set_sensitive(len(found_items) > 1)

    def set_filter(self, filter):
        self.dotwidget.set_filter(filter)

    def set_dotcode(self, dotcode, filename=None):
        if self.dotwidget.set_dotcode(dotcode, filename):
            self.update_title(filename)
            self.dotwidget.zoom_to_fit()

    def set_xdotcode(self, xdotcode, filename=None):
        if self.dotwidget.set_xdotcode(xdotcode):
            self.update_title(filename)
            self.dotwidget.zoom_to_fit()

    def update_title(self, filename=None):
        if filename is None:
            self.set_title(self.base_title)
        else:
            self.set_title(os.path.basename(filename) + ' - ' + self.base_title)

    def open_file(self, filename):
        try:
            fp = open(filename, 'rb')
            self.set_dotcode(fp.read(), filename)
            fp.close()
        except IOError as ex:
            self.error_dialog(str(ex))

    def on_open(self, action):
        chooser = Gtk.FileChooserDialog(parent=self,
                                        title="Open Graphviz File",
                                        action=Gtk.FileChooserAction.OPEN,
                                        buttons=(Gtk.STOCK_CANCEL,
                                                 Gtk.ResponseType.CANCEL,
                                                 Gtk.STOCK_OPEN,
                                                 Gtk.ResponseType.OK))
        chooser.set_default_response(Gtk.ResponseType.OK)
        chooser.set_current_folder(self.last_open_dir)
        filter = Gtk.FileFilter()
        filter.set_name("Graphviz files")
        filter.add_pattern("*.gv")
        filter.add_pattern("*.dot")
        chooser.add_filter(filter)
        filter = Gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        chooser.add_filter(filter)
        if chooser.run() == Gtk.ResponseType.OK:
            filename = chooser.get_filename()
            self.last_open_dir = chooser.get_current_folder()
            chooser.destroy()
            self.open_file(filename)
        else:
            chooser.destroy()
   
    def export_file(self, filename, format_):
        if not filename.endswith("." + format_):
            filename += '.' + format_
        cmd = [
            self.dotwidget.filter, # program name, usually "dot"
            '-T' + format_,
            '-o', filename,
            self.dotwidget.openfilename,
        ]
        subprocess.check_call(cmd)

    def on_export(self, action):
        
        if self.dotwidget.openfilename is None:
            return
        
        default_filter = "PNG image"
    
        output_formats = {
            "dot file": "dot",
            "GIF image": "gif",
            "JPG image": "jpg",
            "JSON": "json",
            "PDF": "pdf",
            "PNG image": "png",
            "PostScript": "ps",
            "SVG image": "svg",
            "XFIG image": "fig",
            "xdot file": "xdot",
        }
        buttons = (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
        chooser = Gtk.FileChooserDialog(
            parent=self,
            title="Export to other file format.",
            action=Gtk.FileChooserAction.SAVE,
            buttons=buttons) 
        chooser.set_default_response(Gtk.ResponseType.OK)
        chooser.set_current_folder(self.last_open_dir)
        
        openfilename = os.path.basename(self.dotwidget.openfilename)
        openfileroot = os.path.splitext(openfilename)[0]
        chooser.set_current_name(openfileroot)

        for name, ext in output_formats.items():
            filter_ = Gtk.FileFilter()
            filter_.set_name(name)
            filter_.add_pattern('*.' + ext)
            chooser.add_filter(filter_)
            if name == default_filter:
                chooser.set_filter(filter_)

        if chooser.run() == Gtk.ResponseType.OK:
            filename = chooser.get_filename()
            format_ = output_formats[chooser.get_filter().get_name()]
            chooser.destroy()
            self.export_file(filename, format_)
        else:
            chooser.destroy()
	

    def on_reload(self, action):
        self.dotwidget.reload()

    def error_dialog(self, message):
        dlg = Gtk.MessageDialog(parent=self,
                                type=Gtk.MessageType.ERROR,
                                message_format=message,
                                buttons=Gtk.ButtonsType.OK)
        dlg.set_title(self.base_title)
        dlg.run()
        dlg.destroy()

    def on_find_next(self, action):
        self.find_index += 1
        entry_text = self.textentry.get_text()
        # Maybe storing the search result would be better
        found_items = self.find_text(entry_text)
        found_item = found_items[self.find_index]
        self.dotwidget.animate_to(found_item.x, found_item.y)
        self.find_next_toolitem.set_sensitive(len(found_items) > self.find_index + 1)

    def on_history(self, action, has_back, has_forward):
        self.back_action.set_sensitive(has_back)
        self.forward_action.set_sensitive(has_forward)
