"""Interface routines to LSF job scheduler commands."""

__all__ = [
    'BatchError',
    'submit',
    'status',
    'unfinished'
]

__author__ = "Rosen Matev"
__version__ = "0.1"
__date__ = "$2010-09-20$"

import re
import subprocess, shlex

class BatchError(Exception):
    def __init__(self, value): self.value = value
    def __str__(self): return str(self.value)

def run(command):
    """Run a command and return its output.
        
    Runs a command using subprocess and blocks until it terminates.
    The function returns a tuple of two strings containing
    command's standard output and standard error.
        
    """
    p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    stdout = p.stdout.read()
    stderr = p.stderr.read()
    return (stdout, stderr)


def submit(command, name='', queue='', logger=None):
    """Submit job to LSF and return job ID."""
    options = []
    if name: options.append('-J ' + name)
    if queue: options.append('-q ' + queue)
    command = command.replace('"', '"\""')
    stdout, stderr = helpers.run('bsub %s "%s"'%(' '.join(options), command), merge=False, logger=logger)
    if stderr: raise BatchError(stderr)
    m = re.match('Job <([0-9]+)>', stdout)
    if m is None: raise BatchError('unexpected output from bsub:\n' + stdout)
    return m.group(1)

def status(**kwargs):
    """Return job status.

    You may supply ``jobId`` or ``jobName`` key argument. If both are passed,
    ``jobId`` takes precedence. Returns empty string if job is not found.

    """
    if 'jobId' in kwargs:
        command = 'bjobs %s'%(kwargs['jobId'])
    elif 'jobName' in kwargs:
        command = 'bjobs -J %s'%(kwargs['jobName'])
    else:
        raise ValueError('Either jobId or jobName must be specified.')
    # Job status is one of PEND,PSUSP,RUN,USUSP,SSUSP,DONE,EXIT,UNKWN,WAIT,ZOMBI
    stdout, stderr = helpers.run(command, merge=False)
    if stderr:
        if 'is not found' in stderr: return ''
        else: raise BatchError(stderr)
    try: status = stdout.splitlines()[1].split()[2]
    except IndexError: raise BatchError('unexpected output from bjobs:\n' + stdout)
    return status

def unfinished():
    """Return list of job ID's of unfinished jobs."""
    stdout, stderr = helpers.run('bjobs', merge=False)
    if stderr:
        if stderr.strip() == 'No unfinished job found': return []
        else: raise BatchError(stderr)
    try: jobIds = [line.split()[0] for line in stdout.splitlines()[1:]]
    except IndexError: raise BatchError('unexpected output from bjobs:\n' + stdout)
    return jobIds
