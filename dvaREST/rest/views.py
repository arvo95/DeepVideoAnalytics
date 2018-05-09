# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import zipfile


@csrf_exempt
def run_script(request):
    with open("images.zip", "wb") as f:
        for chunk in request.FILES["file"].chunks():
            f.write(chunk)
        f.close()
    file = zipfile.ZipFile("images.zip", "r")
    file.extractall("../images")
    file.close()
    subprocess.call(["python", "../detect_text.py"])
    return JsonResponse({"OK": True})
