import subprocess
from color import colors


def hello():
    print(f""" █████  ██████   ██████ ██   ██     ██      ██ ███    ██ ██    ██ ██   ██     ██ ███    ██ ███████ ████████  █████  ██      ██      
██   ██ ██   ██ ██      ██   ██     ██      ██ ████   ██ ██    ██  ██ ██      ██ ████   ██ ██         ██    ██   ██ ██      ██      
███████ ██████  ██      ███████     ██      ██ ██ ██  ██ ██    ██   ███       ██ ██ ██  ██ ███████    ██    ███████ ██      ██      
██   ██ ██   ██ ██      ██   ██     ██      ██ ██  ██ ██ ██    ██  ██ ██      ██ ██  ██ ██      ██    ██    ██   ██ ██      ██      
██   ██ ██   ██  ██████ ██   ██     ███████ ██ ██   ████  ██████  ██   ██     ██ ██   ████ ███████    ██    ██   ██ ███████ ███████


"Internet"
---> iwctl(WIFI)
---> dhcpcd(LAN)

"Disk"
---> fdisk -l 
---> cfdisk /dev/(name your disk)

"Script rename your disk setup.py"
--->def disk():

""")


def run_command(command):
    try:
        return subprocess.run(command, shell=True, check=True, stdout=None, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        print(colors.fg.red + f"Error command: {command}" + colors.reset)
        print(e)
        exit(1)


def other():
    run_command("clear")
    run_command("pacman-key --init")
    run_command("pacman-key --populate archlinux")
    # run_command("pacman -Syy python-tqdm")


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


# def arch_system():
    # run_command("arch-chroot /mnt")


# Виклик функції для встановлення Arch Linux
other()
hello()
disk()
install_system_and_tools()
# arch_system()
