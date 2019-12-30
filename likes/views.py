from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from likes.models import LikeRecord, LikeCount


def SuccessResponse(liked_num):
	data = {}
	data['status'] = 'SUCCESS'
	data['liked_num'] = liked_num
	return JsonResponse(data)


def ErrorResponse(code, message):
	data = {}
	data['status'] = 'ERROR'
	data['code'] = code
	data['message'] = message
	return JsonResponse(data)


def like_change(request):
	# 获取数据
	user = request.user
	if not user.is_authenticated:
		return ErrorResponse(3003, '未登录，不能进行点赞')
	content_type = request.GET.get('content_type')
	object_id = int(request.GET.get('object_id'))
	try:
		content_type = ContentType.objects.get(model=content_type)
		model_class = content_type.model_class()
		model_obj = model_class.objects.get(id=object_id)
	except ObjectDoesNotExist:
		return ErrorResponse(3004, '对象不存在')

	# 处理数据
	if request.GET.get('is_like') == 'true':
		# 点赞
		like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
		if created:
			# 未点赞，进行点赞
			like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
			like_count.liked_num += 1
			like_count.save()
			return SuccessResponse(like_count.liked_num)
		else:
			# 已经点赞，不能点赞
			return ErrorResponse(3000, '您已经点赞过，不能进行点赞')

	else:
		# 取消点赞
		if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
			# 有过点赞，取消点赞
			like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
			like_record.delete()
			# 点赞总数减1
			like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
			if not created:
				like_count.liked_num -= 1
				like_count.save()
				return SuccessResponse(like_count.liked_num)

			else:
				return ErrorResponse(3002, '数据错误')
		else:
			# 没有点赞过，不能取消
			return ErrorResponse(3001, '未点赞，不能进行取消')
