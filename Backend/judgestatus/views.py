# -*- coding: utf-8 -*-
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.pagination import LimitOffsetPagination
from .models import JudgeStatus, CaseStatus
from .serializers import JudgeStatusSerializer, CaseStatusSerializer, JudgeStatusCodeSerializer
from .permission import ManagerOnly, UserRatingOnly, NoContestOnly
from contest.models import ContestInfo
from contest.serializers import ContestInfoSerializer
import datetime



class JudgeStatusView(viewsets.ModelViewSet):
    queryset = JudgeStatus.objects.all().order_by('-id')
    serializer_class = JudgeStatusSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', 'result', "contest", "problem", "language", "problemtitle")
    permission_classes = (ManagerOnly,)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class JudgeStatusPutView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = JudgeStatus.objects.all()
    serializer_class = JudgeStatusCodeSerializer
    permission_classes = (UserRatingOnly,)
    throttle_scope = "judge"
    throttle_classes = [ScopedRateThrottle, ]


class JudgeStatusCodeView(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = JudgeStatus.objects.all()
    serializer_class = JudgeStatusCodeSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', 'result', "contest", "problem", "problemtitle")
    permission_classes = (NoContestOnly,)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class CaseStatusView(viewsets.ModelViewSet):
    queryset = CaseStatus.objects.all()
    serializer_class = CaseStatusSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('username', 'problem', "statusid")
    permission_classes = (ManagerOnly,)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]

class ACRankView(viewsets.ModelViewSet):
    queryset = JudgeStatus.objects.filter(submittime__gte=datetime.datetime.now()-datetime.timedelta(days=7),result=0) # ??????????????????????????????????????????OJ????????????????????????????????????????????????
    serializer_class = JudgeStatusSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', 'result', "contest", "problem", "language")
    permission_classes = (ManagerOnly,)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class RejudgeAPIView(APIView):
    permission_classes = (ManagerOnly,)

    def post(self, request, format=None):
        data = request.data
        contestid = data.get('contestid', "")
        problem = data.get('problem', "")
        statusid = data.get('statusid', "")
        statustype = data.get('statustype', "")

        print(contestid, problem, statusid, statustype)

        if contestid == 0 or problem == -1:
            return Response("bad", status=HTTP_400_BAD_REQUEST)

        if contestid != "" and problem != "":
            JudgeStatus.objects.filter(contest=contestid).filter(
                contestproblem=problem).update(result=-1)
            return Response("ok", status=HTTP_200_OK)

        if problem != "" and contestid == "":
            JudgeStatus.objects.filter(problem=problem).update(result=-1)
            return Response("ok", status=HTTP_200_OK)

        if statusid != "":
            JudgeStatus.objects.filter(id=statusid).update(result=-1)
            return Response("ok", status=HTTP_200_OK)

        if statustype != "":
            JudgeStatus.objects.filter(result=statustype).update(result=-1)
            return Response("ok", status=HTTP_200_OK)

        return Response("bad", status=HTTP_400_BAD_REQUEST)
