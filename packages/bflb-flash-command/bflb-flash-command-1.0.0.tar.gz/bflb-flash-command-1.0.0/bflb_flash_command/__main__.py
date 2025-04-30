# -*- coding:utf-8 -*-

import sys
import BLFlashCommand


def run_main():
    app = BLFlashCommand.MainClass()
    app.main(sys.argv[1:])


if __name__ == "__main__":
    run_main()
