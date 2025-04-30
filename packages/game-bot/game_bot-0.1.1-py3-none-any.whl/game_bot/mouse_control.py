import ctypes
import functools
import inspect
import time
import random
from typing import Tuple, Optional

# Constants for failsafe check and pause
FAILSAFE = True
FAILSAFE_POINTS = [(0, 0)]
PAUSE = 0.1  # Tenth-second pause by default

# Mouse Event Flags
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_HWHEEL = 0x1000

# Mouse Wheel Constants
WHEEL_DELTA = 120  # Default scroll step

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long),
                ("y", ctypes.c_long)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Function imports
SendInput = ctypes.windll.user32.SendInput
GetCursorPos = ctypes.windll.user32.GetCursorPos
SetCursorPos = ctypes.windll.user32.SetCursorPos

class MouseController:
    def __init__(self, speed_factor: float = 1.0, randomness: float = 0.2):
        """Initialize mouse controller with customizable speed and randomness.
        
        Args:
            speed_factor: Movement speed multiplier (1.0 = normal speed)
            randomness: Random variation factor (0.0 = no randomness, 1.0 = high randomness)
        """
        self.speed_factor = max(0.1, min(speed_factor, 5.0))  # Clamp between 0.1 and 5.0
        self.randomness = max(0.0, min(randomness, 1.0))    # Clamp between 0.0 and 1.0
    
    def get_cursor_pos(self) -> Tuple[int, int]:
        """Get current cursor position.
        
        Returns:
            Tuple of (x, y) coordinates.
        """
        point = POINT()
        GetCursorPos(ctypes.byref(point))
        return (point.x, point.y)
    
    def _add_random_offset(self, value: int) -> int:
        """Add random variation to a value."""
        if self.randomness == 0:
            return value
        max_offset = int(value * self.randomness)
        return value + random.randint(-max_offset, max_offset)
    
    def _get_random_delay(self, base_delay: float) -> float:
        """Get randomized delay based on speed factor."""
        delay = base_delay / self.speed_factor
        if self.randomness > 0:
            delay *= random.uniform(1 - self.randomness, 1 + self.randomness)
        return max(0.01, delay)  # Ensure minimum delay of 10ms
    
    def set_cursor_pos(self, x: int, y: int, smooth: bool = False) -> bool:
        """Move cursor to absolute position with optional smooth movement.
        
        Args:
            x: Target x-coordinate
            y: Target y-coordinate
            smooth: Whether to move smoothly to target position
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not smooth:
                extra = ctypes.c_ulong(0)
                ii_ = Input_I()
                ii_.mi = MouseInput(x, y, 0, MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, 0, ctypes.pointer(extra))
                x = Input(ctypes.c_ulong(0), ii_)
                SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
                return True
            
            start_x, start_y = self.get_cursor_pos()
            dx, dy = x - start_x, y - start_y
            distance = (dx * dx + dy * dy) ** 0.5
            steps = int(distance / 20) + 1  # One step per 20 pixels
            
            for i in range(1, steps + 1):
                factor = i / steps
                current_x = int(start_x + dx * factor)
                current_y = int(start_y + dy * factor)
                extra = ctypes.c_ulong(0)
                ii_ = Input_I()
                ii_.mi = MouseInput(current_x, current_y, 0, MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, 0, ctypes.pointer(extra))
                x = Input(ctypes.c_ulong(0), ii_)
                SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
                time.sleep(self._get_random_delay(0.01))
            return True
        except Exception:
            return False
    
    def move_relative(self, dx: int, dy: int, smooth: bool = False) -> bool:
        """Move cursor relative to current position.
        
        Args:
            dx: Change in x-coordinate
            dy: Change in y-coordinate
            smooth: Whether to move smoothly
            
        Returns:
            True if successful, False otherwise
        """
        try:
            x, y = self.get_cursor_pos()
            return self.set_cursor_pos(x + dx, y + dy, smooth)
        except Exception:
            return False
    
    def _click(self, down_flag: int, up_flag: int) -> bool:
        """Perform mouse click with specified events."""
        try:
            extra = ctypes.c_ulong(0)
            ii_ = Input_I()
            ii_.mi = MouseInput(0, 0, 0, down_flag, 0, ctypes.pointer(extra))
            x = Input(ctypes.c_ulong(0), ii_)
            SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
            time.sleep(self._get_random_delay(0.1))
            
            ii_.mi = MouseInput(0, 0, 0, up_flag, 0, ctypes.pointer(extra))
            x = Input(ctypes.c_ulong(0), ii_)
            SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
            return True
        except Exception:
            return False
    
    def left_click(self) -> bool:
        """Perform a left mouse click with randomized timing.
        
        Returns:
            True if successful, False otherwise
        """
        return self._click(MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP)
    
    def right_click(self) -> bool:
        """Perform a right mouse click with randomized timing.
        
        Returns:
            True if successful, False otherwise
        """
        return self._click(MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP)
    
    def middle_click(self) -> bool:
        """Perform a middle mouse click with randomized timing.
        
        Returns:
            True if successful, False otherwise
        """
        return self._click(MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP)
    
    def double_click(self) -> bool:
        """Perform a double left click with randomized timing.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.left_click():
                return False
            time.sleep(self._get_random_delay(0.1))
            return self.left_click()
        except Exception:
            return False
    
    def drag_to(self, x: int, y: int, smooth: bool = True) -> bool:
        """Drag from current position to target position.
        
        Args:
            x: Target x-coordinate
            y: Target y-coordinate
            smooth: Whether to move smoothly during drag
            
        Returns:
            True if successful, False otherwise
        """
        try:
            extra = ctypes.c_ulong(0)
            ii_ = Input_I()
            ii_.mi = MouseInput(0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, ctypes.pointer(extra))
            x_input = Input(ctypes.c_ulong(0), ii_)
            SendInput(1, ctypes.pointer(x_input), ctypes.sizeof(x_input))
            time.sleep(self._get_random_delay(0.1))
            
            success = self.set_cursor_pos(x, y, smooth)
            time.sleep(self._get_random_delay(0.1))
            
            ii_.mi = MouseInput(0, 0, 0, MOUSEEVENTF_LEFTUP, 0, ctypes.pointer(extra))
            x_input = Input(ctypes.c_ulong(0), ii_)
            SendInput(1, ctypes.pointer(x_input), ctypes.sizeof(x_input))
            return success
        except Exception:
            return False

    def _scroll(self, amount: int, horizontal: bool = False) -> bool:
        """Perform mouse wheel scroll.
        
        Args:
            amount: Scroll amount in wheel delta units (positive for up/right, negative for down/left)
            horizontal: If True, performs horizontal scroll instead of vertical
            
        Returns:
            True if successful, False otherwise
        """
        try:
            amount = self._add_random_offset(amount)
            extra = ctypes.c_ulong(0)
            ii_ = Input_I()
            flag = MOUSEEVENTF_HWHEEL if horizontal else MOUSEEVENTF_WHEEL
            ii_.mi = MouseInput(0, 0, amount, flag, 0, ctypes.pointer(extra))
            x = Input(ctypes.c_ulong(0), ii_)
            SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
            time.sleep(self._get_random_delay(0.05))
            return True
        except Exception:
            return False

    def scroll(self, clicks: int = 1, horizontal: bool = False) -> bool:
        """Scroll the mouse wheel by the specified number of clicks.
        
        Args:
            clicks: Number of clicks to scroll (positive for up/right, negative for down/left)
            horizontal: If True, performs horizontal scroll instead of vertical
            
        Returns:
            True if successful, False otherwise
        """
        try:
            amount = clicks * WHEEL_DELTA
            return self._scroll(amount, horizontal)
        except Exception:
            return False

    def scroll_up(self, clicks: int = 1) -> bool:
        """Scroll the mouse wheel up by the specified number of clicks.
        
        Args:
            clicks: Number of clicks to scroll up (must be positive)
            
        Returns:
            True if successful, False otherwise
        """
        return self.scroll(abs(clicks))

    def scroll_down(self, clicks: int = 1) -> bool:
        """Scroll the mouse wheel down by the specified number of clicks.
        
        Args:
            clicks: Number of clicks to scroll down (must be positive)
            
        Returns:
            True if successful, False otherwise
        """
        return self.scroll(-abs(clicks))

# Create a default instance for backward compatibility
_default_controller = MouseController()

# Module-level functions that use the default controller
def get_cursor_pos() -> Tuple[int, int]:
    return _default_controller.get_cursor_pos()

def set_cursor_pos(x: int, y: int, smooth: bool = False) -> bool:
    return _default_controller.set_cursor_pos(x, y, smooth)

def move_relative(dx: int, dy: int, smooth: bool = False) -> bool:
    return _default_controller.move_relative(dx, dy, smooth)

def left_click() -> bool:
    return _default_controller.left_click()

def right_click() -> bool:
    return _default_controller.right_click()

def middle_click() -> bool:
    return _default_controller.middle_click()

def double_click() -> bool:
    return _default_controller.double_click()

def drag_to(x: int, y: int, smooth: bool = True) -> bool:
    return _default_controller.drag_to(x, y, smooth)

def scroll(clicks: int = 1, horizontal: bool = False) -> bool:
    return _default_controller.scroll(clicks, horizontal)

def scroll_up(clicks: int = 1) -> bool:
    return _default_controller.scroll_up(clicks)

def scroll_down(clicks: int = 1) -> bool:
    return _default_controller.scroll_down(clicks)
