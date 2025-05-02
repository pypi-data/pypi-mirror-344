from mcp.server.fastmcp import FastMCP

server = FastMCP("adb-mcp-server")


@server.tool()
def settings(command: str = 'help', sn: str = '') -> str:
    """
        run adb shell "settings <command>" to android phone
        settings is a tool to get or control system settings in the android
        you can use "help" to get the list of all available settings commands.
    Args:
        command: a settings subcommand to run. for example,  "list"; "get system screen_brightness"; default command is "help", to get settings help information.
        sn: android phone serial number which be connected to run command. default is empty, to connected default android phone.
    Returns:
        str: the result of command
    """
    return adb_shell(f'settings {command}', sn)


@server.tool()
def dumpsys(command: str='--help', sn: str = '') -> str:
    """
        run adb shell "dumpsys <command>" to android phone
        dumpsys is a tool to get or control service informantion in the android
        you can use "--help" to get the list of all available dumpsys commands.
        you can use "-l" to get the list of all available services.
        you can try "<service>, "<service> --help" or "<service> help" to get the available commands for the specifed service. we can't guarantee all services provide help information.
    Args:
        command (str): a dumpsys subcommand to run. for example,  "activity". default command is "--help", to get dumpsys help information.
        sn: android phone serial number which be connected to run command. default is empty, to connected default android phone.
    Returns:
        str: the result of command
    """

    return adb_shell(f'dumpsys {command}', sn)

@server.tool()
def cmd(command: str='-l', sn: str = '') -> str:
    """
        run adb -s <sn> shell "cmd <command>" to android phone
        cmd is another tool to get or control service informantion in the android
        you can use "-l" to get the list of all available service to command.
        you can use "<service>" to get the list of all available command for the service.
        you can try "<service>", "<service> --help", "<service> help" to get the available commands for the specifed service. we can't guarantee all services provide help information.
    Args:
        command: a cmd subcommand to run. for example, "package". default command is "-l", to get cmd help information.
        sn: android phone serial number which be connected to run command. default is empty, to connected default android phone.
    Returns:
        str: the result of command
    """
    return adb_shell(f'cmd {command}', sn)

@server.tool()
def getprop(command: str = '', sn: str = '') -> str:
    """
        run adb shell "getprop <command>" to android phone
        you can use "--help" to get the list of all available getprop commands.
    Args:
        command: a getprop subcommand to run. for example,  "" to get all props; "ro.product.model" to get model value; default command is empty, to get all properties.
        sn: android phone serial number which be connected to run command. default is empty, to connected default android phone.
    Returns:
        str: the result of command
    """
    if command.strip() == '':
        full_command = f'getprop'
    else:
        full_command = f'getprop {command}'

    return adb_shell(full_command, sn)

@server.tool()
def setprop(command: str = '', sn: str = '') -> str:
    """
        run adb shell "setprop <command>" to android phone
        you can use "--help" to get the list of all available setprop commands.
    Args:
        command: a setprop subcommand to run. for example,  "persist.sys.usb.config mtp" to set mtp value; default command is empty, to get setprop help information.
        sn: android phone serial number which be connected to run command. default is empty, to connected default android phone.
    Returns:
        str: the result of command
    """
    return adb_shell(f'setprop {command}', sn)


@server.tool()
def pm(command: str = 'help', sn: str = '') -> str:
    """
        run adb shell "pm <command>" to android phone
        pm is a tool to get or control package manager informantion in the android
        you can use "help" to get the list of all available pm commands.
    Args:
        command : a pm subcommand to run. for example,  "list packages"; "install /sdcard/test.apk"; default command is help, to get pm help information.
        sn: android phone serial number which be connected to run command. default is empty, to connected default android phone.
    Returns:
        str: the result of command
    """
    return adb_shell(f'pm {command}', sn)

@server.tool()
def am(command: str = 'help', sn: str = '') -> str:
    """
        run adb shell "am <command>" to android phone
        am is a tool to get or control activity manager informantion in the android
        you can use "help" to get the list of all available am commands.
    Args:
        command : a am subcommand to run. for example,  "start -n com.android.settings/.Settings"; "force-stop com.android.settings"; default command is help, to get am help information.
        sn: android phone serial number which be connected to run command. default is empty, to connected default android phone.
    Returns:
        str: the result of command
    """
    return adb_shell(f'am {command}', sn)

@server.tool()
def perfetto(command: str = '-h', sn: str = '') -> str:
    """
        run adb shell "perfetto <command>" to android phone
        perfetto is a tool to get or control performance informantion in the android
        you can use "-h" or "--help" to get the list of all available perfetto commands.
    Args:
        command : a perfetto subcommand to run. for example,  "--help" to get help; default command is "-h", to get perfetto help information.
        sn: android phone serial number which be connected to run command. default is empty, to connected default android phone.
    Returns:
        str: the result of command
    """
    return adb_shell(f'perfetto {command}', sn)

@server.tool()
def input(command: str = '', sn: str = '') -> str:
    """
        run adb shell "input  <command>" to android phone
    Args:
        command (str): a shell command to run. for example,  "tap 100 200";  swipe 100 200 300 400; text hello world; keyevent KEYCODE_HOME; default command is empty, to get input help information.
        sn: android phone serial number which be connected to run command. default is empty, to connected default android phone.
    Returns:
        str: the result of command
    """
    
    return adb_shell(f'input {command}', sn)

@server.tool()
def logcat(command: str = '-h', sn: str = '') -> str:
    """
        run adb  logcat <command> to android phone
        logcat is a tool to get or control log informantion in the android
        you can use logcat -h to get the list of all available logcat commands.
    Args:
        command : a logcat subcommand to run. for example,  logcat -d to get log in not block mode; default command is -h to get logcat help information.
        sn: android phone serial number which be connected to run command. default is empty, to connected default android phone.
    Returns:
        str: the result of command
    """
    if sn.strip() != '':
        command = f'adb -s {sn} logcat {command}'
    else:
        command = f'adb logcat {command}'

    return __run_command_in_shell(command)

