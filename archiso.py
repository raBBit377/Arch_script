import subprocess
from color import colors
import time
import threading
import sys

def clear():
    run_command("clear")
def hello():
    print(colors.fg.cyan + f""" █████  ██████   ██████ ██   ██     ██      ██ ███    ██ ██    ██ ██   ██     ██ ███    ██ ███████ ████████  █████  ██      ██      
██   ██ ██   ██ ██      ██   ██     ██      ██ ████   ██ ██    ██  ██ ██      ██ ████   ██ ██         ██    ██   ██ ██      ██      
███████ ██████  ██      ███████     ██      ██ ██ ██  ██ ██    ██   ███       ██ ██ ██  ██ ███████    ██    ███████ ██      ██      
██   ██ ██   ██ ██      ██   ██     ██      ██ ██  ██ ██ ██    ██  ██ ██      ██ ██  ██ ██      ██    ██    ██   ██ ██      ██      
██   ██ ██   ██  ██████ ██   ██     ███████ ██ ██   ████  ██████  ██   ██     ██ ██   ████ ███████    ██    ██   ██ ███████ ███████

""" + colors.reset )



log_file = "command_logs.txt"
animation_event = threading.Event()

def loading_animation():
    animation = ["[#    ]", "[##   ]", "[###  ]", "[#### ]", "[#####]"]
    i = 0
    while not animation_event.is_set():  # Поки сигналізація не встановлена
        sys.stdout.write("\r" + animation[i])
        sys.stdout.flush()
        i = (i + 1) % len(animation)
        time.sleep(0.5)
    sys.stdout.write("\r" + " " * 30 + "\r")  # Очистка останнього рядка
    sys.stdout.flush()

def run_command(command):
    print(colors.fg.green + "Running command: " + colors.reset, command)
    log_command(f"Running command: {command}")

    animation_event.clear()
    animation_thread = threading.Thread(target=loading_animation)
    animation_thread.start()

    try:
        process = subprocess.Popen(
            command, shell=True, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        output_lines = []

        for line in process.stdout:
            output_lines.append(line.strip())
            if command == "clear":
                sys.stdout.write(line)  # Вивід виводу команди в консоль
                sys.stdout.flush()

        process.wait()

        animation_event.set()
        animation_thread.join()

        if command == "clear":
            sys.stdout.write("\r" + " " * 30 + "\r")
            sys.stdout.flush()

        for line in output_lines:
            log_command(line)  # Запис виводу команди в лог-файл

    except subprocess.CalledProcessError as e:
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



def arch_chroot():
    run_command('''arch-chroot /mnt sh -c "git clone https://github.com/raBBit377/Arch_script && python /mnt/Arch_script/arch-chroot.py"''')


# Виклик функції для встановлення Arch Linux
clear()
hello()
other()
disk()
install_system_and_tools()
arch_chroot()
sys.exit()