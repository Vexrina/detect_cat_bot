import torch 
import cv2
import numpy as np
from pathlib import Path
import io

confThreshold = 0.4


def outlineCatsOnImage(content:bytes, weights_path: str, whose_model: str = 'ours'):
    img = np.asarray(bytearray(content), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    # img = io.BytesIO(content)


    model = torch.hub.load('ultralytics/yolov5', 'custom', str(weights_path))
    model.conf = 0.1
    model.iou = 0.15
    # model = torch.hub.load('ultralytics/yolov5', 'yolov5s')


    results = model(img)

    outputs =  results.xyxy[0]

    findObjects(outputs, img)

    return img

#def outlineCatsOnVideo(content:bytes, weights_path: str, out_path: str = 'ours'):
def outlineCatsOnVideo(input_path: str, weights_path: str, out_path: str = 'ours'):
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    
    writer = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    if not cap.isOpened():
        raise Exception("Can't open video")

    model = torch.hub.load('ultralytics/yolov5', 'custom', str(weights_path))
    model.conf = 0.1
    model.iou = 0.15
    # model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    while cap.isOpened(): 
        ret, frame = cap.read()
        
        if not ret:
            break

        results = model(frame)
        outputs =  results.xyxy[0]
        findObjects(outputs, frame)
        writer.write(frame)

    cap.release()
    writer.release()
    cv2.destroyAllWindows()

def outlineCatsOnVid(video_url: str, weights_path: str):
    cap = cv2.VideoCapture(video_url)
    if not cap.isOpened():
        raise Exception("Can't open video")
    
# функция, для нахождения котиков UwU :з
def findObjects(outputs, img):
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []

    for det in outputs:

        # scores = det[4]
        classId = det[-1]
        confidence = det[-2]
        if confidence > confThreshold:
            xmin, ymin = int(det[0]), int(det[1])
            xmax, ymax = int(det[2]), int(det[3])
            bbox.append([(xmin, ymin), (xmax, ymax)])
            classIds.append(classId)
            confs.append(float(confidence))
    for ind, box in enumerate(bbox):
        # if classNames[classIds[i]] == "cat":
        start_point = box[0]
        end_point = box[1]
        cv2.rectangle(
            img, start_point, end_point, (15, 255, 15), 4
        )
        cv2.putText(    
            img,
            f"Cat {int(confs[ind]*100)}%",
            # (int(x), int(y - 10)),
            (start_point[0], start_point[1]+10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 0, 255),
            2
        )


if __name__ == '__main__':
    pwd = Path.cwd()

    # пуь к текущей рабочей директоии
    pwd = Path.cwd()
    # путь  кизображению
    img_path = str(pwd / 'cat3.jpg')
    # путь сохранения
    save_path = str(pwd / 'detected.jpg')
    # читаем изображение
    img = cv2.imread(img_path)
    # орог уверенности нейронки


    """ две модели нейронок
        верхняя - наша
        нижняя - оригинальная """

    model = torch.hub.load('ultralytics/yolov5', 'custom', str(pwd / 'best.pt'))
    # model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

    results = model(img)

    results.print()

    outputs =  results.xyxy[0]

    findObjects(outputs, img)

    cv2.imwrite(save_path, img)
