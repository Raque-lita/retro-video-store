from flask import current_app
from app import db
from sqlalchemy.orm import relationship
from datetime import timedelta
from datetime import datetime

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id"))
    video_id = db.Column(db.Integer, db.ForeignKey("video.video_id")) #do we need primary key?
    due_date = db.Column(db.DateTime)
    customer = db.relationship('Customer', backref='rentals', lazy=True)
    video = db.relationship('Video', backref='rentals', lazy=True)

    
    @classmethod
    def checkout(cls, customer_id, video_id):

        from .customer import Customer
        from .video import Video
 
        customer = Customer.query.get(customer_id)
        video = Video.query.get(video_id)

        due_date = datetime.now() + timedelta(days=7)
        new_rental = Rental(
    
                customer_id = customer.customer_id,
                video_id = video.video_id,
                due_date = due_date
    )
        db.session.add(new_rental)
        db.session.commit()
    #customer.helper function to adjust customer attritubve
        video.inventory_checkout()
        customer.added_checkout()

    #helpfer function ot connect increase checkout count()
    #decrease_inventory()
    # .add rental_id
    # .commit 
        return new_rental

    def return_rental_info(self):
        return {"customer_id" : self.customer_id,
                "video_id" : self.video_id,
                "due_date" : self.due_date,
                "videos_checked_out_count": self.customer.videos_checked_out_count,
                "available_inventory": self.video.available_inventory
        }
