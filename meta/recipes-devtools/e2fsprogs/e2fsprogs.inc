SUMMARY = "Ext2 Filesystem Utilities"
DESCRIPTION = "The Ext2 Filesystem Utilities (e2fsprogs) contain all of the standard utilities for creating, \
fixing, configuring , and debugging ext2 filesystems."
HOMEPAGE = "http://e2fsprogs.sourceforge.net/"

LICENSE = "GPL-2.0-only & LGPL-2.0-only & BSD-3-Clause & MIT"
LICENSE:e2fsprogs-dumpe2fs = "GPL-2.0-only"
LICENSE:e2fsprogs-e2fsck = "GPL-2.0-only"
LICENSE:e2fsprogs-mke2fs = "GPL-2.0-only"
LICENSE:e2fsprogs-tune2fs = "GPL-2.0-only"
LICENSE:e2fsprogs-badblocks = "GPL-2.0-only"
LIC_FILES_CHKSUM = "file://NOTICE;md5=d50be0580c0b0a7fbc7a4830bbe6c12b \
                      file://lib/ext2fs/ext2fs.h;beginline=1;endline=9;md5=596a8dedcb4e731c6b21c7a46fba6bef \
                      file://lib/e2p/e2p.h;beginline=1;endline=7;md5=8a74ade8f9d65095d70ef2d4bf48e36a \
                      file://lib/uuid/uuid.h.in;beginline=1;endline=32;md5=dbb8079e114a5f841934b99e59c8820a \
                      file://lib/uuid/COPYING;md5=58dcd8452651fc8b07d1f65ce07ca8af \
                      file://lib/et/et_name.c;beginline=1;endline=11;md5=ead236447dac7b980dbc5b4804d8c836 \
                      file://lib/ss/ss.h;beginline=1;endline=20;md5=6e89ad47da6e75fecd2b5e0e81e1d4a6"
SECTION = "base"
DEPENDS = "util-linux attr autoconf-archive-native"

SRC_URI = "git://git.kernel.org/pub/scm/fs/ext2/e2fsprogs.git;branch=master;protocol=https"

inherit autotools gettext texinfo pkgconfig multilib_header update-alternatives ptest

BBCLASSEXTEND = "native nativesdk"
