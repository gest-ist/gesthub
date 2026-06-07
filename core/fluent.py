from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from django.conf import settings
from django.templatetags.static import static
from django.urls import path, reverse
from django.urls.resolvers import ResolverMatch, URLPattern
from django.utils import translation
from django_ftl.bundles import Bundle, MessageFinderBase
from django_ftl.templatetags import ftl

RouteMap = Mapping[str, tuple[Callable[..., Any], Mapping[str, str]]]

_route_names: set[str] = set()


class RootLocaleFinder(MessageFinderBase):
    @property
    def locale_base_dirs(self) -> list[str]:
        return [str(settings.BASE_DIR / "locales")]


bundle = Bundle(["core.ftl", "pages.ftl"], finder=RootLocaleFinder())


def language_codes() -> tuple[str, ...]:
    return tuple(code for code, _label in settings.LANGUAGES)


def normalize_slug(slug: str) -> str:
    if slug.startswith("/"):
        raise ValueError(f"Localized route slug must be relative, got {slug!r}")

    normalized = slug.strip("/")
    return f"{normalized}/" if normalized else ""


def route_pattern_name(language: str, route_name: str) -> str:
    return f"{language}-{route_name}"


def localized_patterns(routes: RouteMap) -> list[URLPattern]:
    languages = language_codes()
    patterns = []
    seen: set[tuple[str, str]] = set()

    for name, (view, slugs) in routes.items():
        _route_names.add(name)
        missing_languages = set(languages) - set(slugs)
        if missing_languages:
            missing = ", ".join(sorted(missing_languages))
            raise ValueError(f"Localized route {name!r} is missing slugs for: {missing}")

        for language in languages:
            slug = normalize_slug(slugs[language])
            key = (language, slug)
            if key in seen:
                raise ValueError(f"Duplicate localized route slug for {language!r}: {slug!r}")

            seen.add(key)
            patterns.append(
                path(
                    f"{language}/{slug}",
                    view,
                    name=route_pattern_name(language, name),
                )
            )

    return patterns


def route_url(route_name: str, language: str) -> str:
    return reverse(route_pattern_name(language, route_name))


def route_urls(route_name: str) -> dict[str, str]:
    return {language: route_url(route_name, language) for language in language_codes()}


def route_name_from_match(match: ResolverMatch | None) -> str | None:
    if match is None or match.url_name is None:
        return None

    for language in language_codes():
        prefix = f"{language}-"
        if match.url_name.startswith(prefix):
            route_name = match.url_name.removeprefix(prefix)
            if route_name in _route_names:
                return route_name

    return None


class PathLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = self.language_from_path(request.path_info)
        request.LANGUAGE_CODE = language

        with translation.override(language):
            response = self.get_response(request)

        response.headers.setdefault("Content-Language", language)
        return response

    @staticmethod
    def language_from_path(path_info: str) -> str:
        supported_languages = set(language_codes())
        first_segment = path_info.strip("/").split("/", 1)[0]

        if first_segment in supported_languages:
            return first_segment
        return settings.LANGUAGE_CODE


def context(request):
    language = request.LANGUAGE_CODE
    current_route = route_name_from_match(request.resolver_match)
    discord_url = request.build_absolute_uri("/discord")

    language_links = {}
    if current_route is not None:
        language_links = route_urls(current_route)

    return {
        ftl.BUNDLE_VAR_NAME: bundle,
        ftl.MODE_VAR_NAME: "server",
        "current_language": language,
        "current_url": request.build_absolute_uri(),
        "language_links": language_links,
        "social_images": {
            "default": request.build_absolute_uri(static("img/banner.webp")),
            "gestcon": request.build_absolute_uri(static("img/gestcon/2026/banner.webp")),
        },
        "site_urls": {
            "discord": discord_url,
        },
        "site_url_labels": {
            "discord": discord_url.removeprefix("https://").removeprefix("http://"),
        },
        "localized_urls": {
            "home": route_url("home", language),
            "collection": route_url("collection", language),
            "gestcon": route_url("gestcon", language),
            "gestcon_gallery": route_url("gestcon_gallery", language),
        },
    }
