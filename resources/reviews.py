from flask import jsonify, Blueprint, url_for
from flask_restful import Resource, Api, reqparse, inputs, fields, marshal, marshal_with

import models

review_fields = {
	'id': fields.Integer,
	'for_course': fields.String,
	'rating': fields.Integer,
	'comment': fields.String(default=''),
	'created_at': fields.DateTime
}


def add_course(review):
	review.for_course = url_for('resources.courses.course', id=review.course.id)
	return review


class ReviewList(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()

		self.reqparse.add_argument(
			'course',
			type=inputs.positive,
			required=True,
			help='No course provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'rating',
			type=inputs.int_range(1, 5),
			help='No rating provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'comment',
			required=False,
			nullable=True,
			default='',
			location=['form, json']
		)
		
		# super().__init__()
		super(ReviewList, self).__init__()

	def get(self):
		reviews = [
			marshal(add_course(review), review_fields)
			for review in models.Review.select()
		]
		return {'reviews': reviews}

	@marshal_with(review_fields)
	def post(self):
		args = self.reqparse.parse_args()
		review = models.Review.create(**args)
		return add_course(review)


class Review(Resource):
	def get(self, id):
		return jsonify({'course': 1, 'rating': 5})

	def put(self, id):
		return jsonify({'course': 1, 'rating': 5})

	def delete(self, id):
		return jsonify({'course': 1, 'rating': 5})


reviews_api = Blueprint('resources.reviews', __name__)

api = Api(reviews_api)
api.add_resource(ReviewList, '/reviews', endpoint='reviews')
api.add_resource(Review, '/reviews/<int:id>', endpoint='review')
