import gi
import json
import os
import re
import sys
import time
import locale
import gettext
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, Gdk, GLib

from llm_client import LLMClient, DEFAULT_CONVERSATION_NAME
from widgets import Message, MessageWidget, ErrorWidget
from db_operations import ChatHistory
from chat_application import _

# Define APP_NAME and LOCALE_DIR here as well
APP_NAME = "gtk-llm-chat"
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # Running in a PyInstaller bundle
    base_dir = sys._MEIPASS
    LOCALE_DIR = os.path.join(base_dir, 'po')
else:
    # Running in a normal Python environment
    # Adjust path relative to this file's location
    base_dir = os.path.dirname(__file__)
    LOCALE_DIR = os.path.abspath(os.path.join(base_dir, '..', 'po'))

DEBUG = False


def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


class LLMChatWindow(Adw.ApplicationWindow):
    """
    A chat window
    """

    def __init__(self, config=None, chat_history=None, **kwargs):
        super().__init__(**kwargs)

        # Re-initialize gettext context for this window instance
        try:
            locale.setlocale(locale.LC_MESSAGES, '')  # Ensure locale is set
        except Exception as e:
            debug_print(f"Warning: Could not set locale: {e}")  # Use print directly as _ might not be ready
        gettext.bindtextdomain(APP_NAME, LOCALE_DIR)
        gettext.textdomain(APP_NAME)
        self._ = gettext.gettext  # Assign to instance variable

        self.insert_action_group('app', self.get_application())

        # Conectar señal de cierre de ventana
        self.connect('close-request', self._on_close_request)
        self.connect('show', self._on_window_show)  # Connect to the 'show' signal

        # Asegurar que config no sea None
        self.config = config or {}
        # Store benchmark flag and start time from config
        self.benchmark_startup = self.config.get('benchmark_startup', False)
        self.start_time = self.config.get('start_time')

        # Use the passed chat_history or create one if not provided (fallback)
        if chat_history:
            self.chat_history = chat_history
        else:
            debug_print(
                "Warning: chat_history not provided to LLMChatWindow, creating new instance.")
            self.chat_history = ChatHistory()

        # Inicializar LLMClient con la configuración
        # self.llm will be initialized later, after UI setup potentially
        self.llm = None

        # Configurar la ventana principal
        title = self.config.get('template') or DEFAULT_CONVERSATION_NAME()
        self.title_entry = Gtk.Entry()
        self.title_entry.set_hexpand(True)
        self.title_entry.set_text(title)
        self.title_entry.connect('activate', self._on_save_title)

        focus_controller = Gtk.EventControllerKey()
        focus_controller.connect("key-pressed", self._cancel_set_title)
        self.title_entry.add_controller(focus_controller)

        # Add a key controller for Ctrl+W
        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self._on_ctrl_w_pressed)
        self.add_controller(key_controller)

        self.set_default_size(400, 600)

        # Mantener referencia al último mensaje enviado
        self.last_message = None

        # Crear header bar
        self.header = Adw.HeaderBar()
        self.title_widget = Adw.WindowTitle.new(title, self._("LLM Chat"))
        self.header.set_title_widget(self.title_widget)
        self.set_title(title)  # Set window title based on initial title

        # Botón de menú
        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")

        # Crear menú
        menu = Gio.Menu.new()
        menu.append(self._("Delete"), "app.delete")
        menu.append(self._("About"), "app.about")

        # Crear un popover para el menú
        #popover = Gtk.PopoverMenu()
        #menu_button.set_popover(popover)
        #popover.set_menu_model(menu)
        menu_button.set_menu_model(menu)

        # Rename button
        rename_button = Gtk.Button()
        rename_button.set_icon_name("document-edit-symbolic")
        rename_button.connect('clicked',
                              lambda x: self.get_application()
                              .on_rename_activate(None, None))

        self.header.pack_end(menu_button)
        self.header.pack_end(rename_button)

        # Contenedor principal
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.append(self.header)

        # Contenedor para el chat
        chat_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        # ScrolledWindow para el historial de mensajes
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        # Contenedor para mensajes
        self.messages_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.messages_box.set_margin_top(12)
        self.messages_box.set_margin_bottom(12)
        self.messages_box.set_margin_start(12)
        self.messages_box.set_margin_end(12)
        # Desactivar la selección en la lista de mensajes
        self.messages_box.set_can_focus(False)
        scroll.set_child(self.messages_box)

        # Área de entrada
        input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        input_box.set_margin_top(6)
        input_box.set_margin_bottom(6)
        input_box.set_margin_start(6)
        input_box.set_margin_end(6)

        # TextView para entrada
        self.input_text = Gtk.TextView()
        self.input_text.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.input_text.set_pixels_above_lines(3)
        self.input_text.set_pixels_below_lines(3)
        self.input_text.set_pixels_inside_wrap(3)
        self.input_text.set_hexpand(True)

        # Configurar altura dinámica
        buffer = self.input_text.get_buffer()
        buffer.connect('changed', self._on_text_changed)

        # Configurar atajo de teclado Enter
        key_controller = Gtk.EventControllerKey()
        key_controller.connect('key-pressed', self._on_key_pressed)
        self.input_text.add_controller(key_controller)

        # Botón enviar
        self.send_button = Gtk.Button(label=self._("Send"))
        self.send_button.connect('clicked', self._on_send_clicked)
        self.send_button.add_css_class('suggested-action')

        # Ensamblar la interfaz
        input_box.append(self.input_text)
        input_box.append(self.send_button)

        chat_box.append(scroll)
        chat_box.append(input_box)

        main_box.append(chat_box)

        self.set_content(main_box)

        # Agregar CSS provider
        self._setup_css()

        # Agregar soporte para cancelación
        self.current_message_widget = None
        self.accumulated_response = ""

        # Initialize LLMClient *after* basic UI setup
        try:
            self.llm = LLMClient(self.config, self.chat_history)
            # Connect signals *here*
            self.llm.connect('model-loaded', self._on_model_loaded)  # Ensure this is connected
            self.llm.connect('response', self._on_llm_response)
            self.llm.connect('error', self._on_llm_error)
            self.llm.connect('finished', self._on_llm_finished)
        except Exception as e:
            debug_print(_(f"Fatal error starting LLMClient: {e}"))
            # Display error in UI instead of exiting?
            error_widget = ErrorWidget(f"Fatal error starting LLMClient: {e}")
            self.messages_box.append(error_widget)
            self.set_enabled(False)  # Disable input if LLM fails critically
            # Optionally: sys.exit(1) if it should still be fatal

        # Add a focus controller to the window
        focus_controller = Gtk.EventControllerFocus.new()
        focus_controller.connect("enter", self._on_focus_enter)
        self.add_controller(focus_controller)

    def _setup_css(self):
        css_provider = Gtk.CssProvider()
        data = """
            .message {
                padding: 8px;
            }

            .message-content {
                padding: 6px;
                min-width: 400px;
            }

            .user-message .message-content {
                background-color: @blue_3;
                border-radius: 12px 12px 0 12px;
            }

            .assistant-message .message-content {
                background-color: @card_bg_color;
                border-radius: 12px 12px 12px 0;
            }

            .timestamp {
                font-size: 0.8em;
                opacity: 0.7;
            }

            .error-message {
                background-color: alpha(@error_color, 0.1);
                border-radius: 6px;
                padding: 8px;
            }

            .error-icon {
                color: @error_color;
            }

            .error-content {
                padding: 3px;
            }

            textview {
                background: none;
                color: inherit;
                padding: 3px;
            }

            textview text {
                background: none;
            }

            .user-message textview text {
                color: white;
            }

            .user-message textview text selection {
                background-color: rgba(255,255,255,0.3);
                color: white;
            }
        """
        css_provider.load_from_data(data, len(data))

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def set_conversation_name(self, title):
        """Establece el título de la ventana"""
        self.title_widget.set_title(title)
        self.title_entry.set_text(title)
        self.set_title(title)

    def _on_save_title(self, widget):
        app = self.get_application()
        conversation_id = self.config.get('cid')
        if conversation_id:
            app.chat_history.set_conversation_title(
            conversation_id, self.title_entry.get_text())
        else:
            debug_print("Conversation ID is not available yet. Title update deferred.")
            # Schedule the title update for the next prompt
            def update_title_on_next_prompt(llm_client, response):
                conversation_id = self.config.get('cid')
                print("Conversation ID:", conversation_id)
                if conversation_id:
                    app.chat_history.set_conversation_title(
                    conversation_id, self.title_entry.get_text())
                    self.llm.disconnect_by_func(update_title_on_next_prompt)
            self.llm.connect('response', update_title_on_next_prompt)
        self.header.set_title_widget(self.title_widget)
        new_title = self.title_entry.get_text()

        self.title_widget.set_title(new_title)
        self.set_title(new_title)


    def _cancel_set_title(self, controller, keyval, keycode, state):
        """Cancela la edición y restaura el título anterior"""
        if keyval == Gdk.KEY_Escape:
            self.header.set_title_widget(self.title_widget)
            self.title_entry.set_text(self.title_widget.get_title())

    def _on_ctrl_w_pressed(self, controller, keyval, keycode, state):
        """Handles Ctrl+W to remove the conversation."""
        if keyval == Gdk.KEY_w and state & Gdk.ModifierType.CONTROL_MASK:
            app = self.get_application()
            app.on_delete_activate(None, None)
            return True
        return False

    def set_enabled(self, enabled):
        """Habilita o deshabilita la entrada de texto"""
        self.input_text.set_sensitive(enabled)
        self.send_button.set_sensitive(enabled)

    def _on_text_changed(self, buffer):
        lines = buffer.get_line_count()
        # Ajustar altura entre 3 y 6 líneas
        new_height = min(max(lines * 20, 60), 120)
        self.input_text.set_size_request(-1, new_height)

    def _on_key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Return:
            # Permitir Shift+Enter para nuevas líneas
            if not (state & Gdk.ModifierType.SHIFT_MASK):
                self._on_send_clicked(None)
                return True
        return False

    def display_message(self, content, sender="user"):
        """
        Displays a message in the chat window.

        Args:
            content (str): The text content of the message.
            sender (str): The sender of the message ("user" or "assistant").
        """
        message = Message(content, sender)

        if sender == "user":
            self.last_message = message
            # Clear the input buffer after sending a user message
            buffer = self.input_text.get_buffer()
            buffer.set_text("", 0)

        # Create the message widget
        message_widget = MessageWidget(message)

        # Connect to the 'map' signal to scroll *after* the widget is shown
        def scroll_on_map(widget, *args):
            # Use timeout_add to ensure scrolling happens after a short delay
            def do_scroll():
                self._scroll_to_bottom(True) # Force scroll
                return GLib.SOURCE_REMOVE # Run only once
            GLib.timeout_add(50, do_scroll) # Delay of 50ms
            # Return False because we are using connect_after
            return False

        # Use connect_after for potentially better timing
        signal_id = message_widget.connect_after('map', scroll_on_map)

        # Add the widget to the box
        self.messages_box.append(message_widget)

        return message_widget

    def _on_model_loaded(self, llm_client, model_name):
        """Updates the window subtitle with the model name."""
        self.title_widget.set_subtitle(model_name)
        # Save the model name to the chat history
        cid = self.config.get('cid') or llm_client.get_conversation_id()
        if cid:
            if not self.config.get('cid'):
                self.config['cid'] = cid
                debug_print(f"Conversation ID set in config: {cid}")
            try:
                self.chat_history.create_conversation_if_not_exists(
                    cid,
                    DEFAULT_CONVERSATION_NAME(),
                    model_name
                )
            except Exception as e:
                debug_print(f"Error creando la conversación en BD: {e}")

    def _on_send_clicked(self, button):
        buffer = self.input_text.get_buffer()
        text = buffer.get_text(
            buffer.get_start_iter(), buffer.get_end_iter(), True
        )

        if text:
            # Display user message
            self.display_message(text, sender="user")
            # Deshabilitar entrada y empezar tarea LLM
            self.set_enabled(False)
            # NEW: Crear el widget de respuesta aquí
            self.current_message_widget = self.display_message("", sender="assistant")
            # Call _on_llm_response with an empty string to update the widget
            self._on_llm_response(self.llm, "")
            GLib.idle_add(self._start_llm_task, text)

    def _start_llm_task(self, prompt_text):
        """Inicia la tarea del LLM con el prompt dado."""
        # Enviar el prompt usando LLMClient
        self.llm.send_message(prompt_text)

        # Devolver False para que idle_add no se repita
        return GLib.SOURCE_REMOVE

    def _on_llm_error(self, llm_client, message):
        """Muestra un mensaje de error en el chat"""
        debug_print(message, file=sys.stderr)
        # Verificar si el widget actual existe y es hijo del messages_box
        if self.current_message_widget is not None:
            is_child = (self.current_message_widget.get_parent() ==
                        self.messages_box)
            # Si es hijo, removerlo
            if is_child:
                self.messages_box.remove(self.current_message_widget)
                self.current_message_widget = None
        if message.startswith("Traceback"):
            message = message.split("\n")[-2]
            # Let's see if we find some json in the message
            try:
                match = re.search(r"{.*}", message)
                if match:
                    json_part = match.group()
                    error = json.loads(json_part.replace("'", '"')
                                                .replace('None', 'null'))
                    message = error.get('error').get('message')
            except json.JSONDecodeError:
                pass
        error_widget = ErrorWidget(message)
        self.messages_box.append(error_widget)
        self._scroll_to_bottom()

    def _on_llm_finished(self, llm_client, success: bool):
        """Maneja la señal 'finished' de LLMClient."""
        self.set_enabled(True)
        self.accumulated_response = ""
        self.input_text.grab_focus()

        # Actualizar el conversation_id en la configuración si no existe
        if success and not self.config.get('cid'):
            conversation_id = self.llm.get_conversation_id()
            if conversation_id:
                self.config['cid'] = conversation_id
                debug_print(f"Conversation ID updated in config: {conversation_id}")

    def _on_llm_response(self, llm_client, response):
        """Maneja la señal de respuesta del LLM"""
        if not self.current_message_widget:
            return

        # Actualizar el conversation_id en la configuración al recibir la primera respuesta
        if not self.config.get('cid'):
            conversation_id = self.llm.get_conversation_id()
            if conversation_id:
                self.config['cid'] = conversation_id
                debug_print(f"Conversation ID updated early in config: {conversation_id}")

        self.accumulated_response += response
        GLib.idle_add(self.current_message_widget.update_content,
                      self.accumulated_response)
        GLib.idle_add(self._scroll_to_bottom, False)

    def _scroll_to_bottom(self, force=True):
        scroll = self.messages_box.get_parent()
        adj = scroll.get_vadjustment()
        upper = adj.get_upper()
        page_size = adj.get_page_size()
        value = adj.get_value()

        bottom_distance = upper - (value + page_size)
        threshold = page_size * 0.1  # 10% del viewport

        if force:
            adj.set_value(upper - page_size)
            return

        if bottom_distance < threshold:
            def scroll_after():
                adj.set_value(upper - page_size)
                return False
            GLib.timeout_add(50, scroll_after)

    def _on_close_request(self, window):
        """Maneja el cierre de la ventana de manera elegante"""
        self.llm.cancel()
        sys.exit()
        return False

    def _on_window_show(self, window):
        """Set focus to the input text when the window is shown."""
        # Handle benchmark startup
        if self.benchmark_startup and self.start_time:
            end_time = time.time()
            elapsed_time = end_time - self.start_time
            print(f"Startup time: {elapsed_time:.4f} seconds")
            # Use GLib.idle_add to exit after the current event loop iteration
            GLib.idle_add(self.get_application().quit)
            return  # Don't grab focus if we are exiting

        self.input_text.grab_focus()

    def _on_focus_enter(self, controller):
        """Set focus to the input text when the window gains focus."""
        self.input_text.grab_focus()
