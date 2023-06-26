from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Attendee
from events.models import Conference
from common.json import ModelEncoder
import json

class AttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties = ["name"]

class AttendeeDetailEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "name",
        "email"
        # "company_name",
        # "created",
    ]


@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_id):
    if request.method == "GET":
        attendees = Attendee.objects.filter(conference=conference_id)
    #     {
    #         "name": a.name,
    #         "href": a.get_api_url(),
    #     }
    #     for a in Attendee.objects.filter(conference=conference_id)
    # ]
        return JsonResponse({"attendees": attendees},
                            encoder=AttendeeListEncoder,)
    else:
        content = json.loads(request.body)
        try:
            # conference_href = f"/api/conferences/{conference_id}/"
            # conference = Conference.objects.get(import_href=conference_href)
            conference = Conference.objects.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid attendee id"},
                status=400,
            )
        attendee = Attendee.objects.create(**content)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )

@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_attendee(request, id):
    if request.method == "GET":
        attendee = Attendee.objects.get(id=id)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        count, _ = Attendee.objects.filter(id=id).delete()
        return JsonResponse({"deteled": count > 0})
    else:
        content = json.loads(request.body)
        try:
            if "attendee" in content:
                attendee = Attendee.objects.get(id=id)
                content["attendee"] = attendee
        except Attendee.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid attendee id"},
                status=400,
            )
        Attendee.objects.filter(id=id).update(**content)
        attendee = Attendee.objects.get(id=id)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )


