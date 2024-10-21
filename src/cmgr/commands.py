import os
import subprocess
import sys
import click
import shutil

from cmgr import config
from cmgr import utils

CMGR_ROOT = "/var/cmgr"

CHROOT_SOURCE = "stage3-amd64-desktop-openrc-20240728T170359Z.tar.xz"

def check_uid0():
    return os.getuid() == 0

class Cmgr:

    __slots__ = ["config", "_config"]

    def __init__(self):
        #if not check_uid0():
        #    raise PermissionError("User is not root (uid 0)")
        #    sys.exit(1)
        
        if not os.path.isdir(CMGR_ROOT):
            os.makedirs(CMGR_ROOT)
        
        self._config = config.Config()
        self.config = self._config.load_config()
        #print(self.config)
        #if not os.path.isdir(self.config.

    def get_config(self):
        return self.config

    def get_key(self, key):
        return self.config.lookup_key(key)

    def get_root_dir(self):
        try:
            return self.config['cmgr']['root_dir']
        except KeyError:
            return CMGR_ROOT
        
    def get_storage_dir(self):
        try:
            return self.config['cmgr']['storage_dir']
        except KeyError:
            print("storage_dir key not found!")
            sys.exit(1)

    def get_stage3_dir(self):
        try:
            return self.config['cmgr']['stage3_dir']
        except KeyError:
            print("stage3_dir key not found!")
            sys.exit(1)
            
    def get_source_stage3(self):
        try:
            return self.config['cmgr']['source_stage3']
        except KeyError:
            print("source_files key not found!")
            sys.exit(1)

    def get_local_storage(self):
        try:
            return self.config['cmgr']['stage3_storage']
        except KeyError:
            return LOCAL_STORAGE_DIR

    def get_files_to_copy(self):
        try:
            return self.config['cmgr']['files_to_copy']
        except KeyError:
            return []


def run_in_chroot(name, cmd, quiet):
    stdout_val = subprocess.DEVNULL if quiet else None
    subprocess.run(f"", shell=True)


def prepare_chroot(output, quiet, ctx):
    root = ctx.obj['CMGR'].get_root_dir()
    stage3_dir = ctx.obj['CMGR'].get_stage3_dir()
    storage = ctx.obj['CMGR'].get_storage_dir()
    source = ctx.obj['CMGR'].get_source_stage3()

    print(root)
    print(storage)
    print(source)
    print(stage3_dir)

    print(f"{stage3_dir}/{source}")

    sync_cmd = f'chroot "{storage}/{output}" emerge-webrsync'

    os.makedirs(f"{storage}/{output}")
    tar_cmd = f"tar xpvf {stage3_dir}/{source} --xattrs-include='*.*' --numeric-owner -C {storage}/{output}"
    stdout_val = subprocess.DEVNULL if quiet else None
    subprocess.run(tar_cmd, shell=True, stdout=stdout_val)
    
    shutil.copyfile("/etc/resolv.conf", f"{storage}/{output}/etc/resolv.conf")
    
    utils.make_mountpoints(f"{storage}/{output}")
    subprocess.run(sync_cmd, shell=True)

    utils.cleanup_mountpoints(f"{storage}/{output}")


@click.command(name="exec")
@click.pass_context
@click.option("-n", "--name", required=True)
@click.argument("cmd", nargs=-1)
def exec_chroot(ctx, name, cmd):
    print(name)
    cmd_str = ' '.join(map(str, cmd))

    storage = ctx.obj['CMGR'].get_storage_dir()

    utils.make_mountpoints(f"{storage}/{name}")

    subprocess.run(f"chroot {storage}/{name} {cmd_str}", shell=True)

    utils.cleanup_mountpoints(f"{storage}/{name}")


@click.command(name="del")
@click.pass_context
@click.option("-n", "--name", required=True)
def del_chroot(ctx, name):
    storage = ctx.obj['CMGR'].get_storage_dir()
    
    shutil.rmtree(f"{storage}/{name}")
    print(f"Deleted {name}.")

@click.command()
@click.pass_context
@click.option("-n", "--name", required=True)
def update(ctx, name):

    storage = ctx.obj['CMGR'].get_storage_dir()
    
    utils.make_mountpoints(f"{storage}/{output}")
    
    sync_cmd = f'chroot "{storage}/{name}" emaint sync'
    
    update_cmd = f'chroot "{root}/{name}" emerge -avuDU @world'
    subprocess.run(update_cmd, shell=True)
    
    utils.cleanup_mountpoints(f"{storage}/{output}")

@click.command(name="list")
@click.pass_context
def list_chroots(ctx):
    root = ctx.obj['CMGR']
    
    print("Chroots:")
    chroots = os.listdir(CMGR_ROOT)

    for chroot in chroots:
        print(f"- {chroot}")

@click.command()
@click.pass_context
@click.option('--verbose', '-v', default=False, is_flag=True)
@click.option('--quiet', '-q', default=False, is_flag=True)
@click.option("-n", "--name", "name")
def create(ctx, verbose, quiet, name):
    #if os.geteuid() != 0:
    #    print("Please run cmgr as root.")
    #    return 1
    prepare_chroot(name, quiet, ctx)
    return 0
