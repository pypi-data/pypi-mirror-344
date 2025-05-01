from mcp.server.fastmcp import FastMCP

server = FastMCP("adb-mcp-server")

def input(command: str, sn: str = '') -> str:
    """
        adb shell "input  ..." command to android phone
        input support the following commands:
            text <string> (Default: keyboard)
            keyevent [--longpress|--duration <duration to hold key down in ms>] [--doubletap] [--async] [--delay <duration between keycodes in ms>] <key code number or name> ... (Default: keyboard)
            tap <x> <y> (Default: touchscreen)
            swipe <x1> <y1> <x2> <y2> [duration(ms)] (Default: touchscreen)
            draganddrop <x1> <y1> <x2> <y2> [duration(ms)] (Default: touchscreen)
            press (Default: trackball)
            roll <dx> <dy> (Default: trackball)
            motionevent <DOWN|UP|MOVE|CANCEL> <x> <y> (Default: touchscreen)
            scroll (Default: rotaryencoder). Has the following syntax:
                    scroll <x> <y> [axis_value] (for pointer-based sources)
                    scroll [axis_value] (for non-pointer-based sources)
                    Axis options: SCROLL, HSCROLL, VSCROLL
                    None or one or multiple axis value options can be specified.
                    To specify multiple axes, use one axis option for per axis.
                    Example: `scroll --axis VSCROLL,2 --axis SCROLL,-2.4`
            keycombination [-t duration(ms)] <key code 1> <key code 2> ... (Default: keyboard, the key order is important here.)
    Args:
        command (str): a shell command to run. for example,  "tap 100 200";  swipe 100 200 300 400; text hello world; keyevent KEYCODE_HOME; input text hello world; input keyevent KEYCODE_HOME; input tap 100 200; input swipe 100 200 300 400; input draganddrop 100 200 300 400; input press; input roll 100 200; input motionevent DOWN 100 200; input scroll SCROLL,2 SCROLL,-2.4
        sn: android phone serial number which be connected to run command. default is empty, to connected default android phone.
    Returns:
        str: the result of command
    """
    
    return adb_shell(f'input {command}', sn)
    


def run_command_in_shell(command: str) -> str:
    """
        run command in shell
    Args:
        command (str): a shell command to run. for example,  adb shell "input tap 100 200"; echo "hello world";
    Returns:
        str: the result of command
    """
    # run the adb shell command, and get the result
    import subprocess
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"run command failed: {command}, error information: {result.stderr}")
    
    return result.stdout

@server.tool()
def uiautomator_dump(sn: str = '') -> str:
    """
        use uiautomator dump command to observe android phone ui and to find the ui controller which you want
        Args:
            sn: android phone serial number which be connected to run command. default is empty, to connected default android phone.
    Returns:
        str: the content of UI hierarchy, xml file type
    """
    # remove old xml file
    import os
    if os.path.exists("window_dump.xml"):
        os.remove("window_dump.xml")

    adb_wait_for_device(sn)

    command = "uiautomator dump /sdcard/window_dump.xml"

    adb_shell(command, sn)
    
    adb_pull("/sdcard/window_dump.xml", sn)
    
    with open("window_dump.xml", "r", encoding="utf-8") as f:
        content = f.read()
    
    # remove the xml file
    if os.path.exists("window_dump.xml"):
        os.remove("window_dump.xml")

    return content

@server.tool()
def adb_pull(file_path: str, sn: str = '') -> str:
    """
        use adb pull command to pull file from android phone
        Args:
            file_path: the path of file in android phone
            sn: android phone serial number which be connected to run command. default is empty, to connected default android phone.
    Returns:
        str: the result of adb pull command
    """
    adb_wait_for_device(sn)
    
    if sn != '':
        full_command = f'adb -s {sn} pull {file_path}'
    else:
        full_command = f'adb pull {file_path}'
    
    return run_command_in_shell(full_command)

