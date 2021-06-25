import datetime
import random

from django.http import JsonResponse, response, HttpResponse
from django.shortcuts import render, redirect
# from django.contrib.sessions.models import Session
from user_interface.models import Racks, LEDS
from django.core import serializers
from django.views.decorators.csrf import csrf_protect
# from django.views.decorators.cache import never_cache
import json
from user_interface import runInjector
from user_interface.partpicker_database import query_database


@csrf_protect
def part_selector(request):
    data = Racks.objects.all()

    racks = {
        "part_number": data,
        "description": data,
        "location": data,
        "ip": data,
        "id": data
    }

    return render(request, 'part_selector.html', racks)


# @never_cache
def load_data(request):
    if request.method == "POST":
        data = Racks.objects.all()
        data = serializers.serialize('json', data)

        racks = {
            "racks": data
        }

        return HttpResponse(json.dumps(racks))
    else:
        data = Racks.objects.all()
        data = serializers.serialize('json', data)

        racks = {
            "racks": data,
            "data": data
        }
        return render(request, 'part_selector.html', racks)


# @never_cache
def load_map(request, selected_parts=None):
    # TODO fix django session
    # TODO Fix session key issue when database has new locations to add
    if request.method == "POST":
        parts = request.POST.get('parts')
        print(parts)
        parts_dictionary = {'parts': parts,
                            'colors': [],
                            'racks': None}
        # TODO add the rack location name and maybe proportion so the pixels can be upscaled to browser size
        parts = json.loads(parts)
        locations = []
        for part in parts:
            for location in part[2].split('/'):
                if location not in locations:
                    locations.append(location)
        for part in locations:
            try:
                a = LEDS.objects.filter(location=part)[0]
            except IndexError:
                print("Part location is not in proper format")
                continue
            a.timeout = datetime.datetime.now() + datetime.timedelta(minutes=15)
            if a.session_keys:
                a.session_keys = request.session.session_key
            else:
                """if request.session.session_key in a.session_keys.split('|'):
                    # extend timeout possibly?
                    pass"""

                a.session_keys = request.session.session_key  # This needs to be when the parts are
                # initially lit
            a.save()
        colors = get_color()  # has to specify if there are any leds that are already a different color
        parts_dictionary['colors'] = colors[0]
        runInjector.inject(parts, colors[1][0])
        print(parts_dictionary)  # format for url
        led_data = []
        for item in colors[0][1]:
            color_data = '-'.join(hex(x)[2:] for x in colors[0][1][item])
            temp = '+'.join([item, color_data])
            led_data.append(temp)
        e = '-'.join(hex(x)[2:] for x in colors[0][0])
        print(led_data)
        led_data = '_'.join(led_data)
        post_response = '|'.join([e, led_data])
        post_response_parts = []
        for i in parts:
            post_response_parts.append(str(i[4]))
        post_response_parts = '+'.join(post_response_parts)
        post_response = '&&'.join([post_response, post_response_parts])
        print(post_response)
        return HttpResponse(post_response)
    elif request.method == "GET":
        map_data = {}
        selected_parts = selected_parts.split('&&')
        parts_to_query = selected_parts[1].split('+')
        selected_parts = selected_parts[0].split('|')
        main_color = selected_parts[0]
        other_colors = selected_parts[1].split('_')
        other_colors_dict = {}
        if other_colors[0]:
            for location in other_colors:
                location = location.split('+')
                location[1] = location[1].split('-')
                for i, val in enumerate(location[1]):
                    location[1][i] = int(val, 16)
                other_colors_dict[location[0]] = location[1]
        main_color = main_color.split('-')
        for i, val in enumerate(main_color):
            main_color[i] = int(val, 16)
        table = []
        for part in parts_to_query:
            row = Racks.objects.filter(id=part)[0]
            if row.id == int(part):
                table.append([row.part_number, row.description, row.location, row.ip, row.id])
        map_data['parts'] = table
        map_data['colors'] = [main_color, other_colors_dict]
        map_data['racks'] = None
        print(map_data)

        return render(request, 'map.html', map_data)
    else:
        return HttpResponse("Error")


def reset_led(request):
    if request.method == "POST":
        led_parts = request.POST.get('parts_string').split('\\')
        for i, part in enumerate(led_parts):
            led_parts[i] = part.split('|')
            led_parts[i][0] = led_parts[i][0].split('/')
        reset_parts = []
        for part in led_parts:
            for location in part[0]:
                a = LEDS.objects.filter(location=location)[0]
                keys = a.session_keys.split('|')
                if not keys:
                    print("Session already timed out or Error has occured")
                    continue
                else:
                    keys.remove(
                        request.session.session_key)  # TODO session key changes with every get request so a new
                    # solution other than session keys must be found
                    # key from
                    # the session keys and this function tries to remove it again
                    if not keys:
                        a.color = "None"
                        a.session_keys = None
                        a.timeout = None
                        a.save()
                        reset_parts.append(part[1])
                    else:
                        a.session_keys = '|'.join(
                            [a.session_keys, request.session.session_key])
                a.save()
        if len(reset_parts) > 0:
            runInjector.reset_led(reset_parts, request.session.session_key)
            pass
        return HttpResponse("Reset LED")
    else:
        return HttpResponse("Unable to reset LED")


def get_color():
    # Some colors appear differently on the neopixel and on the screen, so each color has an led value and regular value
    # colors for the physical led
    led_dict = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'white': (255, 255, 255),
        'yellow': (255, 150, 0),
        'purple': (200, 0, 255),
        'light_blue': (0, 255, 255),
        'orange': (255, 50, 0),
        'mint_green': (0, 255, 50),
        'pink': (255, 75, 125)
    }
    # colors for the map
    color_dict = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'white': (255, 255, 255),
        'yellow': (255, 255, 0),
        'purple': (200, 0, 255),
        'light_blue': (0, 255, 255),
        'orange': (255, 100, 0),
        'mint_green': (80, 245, 170),
        'pink': (255, 75, 125),
        'None': (0, 0, 0)
    }
    # LED_data = LEDS.objects.all()
    # LED_data = serializers.serialize('json', LED_data)
    color = random.choice(list(led_dict))
    colors_in_use = []
    other_colors = {}
    current_leds = query_database("leds")
    for led in current_leds:
        # r, g, b = led[1].split('/')
        r, g, b = color_dict[led[1]]
        # if led[1] != "None":
        if r != 0 or g != 0 or b != 0:
            # location led[0] is color led[1]
            colors_in_use.append([(int(r), int(g), int(b)), led[0]])
            other_colors[led[0]] = (int(r), int(g), int(b))

    while any(led_dict[color] in x for x in colors_in_use):
        color = random.choice(list(led_dict))
    led_val = led_dict[color]
    color_val = color_dict[color]
    # write_to_table()
    return [[color_val, other_colors], [led_val, colors_in_use]]  # colors in use adds part locations associated
    # with each color
