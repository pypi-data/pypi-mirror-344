"""
extended kivy file chooser widget
=================================

this ae namespace portion provides the :class:`FileChooserPopup` widget (`chooser_popup`) which is embedding Kivy's
:class:`~kivy.uix.filechooser.FileChooser` class in a dropdown window (:class:`~ae.kivy.widgets.FlowDropDown`), and
extending it with a path selector and a button to switch between list and icon view.


file chooser dropdown usage
---------------------------

the :class:`FileChooserPopup` widget can be used like any :class:`Kivy DropDown widget <kivy.uix.dropdown.DropDown>` -
see the python and kv lang examples in the doc strings of the :mod:`~kivy.uix.dropdown` module. Additionally, all the
features of the :class:`~ae.kivy.widgets.FlowDropDown` like e.g., the
:attr:`~ae.kivy_dyn_chi.DynamicChildrenBehavior.child_data_maps` are available.

alternatively (and without the need to explicitly instantiate the file chooser dropdown widget) you simply have to
:meth:`change the application flow <ae.gui.utils.change_flow>` to `id_of_flow('open', 'file_chooser')` to open this
file chooser (see also the section :ref:`application flow`)::

    main_app.change_flow(id_of_flow('open', 'file_chooser'),
                         **update_tap_kwargs(open_button))

the variable `open_button` in this example represents a button widget instance that opens the file chooser dropdown (and
to which the file chooser gets attached to).

use the :attr:`~FileChooserPopup.submit_to` property to distinguish multiple usages of the file chooser in a single
app::

    main_app.change_flow(id_of_flow('open', 'file_chooser'),
                         **update_tap_kwargs(open_button,
                                             popup_kwargs=dict(submit_to=submit_to_str_or_callable))

the variable `submit_to_str_or_callable` of the above example can be either a string or a callable. if you pass a
callable, :class:`FileChooserPopup` will call it if the user has selected a file (by touching or double-clicking on a
file entry). this callback receives two arguments: the file path of the just selected file and the :class:`FileChooser`
dropdown widget instance and can be declared like::

    def submit_to_callable(file_path: str, chooser_popup: Widget):

passing a string to `submit_to` (or if it gets not specified at all), the hard-coded `on_file_chooser_submit` event
handler callback method of your main app instance will be executed with the same two arguments::

    def on_file_chooser_submit(self, file_path: str, chooser_popup: Widget):
        if chooser_popup.submit_to == 'usage1':
            usage1_object_or_process.file_path = file_path
            chooser_popup.dismiss()
        elif chooser_popup.submit_to == 'usage2':
            ...
        elif chooser_popup.submit_to == '': # w/o specifying `submit_to`
            ...

use the key of the :attr:`~ae.kivy.widgets.FlowButton.tap_flow_id` property of the :class:`~ae.kivy.widgets.FlowButton`
to provide a separate i18n help text for each individual button.

the :attr:`~FileChooserPopup.filters` property of Kivy's :class:`kivy.uix.filechooser.FileChooser` can be used
to filter the files displayed in this file chooser widget.

the path selector dropdown (:class:`FileChooserPathSelectPopup`) situated at the top of this file chooser dropdown
is providing all common OS and app specific paths that are registered in the :data:`~ae.paths.PATH_PLACEHOLDERS` dict.
the keys of this dict will be displayed as shortcut path names instead of the full path strings. Additionally,
translation texts can be provided for the shortcut path names to display them in the language selected by the app user.

to extend the path selector dropdown with additional paths, you can either register them within
:data:`~ae.paths.PATH_PLACEHOLDERS`, or you add them to the optional app state variable `file_chooser_paths` by calling
the method :meth:`~FileChooserPopup.register_file_path`.

by adding the list `file_chooser_paths` to the :ref:`app state variables` of your app, the paths provided by the path
selector widget will automatically maintain and keep the OS and user paths persistent between app runs.

to record and remember the last selected path, add also the app state `file_chooser_initial_path` to the
`:ref:`app state variables` of your app.

override the method :meth:`~ae.console.ConsoleApp._init_default_user_cfg_vars` within the main app instance of your app
to make these two persistent :ref:`app state variables` user-specific::

    def _init_default_user_cfg_vars(self):
        super()._init_default_user_cfg_vars()
        self.user_specific_cfg_vars |= {
            (APP_STATE_SECTION_NAME, 'file_chooser_initial_path'),
            (APP_STATE_SECTION_NAME, 'file_chooser_paths'),
        }

.. hint::
    you don't need to override :meth:`~ae.console.ConsoleApp._init_default_user_cfg_vars` if your app is embedding the
    ae portion :mod:`ae.kivy_sideloading`.
"""
import os
from typing import Any, List

from kivy.app import App                                    # type: ignore
from kivy.lang import Builder                               # type: ignore
from kivy.properties import (                               # type: ignore # pylint: disable=no-name-in-module
    ListProperty, ObjectProperty, StringProperty)
from kivy.uix.widget import Widget                          # type: ignore

from ae.base import norm_path                               # type: ignore
from ae.kivy.widgets import FlowDropDown                    # type: ignore


__version__ = '0.3.13'


