#!/usr/bin/env python
#-*- coding: utf-8 -*-

class ParseResult:

    @classmethod
    def parse(cls, result):
        func_name = getattr(result._attributes.action['name'])
        print("****** func_name  ***")

        if func_name == None:
            return None
        output = func_name(result)
        return output

    def copy(self, result):
        return {
            "Name": result._result.invocation['module_args']['_original_basename'],
            "Path": result._result.invocation['module_args']['path'],
            "Change": result._result.invocation['changed']
        }