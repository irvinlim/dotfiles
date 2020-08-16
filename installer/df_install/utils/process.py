import os
import psutil
import subprocess
import tempfile
import time
import signal


def get_shebang_line():
    return '#!/usr/bin/env bash'


def execute(args):
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    return proc.returncode, stdout.decode('utf-8'), stderr.decode('utf-8')


def execute_cmds(cmds, fail_on_error=False):
    # Create temporary file
    with tempfile.NamedTemporaryFile() as fp:
        # Write shebang line
        fp.write(get_shebang_line().encode('utf-8'))
        fp.write('\n'.encode('utf-8'))

        # Set flags
        if fail_on_error:
            fp.write('set -e\n'.encode('utf-8'))

        for cmd in cmds:
            fp.write(cmd.encode('utf-8'))
            fp.write('\n'.encode('utf-8'))

        # Flush writes
        fp.flush()

        # Make file executable
        os.chmod(fp.name, 0o755)

        # Execute file
        return execute([fp.name])


def pkill(names, killsig=signal.SIGTERM):
    names = set(names)
    procs = {}
    alive = set()

    # Get PID of each process
    lower_names = set(name.lower() for name in names)
    for proc in psutil.process_iter():
        if proc.is_running() and proc.status() != 'zombie':
            if proc.name().lower() in lower_names:
                procs[proc.name()] = proc
                alive.add(proc.pid)

    # Send signal to each process
    for name, proc in procs.items():
        # log.debug('[+] Killing process %s (pid %d)...' % (name, proc.pid))
        proc.send_signal(killsig)

    # Poll until each process is killed
    while True:
        for name, proc in procs.items():
            if proc.pid in alive and not proc.is_running():
                # log.debug('[+] Process %s (pid %d) is no longer running' % (name, proc.pid))
                alive.remove(proc.pid)

            if not alive:
                return

        time.sleep(1)


def mac_open(name):
    return subprocess.call(['open', '-a', name])
