This is a truncated fork of DeepVideoAnalitics.
It has almost all deployment configuration removed.
Examples are also removed.
DVA server has only dvalib left and there are only crnn, facenet, yolo and tf_ctpn repos left.

Things added:
- Gunicorn server
- Requirements.txt (Had to install several dependencies manually)
- detect_text.py - that combines the text detection and recognition notepads from OCR examples
- Django app, that launches detect_text.py when called

To launch OCR:
Just launch the docker container and send an HTTP GET to hostname/script/

Issues:
- If there is an issue with bbox, then run python repos/tf_ctpn_cpu/lib/utils/setup.py