@server.tool()
def adb_push(local_file_path: str, remote_file_path: str, sn: str = '') -> str:
    """
        use adb push command to push file to android phone
        Args:
            local_file_path: the path of file in local machine
            remote_file_path: the path of file in android phone
            sn: android phone serial number which be connected to run command. default is empty, to connected default android phone.
    Returns:
        str: the result of adb push command
    """
    adb_wait_for_device(sn)

    if sn != '':
        full_command = f'adb -s {sn} push {local_file_path} {remote_file_path}'
    else:
        full_command = f'adb push {local_file_path} {remote_file_path}'

    import os
    # check if the local file exists
    if not os.path.exists(local_file_path):
        raise Exception(f"local file {local_file_path} does not exist")
    
    return run_command_in_shell(full_command)


@server.tool()
def adb_shell(command: str, sn: str = '') -> str:
    """
        run adb shell command
    Args:
        command (str): a adb shell command to run. for example,  'input tap 100 200' is to run 'adb shell "input tap 100 200"' 
        sn: android phone serial number which be connected to run command. default is empty, to connected default android phone.
    Returns:
        str: the result of adb shell command
    """
    adb_wait_for_device(sn)

    if sn != '':
        full_command = f'adb -s {sn} shell "{command}"'
    else:
        full_command = f'adb shell "{command}"'
    
    # run the adb shell command, and get the result
    return run_command_in_shell(full_command)
    
@server.tool()
def adb_devices() -> str:
    """
        get the list of connected android devices
    Returns:
        str: the list of connected android devices
    """
    full_command = f'adb devices'
    # run the adb devices command, and get the result
    return run_command_in_shell(full_command)

@server.tool()
def adb_wait_for_device(sn: str = '') -> str:
    """
        wait for the android device to be connected
    Args:
        sn: android phone serial number which be connected to run command. default is empty, to connected default android phone.
    Returns:
        str: the result of adb wait-for-device command
    """
    if sn != '':
        full_command = f'adb -s {sn} wait-for-device'
    else:
        full_command = f'adb wait-for-device'
    
    # run the adb wait-for-device command, and get the result
    return run_command_in_shell(full_command)

@server.tool()
def adb_connect(ip: str, port: str = '') -> str:
    """
        connect to the android device by ip
    Args:
        ip: the ip address of android device
        port: the port of android device, default is 5555
    Returns:
        str: the result of adb connect command
    """
    if port != '':
        full_command = f'adb connect {ip}:{port}'
    else:
        full_command = f'adb connect {ip}'
    
    # run the adb connect command, and get the result
    return run_command_in_shell(full_command)

@server.tool()
def adb_disconnect(ip: str='', port: str='') -> str:
    """
        disconnect from the android device by ip and port
        if ip is None, disconnect all devices
        if only ip is provided, disconnect the device by ip on the port 5555
        if ip and port provided, disconnect the device by ip and port
    Args:
        ip: the ip address of android device
        port: the port of android device, default is 5555
    Returns:
        str: the result of adb disconnect command
    """
    if ip != '' and port != '':
        full_command = f'adb disconnect {ip}:{port}'
    elif ip != '':
        full_command = f'adb disconnect {ip}'
    else:
        # disconnect all devices
        full_command = f'adb disconnect'
    
    # run the adb disconnect command, and get the result
    return run_command_in_shell(full_command)


@server.tool()
def adb_start_server() -> str:
    """
        start the adb server
    Returns:
        str: the result of adb start-server command
    """
    full_command = f'adb start-server'
    # run the adb start-server command, and get the result
    return run_command_in_shell(full_command)

@server.tool()
def adb_kill_server() -> str:
    """
        kill the adb server
    Returns:
        str: the result of adb kill-server command
    """
    full_command = f'adb kill-server'

    # run the adb kill-server command, and get the result
    return run_command_in_shell(full_command)



def main():
    
    server.run(transport='stdio')

if __name__ == "__main__":

    main()