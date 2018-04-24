# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import subprocess
from django.http import JsonResponse

def run_script(request):
    subprocess.call(["python", "../detect_text.py"])
    return JsonResponse({"OK": True})
