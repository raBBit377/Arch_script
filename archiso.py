import subprocess
import os
import select
import sys
def hello():
    run_command("clear")
    print(f""" █████  ██████   ██████ ██   ██     ██      ██ ███    ██ ██    ██ ██   ██     ██ ███    ██ ███████ ████████  █████  ██      ██      
██   ██ ██   ██ ██      ██   ██     ██      ██ ████   ██ ██    ██  ██ ██      ██ ████   ██ ██         ██    ██   ██ ██      ██      
███████ ██████  ██      ███████     ██      ██ ██ ██  ██ ██    ██   ███       ██ ██ ██  ██ ███████    ██    ███████ ██      ██      
██   ██ ██   ██ ██      ██   ██     ██      ██ ██  ██ ██ ██    ██  ██ ██      ██ ██  ██ ██      ██    ██    ██   ██ ██      ██      
██   ██ ██   ██  ██████ ██   ██     ███████ ██ ██   ████  ██████  ██   ██     ██ ██   ████ ███████    ██    ██   ██ ███████ ███████

""")



log_file = "command_logs.txt"

def run_command(command):
    print("Running command:", command)
    log_command(f"Running command: {command}")

    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        while True:
            reads, _, _ = select.select([process.stdout, process.stderr], [], [], 1)

            if process.stdout in reads:
                line = process.stdout.readline()
                if not line:
                    break
                print("stdout:", line.strip())
                with open(log_file, "a") as f:
                    f.write("stdout: " + line)

            if process.stderr in reads:
                line = process.stderr.readline()
                if not line:
                    break
                print("stderr:", line.strip())
                with open(log_file, "a") as f:
                    f.write("stderr: " + line)

        process.wait()

    except subprocess.CalledProcessError as e:
        log_command(f"Error command: {command}")
        log_command(str(e))
        exit(1)
def log_command(log_message):
    # Запис інформації у файл логів
    with open(log_file, "a") as f:
        f.write(log_message + "\n")

def other():
    run_command("pacman-key --init")
    run_command("pacman-key --populate archlinux")


def disk():
    run_command("mkfs.btrfs -f /dev/sda2")
    run_command("mkfs.fat -F32 /dev/sda1")
    run_command("mount /dev/sda2 /mnt")
    run_command("btrfs subvolume create /mnt/@root")
    run_command("btrfs subvolume create /mnt/@home")
    run_command("umount /mnt")
    run_command("mount -o noatime,ssd,compress=zstd:3,subvol=@root /dev/sda2 /mnt")
    run_command("mkdir -p /mnt/boot/efi /mnt/home")
    run_command("mount /dev/sda1 /mnt/boot/efi")
    run_command("mount -o noatime,ssd,compress=zstd:3,subvol=@home /dev/sda2 /mnt/home")
    run_command("lsblk")


def install_system_and_tools():
    run_command("pacstrap /mnt base base-devel btrfs-progs linux linux-headers dkms linux-lts linux-lts-headers linux-zen linux-zen-headers kitty linux-firmware nano vim netctl dhcpcd git wget curl reflector rsync")
    run_command("genfstab -pU /mnt >> /mnt/etc/fstab")




# Виклик функції для встановлення Arch Linux
hello()
other()
disk()
install_system_and_tools()

