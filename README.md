## Get Started

### Install 

```
> git clone https://github.com/sidha/white-rose.git stickers
> cd stickers
> python3 -m venv venvstickers
> source venvstickers/bin/activate
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
