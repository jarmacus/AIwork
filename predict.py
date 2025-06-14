def predictting(image_file):
    import os
    import hydra
    import torch
    from ultralytics.yolo.engine.predictor import BasePredictor
    from ultralytics.yolo.utils import DEFAULT_CONFIG, ROOT, ops
    from ultralytics.yolo.utils.checks import check_imgsz
    from ultralytics.yolo.utils.plotting import Annotator, colors, save_one_box
    import easyocr
    import cv2
    import time
    print("predict_input_dir",image_file)
    reader = easyocr.Reader(['en'], gpu=True)

    def ocr_image(img, coordinates):
        x, y, w, h = int(coordinates[0]), int(coordinates[1]), int(coordinates[2]), int(coordinates[3])
        img = img[y:h, x:w]

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        result = reader.readtext(gray)
        text = ""

        for res in result:
            if len(result) == 1:
                text = res[1]
            if len(result) > 1 and len(res[1]) > 6 and res[2] > 0.2:
                text = res[1]

        return str(text)

    class DetectionPredictor(BasePredictor):
        def get_annotator(self, img):
            return Annotator(img, line_width=self.args.line_thickness, example=str(self.model.names))

        def preprocess(self, img):
            img = torch.from_numpy(img).to(self.model.device)
            img = img.half() if self.model.fp16 else img.float()  # uint8 to fp16/32
            img /= 255  # 0 - 255 to 0.0 - 1.0
            return img

        def postprocess(self, preds, img, orig_img):
            preds = ops.non_max_suppression(preds,
                                            self.args.conf,
                                            self.args.iou,
                                            agnostic=self.args.agnostic_nms,
                                            max_det=self.args.max_det)

            for i, pred in enumerate(preds):
                shape = orig_img[i].shape if self.webcam else orig_img.shape
                pred[:, :4] = ops.scale_boxes(img.shape[2:], pred[:, :4], shape).round()

            return preds

        def write_results(self, idx, preds, batch):
            p, im, im0 = batch
            log_string = ""
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim
            self.seen += 1
            im0 = im0.copy()

            frame = getattr(self.dataset, 'frame', 0)
            self.data_path = p
            self.txt_path = str(self.save_dir / 'labels' / p.stem) + ('' if self.dataset.mode == 'image' else f'_{frame}')
            log_string += '%gx%g ' % im.shape[2:]  # print string
            self.annotator = self.get_annotator(im0)

            det = preds[idx]
            self.all_outputs.append(det)
            if len(det) == 0:
                return log_string
            for c in det[:, 5].unique():
                n = (det[:, 5] == c).sum()  # detections per class
                log_string += f"{n} {self.model.names[int(c)]}{'s' * (n > 1)}, "

            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            for *xyxy, conf, cls in reversed(det):
                if self.args.save_txt:  # Write to file
                    xywh = (ops.xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                    line = (cls, *xywh, conf) if self.args.save_conf else (cls, *xywh)  # label format
                    with open(f'{self.txt_path}.txt', 'a') as f:
                        f.write(('%g ' * len(line)).rstrip() % line + '\n')

                if self.args.save or self.args.save_crop or self.args.show:  # Add bbox to image
                    c = int(cls)  # integer class
                    label = None if self.args.hide_labels else (
                        self.model.names[c] if self.args.hide_conf else f'{self.model.names[c]} {conf:.2f}')

                    text_ocr = ocr_image(im0, xyxy)  # 获取车牌号
                    label = text_ocr  # 将车牌号作为标签
                    print(label)
                    if text_ocr is None:
                        print("text_ocr is None")
                    print("text_ocr",text_ocr)
                    with open("C:\\Users\\86178\\Desktop\\Personal_Moments-master\\record\\text_ocr_save.txt", "w") as file:
                        # 写入文本内容
                        file.write(text_ocr)
                    # 识别相同车牌并分类保存

                    if label and len(label) > 0:
                        # 定义车牌号文件夹路径
                        plate_folder = self.save_dir / 'plates' / label
                        # 创建文件夹，如果不存在的话
                        os.makedirs(plate_folder, exist_ok=True)

                        # 确保文件名不重复，添加时间戳
                        timestamp = int(time.time())  # 获取时间戳
                        save_path = plate_folder / f'{label}_{timestamp}.jpg'
                        cv2.imwrite(str(save_path), im0)

                    self.annotator.box_label(xyxy, label, color=colors(c, True))
                if self.args.save_crop:
                    imc = im0.copy()
                    save_one_box(xyxy,
                                 imc,
                                 file=self.save_dir / 'crops' / self.model.model.names[c] / f'{self.data_path.stem}.jpg',
                                 BGR=True)

            return log_string

    @hydra.main(version_base=None, config_path=str(DEFAULT_CONFIG.parent), config_name=DEFAULT_CONFIG.name)
    def predict(cfg):
        cfg.model = cfg.model or "yolov8n.pt"
        cfg.imgsz = check_imgsz(cfg.imgsz, min_dim=2)  # check image size
        # cfg.source = "C:/Users/86178/Desktop/s"  # 修改为你的实际文件路径
        with open("C:\\Users\\86178\\Desktop\\Personal_Moments-master\\record\\text_ocr.txt", "r") as file:
            input_dir = file.read()
        cfg.source = f"{input_dir}"# 使用外部传递的 input_dir 参数
        print("cfg.source", cfg.source)
        # cfg.source = "C:/Users/86178/Desktop/s"
        predictor = DetectionPredictor(cfg)
        predictor()

    with open("C:\\Users\\86178\\Desktop\\Personal_Moments-master\\record\\text_ocr.txt", "w") as file:
        # 写入文本内容
        file.write(image_file)
    predict()
    with open("C:\\Users\\86178\\Desktop\\Personal_Moments-master\\record\\text_ocr_save.txt", "r") as file:
        # 写入文本内容
        text_ocr_save = file.read()
        print("text_ocr_save",text_ocr_save)
    return text_ocr_save
