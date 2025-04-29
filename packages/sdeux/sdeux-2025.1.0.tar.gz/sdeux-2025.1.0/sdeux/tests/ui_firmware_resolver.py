# -*- coding: utf-8 -*-
"""
Created by chiesa

Copyright Alpes Lasers SA, Switzerland
"""
__author__ = 'chiesa'
__copyright__ = "Copyright Alpes Lasers SA"

from sdeux.updater.writer import resolve_version

if __name__ == '__main__':
    print(resolve_version('last'))