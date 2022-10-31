from datetime import datetime

from src import db


class SearchAttempt(db.Model):
    __tablename__ = "search_attempt"
    id = db.Column(db.Integer, primary_key=True)
    query_parameters = db.Column(db.String)
    created = db.Column(db.DateTime, nullable=False)
    search_results = db.relationship("SearchResult", back_populates="search_attempt")

    @staticmethod
    def create(data_dict):
        search_attempt = SearchAttempt(query_parameters=data_dict.get("query_parameters"), created=datetime.now())
        db.session.add(search_attempt)
        db.session.commit()
        return search_attempt

    @staticmethod
    def get_all():
        return SearchAttempt.query.order_by(SearchAttempt.created.desc()).all()

    def to_dict(self):
        return {
            "id": self.id,
            "query_parameters": self.query_parameters,
            "created": self.created,
            "search_results": [res.to_dict() for res in self.search_results],
        }


class SearchResult(db.Model):
    __tablename__ = "search_result"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    screen_name = db.Column(db.String)
    is_closed = db.Column(db.Integer)
    type = db.Column(db.String)
    photo_50 = db.Column(db.String)
    photo_100 = db.Column(db.String)
    photo_200 = db.Column(db.String)
    created = db.Column(db.DateTime, nullable=False)
    search_attempt = db.relationship("SearchAttempt", back_populates="search_results")
    search_attempt_id = db.Column(db.Integer, db.ForeignKey("search_attempt.id"), nullable=False)

    @staticmethod
    def get_total_rows():
        return SearchResult.query.count()

    @staticmethod
    def create(data_dict, search_attempt):
        search_result_item = SearchResult(
            name=data_dict.get("name"),
            screen_name=data_dict.get("screen_name"),
            is_closed=data_dict.get("is_closed"),
            type=data_dict.get("type"),
            photo_50=data_dict.get("photo_50"),
            photo_100=data_dict.get("photo_100"),
            photo_200=data_dict.get("photo_200"),
            search_attempt=search_attempt,
            created=datetime.now(),
        )
        db.session.add(search_result_item)
        db.session.commit()
        return search_result_item

    @staticmethod
    def get_all(limit=None, offset=None):
        return SearchResult.query.order_by(SearchResult.created.desc()).limit(limit).offset(offset).all()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "screen_name": self.screen_name,
            "is_closed": self.is_closed,
            "type": self.type,
            "photo_50": self.photo_50,
            "photo_100": self.photo_100,
            "photo_200": self.photo_200,
        }
