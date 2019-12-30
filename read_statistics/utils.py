import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from read_statistics.models import ReadNum, ReadDetail
from blog.models import Blog


def read_statistics_once_read(request, obj):
	ct = ContentType.objects.get_for_model(obj)
	key = f'{ct.model}_{obj.pk}_read'
	if not request.COOKIES.get(key):
		# 总阅读数 +1
		readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.id)
		readnum.read_num += 1
		readnum.save()

		# 当天阅读数 +1
		date = timezone.now().date()
		read_detail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.id, date=date)
		read_detail.read_num += 1
		read_detail.save()
	return key


def get_seven_days_read_data(content_type):
	today = timezone.now().date()
	read_nums = list()
	dates = list()
	for i in range(7, 0, -1):
		date = today - datetime.timedelta(days=i)
		dates.append(date.strftime('%m/%d'))
		read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
		result = read_details.aggregate(read_num_sum=Sum('read_num'))
		read_nums.append(result['read_num_sum'] or 0)
	return dates, read_nums


def get_today_hot_data(content_type):
	today = timezone.now().date()
	read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
	return read_details[:3]


def get_yesterday_hot_data(content_type):
	today = timezone.now().date()
	yesterday = today - datetime.timedelta(days=1)
	read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
	return read_details[:3]


def get_7_days_hot_data():
	today = timezone.now().date()
	date = today - datetime.timedelta(days=7)
	blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date) \
								 .values('id', 'title') \
								 .annotate(read_num_sum=Sum('read_details__read_num')) \
								 .order_by('-read_num_sum')
	return blogs[:3]

