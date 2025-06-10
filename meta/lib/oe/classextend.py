#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: GPL-2.0-only
#

import collections
import bb.filter

@bb.filter.filter_proc()
def native_filter(val, pn, bpn, regex=False, selfref=True):
    deps = val
    if not deps:
        return
    deps = bb.utils.explode_deps(deps)
    newdeps = []
    for dep in deps:
        if regex and dep.startswith("^") and dep.endswith("$"):
            if not dep.endswith("-native$"):
                newdeps.append(dep[:-1].replace(pn, bpn) + "-native$")
            else:
                newdeps.append(dep)
        elif dep == pn:
            if not selfref:
                continue
            newdeps.append(dep)
        elif "-cross-" in dep:
            newdeps.append(dep.replace("-cross", "-native"))
        elif not dep.endswith("-native"):
            # Replace ${PN} with ${BPN} in the dependency to make sure
            # dependencies on, e.g., ${PN}-foo become ${BPN}-foo-native
            # rather than ${BPN}-native-foo-native.
            newdeps.append(dep.replace(pn, bpn) + "-native")
        else:
            newdeps.append(dep)
    return " ".join(newdeps)

def add_suffix(val, extname, prefixes):
    if val.startswith(extname + "-"):
        return val
    if val.endswith(("-native", "-native-runtime")) or ('nativesdk-' in val) or ('-cross-' in val) or ('-crosssdk-' in val):
        return val
    # If it starts with a known prefix (e.g. multilibs), just pass it through
    for prefix in prefixes:
        if val.startswith(prefix + "-"):
            return val
    if val.startswith("kernel-") or val == "virtual/kernel":
        return val
    if val.startswith("rtld"):
        return val
    if val.endswith("-crosssdk"):
        return val
    if val.endswith("-" + extname):
        val = val.replace("-" + extname, "")
    if val.startswith("virtual/"):
        # Assume large numbers of dashes means a triplet is present and we don't need to convert
        if val.count("-") >= 3 and val.endswith(("-go",)):
            return val
        subs = val.split("/", 1)[1]
        if not subs.startswith(extname):
            return "virtual/" + extname + "-" + subs
        return val
    if val.startswith("/") or (val.startswith("${") and val.endswith("}")):
        return val
    if not val.startswith(extname):
        return extname + "-" + val
    return val

def get_package_mappings(packages, extname):
    pkgs_mapping = []
    for pkg in packages.split():
        if pkg.startswith(extname):
           pkgs_mapping.append([pkg.split(extname + "-")[1], pkg])
           continue
        pkgs_mapping.append([pkg, add_suffix(pkg, extname, [])])
    return pkgs_mapping

@bb.filter.filter_proc()
def package_suffix_filter(val, extname):
    pkgs_mapping = get_package_mappings(val, extname)
    return " ".join([row[1] for row in pkgs_mapping])

@bb.filter.filter_proc()
def suffix_filter(val, extname, prefixes):
    deps = bb.utils.explode_dep_versions2(val)
    newdeps = collections.OrderedDict()
    for dep in deps:
        newdeps[add_suffix(dep, extname, prefixes)] = deps[dep]
    return bb.utils.join_deps(newdeps, False)

class ClassExtender(object):
    def __init__(self, extname, prefixes, d):
        self.extname = extname
        self.d = d
        self.pkgs_mapping = []
        self.prefixes = prefixes

    def map_variable(self, varname, setvar = True):
        var = self.d.getVar(varname)
        if not var:
            return ""
        var = var.split()
        newvar = []
        for v in var:
            newvar.append(add_suffix(v, self.extname, self.prefixes))
        newdata =  " ".join(newvar)
        if setvar:
            self.d.setVar(varname, newdata)
        return newdata

    def map_regexp_variable(self, varname, setvar = True):
        var = self.d.getVar(varname)
        if not var:
            return ""
        var = var.split()
        newvar = []
        for v in var:
            if v.startswith("^" + self.extname):
                newvar.append(v)
            elif v.startswith("^"):
                newvar.append("^" + self.extname + "-" + v[1:])
            else:
                newvar.append(add_suffix(v, self.extname))
        newdata =  " ".join(newvar)
        if setvar:
            self.d.setVar(varname, newdata)
        return newdata

    def set_filter(self, var):
        if self.d.getVar(var, False):
            self.d.setVarFlag(var, "filter", "oe.classextend.suffix_filter(val, '" + self.extname + "', " + str(self.prefixes) + ")")

    def map_packagevars(self):
        for pkg in (self.d.getVar("PACKAGES").split() + [""]):
            self.set_filter("RDEPENDS:" + pkg)
            self.set_filter("RRECOMMENDS:" + pkg)
            self.set_filter("RSUGGESTS:" + pkg)
            self.set_filter("RPROVIDES:" + pkg)
            self.set_filter("RREPLACES:" + pkg)
            self.set_filter("RCONFLICTS:" + pkg)
            self.set_filter("PKG:" + pkg)

    def rename_packages(self):
        self.pkgs_mapping = get_package_mappings(self.d.getVar('PACKAGES'), self.extname)
        self.d.setVarFlag('PACKAGES', "filter", "oe.classextend.package_suffix_filter(val, '" + self.extname + "')")

    def rename_package_variables(self, variables):
        for pkg_mapping in self.pkgs_mapping:
            if pkg_mapping[0].startswith("${") and pkg_mapping[0].endswith("}"):
                continue
            for subs in variables:
                self.d.renameVar("%s:%s" % (subs, pkg_mapping[0]), "%s:%s" % (subs, pkg_mapping[1]))
