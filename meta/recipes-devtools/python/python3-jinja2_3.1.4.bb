SUMMARY = "Python Jinja2: A small but fast and easy to use stand-alone template engine written in pure python."
HOMEPAGE = "https://pypi.org/project/Jinja2/"

LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=5dc88300786f1c214c1e9827a5229462"

SRC_URI[sha256sum] = "4a3aee7acbbe7303aede8e9648d13b8bf88a429282aa6122a993f0ac800cb369"

PYPI_PACKAGE = "jinja2"

CVE_PRODUCT = "jinja2 jinja"

CLEANBROKEN = "1"

inherit pypi python_flit_core ptest-python-pytest

SRC_URI += " \
	file://fix-3.13.patch \
"

RDEPENDS:${PN}-ptest += " \
    python3-unixadmin \
"

RDEPENDS:${PN} += " \
    python3-asyncio \
    python3-crypt \
    python3-io \
    python3-json \
    python3-markupsafe \
    python3-math \
    python3-netclient \
    python3-numbers\
    python3-pickle \
    python3-pprint \
    python3-shell \
    python3-threading \
"

BBCLASSEXTEND = "native nativesdk"
