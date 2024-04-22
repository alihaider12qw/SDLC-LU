import datetime

import cv2, os, sys

from django_toosimple_q.logging import logger

from ...decorators import register_task, schedule_task
from ...models import *


@schedule_task(cron="*/1 * * * *", datetime_kwarg="scheduled_time", queue="demo")
@register_task(name="task_runner", queue="demo")
def task_runner(scheduled_time):
    if scheduled_time is None:
        return "Not scheduled"
    logger.info(f"Task began at scheduled time: {scheduled_time}")
    try:
        # TODO: Put a for loop here to perform the detection task on all Agents
        empty_image_path = "empty_parking_lot.png"
        current_image_path = "new_capture_parking_lot.png"

        no_of_spots_occupied = detect_vehicles(empty_image_path, current_image_path)
        if no_of_spots_occupied:
            save_to_db(1, no_of_spots_occupied)  # TODO: 1 is hardcoded for now
        else:
            logger.error("Didn't work")

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(
            "ERROR at task_runner",
            err,
            "\n",
            "TRACE: ",
            exc_type,
            fname,
            exc_tb.tb_lineno,
        )

    logger.info(
        f"Task completed in {str(datetime.now().replace(tzinfo=None) - scheduled_time.replace(tzinfo=None))}"
    )
    return f"Task Completed"


def detect_vehicles(empty_image_path, current_image_path):
    try:

        # Read the reference (empty) image and the current image
        empty_img = cv2.imread(empty_image_path)
        current_img = cv2.imread(current_image_path)

        # Convert to grayscale
        empty_gray = cv2.cvtColor(empty_img, cv2.COLOR_BGR2GRAY)
        current_gray = cv2.cvtColor(current_img, cv2.COLOR_BGR2GRAY)

        # Compute the absolute difference between the current image and the reference image
        difference = cv2.absdiff(empty_gray, current_gray)

        # Apply a threshold to the difference to isolate regions of interest
        _, thresh = cv2.threshold(difference, 50, 255, cv2.THRESH_BINARY)

        # Find contours from the thresholded image
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        vehicle_count = 0

        # Filter contours based on area and draw bounding boxes
        for contour in contours:
            if cv2.contourArea(contour) > 1000:  # Adjust area threshold as needed
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(current_img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                vehicle_count += 1

        # Uncomment the following to display the image with bounding boxes
        # cv2.imshow("Vehicles Detected", current_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return vehicle_count
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(
            "ERROR at detect_vehicles",
            err,
            "\n",
            "TRACE: ",
            exc_type,
            fname,
            exc_tb.tb_lineno,
        )


def save_to_db(parking_area_id, no_of_spots_occupied):
    try:
        obj = ParkingArea.objects.get(id=parking_area_id)
        obj.no_of_spots_occupied = no_of_spots_occupied
        obj.save()
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(
            f"ERROR at save_to_db {no_of_spots_occupied}",
            f"ERROR at save_to_db 2 {type(no_of_spots_occupied)}",
            err,
            "\n",
            "TRACE: ",
            exc_type,
            fname,
            exc_tb.tb_lineno,
        )
