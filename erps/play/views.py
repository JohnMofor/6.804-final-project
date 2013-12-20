from django.shortcuts import render
from django.http import HttpResponse
from play.models import Player

# Create your views here.


def create(request):
    raw_id_number = request.GET.get("id","")
    try:
        parsed_id_number = int(raw_id_number)
        player = Player(id_number=parsed_id_number)
        player.build()
        response_message = 'done'
        print  "Res: ",response_message

        response = HttpResponse(response_message)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    except Exception as e:
        return HttpResponse("Error: "+str(e))


def get(request):
    id_number = request.GET.get("id","")
    scenario = request.GET.get("scenario","")
    index = request.GET.get("index","")
    try:
        id_number = int(id_number)
        index = int(index)
        player = Player.objects.filter(pk=id_number)
        print id_number,index,player
        if len(player)==0:
            create(request)
            return get(request)
        else:
            player=player[0]
        response_message = player.get(scenario,index)
        print  "Res: ",response_message
        response = HttpResponse(response_message)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    except Exception as e:
        print "EEERRROOOR:",e,'re-try'
        #create(request)
        return HttpResponse("Error: "+str(e))



def show(request):
    id_number = request.GET.get("id","")
    try:
        id_number = int(id_number)
        player = Player.objects.get(pk=id_number)
        return HttpResponse(player.show())
    except Exception as e:
        return HttpResponse("Error: "+str(e))

def show_groups(request):
    id_number = request.GET.get("id","")
    try:
        id_number = int(id_number)
        player = Player.objects.get(pk=id_number)
        response_message =  HttpResponse(player.show_groups())
        print "res: ", response_message

        response = HttpResponse(response_message)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

    except Exception as e:
        return HttpResponse("Error: "+str(e))

def welcome(request):
    return render(request, 'index.html', {})

