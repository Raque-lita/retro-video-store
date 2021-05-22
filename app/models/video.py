from flask import current_app
from app import db
from sqlalchemy.orm import relationship



class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable = True)
    inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer, default=inventory)
    
    def return_video_info(self):
        return {"id" : self.video_id,
                "title" : self.title,
                "release_date": self.release_date,
                "total_inventory": self.inventory     
        }

    
    # def inventory_checkout(self):        
    #     if self.available_inventory:
    #         self.available_inventory = self.available_inventory - 1
    #     # else:
    #     #     self.available_inventory = 1  
    #     db.session.commit()

