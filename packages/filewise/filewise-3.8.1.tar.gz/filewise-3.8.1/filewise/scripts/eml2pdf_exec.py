#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#------------------------#
# Import project modules #
#------------------------#

from filewise.format_converters.pdf_tools import eml_to_pdf

#-------------------#
# Define parameters #
#-------------------#

path = "/home/jonander/Documents"
delete_eml_files = False

#-----------------------------#
# Convert every email message #
#-----------------------------#

eml_to_pdf(path, delete_eml_files)
