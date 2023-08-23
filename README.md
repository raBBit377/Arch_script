# Arch_script_install
![Python 3.11]([https://img.shields.io/pypi/pyversions/clubhouse?color=blueviolet](https://img.shields.io/pypi/pyversions/python))

## A script for almost automatic installation of Arch Linux. (NOT OFFICIAL)

> **step - 1 (NET)** 

```bash
command = iwctl/dhcpd
```
> **step - 2 (Install git)**

```bash
pacman -Sy git
```
> **step - 3 (Disk)** ***You need to divide the disk into two volumes, 1 - grub (/dev/sda1), 2 - system(/dev/sda2)***

```bash
command = cfdisk /dev/sda
```
> **step - 4 (Git clone)**

```bash
git clone https://github.com/raBBit377/Arch_script/tree/main
```
> **step - 5 (Run script)**

```bash
python Arch_script/archiso.py
```
