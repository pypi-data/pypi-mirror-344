# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "mcp",
# ]
# ///
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("adb-mcp-server")

@mcp.tool()
def set_brightness(value: int, sn: str = "") -> None:
    """
        Set the screen brightness of the device
        Args:
            value: The brightness value to set (0-255)
            sn: The serial number of the device. if empty string, use adb shell without serial number
        Returns:
            None
    """
    assert(0 <= value <= 255), "Brightness value must be between 0 and 255"

    import os
    # call adb shell settings put system screen_brightness value
    if sn != "":
        os.system(f'adb -s {sn} shell "settings put system screen_brightness {value}"')
        assert(get_brightness(sn) == value), "Failed to set brightness value"
    else:
        os.system(f'adb shell "settings put system screen_brightness {value}"')
        assert(get_brightness() == value), "Failed to set brightness value"
    

@mcp.tool()
def get_brightness(sn: str = "") -> int:
    """
        Get the screen brightness of the device
        Args:
            sn: The serial number of the device. if empty string, use adb shell without serial number
        Returns:
            The screen brightness of the device
    """
    import os
    # call adb shell settings get system screen_brightness
    if sn != "":
        return int(("\n").join(os.popen(f'adb -s {sn} shell "settings get system screen_brightness"', "r").readlines()))
    else:
        return int(("\n").join(os.popen('adb shell "settings get system screen_brightness"', "r").readlines()))


@mcp.tool()
def dump_hwc_layers(sn: str = "") -> str:
    """
        Dump the HWC layers of the device, so you can tell which application is visible on the screen
        Args:
            sn: The serial number of the device. if empty string, use adb shell without serial number
        Returns:
            The content of the dumped HWC layers
    """
    import os
    cmd = """
        adb shell "dumpsys SurfaceFlinger | sed -n '/(active) HWC layers:/,/^$/p'"
    """
    if sn != "":
        cmd = f'adb -s {sn} shell "dumpsys SurfaceFlinger | sed -n \'/\(active\) HWC layers:/,/^$/p\'"'
    else:
        return ("\n").join(os.popen(cmd, "r").readlines())

# uiautomator dump
@mcp.tool()
def uiautomator_dump(sn: str = "") -> str:
    """
        Dump the current UI hierarchy
        Args:
            sn: The serial number of the device. if empty string, use adb shell without serial number
        Returns:
            The content of the dumped UI hierarchy
    """
    import os
    # call adb shell "uiautomator dump /sdcard/window_dump.xml"
    if sn != "":
        os.system("adb -s {sn} shell uiautomator dump /sdcard/window_dump.xml")
        os.system("adb -s {sn} pull /sdcard/window_dump.xml")
    else:
        os.system("adb shell uiautomator dump /sdcard/window_dump.xml")
        os.system("adb pull /sdcard/window_dump.xml")

    # read file content
    with open("window_dump.xml", "r", encoding="utf8") as f:
        content = f.read()
    
    return content

@mcp.tool()
def get_screen_size(sn: str = "") -> str:
    """
        Get the screen size of the device
        Args:
            sn: The serial number of the device. if empty string, use adb shell without serial number
        Returns:
            The screen size of the device
    """
    import os
    # call adb shell wm size
    if sn != "":
        return ("\n").join(os.popen(f'adb -s {sn} shell wm size', "r").readlines())
    else:
        # call adb shell wm size
        os.system(f'adb shell wm size')

@mcp.tool()
def press_home_button(sn: str = "") -> None:
    """
        Press the home button on the device
        Args:
            sn: The serial number of the device. if empty string, use adb shell without serial number
        Returns:
            None
    """
    import os
    # call adb shell input keyevent 3
    if sn != "":
        os.system(f'adb -s {sn} shell input keyevent 3')
    else:
        os.system("adb shell input keyevent 3")

@mcp.tool()
def press_back_button(sn: str = "") -> None:
    """
        Press the back button on the device
        Args:
            sn: The serial number of the device. if empty string, use adb shell without serial number
        Returns:
            None
    """
    import os
    # call adb shell input keyevent 4
    if sn != "":
        os.system(f'adb -s {sn} shell input keyevent 4')
    else:
        os.system("adb shell input keyevent 4")

@mcp.tool()
def press_menu_button(sn: str = "") -> None:
    """
        Press the menu button on the device
        Args:
            sn: The serial number of the device. if empty string, use adb shell without serial number
        Returns:
            None
    """
    import os
    # call adb shell input keyevent 82
    if sn != "":
        os.system(f'adb -s {sn} shell input keyevent 82')
    else:
        os.system("adb shell input keyevent 82")

