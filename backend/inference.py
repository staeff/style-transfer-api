import config
import cv2


def inference(model, image):
    """
    * perform image resizing, and converted it into the blob format required. Then we passed the pre-processed image into the network/model and obtained the output. The post-processed image and resized image are returned as output.
    """

    model_name = f"{config.MODEL_PATH}{model}.t7"
    # load the Torch model
    model = cv2.dnn.readNetFromTorch(model_name)

    # resize the input image
    height, width = int(image.shape[0]), int(image.shape[1])
    new_width = int((640 / height) * width)
    resized_image = cv2.resize(image, (new_width, 640), interpolation=cv2.INTER_AREA)

    # Create a blob from the pre-processed image
    inp_blob = cv2.dnn.blobFromImage(
        resized_image,
        1.0,
        (new_width, 640),
        (103.93, 116.77, 123.68),
        swapRB=False,
        crop=False,
    )

    # Perform a forward pass run of the network
    model.setInput(inp_blob)
    output = model.forward()

    # Reshape the output Tensor
    output = output.reshape(3, output.shape[2], output.shape[3])

    # Add back the mean substruction
    # the Mean values for the ImageNet training set are R=103.93, G=116.77, B=123.68
    output[0] += 103.93
    output[1] += 116.77
    output[2] += 123.68

    # re-order the channels
    output = output.transpose(1, 2, 0)
    return output, resized_image
