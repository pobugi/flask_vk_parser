import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("VK_ACCESS_TOKEN")
BASE_URL = os.getenv("VK_API_BASE_URL")
VERSION = os.getenv("VK_API_VERSION")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class VkDataUtils:
    @staticmethod
    def get_current_user_friends():
        url = f"{BASE_URL}/friends.get"
        params = {"v": VERSION, "access_token": ACCESS_TOKEN}

        resp = requests.get(url=url, params=params)
        if "error" in resp:
            logger.warning(resp["error"])
            return []
        friends_ids = resp.json()["response"]["items"]
        return friends_ids

    @staticmethod
    def get_current_user():
        url = f"{BASE_URL}/users.get"
        params = {"v": VERSION, "access_token": ACCESS_TOKEN}

        resp = requests.get(url=url, params=params).json()
        if "error" in resp:
            logger.warning(resp["error"])
            return None
        return resp["response"][0].get("id")

    @staticmethod
    def get_groups_by_user(user_id):
        url = f"{BASE_URL}/groups.get"
        params = {"v": VERSION, "access_token": ACCESS_TOKEN, "user_id": user_id, "extended": 1}

        resp = requests.get(url=url, params=params).json()
        if "error" in resp:
            logger.warning(resp["error"])
            return []
        return resp["response"]["items"]

    @staticmethod
    def get_groups_of_user_and_friends(substr, limit):

        friend_ids = VkDataUtils.get_current_user_friends()
        if limit and str(limit).isdigit():
            friend_ids = friend_ids[: int(limit)]
        current_user_id = [VkDataUtils.get_current_user()]
        user_ids = current_user_id + friend_ids

        sub_result = []
        for user_id in user_ids:
            sub_result += VkDataUtils.get_groups_by_user(user_id=user_id)

        result = list({group["id"]: group for group in sub_result}.values())  # unique groups

        if substr:
            result = list(filter(lambda group: substr.lower() in group["name"].lower(), result))
        return result
