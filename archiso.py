import subprocess
from color import colors
import sys


def clear():
    run_command("clear")


def hello():
    print(colors.fg.cyan +
          f"""
 █████  ██████   ██████ ██   ██     ██      ██ ███    ██ ██    ██ ██   ██     ██ ███    ██ ███████ ████████  █████  ██      ██      
██   ██ ██   ██ ██      ██   ██     ██      ██ ████   ██ ██    ██  ██ ██      ██ ████   ██ ██         ██    ██   ██ ██      ██      
███████ ██████  ██      ███████     ██      ██ ██ ██  ██ ██    ██   ███       ██ ██ ██  ██ ███████    ██    ███████ ██      ██      
██   ██ ██   ██ ██      ██   ██     ██      ██ ██  ██ ██ ██    ██  ██ ██      ██ ██  ██ ██      ██    ██    ██   ██ ██      ██      
██   ██ ██   ██  ██████ ██   ██     ███████ ██ ██   ████  ██████  ██   ██     ██ ██   ████ ███████    ██    ██   ██ ███████ ███████

""" + colors.reset)


log_file = "full_logs.txt"
clear_log_file = "clear_log.txt"


def run_command(command):
    print(colors.fg.yellow + "Running command: " + colors.reset, command)
    log_command(f"Running command: {command}")

    try:
        process = subprocess.Popen(
            command, shell=True, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        output_lines = []

        for line in process.stdout:
            output_lines.append(line.strip())
            if command == "clear":
                sys.stdout.write(line)
                sys.stdout.flush()

        process.wait()

        if command != "clear":
            if process.returncode == 0:
                sys.stdout.write("\r" + " " * 30 + "\r" + colors.fg.green + "[OK]\n" + colors.reset)
                log_clear_command(f"Running command: {command} [OK]")
            else:
                sys.stdout.write("\r" + " " * 30 + "\r" + colors.fg.red + "[ERROR]\n" + colors.reset)
                log_clear_command(f"Running command: {command} [ERROR]")
                log_clear_command("\n".join(output_lines))
            sys.stdout.flush()

        for line in output_lines:
            log_command(line)

    except subprocess.CalledProcessError as e:
        log_command(colors.fg.green + f"Error command: {command}" + colors.reset)
        log_command(str(e))
        log_clear_command(f"Running command: {command} [ERROR]")
        log_clear_command(str(e))
        exit(1)


def log_command(log_message):

    with open(log_file, "a") as f:
        f.write(log_message + "\n")


def log_clear_command(log_message):

    with open(clear_log_file, "a") as f:
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
    run_command(
        "pacstrap /mnt base base-devel btrfs-progs linux linux-headers dkms linux-lts linux-lts-headers linux-zen linux-zen-headers kitty linux-firmware nano vim netctl dhcpcd git wget curl reflector rsync zsh")
    run_command("genfstab -pU /mnt >> /mnt/etc/fstab")


def arch_chroot():
    run_command('''arch-chroot /mnt sh -c "git clone https://github.com/raBBit377/Arch_script"''')


def lost():
    print(colors.fg.green + "Installation complete. Press Enter to close the script." + colors.reset)
    input()
    run_command("arch-chroot.sh")
    sys.exit()



clear()
hello()
other()
disk()
install_system_and_tools()
arch_chroot()
lost()
