from django.shortcuts import render, redirect, get_object_or_404
def home(req):
    return redirect('/api/docs')