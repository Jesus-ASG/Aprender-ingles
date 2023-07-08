import json

from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from main.models import RepeatPhrase


@login_required(login_url='/login/')
def request_answer(request):
    if request.method == 'POST':
        key = f'user_request_exercises_{request.user.id}'
        rate_limit = 150
        rate_limit_time = 60

        num_requests = cache.get(key, 0)
        if num_requests > rate_limit:
            return JsonResponse({'error': 'Rate limit exceeded'}, status=429)
        cache.set(key, num_requests + 1, rate_limit_time)


        #data = request.POST["data"]
        #data = json.loads(data)
        #print(data)
        exercise_type = request.POST['exercise_type']
        exercise_id = int(request.POST['exercise_id'])
        response = ''
        match exercise_type:
            case 'repeat_phrase':
                rp = RepeatPhrase.objects.get(id=exercise_id)
                response = rp.content1

        return JsonResponse({'success': True, 'response': response})