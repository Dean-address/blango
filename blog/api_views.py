from http import HTTPStatus

from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response


from blog.models import Post
from blog.api.serializers import PostSerializer




@api_view(["GET", "POST"])
def post_list(request, format=None):
    if request.method == "GET":
        posts = Post.objects.all()
        serializers = PostSerializer(posts, many=True)
        return Response({"data": serializers.data})
    elif request.method == "POST":
        serializers = PostSerializer(data=request.data)
        if serializers.is_valid():
          post = serializers.save()
        return Response(
            status=HTTPStatus.CREATED,
            headers={"Location": reverse("api_post_detail", args=(post.pk,))},
        )

    return Response(serializers.errors, status=HTTPStatus.BAD_REQUEST)


@api_view(["GET", "PUT", 'DELETE'])
def post_detail(request, pk, format=None):
  try:
    post = Post.objects.get(pk=pk)
  except Post.DoesNotExist:
    return Response(status=HTTPStatus.NOT_FOUND)

  if request.method == "GET":
    return Response(PostSerializer(post).data)
  elif request.method == "PUT":
    serializers = PostSerializer(post, data=request.data)
    if serializers.is_valid():
      serializers.save()
      return Response(status=HTTPStatus.NO_CONTENT)
    return Response(serializers.errors, status=HTTPStatus.BAD_REQUEST)
  elif request.method == "DELETE":
    post.delete()
    return Response(status=HTTPStatus.NO_CONTENT)

  
