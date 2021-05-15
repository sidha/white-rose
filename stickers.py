#!/usr/bin/env python
import argparse
import sys
import os
import copy
from random import randrange

sys.path.append(".")

def get_all_values(d):
    if isinstance(d, dict):
        for v in d.values():
            yield from get_all_values(v)
    elif isinstance(d, list):
        for v in d:
            yield from get_all_values(v)
    else:
        yield d 

class Main(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='tools to manage printing stickers with brother ql label printer',
            usage='''printfolder <dir>
                    printimages <images>
''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])

        print('Main {}'.format(args.command))

        if args.command == 'printfolder':
            printfolder = PrintFolder()
            printfolder.start(args)
        elif args.command == 'printimages':
            printimages = PrintImages()
            printimages.start(args)
        else:
            print('Unrecognized command')
            parser.print_help()
            exit(1)

def walk_folder(media_dir, file_extension, modified_since=None):
    # print('walk_folder media_dir: {}'.format(repr(media_dir)))
    # print('walk_folder modified_since: {}'.format(repr(modified_since)))
    # print('os.path.abspath(f): {}'.format(repr(os.path.abspath(media_dir))))
    all_file_paths = get_filepaths(os.path.abspath(media_dir))
    ts_paths = []
    for f in all_file_paths:

        if f.endswith('.{}'.format(file_extension)):
            if modified_since is None:
                ts_paths.append(f)
                # print('output_name: {}'.format(f))
                basename = os.path.basename(f)
                # print('basename: {}'.format(basename))
            else:
                modtime = os.path.getmtime(f)
                # print('modtime: {}'.format(modtime))
                # print('modified_since.timestamp(): {}'.format(modified_since.timestamp()))
                if modtime > modified_since.timestamp():
                    # print('file new enough to be appended: {}'.format(modtime))
                    ts_paths.append(f)
                    basename = os.path.basename(f)

    return sorted(ts_paths, key=lambda i: os.path.splitext(os.path.basename(i))[0])

def get_filepaths(directory):
    """
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths # Self-explanatory.

def sanitize_filename(filepath):

    numbername = filepath.replace('#', 'Number_')
    percentname = numbername.replace('%', '_Percent')

    if percentname != filepath:
        os.rename(filepath, percentname)
        print('sanitized: {}'.format(percentname))
        return percentname
    else:
        return filepath


def build_options(filepath, options):
    components = filepath.split("/")
    filename = components[-1]
    folder_name = components[-2]
    options['filepath'] = filepath
    options['filename'] = filename
    options['folder_name'] = folder_name

    return copy.deepcopy(options)
from pathlib import Path

class PrintFolder(object):
    def __init__(self):
        print('PrintFolder init')

    def start(self, args):
        print('PrintFolder.start args {}'.format(args))
        parser = argparse.ArgumentParser(
            description='parse dirs to determine which images to print to label printer')
        # prefixing the argument with -- means it's optional
        # parser.add_argument('dir')
        parser.add_argument('dirs', nargs='+')#, help='<Required> Set flag', required=True)
        parser.add_argument('--dry-run', dest='dry_run', action='store_true')
        parser.add_argument('--printer-url', dest='printer_url', help='USB path of the printer')
        parser.add_argument('--printer-model', dest='printer_model', help='name of the Brother printer i.e.: QL-800')
        parser.add_argument('--file-extension', dest='file_extension', help='walk dirs to find these types, default is jpg')
        parser.add_argument('--sticker-count', dest='sticker_count', help='number of stickers to print in job')
        parser.add_argument('--sticker-size', dest='sticker_size', help='regular or mini')
        parser.add_argument('--print-at-least', nargs='*', dest='print_at_least', help='print at least this number of this sticker')
        parser.add_argument('--print-extra', nargs='*', dest='print_extra', help='print extra this number of this sticker')
        parser.set_defaults(dry_run=False)
        parser.set_defaults(sticker_size='regular')
        parser.set_defaults(file_extension='jpg')
        args = parser.parse_args(sys.argv[2:])
        print('Running PrintFolder.start, args: {}'.format(repr(args)))

        printfolder_files = []
        paths = []
        for directory in args.dirs:
            files = walk_folder(directory, args.file_extension)
            paths.extend(files)
        # base_options = copy.deepcopy(args)
        for path in paths:
            args_dict = args.__dict__
            # print('args_dict: {}'.format(args_dict))
            sanitized = sanitize_filename(path)
            options = build_options(sanitized, args_dict)
            # options = build_options(sanitized, args_dict)
            # print('options: {}'.format(options))
            printfolder_files.append(options)

        if args.print_at_least:
            if len(args.print_at_least) % 2 != 0:
                print("there must be an even number of items in --print-at-least, found {}".format(len(options["print_at_least"])))
                print("--print-at-least: {}".format(options["print_at_least"]))
                exit()

        if args.print_extra:
            if len(args.print_extra) % 2 != 0:
                print("there must be an even number of items in --print-extra, found {}".format(len(args.print_extra)))
                print("--print-extra: {}".format(args.print_extra))
                exit()

        if args.printer_url is None:
            print("--printer-url is not specified")
            exit()

        if args.printer_model is None:
            print("--printer-model is not specified")
            exit()

        sorted_array = sorted(printfolder_files, key=lambda x: x['filename'], reverse=False)
        if args.dry_run is False:
            if args.file_extension == 'jpg':
                self._printfolder_images(sorted_array, int(args.sticker_count), args.sticker_size, args.printer_model, args.printer_url, args.print_at_least, args.print_extra)
        else:
            print('dry_run sorted_array: {} stickers'.format(len(sorted_array)))

    def _printfolder_images(self, images, sticker_count, sticker_size, printer_model, printer_url, print_at_least=None, print_extra=None):
        remaining_count = sticker_count
        printed = 0
        it = None

        if print_at_least:
            it = iter(print_at_least)

            # print stickers that you want at least x of
            for t in it:
                count = int(t)
                imagefilepath = next(it)
                print('_printfolder_images count {}'.format(count))
                print('_printfolder_images image {}'.format(imagefilepath))

                for x in range(count):
                    printed = printed + 1
                    remaining_count = sticker_count - printed
                    print('printing {} of {}({} remaining): {}'.format(printed, sticker_count, remaining_count, imagefilepath))
                    os.system("brother_ql --model {} --backend pyusb --printer {} print -d --label 62 {}".format(printer_model, printer_url, imagefilepath))

        print('_printfolder_images remaining_count after repeats {}'.format(remaining_count))

        # the remaining stickers will be random
        # remaining_count = sticker_count - repeats
        if remaining_count < 0:
            remaining_count = 0

        for x in range(remaining_count):
            random_sticker = images[randrange(len(images))]
            printed = printed + 1
            remaining_count = sticker_count - printed
            print('printing {} of {}({} remaining): {}'.format(printed, sticker_count, remaining_count, random_sticker["filepath"]))
            os.system("brother_ql --model {} --backend pyusb --printer {} print -d --label 62 {}".format(printer_model, printer_url, random_sticker["filepath"]))
            # os.system("brother_ql --model QL-800 --backend pyusb --printer usb://0x04f9:0x209b print -d --label 62 {}".format(random_sticker["filepath"]))

        # extra stickers beyond sticker_count

        if print_extra:
            it = iter(print_extra)
            # print stickers that you want at least x of
            for t in it:
                count = int(t)
                imagefilepath = next(it)
                print('_printfolder_images count {}'.format(count))
                print('_printfolder_images image {}'.format(imagefilepath))

                for x in range(count):
                    printed = printed + 1
                    print('printing {} of {}: {}'.format(printed, sticker_count, imagefilepath))
                    os.system("brother_ql --model {} --backend pyusb --printer {} print -d --label 62 {}".format(printer_model, printer_url, imagefilepath))
                    # os.system("brother_ql --model QL-800 --backend pyusb --printer usb://0x04f9:0x209b print -d --label 62 {}".format(imagefilepath))


class PrintImages(object):
    def __init__(self):
        print('PrintImages init')

    def start(self, args):
        print('PrintImages.start args {}'.format(args))
        parser = argparse.ArgumentParser(
            description='images to print on brother printer')
        # prefixing the argument with -- means it's optional
        # parser.add_argument('dir')
        parser.add_argument('images', nargs='+')#, help='<Required> Set flag', required=True)
        parser.add_argument('--dry-run', dest='dry_run', action='store_true')
        parser.add_argument('--printer-url', dest='printer_url', help='USB path of the printer i.e: usb://0x04f9:0x209b')
        parser.add_argument('--printer-model', dest='printer_model', help='name of the Brother printer i.e.: QL-800')
        parser.add_argument('--file-extension', dest='file_extension', help='walk dirs to find these types, default is jpg')
        parser.add_argument('--sticker-count', dest='sticker_count', help='number of stickers to print in job')
        parser.add_argument('--sticker-size', dest='sticker_size', help='regular or mini')
        parser.set_defaults(dry_run=False)
        parser.set_defaults(sticker_size='regular')
        parser.set_defaults(file_extension='jpg')
        args = parser.parse_args(sys.argv[2:])
        print('Running PrintImages.start, args: {}'.format(repr(args)))

        if args.printer_url is None:
            print("--printer-url is not specified i.e. usb://0x04f9:0x209b")
            exit()

        if args.printer_model is None:
            print("--printer-model is not specified i.e. QL-800")
            exit()

        printimages_files = []
        # paths = []
        # for directory in args.images:
        #     files = walk_folder(directory, args.file_extension, args.modified_since)
        #     paths.extend(files)
        # base_options = copy.deepcopy(args)
        for path in args.images:
            args_dict = args.__dict__
            print('args_dict: {}'.format(args_dict))
            sanitized = sanitize_filename(path)
            options = build_options(sanitized, args_dict)
            # options = build_options(sanitized, args_dict)
            # print('options: {}'.format(options))
            printimages_files.append(options)
        sorted_array = sorted(printimages_files, key=lambda x: x['filename'], reverse=False)
        if args.dry_run is False:
            if args.file_extension == 'jpg':
                self._printimages_images(sorted_array, int(args.sticker_count), args.sticker_size, args.printer_model, args.printer_url)
        else:
            print('dry_run sorted_array: {} stickers'.format(len(sorted_array)))

    def _printimages_images(self, images, sticker_count, sticker_size, printer_model, printer_url):
        # print('_printimages_images images {}'.format(images))
        # print('_printimages_images sticker_pack_name {}'.format(sticker_pack_name))
        for x in range(sticker_count):
            random_sticker = images[randrange(len(images))]
            print('printing {} of {}({} remaining): {}'.format(x+1, sticker_count, sticker_count - (x+1), random_sticker["filepath"]))
            if sticker_size == "mini":
                os.system("brother_ql --model {} --backend pyusb --printer {} print -d --label 62 --rotate 90 {}".format(printer_model, printer_url, random_sticker["filepath"]))
            elif sticker_size == "regular":
                os.system("brother_ql --model {} --backend pyusb --printer {} print -d --label 62 {}".format(printer_model, printer_url, random_sticker["filepath"]))

if __name__ == '__main__':
    Main()