def __run_command_in_shell(command: str) -> str:
    """
        run command in shell
    Args:
        command (str): a shell command to run. for example,  adb shell "input tap 100 200"; echo "hello world";
    Returns:
        str: the result of command
    """
    # run the adb shell command, and get the result with utf8 decoding
    import subprocess
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    if result.returncode != 0:
        raise Exception(f"run command failed: {command}, error information: { result.stdout + result.stderr }")
    

    if result.stdout != None and result.stdout.replace("\n", "").strip() != "":
        return result.stdout
    elif result.stderr != None and result.stderr.replace("\n", "").strip() != "":
        return result.stderr
    else:
        return ""

@server.tool()
def uiautomator(command: str = 'help', sn: str = '') -> str:
    """
        run adb shell "uiautomator <command>" to android phone
        uiautomator is a tool to run uiautomator test in the android or create an XML dump of current UI hierarchy
        you can use uiautomator help to get the list of all available uiautomator commands.
    Args:
        command : a uiautomator subcommand to run. for example,  "uiautomator dump"; "uiautomator runtest /sdcard/test.jar"; default command is help, to get uiautomator help information.
        sn: android phone serial number which be connected to run command. default is empty, to connected default android phone.
    Returns:
        str: the result of command
    """
    return adb_shell(f'uiautomator {command}', sn)

@server.tool()
def dump_current_ui_hierarchy(sn: str = '') -> str:
    """
        dump of current UI hierarchy to check the UI element in the android phone
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

    command = "uiautomator dump"
    result = adb_shell(command, sn)

    # get generated xml file path
    dump_file_path = result.split(":")[1].strip().replace("\n", "")
    # dump_file_name 
    dump_file_name = os.path.basename(dump_file_path)


    # get tmp dir of  os
    import tempfile
    tmp_dir = tempfile.gettempdir()

    # join the path
    pull_dump_file_path = os.path.join(tmp_dir, dump_file_name)

    if sn.strip() != '':
        pull_command = f"adb -s {sn} pull {dump_file_path} {pull_dump_file_path}"
    else:
        pull_command = f"adb pull {dump_file_path} {pull_dump_file_path}"
    result = __run_command_in_shell(pull_command)


    if(not os.path.exists(pull_dump_file_path)):
        raise Exception(f"fail to pull faile, the pulled file doesn't exist, {os.path.abspath(pull_dump_file_path)}, error information: {result};")

    # remove the xml file in android phone
    adb_shell("rm /sdcard/window_dump.xml", sn)
    
    try:
        # read the xml file
        with open(pull_dump_file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        raise Exception(f"read window_dump.xml failed, error information: {e}")

    # remove the xml file
    if os.path.exists("window_dump.xml"):
        os.remove("window_dump.xml")

    return content

@server.tool()
def adb_pull(remote_file_path: str, local_file_path: str, sn: str = '') -> str:
    """
        use adb pull command to pull file from android phone
        Args:
            remote_file_path: the path of file in android phone
            local_file_path: the path of file in local machine
            sn: android phone serial number which be connected to run command. default is empty, to connected default android phone.
    Returns:
        str: the result of adb pull command
    """
    adb_wait_for_device(sn)
    
    if sn.strip() != '':
        full_command = f'adb -s {sn} pull {remote_file_path} {local_file_path}'
    else:
        full_command = f'adb pull {remote_file_path} {local_file_path}'
    
    return __run_command_in_shell(full_command)

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

    if sn.strip() != '':
        full_command = f'adb -s {sn} push {local_file_path} {remote_file_path}'
    else:
        full_command = f'adb push {local_file_path} {remote_file_path}'

    import os
    # check if the local file exists
    if not os.path.exists(local_file_path):
        raise Exception(f"local file {local_file_path} does not exist")
    
    return __run_command_in_shell(full_command)

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

    if sn.strip() != '':
        full_command = f'adb -s {sn} shell "{command}"'
    else:
        full_command = f'adb shell "{command}"'
    
    # run the adb shell command, and get the result
    return __run_command_in_shell(full_command)
    
@server.tool()
def adb_devices() -> str:
    """
        get the list of connected android devices
    Returns:
        str: the list of connected android devices
    """
    full_command = f'adb devices'
    # run the adb devices command, and get the result
    return __run_command_in_shell(full_command)

@server.tool()
def adb_wait_for_device(sn: str = '') -> str:
    """
        wait for the android device to be connected
    Args:
        sn: android phone serial number which be connected to run command. default is empty, to connected default android phone.
    Returns:
        str: the result of adb wait-for-device command
    """
    if sn.strip() != '':
        full_command = f'adb -s {sn} wait-for-device'
    else:
        full_command = f'adb wait-for-device'
    
    # run the adb wait-for-device command, and get the result
    return __run_command_in_shell(full_command)

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
    return __run_command_in_shell(full_command)

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
    return __run_command_in_shell(full_command)


@server.tool()
def adb_start_server() -> str:
    """
        start the adb server
    Returns:
        str: the result of adb start-server command
    """
    full_command = f'adb start-server'
    # run the adb start-server command, and get the result
    return __run_command_in_shell(full_command)

@server.tool()
def adb_kill_server() -> str:
    """
        kill the adb server
    Returns:
        str: the result of adb kill-server command
    """
    full_command = f'adb kill-server'

    # run the adb kill-server command, and get the result
    return __run_command_in_shell(full_command)



def main():
    server.run(transport='stdio')

if __name__ == "__main__":
    main()