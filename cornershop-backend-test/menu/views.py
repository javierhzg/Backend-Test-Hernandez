import datetime

from django.shortcuts import render
from django import forms

from menu.models import Menu
from menu.models import Options
from menu.models import Selections

import logging
from slack_sdk import WebClient
from slack.errors import SlackApiError


class NewMenuForm(forms.Form):
    date = forms.DateField(widget=forms.TextInput(attrs={
                                    'class': 'datepicker'
                                }))


class NewOptionForm(forms.Form):
    option = forms.CharField()


class NewSelectForm(forms.Form):
    notes = forms.CharField(required=False)
    name = forms.CharField()


# Create your views here.
def menu(request, *args, **kwargs):
    if request.method == "POST":
        form = NewMenuForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            if len(Menu.objects.filter(date=date)) == 0:
                save_record = Menu()
                save_record.date = date
                save_record.save()
    menus = Menu.objects.order_by("date")
    return render(request, "utils/menus.html", {
        "form": NewMenuForm(),
        "menus": menus})


def options(request,  menu_id, **kwargs):
    current_menu = Menu.objects.get(id=menu_id)
    if request.method == "POST":
        form = NewOptionForm(request.POST)
        if form.is_valid():
            save_record = Options()
            save_record.menu = current_menu
            save_record.option = form.cleaned_data["option"]
            save_record.save()
    options_menu = Options.objects.filter(menu_id=menu_id)
    return render(request, "utils/options.html", {
        "form": NewOptionForm(),
        "menu": current_menu,
        "options": options_menu})


def options_delete(request, option_id, *args, **kwargs):
    option = Options.objects.get(id=option_id)
    if request.method == "POST":
        Options.objects.filter(id=option.id).delete()
    options_menu = Options.objects.filter(menu_id=option.menu.id)
    current_menu = Menu.objects.get(id=option.menu.id)
    return render(request, "utils/options.html", {
        "form": NewOptionForm(),
        "menu": current_menu,
        "options": options_menu})


def send(request, menu_id, *args, **kwargs):
    logging.basicConfig(level=logging.DEBUG)
    slack_token = "xoxp-2175961718450-2199764598320-2169213016150-41bcc9bf22993599ea3d9cfa948af0d5"
    client = WebClient(token=slack_token)

    try:
        response = client.chat_postMessage(
            channel="@zt5ph57wsh",
            text="Hello! I share with you today's menu :) http://localhost:8000/select/" + str(menu_id)
        )
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'

    menus = Menu.objects.order_by("date")
    return render(request, "utils/menus.html", {
        "form": NewMenuForm(),
        "menus": menus})


def select(request, menu_id, *args, **kwargs):
    current_menu = Menu.objects.get(id=menu_id)
    options_menu = Options.objects.filter(menu_id=menu_id)
    if request.method == "POST":
        date_time_limit = datetime.datetime.combine(current_menu.date, datetime.datetime.min.time())
        date_time_limit = date_time_limit + datetime.timedelta(hours=11)
        if datetime.datetime.now() > date_time_limit:
            return render(request, "utils/confirmation.html", {
                "done": False})
        form = NewSelectForm(request.POST)
        if form.is_valid():
            option_id = request.POST['option_id']
            option = Options.objects.get(id=option_id)
            save_record = Selections()
            save_record.option = option
            save_record.name = form.cleaned_data["name"]
            save_record.notes = form.cleaned_data["notes"]
            save_record.save()
            menus = Menu.objects.order_by("date")
            return render(request, "utils/confirmation.html", {
                "done": True})
    return render(request, "utils/select.html", {
        "form": NewSelectForm(),
        "menu": current_menu,
        "options": options_menu})
