import os
import sys
import ctypes
try:
    from ctypes import wintypes
except (ImportError, ValueError, AttributeError):
    wintypes = None

# DWM and Window Attributes
DWMWA_USE_IMMERSIVE_DARK_MODE = 20
DWMWA_SYSTEMBACKDROP_TYPE = 38
DWMWA_MICA_EFFECT = 1029

# Windows 11 Backdrop Types
DWMSBT_AUTO = 0
DWMSBT_NONE = 1
DWMSBT_MAINWINDOW = 2       # Mica
DWMSBT_TRANSIENTWINDOW = 3  # Acrylic / Frosted Blur
DWMSBT_TABBEDWINDOW = 4     # Tabbed Mica

# Windows Composition Blur
class ACCENT_POLICY(ctypes.Structure):
    _fields_ = [
        ('AccentState', ctypes.c_uint),
        ('AccentFlags', ctypes.c_uint),
        ('GradientColor', ctypes.c_uint),
        ('AnimationId', ctypes.c_uint)
    ]

class WINCOMPATTRDATA(ctypes.Structure):
    _fields_ = [
        ('Attribute', ctypes.c_int),
        ('Data', ctypes.c_void_p),
        ('SizeOfData', ctypes.c_size_t)
    ]

# Accent States
ACCENT_ENABLE_BLURBEHIND = 3
ACCENT_ENABLE_ACRYLICBLURBEHIND = 4

def get_window_handle(tk_widget):
    """Retrieve HWND from a Tkinter / CustomTkinter window."""
    try:
        tk_widget.update_idletasks()
        return ctypes.windll.user32.GetParent(tk_widget.winfo_id())
    except Exception:
        return None

def apply_acrylic_glass(window, dark=True, alpha=0.92):
    """
    Applies real translucent frosted glass / acrylic blur effect.
    Also configures window-level alpha transparency.
    """
    # 1. Ajuste fino de transparência Tkinter (para o fundo deixar transparecer a área de trabalho)
    try:
        window.attributes("-alpha", alpha)
    except Exception:
        pass

    if sys.platform != "win32" or wintypes is None:
        return False

    try:
        hwnd = get_window_handle(window)
        if not hwnd:
            return False

        dwmapi = ctypes.windll.dwmapi
        user32 = ctypes.windll.user32

        # 2. Immersive Dark / Light Mode
        dark_mode = wintypes.BOOL(True if dark else False)
        dwmapi.DwmSetWindowAttribute(
            wintypes.HWND(hwnd),
            wintypes.DWORD(DWMWA_USE_IMMERSIVE_DARK_MODE),
            ctypes.byref(dark_mode),
            ctypes.sizeof(dark_mode)
        )

        # 3. Windows 11 22H2+ Acrylic backdrop
        backdrop_type = wintypes.DWORD(DWMSBT_TRANSIENTWINDOW)  # Acrylic Frosted Glass
        res = dwmapi.DwmSetWindowAttribute(
            wintypes.HWND(hwnd),
            wintypes.DWORD(DWMWA_SYSTEMBACKDROP_TYPE),
            ctypes.byref(backdrop_type),
            ctypes.sizeof(backdrop_type)
        )
        if res == 0:
            return True

        # 4. Fallback: Windows 10 SetWindowCompositionAttribute (Acrylic Blur)
        try:
            accent = ACCENT_POLICY()
            accent.AccentState = ACCENT_ENABLE_ACRYLICBLURBEHIND
            # ABGR color format: light frosty tint if not dark, dark tint if dark
            accent.GradientColor = 0xAA12161F if dark else 0x99F5F7FA

            data = WINCOMPATTRDATA()
            data.Attribute = 19  # WCA_ACCENT_POLICY
            data.Data = ctypes.cast(ctypes.pointer(accent), ctypes.c_void_p)
            data.SizeOfData = ctypes.sizeof(accent)

            set_attr = user32.SetWindowCompositionAttribute
            set_attr.argtypes = [wintypes.HWND, ctypes.POINTER(WINCOMPATTRDATA)]
            set_attr.restype = wintypes.BOOL
            set_attr(wintypes.HWND(hwnd), ctypes.byref(data))
            return True
        except Exception:
            pass

        # 5. Fallback Windows 11 21H2 Mica
        mica = wintypes.BOOL(True)
        dwmapi.DwmSetWindowAttribute(
            wintypes.HWND(hwnd),
            wintypes.DWORD(DWMWA_MICA_EFFECT),
            ctypes.byref(mica),
            ctypes.sizeof(mica)
        )
        return True
    except Exception as e:
        print(f"[AcrylicEffect] Warning: {e}")
        return False
