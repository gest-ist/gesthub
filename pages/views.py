from __future__ import annotations

from django.shortcuts import render

from .gallery import load_gallery


def home(request):
    return render(
        request,
        "pages/home.html",
        {
            "home_gallery": load_gallery("home"),
        },
    )


def gestcon_gallery(request):
    return render(
        request,
        "pages/gestcon_gallery.html",
        {
            "gallery": load_gallery("gestcon/2026"),
        },
    )
