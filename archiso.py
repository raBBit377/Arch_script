import subprocess
from color import colors
from tqdm import tqdm

def hello():
    print(f""" █████  ██████   ██████ ██   ██     ██      ██ ███    ██ ██    ██ ██   ██     ██ ███    ██ ███████ ████████  █████  ██      ██      
██   ██ ██   ██ ██      ██   ██     ██      ██ ████   ██ ██    ██  ██ ██      ██ ████   ██ ██         ██    ██   ██ ██      ██      
███████ ██████  ██      ███████     ██      ██ ██ ██  ██ ██    ██   ███       ██ ██ ██  ██ ███████    ██    ███████ ██      ██      
██   ██ ██   ██ ██      ██   ██     ██      ██ ██  ██ ██ ██    ██  ██ ██      ██ ██  ██ ██      ██    ██    ██   ██ ██      ██      
██   ██ ██   ██  ██████ ██   ██     ███████ ██ ██   ████  ██████  ██   ██     ██ ██   ████ ███████    ██    ██   ██ ███████ ███████


""")

log_file = "command_logs.txt"

def run_command(command):
    print(f"Running command: {command}")
    log_command(f"Running command: {command}")

    try:
        # Виконання команди і збереження виводу в змінну
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True)
        tqdm.write(result.stdout)
        print(result.stdout)

        # Збереження виводу команди у файл логів
        with open(log_file, "a") as f:
            f.write(result.stdout)

    except subprocess.CalledProcessError as e:
        # Збереження інформації про помилку
        log_command(colors.fg.red + f"Error command: {command}" + colors.reset)
        log_command(str(e))
        exit(1)


def log_command(log_message):
    # Запис інформації у файл логів
    with open(log_file, "a") as f:
        f.write(log_message + "\n")


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


def arch_system():
    run_command("arch-chroot /mnt")


# Виклик функції для встановлення Arch Linux
other()
hello()
disk()
install_system_and_tools()
arch_system()