Builder.load_string('''\
#: import os os
<FileChooserPopup>
    do_scroll_x: True
    do_scroll_y: False
    on_initial_path: app.main_app.change_app_state('file_chooser_initial_path', self.initial_path)
    auto_width_minimum: min(Window.width * 0.96, app.app_states['font_size'] * 24)
    BoxLayout:
        size_hint_y: None
        height: app.app_states['font_size'] * 1.8
        padding: sp(3), 0, sp(3), sp(-9)  # negative bottom spacing to see top border of pathSel dropdown?!?!?
        spacing: sp(3)
        FlowButton:
            tap_flow_id: id_of_flow('select', 'file_chooser_path', root.initial_path)
            tap_kwargs: update_tap_kwargs(self)
            text: path_name(root.initial_path) and _(path_name(root.initial_path)) or root.initial_path
            text_size: self.width, None
            halign: 'center'
            shorten: True
            shorten_from: 'left'
            relief_square_inner_colors: relief_colors((1, 1, 0))
            relief_square_inner_lines: int(sp(6))
        FlowToggler:
            tap_flow_id: id_of_flow('toggle', 'file_chooser_view')
            tap_kwargs: update_tap_kwargs(self)
            icon_name: chooser_widget.view_mode + "_view"
            on_state: chooser_widget.view_mode = 'icon' if self.state == 'down' else 'list'
            size_hint_x: None
            width: self.height
    FileChooser:
        id: chooser_widget
        filters: root.filters
        multiselect: True
        path: root.initial_path
        show_hidden: True
        size_hint_y: None
        height: (root.attach_to.top if root.attach_to else Window.height) * 0.96 - app.main_app.font_size * 3.0
        on_selection:
            args[1] and \
            (root.submit_to if callable(root.submit_to) else app.main_app.on_file_chooser_submit)(args[1][-1], root)
        on_entry_added: root.on_file_chooser_entry_added(args[1])
        on_subentry_to_entry: root.on_file_chooser_entry_added(args[1])
        FileChooserListLayout
        FileChooserIconLayout

<FileChooserPathSelectPopup>
    paths:
        [normalize(path) for path in set(list(PATH_PLACEHOLDERS.values()) + app.app_states['file_chooser_paths']) \
        if os.path.exists(normalize(path)) and os.path.isdir(normalize(path))]
    on_paths: app.main_app.change_app_state('file_chooser_paths', list(self.paths))
    on_select: self.attach_to.parent.parent.parent.initial_path = args[1]
    child_data_maps:
        [dict(cls='FlowButton', kwargs=dict( \
        text=_(path_name(path)) + (" (" + path + ")" if app.landscape else "") if path_name(path) else path, \
        tap_flow_id=id_of_flow('change', 'file_chooser_path', path), \
        on_release=lambda btn: self.select(flow_key(btn.tap_flow_id)))) \
        for path in self.paths]
''')


class FileChooserPopup(FlowDropDown):
    """ file chooser DropDown container. """
    initial_path = StringProperty(".")  #: initial file path displayed on opening
    submit_to = ObjectProperty("")      #: callable or string to identify which action/part requested the selected file
    filters = ListProperty()            #: see :attr:`kivy.uix.filechooser.FileChooser.filters`.

    @staticmethod
    def on_file_chooser_entry_added(view_entries: List[Widget]):
        """ on_entry_added/on_subentry_to_entry event handler to patch theme-related properties of Kivy FileChooser.

        :param view_entries:    list of view entries for a node (icon or label) of the file chooser.

        .. note::
            this method gets called for each node when a file entry widget (FileListEntry or FileIconEntry)
            gets added to an instance of Kivy's :class:`~kivy.uix.filechooser.FileChooser` widget class.

            therefore, the patches done here are not affected if the user preferences (e.g., the font size or light/dark
            theme) get changed while a file chooser instance is displayed. in this case the user has to simply close
            and reopen/re-instantiate the file chooser to display the nodes with the just changed user preferences.

            theme adaption is still missing for the file chooser progress: all font sizes and colors of the currently
            used :class:`~kivy.uix.filechooser.FileChooserProgressBase` are hard-coded, so a theme-aware progress class
            has to be implemented (and assigned to the :attr:`~kivy.uix.filechooser.FileChooserController.progress_cls`
            property).

        """
        app = App.get_running_app()
        font_color = app.font_color
        font_size = app.app_states['font_size']
        sel_color = app.app_states['selected_ink']
        for entry in view_entries:
            if 'FileListEntry' in str(entry):               # isinstance(entry, Factory.FileListEntry) -> TypeError
                box, entry = entry, entry.children[0]       # entry is a BoxLayout
                # box.children[0].children[1] is box.ids.filename
                box.color_selected = sel_color
                entry.children[1].color = font_color        # children[1] is a file name label
                entry.children[1].font_size = min(box.height * 0.87, font_size)
                entry.children[0].color = font_color        # children[0] is a file size label
                entry.children[0].font_size = min(box.height * 0.69, font_size)

            elif 'FileIconEntry' in str(entry):             # TypeError if using isinstance()
                entry.children[1].color = font_color
                entry.children[1].font_size = min(entry.children[1].height * 0.99, font_size)
                entry.children[0].color = font_color
                entry.children[0].font_size = min(entry.children[0].height * 0.90, font_size)

    @staticmethod
    def register_file_path(file_path: str, main_app: Any):
        """ set the folder of the passed file path as the new initial path and add it to path history.

        :param file_path:       file path (mostly the last just selected file) of which the folder will be registered.
        :param main_app:        main app instance.
        """
        folder = os.path.dirname(norm_path(file_path))
        main_app.change_app_state('file_chooser_initial_path', folder)
        if folder not in main_app.file_chooser_paths:
            main_app.file_chooser_paths.insert(0, folder)
            main_app.change_app_state('file_chooser_paths', main_app.file_chooser_paths)


class FileChooserPathSelectPopup(FlowDropDown):
    """ file chooser path selector dropdown. """
    paths = ListProperty()                      #: list of file paths in the path selection dropdown
