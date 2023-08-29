import subprocess
from color import colors
import sys


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


def modify_lines_in_file(filename, lines_to_modify):
    with open(filename, 'r') as f:
        lines = f.readlines()

    with open(filename, 'w') as f:
        for line in lines:
            modified_line = line
            for target_line, replacement in lines_to_modify:
                if target_line in line:
                    modified_line = line.replace(target_line, replacement).lstrip("#")
            f.write(modified_line)


def clear():
    run_command("clear")


def arch_system():
    run_command("echo 'User-PC' >> /etc/hostname")
    run_command("ln -sf /usr/share/zoneinfo/Europe/Kiev /etc/localtime")
    uncomment_lines = [
        ("#en_US.UTF-8 UTF-8", "en_US.UTF-8 UTF-8"),
        ("#uk_UA.UTF-8 UTF-8", "uk_UA.UTF-8 UTF-8"),
        ("#ru_RU.UTF-8 UTF-8", "ru_RU.UTF-8 UTF-8")
    ]
    modify_lines_in_file("/etc/locale.gen", uncomment_lines)

    run_command("locale-gen")
    run_command("echo 'LANG=en_US.UTF-8' >> /etc/locale.conf")
    run_command("mkinitcpio -P")


def grub():
    run_command("pacman -Syy")
    run_command("pacman -S --noconfirm grub efibootmgr")
    run_command("grub-install /dev/sda")
    run_command("pacman -S --noconfirm os-prober mtools fuse")
    run_command("grub-mkconfig -o /boot/grub/grub.cfg")

    lines_to_modify = [
        ("#GRUB_DISABLE_OS_PROBER=false", "GRUB_DISABLE_OS_PROBER=true")
    ]
    modify_lines_in_file("/etc/default/grub", lines_to_modify)

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
        ("#ParallelDownloads = 5", "ParallelDownloads = 5"),
        ("#UseSyslog", "UseSyslog"),
        ("#Color", "Color"),
        ("#VerbosePkgLists", "VerbosePkgLists"),
        ("#[multilib]", "[multilib]")
    ]
    modify_lines_in_file("etc/pacman.conf", uncomment_lines)

    run_command(r"sed -i '/^\[multilib\]$/,/^$/ s/^#[[:space:]]*\(.*\)/\1/' /etc/pacman.conf")
    run_command("reflector --verbose --country 'Ukraine,Germany' --sort rate --save /etc/pacman.d/mirrorlist")


def black_list():
    run_command("curl -O https://blackarch.org/strap.sh")
    run_command("chmod +x strap.sh")
    run_command("sh strap.sh")
    run_command("sudo pacman -Syu --noconfirm")
    run_command("rm strap.sh")


def install_pkg():
    run_command("pacman -Syy")
    run_command("pacman -Syy")
    run_command("pacman-key --init")
    run_command("pacman-key --populate archlinux")


def de_win():
    run_command("pacman -S --noconfirm xfce4 xfce4-goodies ly")
    run_command("systemctl enable ly")


def audio():
    run_command("pacman -S --noconfirm pulseaudio pulseaudio-alsa pulseaudio-jack pavucontrol")
    run_command("pacman -S --noconfirm alsa-lib alsa-utils alsa-firmware alsa-card-profiles alsa-plugins")


def file_m():
    run_command("pacman -S --noconfirm pcmanfm-gtk3 gvfs gvfs-mtp")


def net():
    run_command("pacman -S --noconfirm dialog wpa_supplicant dhcpcd netctl networkmanager network-manager-applet ppp")
    run_command("systemctl enable NetworkManager")


def fonts():
    run_command("pacman -S --noconfirm noto-fonts noto-fonts-cjk noto-fonts-emoji ttf-liberation ttf-dejavu")


def xorg():
    run_command("pacman -S --noconfirm xorg-server xorg-server-common xorg-xinit")


