import os
import psutil
import subprocess
import tempfile
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
    killed = set()

    for proc in psutil.process_iter():
        if proc.is_running() and proc.status() != 'zombie' and proc.name() in names:
            proc.send_signal(killsig)
            killed.add(proc.name())

    return killed
