from django.shortcuts import render, redirect
from django import forms
from . import util
from markdown2 import Markdown
import random
markdowner = Markdown()

#class for form to edit page
class EditPageForm(forms.Form):
    text = forms.CharField(label="Content", widget=forms.Textarea(attrs={'rows':1, 'col':1}))

#class for form to create new page
class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'size': 80}))
    text = forms.CharField(label="Content", widget=forms.Textarea(attrs={'rows':1, 'col':1}))

#main page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#wiki entry pages
def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "entry": markdowner.convert(util.get_entry(title)),
        "editurl" : "/wiki/" + title + "/edit"
    })

#function to send to a new page
def rng(request):
    entries = util.list_entries()
    selected = random.choice(entries)
    return entry(request, selected)

#add a new page
def add(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            for entry in util.list_entries():
                if entry == title:
                    return render(request, "encyclopedia/error.html")
            text = form.cleaned_data["text"]
            util.save_entry(title, text)
            return redirect(title + '/')
        else:
            return render(request, "encyclopedia/add.html", {
                "form" : form
            })

    return render(request, "encyclopedia/add.html", {
        "form": NewPageForm()
    })

#edit a page entry
def edit(request, title):

    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            util.save_entry(title, text)
            return redirect("/wiki/" + title, {
                "entry": markdowner.convert(util.get_entry(title)),
                "editurl" : "/wiki/" + title + "/edit"
            })
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form,
            "editurl" : "/wiki/" + title + "/edit"
            })
    else:
        form = EditPageForm(initial={"text":util.get_entry(title)})
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "editurl" : "/wiki/" + title + "/edit"
        })

def get_query(request):

    queryset = []
    q = request.GET.get('q', '')

    pages = util.list_entries()

    for page in pages:
        if page == q:
            return redirect("/wiki/" + page, {
                "entry": markdowner.convert(util.get_entry(page)),
                "editurl" : "/wiki/" + page + "/edit"
            })
        elif page.find(q) != -1:
            queryset.append(page)

    return render(request, "encyclopedia/searchresults.html", {
        "query": q,
        "queryset": queryset,
    })
