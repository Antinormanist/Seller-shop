from django.db.models import Q


def q_search(search: str) -> Q:
    '''
    Return Q objects
    '''
    result = Q()
    for word in search.split():
        result |= Q(name__icontains=word)
        result |= Q(description__icontains=word)
    return result