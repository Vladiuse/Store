from store.models import Position

POSITIONS = [
    {
        'id': 'moderator',
        'name': 'Модератор сайта'
    },
    {
        'id': 'manager',
        'name': 'Менеджер'
    },
    {
        'id': 'seller',
        'name': 'Продавец'
    },
]


def create_positions():
    to_create = []
    for item in POSITIONS:
        pos = Position(id=item['id'], name=item['name'])
        to_create.append(pos)
    Position.objects.bulk_create(to_create)
    print('Position created', Position.objects.count())


def delete_all_positions():
    Position.objects.all().delete()


delete_all_positions()
create_positions()
