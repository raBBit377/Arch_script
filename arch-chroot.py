import subprocess
from color import colors


def run_command(command):
    try:
        return subprocess.run(command, shell=True, check=True, stdout=None, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        print(colors.fg.red + f"Error command: {command}" + colors.reset)
        print(e)
        exit(1)


def arch_system():
    run_command("echo 'User-PC' >> /etc/hostname")
    run_command("ln -sf /usr/share/zoneinfo/Europe/Kiev /etc/localtime")
    run_command("sed -i 's/^# *\(en_US.UTF-8 UTF-8\)/\1/' /etc/locale.gen")
    run_command("sed -i 's/^# *\(uk_UA.UTF-8 UTF-8\)/\1/' /etc/locale.gen")
    run_command("sed -i 's/^# *\(ru_RU.UTF-8 UTF-8\)/\1/' /etc/locale.gen")
    run_command("locale-gen")
    run_command("echo 'LANG=ru_RU.UTF-8' >> /etc/locale.conf")
    run_command("mkinitcpio -P")


def grub():
    run_command("pacman -Syy")
    run_command("pacman -S --noconfirm grub efibootmgr")
    run_command("grub-install /dev/sda")
    run_command("pacman -S --noconfirm os-prober mtools fuse")
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
    run_command("sed -i '/root ALL=(ALL:ALL) ALL/a user ALL=(ALL:ALL) ALL' /etc/sudoers")


def list():
    run_command("sed -i 's/^#\(ParallelDownloads = 5\)/\1/' /etc/pacman.conf")
    run_command("sed -i 's/^#[[:space:]]*\(UseSyslog\)/\1/' /etc/pacman.conf")
    run_command("sed -i 's/^#[[:space:]]*\(Color\)/\1/' /etc/pacman.conf")
    run_command("sed -i 's/^#[[:space:]]*\(VerbosePkgLists\)/\1/' /etc/pacman.conf")
    run_command("sed -i 's/^#[[:space:]]*\[multilib\]/[multilib]/' /etc/pacman.conf")
    run_command("sed -i '/^\[multilib\]$/,/^$/ s/^#[[:space:]]*\(.*\)/\1/' /etc/pacman.conf")
    run_command("reflector --verbose --country 'Ukraine,Germany' --sort rate --save /etc/pacman.d/mirrorlist")


def aur():
    run_command("git clone https://aur.archlinux.org/yay.git")
    run_command("cd yay")
    run_command("makepkg -sric --install")
    run_command("pacman -Syy")
    run_command("cd")


def install_pkg():
    run_command("pacman -Syy")
    run_command("pacman -Syy")
    run_command("pacman-key --init")
    run_command("pacman-key --populate archlinux")
    run_command("pacman -S --noconfirm lrzip unrar unzip unace p7zip squashfs-tools")
    run_command("pacman -S --noconfirm file-roller")
    run_command("pacman -S --noconfirm nvidia-dkms nvidia-utils lib32-nvidia-utils nvidia-settings vulkan-icd-loader lib32-vulkan-icd-loader lib32-opencl-nvidia opencl-nvidia libxnvctrl nvidia-prime")
    run_command("mkinitcpio -P")
    run_command("pacman -S --noconfirm xorg-server xorg-server-common xorg-server-xwayland xorg-xinit")
    run_command("pacman -S --noconfirm noto-fonts noto-fonts-cjk noto-fonts-emoji ttf-liberation")
    run_command("pacman -S --noconfirm mesa lib32-mesa vulkan-intel lib32-vulkan-intel vulkan-icd-loader lib32-vulkan-icd-loader")
    run_command("pacman -S --noconfirm intel-ucode polkit ntfs-3g")
    run_command("mkinitcpio -P")
    run_command("grub-mkconfig -o /boot/grub/grub.cfg")
    run_command("pacman -S --noconfirm dialog wpa_supplicant dhcpcd netctl networkmanager network-manager-applet ppp")
    run_command("pacman -S --noconfirm pulseaudio pulseaudio-alsa pulseaudio-jack pavucontrol")
    run_command("pacman -S --noconfirm alsa-lib alsa-utils alsa-firmware alsa-card-profiles alsa-plugins")
    run_command("pacman -S --noconfirm pulseaudio pulseaudio-alsa pulseaudio-jack pavucontrol")
    run_command("pacman -S --noconfirm grub-customizer obs-studio vlc kitty firefox qbittorrent ntp")
    run_command("pacman -Rscn --noconfirm $(pacman -Qtdq --noconfirm)")
