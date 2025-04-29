import pywinauto.win32_hooks


class COORDS:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y


class RECT():
    def __init__(self, left: int = None, top: int = None, right: int = None, bottom: int = None, width: int = None, height: int = None, middle: COORDS = None):
        _left: int = None
        _top: int = None

        if height is None and width:
            height: int = width

        elif width is None and height:
            width: int = height

        if middle is not None:
            _left: int = middle.x - width // 2
            _top: int = middle.y - height // 2

        self.left: int = left if left is not None else _left
        self.top: int = top if top is not None else _top

        if not self.left or not self.top:
            raise "Error, set at least a width or height with center"

        if right is not None:
            self.right: int = right

        elif width is not None:
            self.right: int = self.left + width

        else:
            raise "Error, set at least right, width or center"

        if bottom is not None:
            self.bottom: int = bottom

        elif width is not None:
            self.bottom: int = self.top + height

        else:
            raise "Error, set at least bottom, width or center"

        self._width: int = width if width is not None else self.width()
        self._height: int = height if height is not None else self.height()
        self._middle: COORDS = self.mid_point()

    def width(self):
        return abs(self.right-self.left)

    def height(self):
        return abs(self.bottom-self.top)

    def mid_point(self):
        x: int = self.left + int(float(self._width) / 2.)
        y: int = self.top + int(float(self._height) / 2.)
        return COORDS(x, y)


class InputEvent:
    def __init__(self, event, cursor_pos: COORDS):
        self.event = event
        self.current_key: str = event.current_key
        self.event_type: str = event.event_type
        self.x, self.y = cursor_pos.x, cursor_pos.y

        if isinstance(event, pywinauto.win32_hooks.KeyboardEvent):
            self.event_input: str = "keyboard"
            self.pressed_key: list = event.pressed_key
            self.mouse_x: int = self.x
            self.mouse_y: int = self.y

        if isinstance(event, pywinauto.win32_hooks.MouseEvent):
            self.event_input: str = "mouse"
            self.mouse_x: int = event.mouse_x
            self.mouse_y: int = event.mouse_y
            self.pressed_key = None


class PynputEvent:
    def __init__(self, x: int = None, y: int = None, button: str = None, pressed: bool = None, key: str = None, event_input: str = None, event_type: str = None, cursor_pos: COORDS=None):
        self.x: int = x if x is not None else cursor_pos.x
        self.y: int = y if y is not None else cursor_pos.y
        self.current_key: str = button if button is not None else key

        self.button: str = button
        self.key: str = key

        self.event_input: str = event_input
        self.event_type: str = event_type
        self.pressed_key: list = [button] if button is not None else [key]

        self.pressed: bool = pressed

        if event_type == "on click" and pressed == False:
            self.event_type: str = "key up"

        elif event_type == "on click" and pressed == True:
            self.event_type: str = "key down"
