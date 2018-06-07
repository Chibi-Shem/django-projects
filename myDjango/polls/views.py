# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse


def detail(request, question_id):
	return HttpResponse("Question " + str(question_id))


def results(request, question_id):
	return HttpResponse("Question results are" + str(question_id))


def vote(request, question_id):
	return HttpResponse("Question vote " + str(question_id))
