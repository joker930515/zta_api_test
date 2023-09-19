# coding=utf-8
import unittest
import os


def load_all_test():
    case_path = os.path.join(os.getcwd(), '../case')
    discover = unittest.defaultTestLoader.discover(case_path, pattern='*Case.py', top_level_dir=None)
    return discover


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(load_all_test())
