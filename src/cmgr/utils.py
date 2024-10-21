import os
import sys
import subprocess

def make_mountpoints(chroot):
    filesystems = ["proc", "sys", "dev", "run"]

    for fs in filesystems:
        #subprocess.run(f"mount /{fs} {chroot}/{fs}", shell=True)
        if fs == "run":
            subprocess.run(f"mount /{fs} {chroot}/{fs}", shell=True)
            #print(f"mount -B /{fs} {chroot}/{fs}")
            continue
        #print(f"mount -R /{fs} {chroot}/{fs}")
        subprocess.run(f"mount -R /{fs} {chroot}/{fs}", shell=True)


def cleanup_mountpoints(chroot):
    subprocess.run(f"umount -l {chroot}/dev/{{/shm,/pts,}}", shell=True)
    #print(f"umount -l {chroot}/dev/{{/shm,/pts,}}")
    subprocess.run(f"umount -R {chroot}", shell=True)
