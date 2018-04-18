from django.shortcuts import render

from madrid.models import District, TrafficTicket, Neighborhood


def stats_by_district(request):

    districts = District.objects.all()
    result = []

    for district in districts:

        traffic_ticket = TrafficTicket.objects.filter(geom__intersects=district.geom)
        result.append({
            'name': district.name,
            'ticket_count': len(traffic_ticket),
        })

    ordered_result = sorted(result, key=lambda stat: stat['ticket_count'], reverse=True)

    context = {'statistics': ordered_result,
               'entity': 'Distritos'}

    return render(request, 'madrid/index.html', context)


def stats_by_neighborhood(request):

    neighborhoods = Neighborhood.objects.all()
    result = []

    for neighborhood in neighborhoods:

        traffic_tickets = TrafficTicket.objects.filter(geom__intersects=neighborhood.geom)
        result.append({
            'name': neighborhood.name,
            'ticket_count': len(traffic_tickets),
        })

    ordered_result = sorted(result, key=lambda stat: stat['ticket_count'], reverse=True)

    context = {'statistics': ordered_result,
               'entity': 'Barrios'}

    return render(request, 'madrid/index.html', context)
