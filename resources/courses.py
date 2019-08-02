from flask import (
	jsonify, Blueprint, abort, url_for
)
from flask_restful import (
	Resource, Api, reqparse, inputs, fields, marshal, marshal_with
)

import models

course_fields = {
	'id': fields.Integer,
	'title': fields.String,
	'url': fields.String,
	'reviews': fields.List(fields.String)
}


def course_or_404(course_id):
	try:
		course = models.Course.get(models.Course.id == course_id)
	except models.Course.DoesNotExist:
		abort(404, 'Course %d does not exist' % course_id)
	else:
		return course


def add_reviews(course):
	course.reviews = [
		url_for('resources.reviews.review', id=review.id)
		for review in course.review_set
	]
	return course


class CourseList(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()

		self.reqparse.add_argument(
			'title',
			required=True,
			help='No title provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'url',
			type=inputs.url,
			required=True,
			help='No URL provided',
			location=['form', 'json']
		)

		# super().__init__()
		super(CourseList, self).__init__()

	def get(self):
		# courses = [
		# 	marshal(add_reviews(course), course_fields)
		# 	for course in models.Course.select()
		# ]
		# return {'courses': courses}

		courses = [add_reviews(course) for course in models.Course.select()]
		return {'courses': marshal(courses, course_fields)}

	@marshal_with(course_fields)
	def post(self):
		args = self.reqparse.parse_args()
		course = models.Course.create(**args)
		return add_reviews(course), 201, {
			'Location': url_for('resources.courses.course', id=course.id)
		}


class Course(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()

		self.reqparse.add_argument(
			'title',
			required=True,
			help='No title provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'url',
			type=inputs.url,
			required=True,
			help='No URL provided',
			location=['form', 'json']
		)

	@marshal_with(course_fields)
	def get(self, id):
		return add_reviews(course_or_404(id))

	@marshal_with(course_fields)
	def put(self, id):
		args = self.reqparse.parse_args()
		query = models.Course.update(**args).where(models.Course.id == id)
		query.execute()
		return add_reviews(models.Course.get(models.Course.id == id)), 200, {
			'Location': url_for('resources.courses.course', id=id)
		}

	def delete(self, id):
		query = models.Course.delete().where(models.Course.id == id)
		query.execute()
		return '', 204, {'Location': url_for('resources.courses.courses')}


courses_api = Blueprint('resources.courses', __name__)

api = Api(courses_api)
api.add_resource(CourseList, '/api/v1/courses', endpoint='courses')
api.add_resource(Course, '/api/v1/courses/<int:id>', endpoint='course')
