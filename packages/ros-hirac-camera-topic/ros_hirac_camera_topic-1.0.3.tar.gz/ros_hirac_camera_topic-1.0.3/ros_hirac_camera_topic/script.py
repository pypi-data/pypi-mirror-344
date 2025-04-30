import subprocess
import logging
import logging.config
import time

def get_image_topic():
    while True:
        result = subprocess.run(
            ["ros2", "topic", "list"], stdout=subprocess.PIPE, text=True
        )
        topics = result.stdout.splitlines()

        for topic_name in topics:
            if "/camera/color/image_raw" in topic_name:
                logging.info("Subscribed Topic is: ")
                logging.info(topic_name)
                return topic_name
            elif "/oak/rgb/image_raw" in topic_name:
                logging.info("Subscribed Topic is: ")
                logging.info(topic_name)
                return topic_name
            elif "/right/image_rect" in topic_name:
                logging.info("Subscribed Topic is: ")
                logging.info(topic_name)
                return topic_name
        
        logging.info("No matching topic found. Retrying in 1 second...")
        time.sleep(1)

def get_pointcloud_topic():
    while True: 
        result = subprocess.run(
            ["ros2", "topic", "list"], stdout=subprocess.PIPE, text=True
        )
        topics = result.stdout.splitlines()

        for topic_name in topics:

            if "/camera/camera/depth/color/points" in topic_name:
                logging.info("Subscribed Topic is: ")
                logging.info(topic_name)
                return topic_name
            elif "/stereo/points" in topic_name:
                logging.info("Subscribed Topic is: ")
                logging.info(topic_name)
                return topic_name
            elif "/oak/points" in topic_name:
                logging.info("Subscribed Topic is: ")
                logging.info(topic_name)
                return topic_name
            
        logging.info("No matching pointcloud topic found. Retrying in 1 second...")
        time.sleep(1)

def get_camera_info_topic():
    while True:
        result = subprocess.run(
            ["ros2", "topic", "list"], stdout=subprocess.PIPE, text=True
        )
        topics = result.stdout.splitlines()

        for topic_name in topics: 

            if "/camera/depth/camera_info" in topic_name:
                logging.info("Subscribed Topic is: ")
                logging.info(topic_name)
                return topic_name
            elif "/stereo/camera_info" in topic_name:
                logging.info("Subscribed Topic is: ")
                logging.info(topic_name)
                return topic_name
            
        logging.info("No matching camera info topic found. Retrying in 1 second...")
        time.sleep(1)