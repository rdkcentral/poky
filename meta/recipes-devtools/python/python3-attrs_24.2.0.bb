SUMMARY = "Classes Without Boilerplate"
HOMEPAGE = "http://www.attrs.org/"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=5e55731824cf9205cfabeab9a0600887"

SRC_URI[sha256sum] = "5cfb1b9148b5b086569baec03f20d7b6bf3bcacc9a42bebf87ffaaca362f6346"

inherit pypi ptest-python-pytest python_hatchling

DEPENDS += " \
    python3-hatch-vcs-native \
    python3-hatch-fancy-pypi-readme-native \
"

RDEPENDS:${PN}+= " \
    python3-compression \
    python3-crypt \
"

RDEPENDS:${PN}-ptest += " \
    python3-hypothesis \
"

do_install_ptest:append() {
    install ${S}/conftest.py ${D}${PTEST_PATH}/
}

BBCLASSEXTEND = "native nativesdk"
