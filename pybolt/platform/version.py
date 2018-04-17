from pybolt.util.filebase import FileBase
import re


class Version(FileBase):
    def verify(self, request):
        try:
            postpath = request.postpath
            re_prepath = re.match("(^m|^v)(\d+).(\d+)$", request.prepath[0])
            if (re_prepath is None) or \
                    (len(postpath) == 0) or \
                    (len(postpath) == 1 and postpath[0] == ''):
                return False
            prepath = re_prepath.groups()
            if prepath[0] == "v":
                version = self.get(re_prepath.group(), postpath[0])
                if version is None:
                    return False
            elif prepath[0] != "m":
                return False
        except:
            return False
            
        return True

    def make(self, request, method=""):
        if request.prepath[0][0] == "v":
            version = self.get(request.prepath[0], request.postpath[0])
        else:
            version = request.prepath[0]
        funcname = version.replace('m', '')
        funcname = funcname.replace('.', '_')
        return 'method_{}{}'.format(funcname, method)
