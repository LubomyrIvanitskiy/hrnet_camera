import threading
import binascii
from time import sleep
from image_utils import base64_to_pil_image, pil_image_to_base64


class Camera(object):
    def __init__(self, image_processor):
        self.to_process = []
        self.to_output = []
        self.image_processor = image_processor

        thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()

    def process_one(self):
        if not self.to_process:
            return

        # input is an ascii string. 
        message = self.to_process.pop(0)
        parts = message.split(",")
        input_str = parts[1]
        # convert it to a pil image
        input_img = base64_to_pil_image(input_str)

        ################## where the hard work is done ############
        # output_img is an PIL image
        output_img = self.image_processor.process(input_img)

        # output_str is a base64 string in ascii
        output_str = pil_image_to_base64(output_img)

        # convert eh base64 string in ascii to base64 string in _bytes_
        # self.to_output.append(binascii.a2b_base64(output_str))
        parts[1] = output_str.decode("utf-8")
        output = ",".join(parts)
        self.to_output.append(output)

    def keep_processing(self):
        while True:
            self.process_one()
            sleep(0.1)

    def enqueue_input(self, message):
        if not self.to_process:
            self.to_process.append(message)

    def get_frame(self):
        while not self.to_output:
            sleep(0.1)
        return self.to_output.pop(0)
