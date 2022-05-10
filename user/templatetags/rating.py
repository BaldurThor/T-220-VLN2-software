from django import template
register = template.Library()


@register.inclusion_tag('user/user_rating_hunger_games.html')
def rating_tag(rating):
    context = {
        'full': rating // 2,
        'half': rating % 2,
        'empty': (10 - rating) // 2,
    }
    return context


@register.simple_tag()
def get_rating(rating):
    return rating / 2
