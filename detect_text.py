import cv2
import os
import tensorflow as tf
from server.dvalib import detector
import repos.crnn.utils as utils
import repos.crnn.dataset as dataset
import torch
from torch.autograd import Variable
from PIL import Image
import repos.crnn.models.crnn as crnn
from glob import glob
try:
    os.mkdir('../boxes')
except:
    pass
text_detector = detector.TextBoxDetector(model_path='../repos/tf_ctpn_cpu/checkpoints/checkpoint')
text_detector.load()
box_count = 0
model_path = '../crnn.pth'
alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
model = crnn.CRNN(32, 1, 37, 256, 1)
print('loading pretrained model from %s' % model_path)
model.load_state_dict(torch.load(model_path))
converter = utils.strLabelConverter(alphabet)
transformer = dataset.resizeNormalize((100, 32))
recognized_text = []
for im_name in glob("../images/*.jpg"):
    regions = text_detector.detect(im_name)
    im=cv2.imread(im_name)
    for k in regions:
        if k['score'] > 0.95:
            crop_img = im[int(k['y']):int(k['y'] + k['h']),int(k['x']):int(k['x'] + k['w'])]
            cv2.rectangle(im, (int(k['x']), int(k['y'])), (int(k['x'] + k['w']), int(k['y'] + k['h'])), (255, 0, 0), 2)
            print(k['score'])
            cv2.imwrite('../boxes/box.jpg', crop_img)
            box_count += 1
            image = Image.open('../boxes/box.jpg').convert('L')
            image = transformer(image)
            image = image.view(1, *image.size())
            image = Variable(image)
            model.eval()
            preds = model(image)
            _, preds = preds.max(2)
            preds = preds.transpose(1, 0).contiguous().view(-1)
            preds_size = Variable(torch.IntTensor([preds.size(0)]))
            sim_pred = converter.decode(preds.data, preds_size.data, raw=False)
            print(sim_pred)
            os.remove('../boxes/box.jpg')