@mcp.tool()
def press_power_button(sn: str = "") -> None:
    """
        Press the power button on the device
        Args:
            sn: The serial number of the device. if empty string, use adb shell without serial number
        Returns:
            None
    """
    import os
    # call adb shell input keyevent 26
    if sn != "":
        os.system(f'adb -s {sn} shell input keyevent 26')
    else:
        os.system("adb shell input keyevent 26")

@mcp.tool()
def press_volume_up_button(sn: str = "") -> None:
    """
        Press the volume up button on the device
        Args:
            sn: The serial number of the device. if empty string, use adb shell without serial number
        Returns:
            None
    """
    import os
    if sn != "":
        os.system(f'adb -s {sn} shell input keyevent 25')
    else:
        os.system("adb shell input keyevent 25")

@mcp.tool()
def press_volume_down_button(sn: str = "") -> None:
    """
        Press the volume up button on the device
        Args:
            sn: The serial number of the device. if empty string, use adb shell without serial number
        Returns:
            None
    """
    import os
    if sn != "":
        os.system(f'adb -s {sn} shell input keyevent 24')
    else:
        os.system("adb shell input keyevent 24")

@mcp.tool()
def input_swipe(x1: int, y1: int, x2: int, y2: int, sn: str = "") -> None:
    """
        Swipe on the screen from (x1, y1) to (x2, y2) by adb shell input swipe command
        Args:
            x1: The starting x coordinate
            y1: The starting y coordinate
            x2: The ending x coordinate
            y2: The ending y coordinate
            sn: The serial number of the device. if empty string, use adb shell without serial number
        Returns:
            None
    """
    import os
    # call adb shell input swipe x1 y1 x2 y2
    if sn != "":
        os.system(f"adb -s {sn} shell input swipe {x1} {y1} {x2} {y2}")
    else:
        os.system(f"adb shell input swipe {x1} {y1} {x2} {y2}")

@mcp.tool()
def input_tap(x: int, y: int, sn: str = "") -> None:
    """
        Tap on the screen at (x, y) by adb shell input tap command
        Args:
            x: The x coordinate
            y: The y coordinate
            sn: The serial number of the device. if empty string, use adb shell without serial number
        Returns:
            None
    """
    import os
    # call adb shell input tap x y
    if sn != "":
        os.system(f"adb -s {sn} shell input tap {x} {y}")
    else:
        os.system(f"adb shell input tap {x} {y}")

@mcp.tool()
def shell(command: str, sn: str = "") -> str:
    """
        Execute a shell command on the device
        Args:
            command: The command to execute
            sn: The serial number of the device. if empty string, use adb shell without serial number
        Returns:
            The output of the command
    """
    import os
    # call adb shell command, and read ouput of adb shell command
    if sn != "":
        return ("\n").join(os.popen(f"adb -s {sn} shell {command}", "r").readlines())
    else:
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
    
    sn = []

    # read output of adb devices command, and extract sn number
    for line in os.popen("adb devices", "r").readlines():
        # remove the first line
        if line.startswith("List of devices attached"):
            continue
        # remove the last line
        if line == "\n":
            continue
        # remove the serial number and state
        sn.append(line.split()[0])
    
    return "\n".join(sn)

@mcp.tool()
def wait_for_device(sn: str = "") -> None:
    """
        Wait for a device to be connected
        Args:
            sn: The serial number of the device. if empty string, use adb shell without serial number
        Returns:
            None
    """
    import os
    # call adb wait-for-device
    if sn != "":
        os.system(f"adb -s {sn} wait-for-device")
    else:
        os.system("adb wait-for-device")

@mcp.tool()
def pull(src: str, dst: str, sn: str = "") -> str:
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
    if sn != "":
        os.system(f"adb -s {sn} pull {src} {dst}")
    else:
        os.system(f"adb pull {src} {dst}")

    # return relative path of the file
    return os.path.relpath(dst)

@mcp.tool()
def push(src: str, dst: str, sn: str = "") -> str:
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
    if sn != "":
        os.system(f"adb -s {sn} push {src} {dst}")
    else:
        os.system(f"adb push {src} {dst}")

    # return relative path of the file
    return os.path.join(os.path.dirname(dst), os.path.basename(src))


def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()