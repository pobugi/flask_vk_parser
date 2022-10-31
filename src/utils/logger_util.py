import functools
import logging
from datetime import datetime

from flask import request, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def write_logs(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        method = request.method or None
        pth = request.path or None
        params = request.args or None

        logger.info(
            "[{dt}] [{fname}] {method} {pth}, params: {params}".format(
                dt=(datetime.now()).strftime("%d/%m/%Y %H:%M:%S"),
                fname=func.__name__,
                method=method,
                pth=pth,
                params=params,
            )
        )
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as exc:
            logger.exception("Exception raised in {0}. exception: {1}".format(func.__name__, exc.args))
            return jsonify({"error": "Bad request"}), 400

    return wrapper
