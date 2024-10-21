import os
import subprocess
import click
import shutil
from cmgr import commands

#CMGR_ROOT = "/var/tmp/cmgr"
#
#CHROOT_SOURCE = "stage3-amd64-desktop-openrc-20240728T170359Z.tar.xz"
#
#def check_uid0():
#    return os.geteuid() == 0
#
#def prepare_chroot(output, quiet):
#    sync_cmd = f'arch-chroot "{CMGR_ROOT}/{output}" emaint sync'
#    
#    os.makedirs(f"{CMGR_ROOT}/{output}")
#    tar_cmd = f"tar xpvf {CHROOT_SOURCE} --xattrs-include='*.*' --numeric-owner -C {CMGR_ROOT}/{output}"
#    stdout_val = subprocess.DEVNULL if quiet else None
#    subprocess.run(tar_cmd, shell=True, stdout=stdout_val)
#    shutil.copyfile("/etc/resolv.conf", f"{CMGR_ROOT}/{output}/etc/resolv.conf")
#    subprocess.run(sync_cmd, shell=True)
#
#@click.command(name="del")
#@click.option("-n", "--name", required=True)
#def del_chroot(name):
#    shutil.rmtree(f"{CMGR_ROOT}/{name}")
#    
#@click.command()
#@click.option("-n", "--name", required=True)
#def update(name):
#    update_cmd = f'arch-chroot "{CMGR_ROOT}/{name}" emerge -avuDU @world'
#    subprocess.run(update_cmd, shell=True)
#    
#@click.command(name="list")
#def list_chroots():
#    print("Chroots:")
#    chroots = os.listdir(CMGR_ROOT)
#
#    for chroot in chroots:
#        print(f"- {chroot}")
#    
#@click.command()
#@click.option('--verbose', '-v', default=False, is_flag=True)
#@click.option('--quiet', '-q', default=False, is_flag=True)
#@click.option("-o", "--output", "output")
#def create(verbose, quiet, output):
#    #if os.geteuid() != 0:
#    #    print("Please run cmgr as root.")
#    #    return 1
#    prepare_chroot(output, quiet)
#    return 0

@click.group(invoke_without_command=True)
@click.option('--verbose', '-v', default=False, is_flag=True)
@click.option('--quiet', '-q', default=False, is_flag=True)
@click.pass_context
def cmd(ctx, verbose, quiet):
    ctx.ensure_object(dict)
    ctx.obj['CMGR'] = commands.Cmgr()

cmd.add_command(commands.create)
cmd.add_command(commands.list_chroots)
cmd.add_command(commands.update)
cmd.add_command(commands.del_chroot)
cmd.add_command(commands.exec_chroot)


def main():
    cmd()

if __name__ == "__main__":
    main()
