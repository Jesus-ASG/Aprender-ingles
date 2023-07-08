from django.core.paginator import Paginator
from django.db.models import Q
from main.models import Story, Tag


def paginate_stories(request, items_per_page):
    # Get query params
	q_collection = request.GET.get('collection')
	q_search = request.GET.get('s')
	q_tags = request.GET.getlist('tag')
	q_sort = request.GET.get('sort')
	q_page = request.GET.get('p')

	filter_form = {
		'collection': q_collection,
		's': q_search,
		'tags': q_tags,
		'sort': q_sort
	}
	
	user_profile = request.user.profile
	stories = None
	page_title = ''
	message_if_empty = ''
	match q_collection:
		case 'liked':
			stories = Story.objects.filter(likedstory__user_profile=user_profile).exclude(xp_required__gt = user_profile.xp)
			page_title = 'Your liked stories'
			message_if_empty = "You don't have liked stories yet"
			stories = stories.order_by('-likedstory__date')
		case 'saved':
			page_title = 'Your saved stories'
			stories = Story.objects.filter(savedstory__user_profile=user_profile).exclude(xp_required__gt = user_profile.xp)
			message_if_empty = "You don't have saved stories yet"
			stories = stories.order_by('-savedstory__date')
		case _:
			page_title = 'Stories Gallery'
			stories = Story.objects.all().exclude(xp_required__gt = user_profile.xp)
			stories = stories.order_by('-updated_at')

	tags = Tag.objects.all().order_by('name1')
	
	# Custom filters
	# Search
	if q_search:
		stories = stories.filter(Q(title1__icontains=q_search) | Q(title2__icontains=q_search))

	# Filter by tags
	try:
		if not q_tags[0] == 'all':
			q_tag_ids = [int(x) for x in q_tags]    
			stories = stories.filter(tags__id__in=q_tag_ids).distinct()
	except:
		pass
			
	# Sort
	if not q_sort == 'default':
		match q_sort:
			case 'a-z':
				stories = stories.order_by('title1')
			case 'updated':
				stories = stories.order_by('-updated_at')
			case 'created':
				stories = stories.order_by('-created_at')
	
	# Paginate        
	paginator = Paginator(stories, items_per_page)
	try:
		q_page = int(q_page)
		if q_page <=0:
			q_page = 1
		if q_page > paginator.num_pages:
			q_page = paginator.num_pages
	except:
		q_page = 1


	elided_page_range = list(paginator.get_elided_page_range(q_page, on_each_side=2, on_ends=1))

	query_params = request.GET.copy()
	page_range = []
	for p in elided_page_range:
		if type(p) == int:
			query_params['p'] = p
			url = '{}?{}'.format(request.path, query_params.urlencode())
		else:
			url = '#'
		page_range.append({'label': p, 'url': url})
	
	
	stories = paginator.page(q_page)
	urls = {}
	query_params = request.GET.copy()

	if stories.has_previous():
		query_params['p'] = stories.previous_page_number()
		urls['prev'] = '{}?{}'.format(request.path, query_params.urlencode())

	if stories.has_next():
		query_params['p'] = stories.next_page_number()
		urls['next'] = '{}?{}'.format(request.path, query_params.urlencode())
	

	context = {
		'page_title': page_title,
		'stories': stories,
		'tags': tags,
		'filter_form': filter_form,
		'page_range': page_range,
		'urls': urls,
		'message_if_empty': message_if_empty,
	}
	return context