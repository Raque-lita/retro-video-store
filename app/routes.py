from app import db
from flask import Blueprint, request, make_response, jsonify
from .models.customer import Customer
from .models.video import Video



customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


def error_handling(request_body):
    if "name" or "postal_code" or "phone" not in request_body:
        return True
    
    # if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
    #     return make_response({"details": "Invalid data"}, 400)
    

@customers_bp.route("", methods=["POST"])
def create_customer():
    
    form_data = request.get_json()
    if "name" not in form_data or "postal_code" not in form_data or "phone" not in form_data:
        return make_response({"details": "Invalid data"}), 400
    customer = Customer(customer_name=form_data["name"],
                    postal_code=form_data["postal_code"],
                    phone_number=form_data["phone"],
                    )

    db.session.add(customer)
    db.session.commit()

    return make_response(customer.return_customer_info(), 201)

@customers_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    customer_list = []
    for customer in customers:
        customer_list.append(customer.return_customer_info())

    return jsonify(customer_list), 200

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    #form_data = request.get_json()
    if customer is None:
        return make_response({"details": "invalid data"}, 404)

    return make_response(customer.return_customer_info(), 200)

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer_info(customer_id):
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response({"details": "invalid data"}, 404)

    form_data = request.get_json()
    if "name" not in form_data or "postal_code" not in form_data or "phone" not in form_data:
        return make_response({"details": "Invalid data"}, 400)

    customer.customer_name = form_data["name"]
    customer.postal_code = form_data["postal_code"]
    customer.phone_number = form_data["phone"]

    db.session.commit()

    return make_response(customer.return_customer_info())

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_response({"details": "id does not exist"}, 404)

    # Customer.query.filter_by(customer_id=customer_id).delete()
    db.session.delete(customer) 
    db.session.commit()

    return make_response({"id":int(customer_id)})

@videos_bp.route("", methods=["POST"])
def create_video():
    
    form_data = request.get_json()
    if "title" not in form_data or "release_date" not in form_data or "total_inventory" not in form_data:
        return make_response({"details": "Invalid data"}, 400)

    video = Video(title=form_data["title"],
                    release_date=form_data["release_date"],
                    inventory=form_data["total_inventory"],
                    )

    db.session.add(video)
    db.session.commit()

    return make_response({"id": video.video_id}, 201)


@videos_bp.route("", methods=["GET"])
def get_videos():
    videos = Video.query.all()
    video_list = []
    for video in videos:
        video_list.append(video.return_video_info())

    return jsonify(video_list), 200

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = Video.query.get(video_id)
    if video is None:
        return make_response({"details": "id does not exist"}, 404)

    db.session.delete(video) 
    db.session.commit()

    return make_response({"id":int(video_id)})

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video_info(video_id):
    video = Video.query.get(video_id)

    if video is None:
        return make_response({"details": "video not found"}, 404)

    form_data = request.get_json()
    if "title" not in form_data or "release_date" not in form_data or "total_inventory" not in form_data:
        return make_response({"details": "Invalid/Missing data"}, 400)

    video.title = form_data["title"]
    video.release_date = form_data["release_date"]
    video.inventory = form_data["total_inventory"]

    db.session.commit()

    return make_response(video.return_video_info())


@videos_bp.route("/<video_id>", methods=["GET"])
def get_single_video(video_id):
    video = Video.query.get(video_id)
    #form_data = request.get_json()
    if video is None:
        return make_response({"details": "invalid data"}, 404)

    return make_response(video.return_video_info(), 200)