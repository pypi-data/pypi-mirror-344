#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
from shutil import rmtree
from multiprocessing import Pool

from postgres_ddl.Config import Config
from postgres_ddl.Database import Database
from postgres_ddl.System import SetupLogging, FileDataProcess

class Grabber():
    def __init__(self, config):
        self.Connect = config.get("connect") or {}

        self.Path = (config.get("path") or "").strip()
        assert len(self.Path) > 0, \
            "Grabber path is null"

        self.ExcludeSchemas = config.get("exclude_schemas") or []
        self.Threads = config.get("threads") or 8

        SetupLogging(config)

        Config.Parse(config)

    def NonSuperUserUndo(self):
        """
        Undo changes for superuser-only files
        """
        os.chdir(self.Path)
        res = subprocess.run(["git", "status", "--short"], shell=True, capture_output=True)
        res = res.stdout.decode("utf-8")
        res = FileDataProcess(res)
        for file in res.split(Config.NL):
            file = file[3:]
            if file.find("_logical") >= 0:
                subprocess.run(["git", "checkout", "-q", "--", file], shell=True)

    def WriteFile(self, file):
        with open(file.get("path"), "w", encoding="utf-8") as wf:
            wf.write(FileDataProcess(file.get("data")) + Config.NL)

    def Run(self):
        database = Database(connect=self.Connect, exclude_schemas=self.ExcludeSchemas)
        database.Parse()

        if os.path.exists(self.Path):
            rmtree(self.Path)

        write_data = []
        for k,o in database.Objects.items():
            path = o.GetPath()
            if len(path) <= 0:
                continue

            file_name = o.GetFileName()
            if len(file_name) <= 0:
                continue
            file_name = file_name.replace("\\", "_")
            file_name = file_name.replace("/", "_")
            file_name = file_name.replace('"', "")

            path = [self.Path] + path
            path = "/".join(path)

            if not os.path.exists(path):
                os.makedirs(path)

            write_data.append({
                "path" : "/".join([path, file_name]),
                "data" : o.DDL_Create()
            })

        if (self.Threads or 1) <= 1:
            for file in write_data:
                self.WriteFile(file)
        else:
            with Pool(self.Threads) as pool:
                pool.map(self.WriteFile, write_data)

        if not database.IsSuperUser:
            self.NonSuperUserUndo()
