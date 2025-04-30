from ctypes import windll, wintypes, byref

import pywinauto

import threading
import asyncio
import time

from .utils import COORDS, RECT, InputEvent, PynputEvent


class WinController:
    def __init__(self, main_process: str = None, process_name: str = None, input_per_sec: int = 1):
        self.main_process: str = main_process
        self.process_name: str = process_name

        self.input_per_sec: int = input_per_sec
        self._refresh: float = 1 / self.input_per_sec

        self._run: bool = False
        self._focus: bool = False

        self.core: str = None

        self.app = None
        self.main_win = None

        self.test: str = "no"

        if main_process is not None:
            try:
                self.app = pywinauto.Application().connect(path=self.main_process)
            except Exception as e:
                print("WARNING", type(e), e)

        if process_name is not None:
            try:
                self.main_win = self.app[self.process_name]
                self._focus: bool = True
            except Exception as e:
                print("WARNING", type(e), e)

        self.actions: dict = {}
        self.last_buttons: list = [[], []]

        self._click_option: str = "on click"

        if self.main_win is not None:
            self.update_window()
            self.focus()

    def update_window(self):
        rect = self.main_win.rectangle()

        self.left, self.top, self.bottom, self.right, self.width, self.height, self.middle = rect.left, rect.top, rect.bottom, rect.right, rect.width(), rect.height(), rect.mid_point()
        self.windows = [self.left, self.top, self.width, self.height]
        self.rect = RECT(left=self.left, top=self.top, right=self.right, bottom=self.bottom, width=self.width, height=self.height)

    def to_image(self):
        return self.main_win.capture_as_image(self.main_win.rectangle())

    def get_cursor_pos(self):
        cursor = wintypes.POINT()
        windll.user32.GetCursorPos(byref(cursor))
        return COORDS(cursor.x, cursor.y)

    def get_capture(self, size: int, center: tuple = None):
        if isinstance(center, tuple) or isinstance(center, list):
            center: COORDS = COORDS(center[0], center[1])

        elif center is None:
            center: COORDS = self.get_cursor_pos()

        rect: RECT = RECT(width=size, middle=center)
        return self.main_win.capture_as_image(rect)

    def stop(self):
        self._run: bool = False
        self.release_all()

        if self.core == "pywinauto":
            if self.k_listener is not None:
                self.hook.unhook_keyboard()

            if self.m_listener is not None:
                self.hook.unhook_mouse()

        elif self.core == "pynput":
            if self.k_listener is not None:
                self.k_listener.stop()

            if self.m_listener is not None:
                self.m_listener.stop()

    def focus(self):
        if self._focus:
            self.main_win.set_focus()

    def type_keys(self, keys: str, pause=None, with_spaces: bool = False, with_tabs: bool = False, with_newlines: bool = False, turn_off_numlock: bool = True, set_foreground: bool = True, vk_packet: bool = True):
        self.focus()
        self.main_win.type_keys(keys=keys, pause=pause, with_spaces=with_spaces, with_tabs=with_tabs, with_newlines=with_newlines, turn_off_numlock=turn_off_numlock, set_foreground=set_foreground, vk_packet=vk_packet)

    def press(self, button: str = None, action: str = None):
        if action is not None:
            button: str = self.get_button(action)

        if button == button.upper() or len(button) == 1:
            self.type_keys("{" + f"{button} down" + "}")

        else:
            self.type_keys(button)

    def release(self, button: str = None, action: str = None):
        if action is not None:
            button: str = self.get_button(action)

        if button == button.upper() or len(button) == 1:
            self.type_keys("{" + f"{button} up" + "}")

    def release_all(self):
        for v in self.actions.values():
            if "CLICK" in v:
                self.release_cursor(v.split("_")[-1].lower())
                continue

            self.release(v)

    def get_button(self, action: str):
        return self.actions.get(action.upper(), None)

    def move_cursor(self, x: int, y: int, key_pressed: str = ""):
        self.focus()
        self.main_win.move_mouse_input(coords=(x, y), pressed=key_pressed, absolute=False)

    def drag_cursor(self, x: int, y: int, button: str = "left", key_pressed: str = ""):
        self.focus()
        self.main_win.drag_mouse_input(dst=(x, y), button=button, pressed=key_pressed, absolute=False)

    def click(self, button: str = "left", double: bool = False, coords: tuple = (None, None)):
        self.focus()
        self.main_win.click_input(button=button, double=double, coords=coords)

    def press_cursor(self, button: str = "left", coords: tuple = (None, None), key_pressed: str = ""):
        self.focus()
        self.main_win.press_mouse_input(button=button, coords=coords, pressed=key_pressed, absolute=False)

    def release_cursor(self, button: str = "left", coords: tuple = (None, None), key_pressed: str = ""):
        self.focus()
        self.main_win.release_mouse_input(button=button, coords=coords, pressed=key_pressed, absolute=False)

    def client_to_screen(self, client_point):
        self.main_win.client_to_screen(client_point)

    def do(self, actions: list = [], buttons: list = [], coords: tuple = (None, None)):
        self.last_buttons[1]: list = self.last_buttons[0]
        undo: list = []

        if actions == [] and buttons == []:
            return

        elif buttons != []:
            pass

        elif isinstance(actions, list):
            for action in actions:
                buttons.append(self.get_button(action))

        elif isinstance(actions, str):
            buttons.append(self.get_button(actions))
            actions: list = [actions]

        for button in self.last_buttons[1]:
            if button not in buttons:
                undo.append(button)

        self.undo(buttons=undo)

        self.last_buttons[0]: list = buttons.copy()

        for button in buttons:
            if button is None:
                continue

            if button in self.last_buttons[1]:
                continue

            if "CLICK" in button:
                button: str = button.split("_")[-1].lower()
                self.click(button=button, coords=coords)
                continue

            self.press(button)

        actions.clear()
        buttons.clear()

    def undo(self, actions: list = [], buttons: list = [], coords: tuple = (None, None)):
        if actions == [] and buttons == []:
            return

        elif buttons != []:
            pass

        elif isinstance(actions, list):
            for action in actions:
                buttons.append(self.get_button(action))

        elif isinstance(actions, str):
            buttons.append(self.get_button(actions))
            actions: list = [actions]

        for button in buttons:
            if button is None:
                continue

            if "CLICK" in button:
                button: str = button.split("_")[-1].lower()
                self.release_cursor(button=button, coords=coords)
                continue

            self.release(button)

            if button in self.last_buttons[1]:
                self.last_buttons[1].remove(button)

        actions.clear()
        buttons.clear()

    async def _run_async_update(self):
        await asyncio.sleep(.01)

        while self._run:
            await self._to_call_update()
            await asyncio.sleep(self._refresh)

    def _run_sync_update(self):
        time.sleep(.01)

        while self._run:
            self._to_call_update()
            time.sleep(self._refresh)

    def _check_run_update(self, run_async: bool = True):
        if not self._run:
            self._run: bool = True

            if run_async:
                self.start_async_thread(self._run_async_update())

            else:
                threading.Thread(target=self._run_sync_update).start()

    # https://gist.github.com/ultrafunkamsterdam/8be3d55ac45759aa1bd843ab64ce876d#file-python-3-6-asyncio-multiple-async-event-loops-in-multiple-threads-running-and-shutting-down-gracefully-py-L15
    def create_bg_loop(self):
        def to_bg(loop):
            asyncio.set_event_loop(loop)

            try:
                loop.run_forever()

            except asyncio.CancelledError as e:
                print('CANCELLEDERROR {}'.format(e))

            finally:
                for task in asyncio.Task.all_tasks():
                    task.cancel()

                loop.run_until_complete(loop.shutdown_asyncgens())
                loop.stop()
                loop.close()

        new_loop = asyncio.new_event_loop()
        t = threading.Thread(target=to_bg, args=(new_loop,))
        t.start()
        return new_loop


    def start_async_thread(self, awaitable):
        # old
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        threading.Thread(target=loop.run_forever).start()
        """
        # new
        loop = self.create_bg_loop()

        coro = asyncio.run_coroutine_threadsafe(awaitable, loop)
        return loop, coro

    def stop_async_thread(self, loop):
        loop.call_soon_threadsafe(loop.stop)

    def on_update(self, callback: callable = None):
        def add_debug(func):
            self._check_run_update(asyncio.iscoroutinefunction(func))
            self._to_call_update: callable = func
            return func

        if callable(callback):
            return add_debug(callback)

        return add_debug

    def on_event1(self, data):
        data: InputEvent = InputEvent(data, self.get_cursor_pos())
        return self._to_call_event(data)

    def on_move(self, x, y):
        data = PynputEvent(x=x, y=y, event_input="mouse", event_type="on move")
        self._to_call_event(data)

    def on_click(self, x, y, button, pressed):
        if pressed and self._click_option in ["on press", "on click"]:
            data = PynputEvent(x=x, y=y, button=button, pressed=pressed, event_input="mouse", event_type="on click")
            self._to_call_event(data)

        if not pressed and self._click_option in ["on release", "on click"]:
            data = PynputEvent(x=x, y=y, button=button, pressed=pressed, event_input="mouse", event_type="on click")
            self._to_call_event(data)

    def on_scroll(self, x, y, dx, dy):
        data = PynputEvent(x=x, y=y, dx=dx, dy=dy, event_input="mouse", event_type="on scroll")
        self._to_call_event(data)

    def on_press(self, key):
        data = PynputEvent(key=key, event_input="keyboard", cursor_pos=self.get_cursor_pos(), event_type="key down")
        self._to_call_event(data)

    def on_release(self, key):
        data = PynputEvent(key=key, event_input="keyboard", cursor_pos=self.get_cursor_pos(), event_type="key up")
        self._to_call_event(data)

    def on_input(self, callback: callable = None, keyboard: dict = {"on press": True, "on release": False}, mouse: dict = {"on move": False, "on click": True, "on scroll": False}, core: str = "pynput"):
        if isinstance(callback, bool):
            keyboard: bool = callback
            callback = None

        self.core: str = core

        if core == "pywinauto":
            import pywinauto.win32_hooks

            self.k_listener: bool = True if True in keyboard.values() else False
            self.m_listener: bool = True if True in mouse.values() else False

            self.hook = pywinauto.win32_hooks.Hook()

            def add_event1(func):
                self._to_call_event: callable = func
                self.hook.handler = self.on_event1
                threading.Thread(target=self.hook.hook, kwargs={"keyboard": self.k_listener, "mouse": self.m_listener}).start()
                # self.hook.hook(keyboard=keyboard, mouse=mouse)
                return func

            if callable(callback):
                return add_event1(callback)

            return add_event1

        elif core == "pynput":
            self.k_listener = None
            self.m_listener = None

            if keyboard:
                import pynput.keyboard

                if keyboard == True:
                    keyboard: dict = {"on press": True, "on release": True}

                self.k_listener = pynput.keyboard.Listener(
                    on_press=self.on_press if keyboard.get("on press") else None,
                    on_release=self.on_release if keyboard.get("on release") else None
                )

                self.k_listener.start()

            if mouse:
                import pynput.mouse

                if mouse == True:
                    mouse: dict = {"on move": False, "on click": True, "on scroll": False}

                if mouse.get("on click"):
                    self._click_option: str = "on click"
                    mouse["on click"] = True

                elif mouse.get("on press"):
                    self._click_option: str = "on press"
                    mouse["on click"] = True

                elif mouse.get("on release"):
                    self._click_option: str = "on release"
                    mouse["on click"] = True

                self.m_listener = pynput.mouse.Listener(
                    on_move=self.on_move if mouse.get("on move") else None,
                    on_click=self.on_click if mouse.get("on click") else None,
                    on_scroll=self.on_scroll if mouse.get("on scroll") else None
                )

                self.m_listener.start()

            def add_event2(func):
                self._to_call_event: callable = func

                if self.k_listener is not None:
                    self.k_listener.join()

                if self.m_listener is not None:
                    self.m_listener.join()

            if callable(callback):
                return add_event2(callback)

            return add_event2
