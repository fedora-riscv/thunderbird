# Makefile for source rpm: thunderbird
# $Id$
NAME := thunderbird
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
