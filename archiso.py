import subprocess
from color import colors
import time
import threading
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

def loading_animation():
    animation = ["[#    ]", "[##   ]", "[###  ]", "[#### ]","[#####]"]
    for _ in range(10):  # Змініть кількість ітерацій за потреби
        for char in animation:
            sys.stdout.write("\r" + "Loading " + char)
            sys.stdout.flush()
            time.sleep(0.5)

def run_command(command):
    print(colors.fg.green + "Running command: " + colors.reset, command)
    log_command(f"Running command: {command}")

    try:
        process = subprocess.Popen(
            command, shell=True, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        animation_thread = threading.Thread(target=loading_animation)
        animation_thread.start()

        for line in process.stdout:
            log_command(line.strip())

        process.wait()

        animation_thread.join()

    except subprocess.CalledProcessError as e:
        # Збереження інформації про помилку
        log_command(colors.fg.green + f"Error command: {command}" + colors.reset)
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

