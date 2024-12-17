#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

inherit ptest

FILESEXTRAPATHS:prepend := "${COREBASE}/meta/files:"

SRC_URI += "file://ptest-python-pytest/run-ptest"

# Overridable configuration for the directory within the source tree
# containing the pytest files
PTEST_PYTEST_DIR ?= "/tests"

do_install_ptest_python_pytest() {
	if [ ! -f ${D}${PTEST_PATH}/run-ptest ]; then
		install -m 0755 ${UNPACKDIR}/ptest-python-pytest/run-ptest ${D}${PTEST_PATH}
	fi
    if [ -d "${S}/${PTEST_PYTEST_DIR}" ]; then
        install -d ${D}${PTEST_PATH}/${PTEST_PYTEST_DIR}
        cp -rf ${S}/${PTEST_PYTEST_DIR}/* ${D}${PTEST_PATH}/${PTEST_PYTEST_DIR}/
    fi
}

FILES:${PN}-ptest:prepend = "${PTEST_PATH}/tests/* ${PTEST_PATH}/run-ptest "

RDEPENDS:${PN}-ptest:prepend = "python3-pytest python3-unittest-automake-output"

addtask install_ptest_python_pytest after do_install_ptest_base before do_package

python () {
    if not bb.data.inherits_class('native', d) and not bb.data.inherits_class('cross', d):
        d.setVarFlag('do_install_ptest_python_pytest', 'fakeroot', '1')
        d.setVarFlag('do_install_ptest_python_pytest', 'umask', '022')

    # Remove all '*ptest_python_pytest' tasks when ptest is not enabled
    if not(d.getVar('PTEST_ENABLED') == "1"):
        for i in ['do_install_ptest_python_pytest']:
            bb.build.deltask(i, d)
}
