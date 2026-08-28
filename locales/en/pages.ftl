partners-title = Partners
partners-description = GEST partners.
partners-intro = GEST is grateful to the partners who make our activities and initiatives possible. Meet the organizations that support our community and help bring more games and events to IST.
partner-galp-thanks = Sponsor of Board Game Café in 2026 through the CA2EC Prize.
partner-jogonamesa-thanks = Thank you to Jogo na Mesa for supporting
partner-santander-thanks = Sponsor of Board Game Café in 2025 through the CA2EC Prize.
partner-aeist-thanks = Thank you to AEIST, through the P3A programme, for supporting RPGIST and the renovations to GEST's game library.
partner-newborn-games-thanks = Thank you to Newborn Games for supporting RPGIST.
partner-games-omnivorous-thanks = Thank you to Games Omnivorous for supporting RPGIST.

home-hero-alt = GEST banner
home-description = Board game and tabletop group at Instituto Superior Técnico: Game Nights, D&D, tournaments, conventions, and community.

home-about-title = About us
home-about-body-1 = We're a student group at IST passionate about bringing people together through games of all kinds, from board games and role playing games, to card games, video games, and more. We organise events such as Game Nights, TTRPG campaigns and one-shots, tournaments, and other activities. In addition, we strive to foster a welcoming and inclusive community, where everyone is welcome to share their love of games. To keep up with our events, join our community on Discord and follow us on Instagram! If you have any questions, feel free to contact us by email or through our socials.
home-discord-invite = Join us on Discord to chat, participate in activities, and engage with the community!
home-whatsapp-invite = Join our WhatsApp group for event updates and community news!

home-events-title = Recurring events
home-gamenights-title = Game Nights
home-gamenights-body =
  Come hang out at our weekly Game Nights! Mark your calendars for the next date and come play Catan, HEAT: Pedal to the Metal, Cat in the Box, Wavelength, and more. No registration is required, and you can bring your own group or come on your own. The events are open to veterans and beginners alike (even with no experience!).
  Check our collection by clicking on the button below.
home-game-collection = Game collection
home-oneshots-title = D&D One-Shots
home-oneshots-body =
  Dungeons & Dragons (D&D) One-Shot events are held quarterly and are geared toward players of all experience levels, from curious beginners to seasoned veterans. Each session is self-contained, giving participants a complete adventure without a long-term commitment. Registration is available individually or as a group.
home-sign-up = Sign up
home-oneshots-closed = We are not running one-shots at the moment.

home-calendar-title = Calendar
home-calendar-frame-title = GEST calendar
calendar-unavailable = Calendar not yet available. Try again in a few moments.
calendar-previous-month = Previous month
calendar-next-month = Next month
calendar-weekday-mon = Mon
calendar-weekday-tue = Tue
calendar-weekday-wed = Wed
calendar-weekday-thu = Thu
calendar-weekday-fri = Fri
calendar-weekday-sat = Sat
calendar-weekday-sun = Sun
calendar-view-label = Calendar view
calendar-agenda-label = Monthly event list
calendar-agenda-empty-prefix = No events in
calendar-origin-link = View full calendar

home-gallery-title = Gallery
home-gallery-label = Event photos
home-gallery-previous = Previous photos
home-gallery-next = Next photos
home-gallery-close = Close photo

home-contact-title = Contact
home-contact-intro = Reach out if you have questions about events, the game library, or the group.

gestcon-title = GESTCon — Board Game Convention
gestcon-description = Board game convention organized by GEST at Instituto Superior Técnico.
gestcon-hero-alt = GESTCon banner
gestcon-about-body =
  GESTCon is a Board Game convention organized by GEST, a students group of IST dedicated to tabletop games and more.
  The first GESTCon happened on the 9th, 10th and 11th of January 2026 and it was the first event of this type in Lisbon since 2019! We had hundreds of board games, classic and new, played between friends and family over three days.
gestcon-gallery-title = Gallery
gestcon-ludoteca-left-alt = GESTCon game library
gestcon-ludoteca-right-alt = GESTCon game library
gestcon-ludoteca-caption = With a library of over 300 selected games, there was fun for every age and experience level!
gestcon-root-alt = Root being played at GESTCon
gestcon-cubitos-alt = Cubitos being played at GESTCon
gestcon-cubitos-caption = Cubitos!
gestcon-gesticieiro-alt = GESTiceiro at GESTCon
gestcon-gallery-cta = Looking for more moments?
gestcon-gallery-button = View full gallery
gestcon-gallery-url = /en/gestcon/2026/gallery/
gestcon-gallery-page-title = GESTCon — Gallery
gestcon-gallery-description = Photos and moments from GESTCon 2026.
gestcon-gallery-label = GESTCon photos

collection-title = Library
collection-description = Board games and TTRPG material available in GEST's library.
collection-about =
  This is our library! Here you can see all the board games and TTRPG material we have available.
  Right now, we have <strong>{ $bg_count }</strong> { collection-about.boardgames }{ collection-about.bg-unavailable } and <strong>{ $rpg_count }</strong> { collection-about.rpg-items }{ collection-about.rpg-unavailable }.
  .boardgames =
    { $bg_count ->
      [one] board game
     *[other] board games
    }
  .rpg-items =
    { $rpg_count ->
      [one] RPG item
     *[other] RPG items
    }
  .bg-unavailable =
    { $bg_unavailable ->
      [0] {""}
     *[other] { " " }{ $bg_unavailable ->
        [one] ({ $bg_unavailable } of which is unavailable)
       *[other] ({ $bg_unavailable } of which are unavailable)
      }
    }
  .rpg-unavailable =
    { $rpg_unavailable ->
      [0] {""}
     *[other] { " " }{ $rpg_unavailable ->
        [one] ({ $rpg_unavailable } of which is unavailable)
       *[other] ({ $rpg_unavailable } of which are unavailable)
      }
    }
collection-boardgames-title = Board games
collection-ttrpg-title = Tabletop RPGs
collection-empty = There are no public items in this category yet.
collection-modal-close = Close details
collection-no-image = No image
collection-available = Available
collection-ceded-to-gest = (lent to GEST)
collection-unavailable = Unavailable
collection-tags = Tags
collection-year = Year
collection-system = System
collection-weight = Complexity
collection-rating = Rating
collection-players = Players
collection-best-with = (best with { $count })
collection-duration = Duration
collection-bgg-link = View in BGG
collection-request-gamenight = Request for the next Game Night
collection-expansions = Expansions
