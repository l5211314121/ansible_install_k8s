#!/usr/bin/env python
#-*- coding: utf-8 -*-
import json

class ParseResult:

    @classmethod
    def parse(cls, result):
        func_name = getattr(cls, result._task_fields["action"],None)
        # print("Module Name: ", func_name.__name__ if func_name !=None else None)

        if func_name == None:
            return result.__dict__
        output = func_name(ParseResult, result)
        return output

    def copy(self, result):
        return json.dumps({
            "Action": result._task_fields["action"],
            "Src": result._task_fields['args']['src'],
            "Dest": result._task_fields['args']['dest'],
        }, indent=4)

    def git(self, result):
        return json.dumps({
            "Action": result._task_fields["action"],
            "Repo": result._task_fields["args"]["repo"],
            "Dest": result._task_fields["args"]["dest"],
        }, indent=4)

    def command(self, result):
        return json.dumps({
            "Action": result._task_fields["action"],
            # "Chdir": result._task_fields["args"]["chdir"],
            "Command": result._task_fields["args"]["_raw_params"]
        }, indent=4)

    def unarchive(self, result):
        return json.dumps({
            "Action": result._task_fields["action"],
            "Src": result._task_fields["args"]["src"],
            "Dest": result._task_fields["args"]["dest"]
        }, indent=4)

    def file(self, result):
        res = []
        mult_result = result._result.get("results")
        if mult_result:
            for i in result._result["results"]:
                res.append({
                    "Mode": i["mode"],
                    "State": i["state"],
                    "Path": i["path"]
                })
        else:
            res = {
                    "Change": result._result["changed"],
                    "State": result._result["state"],
                    "Path": result._result["path"]
                }
        return json.dumps(res, indent=4)
    def debug(self, result):
        return json.dumps(result._task_fields["args"], indent=4)

    def yum(self, result):
        return json.dumps(result._task_fields["args"], indent=4)

    def template(self, result):
        return json.dumps(result._task_fields["args"])

    def systemd(self, result):
        return json.dumps({
            "Action": "Systemd",
            "Name": result._task_fields["args"]["name"],
            "State": result._task_fields["args"]["state"]
        })