# cmgr

Chroot Manager is a utility designed to help orchestrate multiple chroots to optimize testing

## Installing

> [!NOTE]
> There is not a package available for this so beware

- Create a Python Virtual Environment with `python -m venv .venv`
- Source it with `. .venv/bin/activate`
- Run `pip install .`
- And you're all set to run `.venv/bin/cmgr`!

## Configuration

Configuring cmgr is done through `/etc/cmgr/config.toml`

|      Name     |  Type  | Description | Default |
|---------------|--------|--------------------------------------|---------|
| root_dir      | string | Root location for everything in cmgr | `/var/cmgr` |
| storage_dir   | string | Location for cmgr's chroots | `/var/cmgr/chroots` |
| stage3_dir    | string | Directory that stage3s are stored in | `/var/cmgr/stage3s` |
| source_stage3 | string | Source stage3 to use for chroots | N/A |
