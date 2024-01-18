from content.models import People


def generate_name(array):
    if not array:
        return ""
    if '!H' in array[0]:
        return generate_name(array[1:])
    return array[0] + " " + generate_name(array[1:])


def generate_director_code(code):
    if code:
        return code
    return str(People.objects.filter(is_director=True).count())


def generate_actor_code(code):
    if code:
        return code
    return "t" + str(People.objects.filter(is_actor=True).count())


def generate_writer_code():
    return str(People.objects.filter(is_writer=True).count())


def generate_role(name):
    if name:
        return name
    return '출연'
