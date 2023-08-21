import subprocess
from color import colors
import time
import threading
import sys

log_file = "command_logs.txt"


def clear():
    run_command("clear")

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


def update_config_line(filename, target_line, new_value):
    updated_lines = []
    found_target = False

    with open(filename, 'r') as file:
        lines = file.readlines()

    with open(filename, 'w') as file:
        for line in lines:
            if line.strip().startswith(target_line):
                updated_lines.append(f'{target_line}={new_value}\n')
                found_target = True
            else:
                updated_lines.append(line.replace('false', new_value))

        file.writelines(updated_lines)

    return found_target

def uncomment_line_in_file(filename, target_line):
    with open(filename, 'r') as f:
        lines = f.readlines()

    with open(filename, 'w') as f:
        for line in lines:
            if line.strip() == target_line:
                f.write(line.lstrip("#"))  # Видаляємо символ '#' з початку рядка
            else:
                f.write(line)

def uncomment_lines_in_config_file(filename, lines_to_uncomment):
    for line in lines_to_uncomment:
        uncomment_line_in_file(filename, line)

def arch_system():
    run_command("echo 'User-PC' >> /etc/hostname")
    run_command("ln -sf /usr/share/zoneinfo/Europe/Kiev /etc/localtime")
    uncomment_lines = [
        "#en_US.UTF-8 UTF-8",
        "#uk_UA.UTF-8 UTF-8",
        "#ru_RU.UTF-8 UTF-8"
    ]
    uncomment_lines_in_config_file("/etc/locale.gen", uncomment_lines)

    run_command("locale-gen")
    run_command("echo 'LANG=en_US.UTF-8' >> /etc/locale.conf")
    run_command("mkinitcpio -P")


def grub():
    run_command("pacman -Syy")
    run_command("pacman -S --noconfirm grub efibootmgr")
    run_command("grub-install /dev/sda")
    run_command("pacman -S --noconfirm os-prober mtools fuse")

    filename = '/etc/default/grub'
    target_line = '#GRUB_DISABLE_OS_PROBER=false'
    new_value = 'true'

    update_config_line(filename, target_line, new_value)

    run_command("grub-mkconfig -o /boot/grub/grub.cfg")


def user():
    run_command("useradd -m -g users -G wheel -s /bin/zsh user")


def root_password():
    new_password = "1234"  # Замініть на фактичний пароль
    command = f"echo '{new_password}\n{new_password}' | passwd"
    subprocess.run(command, shell=True)


def user_password():
    new_password = "1234"  # Замініть на фактичний пароль
    command = f"echo '{new_password}\n{new_password}' | passwd user"
    subprocess.run(command, shell=True)


def add_user_root():
    run_command(r"sed -i '/root ALL=(ALL:ALL) ALL/a user ALL=(ALL:ALL) ALL' /etc/sudoers")


def mirrorlist():
    uncomment_lines = [
        "#ParallelDownloads = 5",
        "#UseSyslog",
        "#Color",
        "#VerbosePkgLists",
        "#[multilib]"
    ]
    uncomment_lines_in_config_file("/etc/pacman.conf", uncomment_lines)

    run_command(r"sed -i '/^\[multilib\]$/,/^$/ s/^#[[:space:]]*\(.*\)/\1/' /etc/pacman.conf")
    run_command("reflector --verbose --country 'Ukraine,Germany' --sort rate --save /etc/pacman.d/mirrorlist")


def black_repository():
    run_command("curl -O https://blackarch.org/strap.sh")
    run_command("chmod +x strap.sh")
    run_command("strap.sh")
    run_command("sudo pacman -Syy")
    run_command("sudo pacman -Syu")
    run_command("strap.sh")


def install_pkg():
    run_command("pacman -Syy")
    run_command("pacman -Syy")
    run_command("pacman-key --init")
    run_command("pacman-key --populate archlinux")
    run_command("pacman -S --noconfirm lrzip unrar unzip unace p7zip squashfs-tools")
    run_command("pacman -S --noconfirm file-roller")
    run_command(
        "pacman -S --noconfirm nvidia-dkms nvidia-utils lib32-nvidia-utils nvidia-settings vulkan-icd-loader lib32-vulkan-icd-loader lib32-opencl-nvidia opencl-nvidia libxnvctrl nvidia-prime")
    run_command("mkinitcpio -P")
    run_command("pacman -S --noconfirm xorg-server xorg-server-common xorg-server-xwayland xorg-xinit")
    run_command("pacman -S --noconfirm noto-fonts noto-fonts-cjk noto-fonts-emoji ttf-liberation")
    run_command(
        "pacman -S --noconfirm mesa lib32-mesa vulkan-intel lib32-vulkan-intel vulkan-icd-loader lib32-vulkan-icd-loader")
    run_command("pacman -S --noconfirm intel-ucode polkit ntfs-3g")
    run_command("mkinitcpio -P")
    run_command("grub-mkconfig -o /boot/grub/grub.cfg")
    run_command("pacman -S --noconfirm dialog wpa_supplicant dhcpcd netctl networkmanager network-manager-applet ppp")
    run_command("pacman -S --noconfirm pulseaudio pulseaudio-alsa pulseaudio-jack pavucontrol")
    run_command("pacman -S --noconfirm alsa-lib alsa-utils alsa-firmware alsa-card-profiles alsa-plugins")
    run_command("pacman -S --noconfirm pulseaudio pulseaudio-alsa pulseaudio-jack pavucontrol")
    run_command("pacman -S --noconfirm grub-customizer obs-studio vlc kitty firefox qbittorrent ntp")
    run_command("pacman -S --noconfirm grub-customizer obs-studio vlc kitty firefox qbittorrent ntp")
    run_command("pacman -S --noconfirm xfce4 xfce4-goodies lightdm")
    run_command("pacman -Rscn --noconfirm $(pacman -Qtdq --noconfirm)")


def sysctl():
    run_command("systemctl enable NetworkManager")
    run_command("systemctl enable lightdm")

clear()
arch_system()
grub()
user()
root_password()
user_password()
add_user_root()
mirrorlist()
black_repository()
install_pkg()
sysctl()
