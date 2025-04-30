#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Config import Config

class DDL(object):
    def __init__(self, parent, data):
        self.Parent = (parent or "").strip()

        assert data is not None, \
            "{0} data is null".format(type(self))

        assert isinstance(data, dict), \
            "{0} data type is not dict".format(type(self))

        assert len(data.keys()) > 0, \
            "{0} data is empty".format(type(self))

    def __str__(self):
        raise NotImplementedError("__str__ method is not implemented for class {0}".format(type(self)))

    def DDL_Create(self):
        raise NotImplementedError("DDL_Create method is not implemented for class {0}".format(type(self)))

    def DDL_Drop(self):
        raise NotImplementedError("DDL_Drop method is not implemented for class {0}".format(type(self)))

    def GetObjectType(self):
        raise NotImplementedError("GetObjectType method is not implemented for class {0}".format(type(self)))

    def GetObjectTypeComment(self):
        raise NotImplementedError("GetObjectTypeComment method is not implemented for class {0}".format(type(self)))

    def GetObjectName(self):
        raise NotImplementedError("GetObjectName method is not implemented for class {0}".format(type(self)))

    def GetObjectTypeFile(self, path):
        return "/".join([path, "{0}.sql".format(self.GetObjectType())])

    def GetFullName(self):
        raise NotImplementedError("GetFullName method is not implemented for class {0}".format(type(self)))

    def GetTag(self):
        raise NotImplementedError("GetTag method is not implemented for class {0}".format(type(self)))

    def Export(self):
        raise NotImplementedError("Export method is not implemented for class {0}".format(type(self)))

    def GetPath(self):
        return []

    def GetFileName(self):
        return None

    def GetChildObjects(self):
        return {}

    def Diff(self, another):
        return []

    def FillFunctionParams(self, params=[], is_inline=False, sign=Config.FunctionParamSign):
        result = []

        sep = Config.NL
        indent = Config.Indent
        if is_inline is True:
            sep = " "
            indent = ""

        for (name, value, is_quote) in (params or []):
            if is_quote is True:
                value = f"'{value}'"
            result.append(f"{indent}{name} {sign} {value}")

        return f",{sep}".join(sorted(result))
