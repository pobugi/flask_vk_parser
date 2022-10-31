import logging
import os

from dotenv import load_dotenv
from flask import Blueprint, jsonify, request

from src.api.parser.models import SearchAttempt, SearchResult
from src.utils.logger_util import write_logs
from src.utils.paginate import Paginator
from src.utils.vk_data import VkDataUtils

load_dotenv()

ACCESS_TOKEN = os.getenv("VK_ACCESS_TOKEN")

vk_parser_api = Blueprint("parser_api", __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


@vk_parser_api.route("/groups", methods=["GET"])
@write_logs
def get_groups():

    substr = request.args.get("substr")
    limit = request.args.get("limit")

    result = VkDataUtils.get_groups_of_user_and_friends(substr, limit)
    return jsonify(result)


@vk_parser_api.route("/groups/my", methods=["GET"])
@write_logs
def get_my_groups():

    substr = request.args.get("substr")
    user_id = VkDataUtils.get_current_user()
    my_groups = VkDataUtils.get_groups_by_user(user_id=user_id)
    if substr:
        my_groups = list(filter(lambda group: substr.lower() in group["name"].lower(), my_groups))

    attempt = SearchAttempt.create({"query_parameters": f"substr: {substr}"})
    for group in my_groups:
        try:
            SearchResult.create(group, attempt)
        except Exception as exc:
            logger.warning(exc.args)
            pass
    return jsonify(my_groups)


@vk_parser_api.route("/groups/my/attempts", methods=["GET"])
@write_logs
def get_request_attempts():

    results = SearchAttempt.get_all()
    return jsonify([r.to_dict() for r in results])


@vk_parser_api.route("/groups/my/results", methods=["GET"])
@write_logs
def get_request_results():
    total_rows = SearchResult.get_total_rows()
    pagination = Paginator.apply(params=request.args, total_rows=total_rows)
    limit = pagination.get("limit")
    offset = pagination.get("offset")
    page = pagination.get("page")
    results = [r.to_dict() for r in SearchResult.get_all(limit=limit, offset=offset)]
    return jsonify(
        {
            "items": results,
            "count": SearchResult.get_total_rows(),
            "per_page": limit,
            "page": page,
            "pages": pagination.get("pages"),
        }
    )
