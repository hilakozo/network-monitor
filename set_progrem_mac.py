import plistlib
import subprocess
import os

def create_and_load_plist(script_path, python_path='/Users/yoavpinto/Desktop/gpt-angineer-try/gpt-engineer/hila'):
    plist = {
        'Label': 'com.user.networkmonitor',
        'ProgramArguments': [python_path, script_path],
        'RunAtLoad': True,
        'StandardErrorPath': '/tmp/networkmonitor.err',
        'StandardOutPath': '/tmp/networkmonitor.out'
    }

    # Ensure the LaunchAgents directory exists
    launch_agents_dir = os.path.expanduser('~/Library/LaunchAgents')
    os.makedirs(launch_agents_dir, exist_ok=True)

    # Define the path for the plist
    plist_path = os.path.join(launch_agents_dir, 'com.user.networkmonitor.plist')

    # Write the plist file
    with open(plist_path, 'wb') as plist_file:
        plistlib.dump(plist, plist_file)

    # Load the plist with launchctl
    subprocess.run(['launchctl', 'load', plist_path], check=True)
