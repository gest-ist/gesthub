> :warning: Unorganized ramble!

# Main website + game library + GESTCon platform refactor

This is our website's source, all of it.
It is currently in a weird state of being mid-migration to a static website generator (Zola), which
we have decided to stop and pivot to something else instead.
Much of this was done in a rush the week before the Con started, before we had access to any server
infrastructure.
We now have access to a Debian Trixie VPS and a managed Postgres instance.
We thus want to rewrite the website in basically its entirety. From scratch.
We want to have the flexibility of a backend for our current and possibly future needs.

## Preliminary context

We are a small student association within a public university, focused on board, table-top,
trading-card, and video games, with greater emphasis on the first two. We see members come and go
pretty much every year, and we come from all sorts of fields. A few of us come from Computer Science
/ Software Engineering, but the vast majority comes from Physics, Maths, Electrical Engineering, etc.
Thus it is quite imperative that our systems are implemented in well known languages and stacks, so
that contributing and maintaining it is simple enough for pretty much everyone. We want to minimize
moving parts, we want to simplify deployment and maintenance duties. We want to not have to rely on
CS/SE students and risk a low "bus factor".

## What we want

Here's a summary of the pages/platforms we need.

### Landing + events + contact + gallery page(s)

One or more pages of mostly static content introducing the group, who we are, what we do, etc.
There should be a section about our recurring events (gamenights and D&D one-shots). There should
also be a calendar view of all our planned events.
There should also be a page/section for our contact information, socials (Instagram, Discord,
Whatsapp, etc) and another one with some selection of pictures from our events and inventory.

### Game library / inventory management

We own a growing collection of boardgames and TTRPG material (books, figures, accessories, etc).
We've been managing it by hand, but we're looking into having a better organized system for this.
Such a system would help us track which items we have in our inventory, who owns them (the group
itself owns most, but we have several lent by members and outsiders), if they're available or taken
(and who currently has them). It would also implement a system for registering/removing/updating
items manually, a system for allowed group members to register a take out and return, and more.
We'd also like to have some integration with our recurring events, namely the weekly gamenights; we
should be able to get requests for specific games to be taken to the gamenight (we never take our
full inventory), as well as being able to mark specific games as being taken on the actual day (so
people can know which games will be available and maybe make last requests).
Inventory items should be categorizable and either private (viewable only to members) or public.
Items should have relevant metadata and links when applicable (eg pulled from BGG in the case of
boardgames). The inventory should be easily searchable, and have category-specific filters (eg BGG
complexity for boardgames) and sorts. Items should also have an associated location, so we can
physically find them with ease.

### Boardgame convention management

We've already held one edition of our boardgame convention (GESTCon) and will be holding another one
early next year. This requires some inventory management similar to our day-to-day library described
in the previous section, with some extra features on top:

- "frontdesk staff" accounts (simple and quick to set up for one-off collaborators helping us out)
  - these are the people welcoming attendees and taking care of game checkouts/returns, both digitally and physically
- streamlined interface for frontdesk staff to register new participants and log checkouts/returns
- live updating game availability, with a queue/reminder system
- and more

The convention is free so ticket management is out of scope for now.

## Decisions

With all this in mind, we have decided on the following:

- Python (well typed) + uv + ruff + ty
- Postgres
- Docker + Compose
- Caddy
- Django (+ pushpin once we need SSE)

Not concrete choices, but requirements:

- Solid i18n from day one (including URL slugs), using path style (eg domain/pt/eventos - domain/en/events)

### Deployment

The backend should be packaged as a Docker image, and Caddy should use an image based on the
official Alpine images and bundling the app's core static assets (CSS, JS, fonts, icons, etc). Both
should be orchestrated through Docker Compose. There should be a volume for larger runtime media
that is not checked into the repo (eg inventory images/thumbnails). Caddy should serve all these
static contents directly, and reverse proxy everything else to the app container. The app container
should not expose anything to the outside except through Caddy. Caddy should serve a simple page in
case of proxy errors (saying something like "The website is being updated" if the app isn't
reachable); these pages should be bundled in its image as well.

Nothing is done automatically by the CI. GitHub CI, Packages and Container Registry have low limits
for free orgs, which will hit us sooner or later. Giving SSH access to a CI is also something to be
very careful with. To avoid more complicated secret management, we instead manage deployments
entirely on our server, through a simple and easy to use Python script. This script requires
authorized SSH credentials and will do all the necessary steps to get the latest commit on `main`
deployed, with interactivity to prevent accidental runs. Roughly, it will `git pull` on the server,
then `docker compose build`, then `docker compose up -d`. This is perhaps slightly less magical than
a fully automated blue/green CI/CD deployment, but we think that's a good thing, considering our
org's characteristics.

## Implementing this

We don't need to do all of this in one go. We should start by getting a basic Django app working,
then port the main static(ish) pages, then start implementing the library/inventory management
system on top of it, then work on deployment, then test and improve it, then extend it with the
convention pages and features.
