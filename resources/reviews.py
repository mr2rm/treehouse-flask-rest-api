from flask import jsonify
from flask.ext.restful import Resource


class ReviewList(Resource):
	def get(self):
		return jsonify({
			'reviews': [{'course': 1, 'rating': 5}]
		})


class Review(Resource):
	def get(self, id):
		return jsonify({'course': 1, 'rating': 5})

	def put(self, id):
		return jsonify({'course': 1, 'rating': 5})

	def delete(self, id):
		return jsonify({'course': 1, 'rating': 5})
