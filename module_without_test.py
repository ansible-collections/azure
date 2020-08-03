#!/usr/bin/python
#
# Copyright (c) 2020 Guopeng Lin, <linguopeng1998@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# usage: put this script in the azure collection directory which contains tests and plugins
#        python module_without_test.py
#        or python module_without_test.py -d

import os
import re
import logging
import sys
import getopt
import traceback

warn_msg = []
modules = {}


def get_tests():
    global modules
    global warn_msg
    test_dir_path = os.path.join(os.getcwd(), "tests", 'integration', 'targets')
    targets = os.listdir(test_dir_path)
    pattern = "azure_rm_[a-z_]+"
    for target in targets:
        if not re.match(pattern, target):
            continue
        tasks = os.listdir(os.path.join(test_dir_path, target, 'tasks'))
        for task in tasks:
            test_file_name = os.path.join(test_dir_path, target, 'tasks', task)
            try:
                test_file = open(test_file_name)
                file_content = test_file.read()
                test_modules = re.findall(pattern, file_content)
                for test_module in test_modules:
                    if modules.get(test_module) is None:
                        warn_msg.append("{0} is not implemented but find in the test, target name: {1}, task name: {2}".format(test_module, target, task))
                        continue
                    modules[test_module]['test_count'] = modules[test_module]['test_count'] +1
                    modules[test_module]['test_files'].add(target)
            except Exception as er:
                traceback.print_exc()
                logging.error("target name: {0}  task name: {1}".format(target, task))
                exit(1)


def get_modules():
    global modules
    dir_path = os.path.join(os.getcwd(), "plugins", 'modules')
    if not os.path.exists(dir_path):
        logging.error("script should be put in the azure directory which contains the plugins and tests")
        exit(0)
    files = os.listdir(dir_path)
    modules = {}
    for file in files:
        module_name = file[0:-3]
        module_info = {
            'test_count': 0,
            'test_files': set()
        }
        modules[module_name] = module_info


def output_result(detail):
    global modules
    global warn_msg

    if detail:
        print("test details: ")
        for module_name in sorted(modules.keys()):
            msg = "     {0}:  \n" \
                  "         test_count: {1} \n" \
                  "         relevant files: {2}".format(module_name, modules[module_name]['test_count'], modules[module_name]['test_files'])
            print(msg)
    print("modules without test: ")
    for module_name in sorted(modules.keys()):
        if modules[module_name]['test_count'] == 0:
            print("  {0}".format(module_name))
    print("warning: ")
    for msg in warn_msg:
        print("  {0}:".format(msg))

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "d")
    except getopt.GetoptError:
        msg = "usage: python module_without_test.py \n " \
              " options: \n" \
              "     -d : to get the details"
        print(msg)
        sys.exit(2)
    detail = False
    for opt, arg in opts:
        if opt == '-d':
            detail = True
    get_modules()
    get_tests()
    output_result(detail)


if __name__ == '__main__':
    main(sys.argv[1:])