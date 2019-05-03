import argparse
import logging
import time

import cv2
import numpy as np

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

logger = logging.getLogger('TfPoseEstimator-Video')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

fps_time = 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation Video')
    parser.add_argument('-video', type=str, default='', required=True)
    parser.add_argument('-resolution', type=str, default='0x0', help='network input resolution. default=224x224', required=False)
    parser.add_argument('-model', type=str, default='cmu', help='cmu / mobilenet_thin', required=False)
    parser.add_argument('-show-process', type=bool, default=False,
                        help='for debug purpose, if enabled, speed for inference is dropped.')
    parser.add_argument('-showBG', type=bool, default=False, help='False to show skeleton only.', required=False)

    try:
        args = argp.parse_args()
    except:
        argp.print_help(sys.stderr)
        exit(1)

    logger.debug('initialization %s : %s' % (args.model[0], get_graph_path(args.model[0])))
    w, h = model_wh(args.resolution)
    if w > 0 and h > 0:
        e = TfPoseEstimator(get_graph_path(args.model[0]), target_size=(w, h))
    else:
        e = TfPoseEstimator(get_graph_path(args.model[0]), target_size=(224, 224))
    cap = cv2.VideoCapture(args.video[0])

    if cap.isOpened() is False:
        print("Error opening video stream or file")
    
    print(args.path)
    i = 0
    while cap.isOpened():
        ret_val, image = cap.read()

        if ret_val == False:
            break
        
        i+=1

        humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=4.0)
        if not args.showBG[0]:
            image = np.zeros(image.shape)

        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

        last = args.video[0].rfind('/')

        cv2.imwrite(args.video[0][:last] + '/pose_' + str(i).zfill(5) + '.jpg', image)

    cv2.destroyAllWindows()
logger.debug('finished+')