def wine():
    run_command("pacman -S --noconfirm wine-staging winetricks wine-mono giflib lib32-giflib libpng lib32-libpng")
    run_command("pacman -S --noconfirm gst-plugins-base-libs lib32-gst-plugins-base-libs vulkan-icd-loader")
    run_command("pacman -S --noconfirm opencl-icd-loader lib32-opencl-icd-loader libxslt lib32-libxslt libva")
    run_command("pacman -S --noconfirm libxcomposite lib32-libxcomposite libxinerama lib32-libgcrypt libgcrypt")
    run_command("pacman -S --noconfirm alsa-plugins lib32-alsa-plugins alsa-lib lib32-alsa-lib libjpeg-turbo")
    run_command("pacman -S --noconfirm openal lib32-openal v4l-utils lib32-v4l-utils libpulse lib32-libpulse")
    run_command("pacman -S --noconfirm libldap lib32-libldap gnutls lib32-gnutls mpg123 lib32-mpg123")
    run_command("pacman -S --noconfirm lib32-vulkan-icd-loader lib32-libva gtk3 lib32-gtk3")
    run_command("pacman -S --noconfirm libgpg-error lib32-libgpg-error lib32-libjpeg-turbo sqlite lib32-sqlite")
    run_command("pacman -S --noconfirm lib32-libxinerama ncurses lib32-ncurses")
    run_command("mkinitcpio -P")


def archive():
    run_command("pacman -S --noconfirm lrzip unrar unzip unace p7zip squashfs-tools file-roller")


def intel():
    run_command("pacman -Syy")
    run_command("pacman -S --noconfirm mesa lib32-mesa vulkan-intel lib32-vulkan-intel ")
    run_command("pacman -S --noconfirm vulkan-icd-loader lib32-vulkan-icd-loader")
    run_command("pacman -S --noconfirm intel-ucode polkit")
    run_command("mkinitcpio -P")
    run_command("grub-mkconfig -o /boot/grub/grub.cfg")


def nvidia():
    run_command("pacman -Syy")
    run_command("pacman -S --noconfirm nvidia-dkms nvidia-utils lib32-nvidia-utils nvidia-settings vulkan-icd-loader")
    run_command("pacman -S --noconfirm lib32-vulkan-icd-loader lib32-opencl-nvidia opencl-nvidia libxnvctrl")
    run_command("pacman -S --noconfirm nvidia-prime")
    run_command("mkinitcpio -P")


def other():
    run_command("pacman -S --noconfirm grub-customizer obs-studio vlc kitty bleachbit")
    run_command("pacman -S --noconfirm steam firefox qbittorrent ntp go ntfs-3g")
    run_command("pacman -S --noconfirm gufw")
    run_command("systemctl enable ufw.service")

def yay():
    run_command("pacman -S --noconfirm yay")


def zsh():
    run_command("pacman -S --noconfirm zsh")
    run_command('sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"')
    run_command('sudo -u user sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"')
    # run_command("sudo -u user chsh -s /bin/zsh")

def optimizm():
    run_command("systemctl enable fstrim.timer ")
    run_command("fstrim -av")
    run_command("pacman -S --noconfirm rng-tools")
    run_command("systemctl enable rngd")
    run_command("pacman -S --noconfirm dbus-broker")
    run_command("systemctl enable dbus-broker.service")
    run_command("systemctl --global enable dbus-broker.service")
    run_command("pacman -S --noconfirm irqbalance")
    run_command("systemctl enable irqbalance")
    run_command("pacman -S --noconfirm jemalloc")
    run_command('echo "LD_PRELOAD=/usr/lib/libjemalloc.so" >> /etc/environment')
    run_command("systemctl mask NetworkManager-wait-online.service")

    uncomment_lines = [
        ("HOOKS=(base udev autodetect modconf kms keyboard keymap consolefont block filesystems fsck)",
         "HOOKS=(systemd autodetect modconf kms keymap keyboard  block btrfs usr)"
         ),
        ("MODULES=()", "MODULES=(btrfs nvme i915 nvidia)")
    ]
    modify_lines_in_file("/etc/mkinitcpio.conf", uncomment_lines)

    run_command("mkinitcpio -P")

    uncomment_lines = [
        ('GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 quiet"',
         'GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 rootfstype=btrfs page_alloc.shuffle=1 split_lock_detect=off raid=noautodetect nowatchdog noibrs noibpb nospec_store_bypass_disable no_stf_barrier mitigations=off"')
    ]

    modify_lines_in_file("/etc/default/grub", uncomment_lines)
    run_command("grub-mkconfig -o /boot/grub/grub.cfg")
    run_command("pacman -S --noconfirm gamemode lib32-gamemode gamescope")
    run_command("systemctl --user enable gamemoded")

def lost():
    print(colors.fg.green + "Installation complete. Press Enter to close the script." + colors.reset)
    input()
    sys.exit()


clear()
hello()
arch_system()
grub()
user()
root_password()
user_password()
add_user_root()
mirrorlist()
black_list()
install_pkg()
de_win()
audio()
file_m()
net()
fonts()
xorg()
wine()
archive()
intel()
nvidia()
other()
yay()
zsh()
optimizm()
lost()
