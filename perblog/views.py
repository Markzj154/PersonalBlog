from django.core.cache import cache
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data, get_7_days_hot_data
from blog.models import Blog


def home(request):
	blog_content_type = ContentType.objects.get_for_model(Blog)
	dates, read_nums = get_seven_days_read_data(blog_content_type)

	# 获取7天热门博客的缓存数据
	seven_days_hot_data = cache.get('seven_days_hot_data')
	if seven_days_hot_data is None:
		seven_days_hot_data = get_7_days_hot_data()
		cache.set('seven_days_hot_data', seven_days_hot_data, 3600)

	today_hot_data = get_today_hot_data(blog_content_type)
	yesterday_hot_data = get_yesterday_hot_data(blog_content_type)

	context = {}
	context['read_nums'] = read_nums
	context['dates'] = dates
	context['today_hot_data'] = today_hot_data
	context['yesterday_hot_data'] = yesterday_hot_data
	context['seven_days_hot_data'] = seven_days_hot_data
	return render(request, 'home.html', context)



