# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "mcp",
# ]
# ///
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("ADB")

@mcp.tool()
def set_brightness(value: int) -> None:
    """
        Set the screen brightness of the device
        Args:
            value: The brightness value to set (0-255)
        Returns:
            None
    """
    assert(0 <= value <= 255), "Brightness value must be between 0 and 255"

    import os
    # call adb shell settings put system screen_brightness value
    os.system(f'adb shell "settings put system screen_brightness {value}"')

    assert(get_brightness() == value), "Failed to set brightness value"
    

@mcp.tool()
def get_brightness() -> int:
    """
        Get the screen brightness of the device
        Returns:
            The screen brightness of the device
    """
    import os
    # call adb shell settings get system screen_brightness
    return int(("\n").join(os.popen('adb shell "settings get system screen_brightness"', "r").readlines()))


@mcp.tool()
def dump_hwc_layers() -> str:
    """
        Dump the HWC layers of the device, so you can tell which application is visible on the screen
        Returns:
            The content of the dumped HWC layers
    """
    import os
    cmd = """
        adb shell "dumpsys SurfaceFlinger | sed -n '/(active) HWC layers:/,/^$/p'"
    """
    return ("\n").join(os.popen(cmd, "r").readlines())

# uiautomator dump
@mcp.tool()
def uiautomator_dump() -> str:
    """
        Dump the current UI hierarchy

        Returns:
            The content of the dumped UI hierarchy
    """
    import os
    # call adb shell "uiautomator dump /sdcard/window_dump.xml"
    os.system("adb shell uiautomator dump /sdcard/window_dump.xml")

    # adb pull the file to local
    os.system("adb pull /sdcard/window_dump.xml")

    # read file content
    with open("window_dump.xml", "r", encoding="utf8") as f:
        content = f.read()
    
    return content

@mcp.tool()
def get_screen_size() -> str:
    """
        Get the screen size of the device
        Returns:
            The screen size of the device
    """
    import os
    # call adb shell wm size
    return ("\n").join(os.popen("adb shell wm size", "r").readlines())

@mcp.tool()
def press_home_button() -> None:
    """
        Press the home button on the device
        Returns:
            None
    """
    import os
    # call adb shell input keyevent 3
    os.system("adb shell input keyevent 3")

@mcp.tool()
def press_back_button() -> None:
    """
        Press the back button on the device
        Returns:
            None
    """
    import os
    # call adb shell input keyevent 4
    os.system("adb shell input keyevent 4")

@mcp.tool()
def press_menu_button() -> None:
    """
        Press the menu button on the device
        Returns:
            None
    """
    import os
    # call adb shell input keyevent 82
    os.system("adb shell input keyevent 82")

@mcp.tool()
def input_swipe(x1: int, y1: int, x2: int, y2: int) -> None:
    """
        Swipe on the screen from (x1, y1) to (x2, y2) by adb shell input swipe command
        Args:
            x1: The starting x coordinate
            y1: The starting y coordinate
            x2: The ending x coordinate
            y2: The ending y coordinate
        Returns:
            None
    """
    import os
    # call adb shell input swipe x1 y1 x2 y2
    os.system(f"adb shell input swipe {x1} {y1} {x2} {y2}")

@mcp.tool()
def input_tap(x: int, y: int) -> None:
    """
        Tap on the screen at (x, y) by adb shell input tap command
        Args:
            x: The x coordinate
            y: The y coordinate
        Returns:
            None
    """
    import os
    # call adb shell input tap x y
    os.system(f"adb shell input tap {x} {y}")

@mcp.tool()
def shell(command: str) -> str:
    """
        Execute a shell command on the device
        Args:
            command: The command to execute
        Returns:
            The output of the command
    """
    import os
    # call adb shell command, and read ouput of adb shell command
    return ("\n").join(os.popen(f"adb shell {command}", "r").readlines())


@mcp.tool()
def devices() -> str:
    """
        Get the list of connected devices
        Returns:
            output of adb devices command
    """
    import os
    # call adb devices
    return ("\n").join(os.popen("adb devices", "r").readlines())


@mcp.tool()
def pull(src: str, dst: str) -> str:
    """
        Pull a file from the device
        Args:
            src: The source file path on the device
            dst: The destination file path on the host
        Returns:
            relative path of the file
    """
    import os
    # call adb pull src dst
    os.system(f"adb pull {src} {dst}")

    # return relative path of the file
    return os.path.relpath(dst)

@mcp.tool()
def push(src: str, dst: str) -> str:
    """
        Push a file to the device
        Args:
            src: The source file path on the host
            dst: The destination file path on the device
        Returns:
            relative path of the file
    """
    import os
    # call adb push src dst
    os.system(f"adb push {src} {dst}")

    # return relative path of the file
    return os.path.join(os.path.dirname(dst), os.path.basename(src))
    

if __name__ == "__main__":
    mcp.run(transport="stdio")