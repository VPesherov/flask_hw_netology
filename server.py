import pydantic
from flask import Flask, jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from models import Ad, Session
from schema import CreateAd, UpdateAd

app = Flask('app')


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response):
    request.session.close()
    return response


class HttpError(Exception):
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.description})
    response.status_code = error.status_code
    return response


def validate(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)


def add_ad(ad: Ad):
    try:
        request.session.add(ad)
        request.session.commit()
    except IntegrityError:
        raise HttpError(400, "ad arleady exists")


def get_ad_by_id(user_id: int):
    ad = request.session.get(Ad, user_id)
    if ad is None:
        raise HttpError(404, "ad not found")
    return ad


class AdView(MethodView):

    def get(self, ad_id):
        ad = get_ad_by_id(ad_id)
        return jsonify(ad.ads_dict)

    def patch(self, ad_id):
        json_data = validate(UpdateAd, request.json)
        ad = get_ad_by_id(ad_id)
        for key, value in json_data.items():
            setattr(ad, key, value)
        add_ad(ad)
        return jsonify(ad.ads_dict)

    def post(self):
        json_data = validate(CreateAd, request.json)
        ad = Ad(**json_data)
        add_ad(ad)
        # print(user.id, user.name, user.registration_time)
        return jsonify(ad.ads_dict)

    def delete(self, ad_id):
        ad = get_ad_by_id(ad_id)
        request.session.delete(ad)
        request.session.commit()
        return jsonify(
            {
                "status": "deleted",
            }
        )


def start_server():
    ad_view = AdView.as_view("user")
    app.add_url_rule("/ads/", view_func=ad_view, methods=["POST"])
    app.add_url_rule("/ads/<int:ad_id>", view_func=ad_view, methods=["GET", "PATCH", "DELETE"])
    app.run()
