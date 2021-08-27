## Get Started

-  The network backend doesn't support reading back the printer state, currently. Failure such as wrong label type or end of label roll reached won't be detected by this software.
-  (Linux) The label printer should show up automatically as /dev/usb/lp0 when connected. Please check the ownership (user, group) of this file to be able to print as a regular user. Consider setting up a udev .rules file.

### PyUSB is a Python wrapper allowing to implement USB communication in userspace.

On Linux: install libusb1 as offered by your distribution: `sudo apt-get install libusb-1.0-0` (Ubuntu, Debian), `sudo zyppe in libusb-1_0-0` (OpenSUSE), `sudo pacman -S libusb` (Arch).

On Mac OS: Install Homebrew and then install libusb1 using: `brew install libusb`.

On Windows: download `libusb-win32-devel-filter-1.2.6.0.exe` from https://sourceforge.net/projects/libusb-win32/files/libusb-win32-releases/1.2.6.0/ and install it. After installing, you have to use the "Filter Wizard" to setup a "device filter" for the label printer.`

### Linux/macOS Install

```
> git clone https://github.com/sidha/white-rose.git stickers
> cd stickers
> python3 -m venv venvstickers
> source venvstickers/bin/activate
> pip install -U pip
> pip install -r requirements.txt
```

### Windows Install

Follow instructions here to install venv on Windows:
https://www.c-sharpcorner.com/article/steps-to-set-up-a-virtual-environment-for-python-development/

then:

```
> pip install -U pip
> pip install -r requirements.txt
```

### Find Your Printer

Connect your printer to your USB port and turn it on. Then run:

`brother_ql -b pyusb discover`

You should see something like:

`usb://0x04f9:0x209b_Љ`

when using this url, remove the ending `_Љ` so the correct path is:

`usb://0x04f9:0x209b`


### Supported Printers(USB Only):

The library that this script depends on supports the following printers, but the script itself currenly only supports USB-connected printers.

* QL-500
* QL-550
* QL-560
* QL-570
* QL-580N
* QL-650TD
* QL-700
* QL-710W
* QL-720NW
* QL-800
* QL-810W
* QL-820NWB
* QL-1050
* QL-1060N

## Examples

## PRINT FOLDER
### Print a total of 70 random stickers from a folder of JPGs to a QL-800:
* Print 70 random stickers from a folder

`python stickers.py printfolder file/path/to/stickers/whiterose_caffeine_pack --printer-model QL-800 --printer-url usb://0x04f9:0x209b --sticker-count 70`

### Print a total of 70 random stickers from a folder of JPGs to a QL-700:
* Print 60 random stickers from a folder
* Print at least 10 kary-mullis-pcr-1.jpg
* (will print a total of 70 stickers, 60 random from a folder, and 10 of them will be kary-mullis-pcr-1.jpg):

`python stickers.py printfolder stickers/whiterose_caffeine_pack --printer-model QL-700 --printer-url usb://0x04f9:0x209b --sticker-count 70 --print-at-least 10 path/to/stickers/custom/kary-mullis-pcr-1.jpg`

### Print a total of 80 random stickers from a folder of JPGs to a QL-800:
* Print 50 random stickers from a folder
* Print at least 10 kary-mullis-pcr-1.jpg
* Print at least 10 mike-yeadon-gov-virus-lie.jpg
* Print an extra 5 redpillsxyz-sticker21.jpg
* Print an extra 5 jointhewhiterose2-qr.jpg
* (will print a total of 80 stickers, 50 random from a folder, and 10 of them will be kary-mullis-pcr-1.jpg, 10 of them will be mike-yeadon-gov-virus-lie.jpg, 5 extra redpillsxyz-sticker21.jpg, 5 extra jointhewhiterose2-qr.jpg):

`python stickers.py printfolder stickers/whiterose_caffeine_pack --printer-model QL-800 --printer-url usb://0x04f9:0x209b --sticker-count 70 --print-at-least 10 path/to/stickers/custom/kary-mullis-pcr-1.jpg 10  path/to/stickers/custom/mike-yeadon-gov-virus-lie.jpg --print-extra 5 /Users/michael/bin/redpills-xyz/stickers/custom/redpillsxyz-sticker21.jpg 5 path/to/stickers/custom/jointhewhiterose2-qr.jpg`

## PRINT IMAGES

* Print a total of 15 random stickers with five specific stickers:

`python stickers.py printimages path/to/stickers/custom/redpillsxyz-sticker21.jpg path/to/stickers/custom/mike-yeadon-gov-virus-lie.jpg path/to/stickers/custom/jointhewhiterose2-qr.jpg path/to/stickers/custom/kary-mullis-pcr-1.jpg path/to/stickers/custom/BreathingBacteriaKeepsMeSafe.jpg --printer-model QL-800 --printer-url usb://0x04f9:0x209b --sticker-count 15`

* Print individual sticker 
python stickers.py printimages Folder\LittleSusie.cleaned.jpg --printer-url usb://0x04f9:0x209b --printer-model QL-800 --sticker-count 2

### Disable Autorotate

Wide stickers are auto-rotated 90 degrees. If you need to disable this, add the flag `--disable-autorotate` to the command.
