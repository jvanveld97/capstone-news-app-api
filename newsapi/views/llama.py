import json
import requests
from django.http import JsonResponse
from llamaapi import LlamaAPI
from newsapi.models import Article
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response


class SummarizerView(viewsets.ViewSet):
    def create(self, request):
        try:
            data = json.loads(request.body)
            article_url = data.get("articleUrl")
        except (ValueError, KeyError):
            return Response(
                {"error": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not article_url:
            return Response(
                {"error": "articleUrl is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        llama_api = (
            "LL-6zFkA7yCPfHfYBQAosu7sUGSaJ0nxRS4ccF4DGPWI8797w3qrYML1lvDTS8pR9mt"
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {llama_api}",
        }
        url = f"https://api.llama-api.com/chat/completions"

        api_request_json = {
            "messages": [
                {
                    "role": "user",
                    "content": f"Summarize the following link: {article_url}",
                },
            ],
        }

        response = requests.post(url, headers=headers, json=api_request_json)
        return Response(response.json())
