#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import logging
from timeit import default_timer
from postgres_ddl.Config import Config

def CheckPath(path):
    """
        Create folder structure if not exists
        @param path: Path to folder
    """
    result = []
    for p in path.split("/"):
        result.append(p)
        p = "/".join(result)

        if not os.path.exists(p):
            os.mkdir(p)

def ReadConfig(path):
    assert os.path.exists(path), \
        "Config file {0} is not exists".format(path)

    with open(path, "r", encoding="utf8") as rf:
        data = json.loads(rf.read())

        assert data is not None, \
            "Config file is empty"

        assert isinstance(data, dict), \
            "Config file must contains dict"

        assert len(data or {}) > 0, \
            "Config file is empty"

        return data

def ParseACL(acl, owner):
    result = []
    roles  = []

    for acl in (acl or []):
        spl = acl.split("=")
        if len(spl) != 2:
            continue

        role_name = spl[0].strip()
        if role_name == "":
            role_name = "public"

        permissions = []

        grants = spl[1].replace("/%s" % (owner), "").strip()
        if grants.strip() == "":
            permissions.append("ALL")
        elif grants == "U":
            permissions.append("USAGE")
        elif grants == "UC":
            permissions.append("ALL")
        elif grants == "arwdDxt":
            permissions.append("ALL")
        elif grants == "arwdDxtm":
            permissions.append("ALL")
        elif grants == "rwU":
            permissions.append("ALL")
        elif grants == "X":
            permissions.append("EXECUTE")
        else:
            if grants.find("r") >= 0:
                permissions.append("SELECT")
            if grants.find("a") >= 0:
                permissions.append("INSERT")
            if grants.find("w") >= 0:
                permissions.append("UPDATE")
            if grants.find("d") >= 0:
                permissions.append("DELETE")
            if grants.find("D") >= 0:
                permissions.append("TRUNCATE")
            if grants.find("x") >= 0:
                permissions.append("REFERENCES")
            if grants.find("t") >= 0:
                permissions.append("TRIGGER")
            if grants.find("m") >= 0:
                permissions.append("MAINTAIN")

        result.append({
            "is_grant" : True,
            "perm"     : permissions,
            "role"     : role_name
        })

        roles.append(role_name)

    if "public" not in roles:
        result.append({
            "is_grant" : False,
            "perm"     : ["ALL"],
            "role"     : "public"
        })

    if owner not in roles:
        result.append({
            "is_grant" : True,
            "perm"     : ["ALL"],
            "role"     : owner
        })

    result.sort(key=lambda x: (x.get('is_grant') is False, x.get('role')))

    return result

def ParseOptions(opt, exclude_extra=[]):
    exclude_names = [""] + exclude_extra

    eq_idx = opt.find("=")
    if eq_idx < 0 or eq_idx+1 == len(opt):
        return None

    name = (opt[:eq_idx] or "").strip()
    if name.lower() in exclude_names:
        return None

    value = (opt[eq_idx+1:] or "").strip()
    if len(value) <= 0:
        return None

    return f"{name} '{value}'"

def CalcDuration(fnc):
    def wrapper(*args):
        time_start = default_timer()
        result = fnc(*args)
        logging.info("{0} duration = {1} sec".format(fnc.__name__, round(default_timer() - time_start, 2)))
        return result
    return wrapper

def SetupLogging(config):
    logging.basicConfig(
        level=logging.getLevelName(config.get("log_level") or "INFO"),
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(),
            #handlers.TimedRotatingFileHandler("log.log", backupCount=7, when='D', interval=1)
        ]
    )

def FileDataProcess(data=""):
    """
    File content processing
    @param data: File content
    """
    data = (data or "")
    data = data.replace(chr(10)+chr(13), Config.NL)
    data = data.replace(chr(13)+chr(10), Config.NL)
    data = data.replace(chr(13), Config.NL)
    data = data.replace(chr(10), Config.NL)
    return data.strip()
