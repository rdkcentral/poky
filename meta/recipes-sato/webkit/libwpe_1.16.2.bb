SUMMARY = "General-purpose library specifically developed for the WPE-flavored port of WebKit."
HOMEPAGE = "https://github.com/WebPlatformForEmbedded/libwpe"
BUGTRACKER = "https://github.com/WebPlatformForEmbedded/libwpe/issues"

LICENSE = "BSD-2-Clause"
LIC_FILES_CHKSUM = "file://COPYING;md5=371a616eb4903c6cb79e9893a5f615cc"
DEPENDS = "virtual/egl libxkbcommon"

inherit cmake features_check pkgconfig

REQUIRED_DISTRO_FEATURES = "opengl"

SRC_URI = "https://wpewebkit.org/releases/${BPN}-${PV}.tar.xz \
           file://0001-cmake-Bump-required-CMake-version-to-3.5-to-allow-bu.patch \
           "
SRC_URI[sha256sum] = "960bdd11c3f2cf5bd91569603ed6d2aa42fd4000ed7cac930a804eac367888d7"

# This is a tweak of upstream-version-is-even needed because
# upstream directory contains tarballs for other components as well.
UPSTREAM_CHECK_REGEX = "libwpe-(?P<pver>\d+\.(\d*[02468])+(\.\d+)+)\.tar"
