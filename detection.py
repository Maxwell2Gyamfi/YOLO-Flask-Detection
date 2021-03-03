
from decimal import Decimal
import cv2
# -*- coding: utf-8 -*-


class YoloDetection():
    def __init__(self):
        self.COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
        self.CONFIDENCE_THRESHOLD = 0.2
        self.NMS_THRESHOLD = 0.4
        self.class_names = [
            '1p', '2p', '5p', '10p', '20p', '50p', '1P', '2P']
        self.weights, self.cfg = self.loadYoloModel()
        self.net = self.readNet()
        self.model = self.setModel()

    def loadYoloModel(self):
        weights = ("yolo.weights")
        cfg = ("yolo.cfg")
        return weights, cfg

    def readNet(self):
        yolonet = cv2.dnn.readNet(self.weights, self.cfg)
        return yolonet

    def setModel(self):
        yolomodel = cv2.dnn_DetectionModel(self.net)
        yolomodel.setInputParams(size=(608, 608), scale=1/255)
        return yolomodel

    def getItems(self):
        items = {"1p": 0.01, "2p": 0.02, "5p": 0.05, "10p": 0.10,
                 "20p": 0.20, "50p": 0.50, "1P": 1.0, "2P": 2.0}
        return items

    def detectAll(self):
        items = self.getItems()
        total = 0
        frame = cv2.imread('image.png')
        classes, scores, boxes = self.model.detect(
            frame, self.CONFIDENCE_THRESHOLD, self.NMS_THRESHOLD)
        for (classid, score, box) in zip(classes, scores, boxes):
            color = self.COLORS[int(classid) % len(self.COLORS)]
            label = "%s %.2f" % (self.class_names[classid[0]], score)
            name = self.class_names[classid[0]]
            total = Decimal(total)+Decimal(items.get(name))
            cv2.rectangle(frame, box, color, 2)
            cv2.putText(frame, label, (box[0], box[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        cv2.imwrite('static/images/detection.jpg', frame)
        total = "%.2f" % total
        return str(total)

    def detectSpecific(self, classID):
        total = 0
        items = self.getItems()
        frame = cv2.imread('image.png')
        classes, scores, boxes = self.model.detect(
            frame, self.CONFIDENCE_THRESHOLD, self.NMS_THRESHOLD)
        for (classid, score, box) in zip(classes, scores, boxes):
            color = self.COLORS[int(classid) % len(self.COLORS)]
            label = "%s %.2f" % (self.class_names[classid[0]], score)
            name = self.class_names[classid[0]]
            if name == classID:
                total = Decimal(total)+Decimal(items.get(name))
                cv2.rectangle(frame, box, color, 2)
                cv2.putText(frame, label, (box[0], box[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.imwrite('static/images/detection.jpg', frame)
        total = "%.2f" % total
        return str(total)

    def detectVideo(self, frame):
        total = 0
        items = self.getItems()
        classes, scores, boxes = self.model.detect(
            frame, self.CONFIDENCE_THRESHOLD, self.NMS_THRESHOLD)
        for (classid, score, box) in zip(classes, scores, boxes):
            color = self.COLORS[int(classid) % len(self.COLORS)]
            label = "%s %.2f" % (self.class_names[classid[0]], score)
            name = self.class_names[classid[0]]

            total = Decimal(total)+Decimal(items.get(name))
            cv2.rectangle(frame, box, color, 2)
            cv2.putText(frame, label, (box[0], box[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2

        total = "%.2f" % (total)
        cv2.putText(frame, str(total), org, font,
                    fontScale, color, thickness, cv2.LINE_AA)

        return frame


# def main(data):
#     CONFIDENCE_THRESHOLD = 0.2
#     NMS_THRESHOLD = 0.4
#     COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

#     class_names = ['1p', '2p', '5p', '10p', '20p', '50p', '1P', '2P']
#     weights = join(dirname(__file__), "yolo.weights")
#     cfg = join(dirname(__file__), "yolo.cfg")

#     decoded_data = base64.b64decode(data)
#     np_data = np.fromstring(decoded_data, np.uint8)
#     frame = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)

#     net = cv2.dnn.readNet(weights, cfg)

#     files_dir = str(Python.getPlatform().getApplication().getFilesDir())

#     model = cv2.dnn_DetectionModel(net)
#     model.setInputParams(size=(608, 608), scale=1/255)

#     total = 0
#     items = {"1p": 0.01, "2p": 0.02, "5p": 0.05, "10p": 0.10,
#              "20p": 0.20, "50p": 0.50, "1P": 1.0, "2P": 2.0}

#     classes, scores, boxes = model.detect(
#         frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
#     for (classid, score, box) in zip(classes, scores, boxes):
#         color = COLORS[int(classid) % len(COLORS)]
#         label = "%s" % (class_names[classid[0]])
#         name = class_names[classid[0]]
#         total = Decimal(total)+Decimal(items.get(name))
#         cv2.rectangle(frame, box, color, 2)
#         cv2.putText(frame, label, (box[0], box[1] - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

#     print(files_dir)
#     cv2.imwrite(files_dir+'/detection.jpg', frame)

#     # array = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)

#     # pil_image = Image.fromarray(array)
#     # buff = io.BytesIO()
#     # pil_image.save(buff, format="PNG")
#     # img_str = base64.b64encode(buff.getvalue())
#     # return ""+str(img_str, 'utf-8')
#     result = "%.2f" % (total)
#     return result


# # main()


# def loadModel():


# def main2():
#     frame = cv2.imread(
#         "C:/Users/max_x/MyApplication2/app/src/main/python/h1.jpg")
#     return "haha"
