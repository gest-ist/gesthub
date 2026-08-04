home-hero-alt = Banner del GEST
home-description = Grupo de juegos del Instituto Superior Técnico: Game Nights, D&D, torneos, convenciones y comunidad.

home-about-title = Sobre nosotros
home-about-body-1 = Somos un grupo de estudiantes del IST que promueve el convívio através de todo tipo de juegos, desde juegos de tablero y juegos narrativos, a juegos de cartas, videojuegos, y más. Organizamos eventos como las Game Nights, Campañas y One-Shots de TTRPGs, torneos, y otras actividades a lo largo del año. Además de eso, buscamos fomentar uma comunidad acogedora e inclusiva, en la cual todos son bienvenidos a compartir el gusto por los diversos juegos. ¡Únete a nuestra comunidad en Discord y síguenos en Instagram para estar informado de nuestros eventos! Si tienes alguna duda, contactanos por mail o por nuestras redes sociales.
home-discord-invite = ¡Únete a nosotros en Discord para hablar, participar en actividades e interactuar com la comunidad!

home-events-title = Eventos recurrentes
home-gamenights-title = Game Nights
home-gamenights-body =
  ¡Aparece en nuestras Game Nights semanales! Marca en tu calendario la próxima fecha y ven jugar Catan, HEAT: Pedal to the Metal, Cat in the Box, Wavelength y mucho más. No es necessaria inscripción, y puedes traer tu grupo o venir individualmente. Este evento es abierto tanto a veteranos como a principiantes (¡o sin experiencia de todo!).
  Consulta nuestra ludoteca pulsando el botón abajo.
home-game-collection = Colección de juegos
home-oneshots-title = One-Shots de D&D
home-oneshots-body =
  Los eventos de One-Shots de Dungeons & Dragons (D&D) se realizan trimestralmente y se dirigen a jugadores de todos los niveles de experiencia, desde iniciantes curiosos hasta veteranos experientes. Cada sesión es independente, dando a sus participantes una aventura completa sin compromiso a largo plazo. Las inscripciones pueden ser hechas individualmente o en grupo.
home-sign-up = Inscripciones
home-oneshots-closed = Por ahora no hay inscripciones en marcha.

home-calendar-title = Calendario
home-calendar-frame-title = Calendario del GEST
calendar-unavailable = Calendario todavía indisponible. Intenta novamente dentro de momentos.
calendar-previous-month = Mes anterior
calendar-next-month = Mes seguiente
calendar-weekday-mon = Lun
calendar-weekday-tue = Mar
calendar-weekday-wed = Mie
calendar-weekday-thu = Jue
calendar-weekday-fri = Vie
calendar-weekday-sat = Sáb
calendar-weekday-sun = Dom
calendar-view-label = Vista del calendário
calendar-agenda-label = Lista de eventos del mes
calendar-agenda-empty-prefix = Sin eventos en
calendar-origin-link = Ver calendario completo

home-gallery-title = Galería
home-gallery-label = Fotografías de eventos
home-gallery-previous = Fotografías anteriores
home-gallery-next = Fotografías seguientes
home-gallery-close = Cerrar fotografía

home-contact-title = Contactos
home-contact-intro = Habla con nosotros se tienes dudas sobre eventos, la ludoteca, o el grupo.

gestcon-title = GESTCon — Convención de Juegos de Tablero
gestcon-description = Convención de juegos de tablero organizada por el GEST en el Instituto Superior Técnico.
gestcon-hero-alt = Banner de la GESTCon
gestcon-about-body =
  La GESTCon es una convención de Juegos de Tablero organizada por el GEST, un grupo de estudiantes del IST dedicado a los juegos de mesa y a los demás tipos de juegos.
  La primera edición de este evento se realizó el 9, 10 e 11 de Enero de 2026 y fue el primer evento de este estilo en Lisboa desde 2019. Tuvimos centenas de juegos de tablero, clásicos y novedades, jugados entre amigos y familia a lo largo de tres días de convención.
gestcon-gallery-title = Galería
gestcon-ludoteca-left-alt = Ludoteca de la GESTCon
gestcon-ludoteca-right-alt = Ludoteca de la GESTCon
gestcon-ludoteca-caption = ¡Con una ludoteca con más de 300 juegos seleccionados, hubo diversión para todas las edades y niveles de experiencia!
gestcon-root-alt = Juego Root en una mesa de la GESTCon
gestcon-cubitos-alt = Juego Cubitos en una mesa de la GESTCon
gestcon-cubitos-caption = ¡Cubitos!
gestcon-gesticieiro-alt = GESTiceiro en la GESTCon
gestcon-gallery-cta = ¿Buscando más momentos?
gestcon-gallery-button = Ve la galería completa
gestcon-gallery-url = /pt/gestcon/2026/galeria/
gestcon-gallery-page-title = GESTCon — Galeria
gestcon-gallery-description = Fotografías y momentos de la GESTCon 2026.
gestcon-gallery-label = Fotografías de la GESTCon

collection-title = Ludoteca
collection-description = Juegos de tabulero y material de TTRPG disponibles en la ludoteca del GEST.
collection-about =
  ¡Aquí está nuestra ludoteca! Aquí puedes ver todos los juegos y material de TTRPG que tenemos disponibles.
  De momento, tenemos <strong>{ $bg_count }</strong> { collection-about.boardgames }{ collection-about.bg-unavailable } y <strong>{ $rpg_count }</strong> { collection-about.rpg-items }{ collection-about.rpg-unavailable }.
  .boardgames =
    { $bg_count ->
      [one] juego de tablero
     *[other] juegos de tablero
    }
  .rpg-items =
    { $rpg_count ->
      [one] artículo de RPG
     *[other] artículos de RPG
    }
  .bg-unavailable =
    { $bg_unavailable ->
      [0] {""}
     *[other] { $bg_count ->
        [one] { " " }(del cual { $bg_unavailable } { $bg_unavailable ->
          [one] no está disponible
         *[other] no están disponibles
        })
       *[other] { " " }(de los cuales { $bg_unavailable } { $bg_unavailable ->
          [one] no está disponible
         *[other] no están disponibles
        })
      }
    }
  .rpg-unavailable =
    { $rpg_unavailable ->
      [0] {""}
     *[other] { $rpg_count ->
        [one] { " " }(del cual { $rpg_unavailable } { $rpg_unavailable ->
          [one] no está disponible
         *[other] no están disponibles
        })
       *[other] { " " }(de los cuales { $rpg_unavailable } { $rpg_unavailable ->
          [one] no está disponible
         *[other] no están disponibles
        })
      }
    }
collection-boardgames-title = Juegos de tablero
collection-ttrpg-title = Narrativos
collection-empty = Todavía no hay artículos públicos en esta categoría.
collection-modal-close = Cerrar detalles
collection-no-image = Sin imagen
collection-available = Disponible
collection-ceded-to-gest = (cedido al GEST)
collection-unavailable = Indisponible
collection-tags = Etiquetas
collection-year = Año
collection-system = Sistema
collection-weight = Complejidad
collection-rating = Clasificación
collection-players = Jugadores
collection-best-with = (mejor con { $count })
collection-duration = Duración
collection-bgg-link = Ver en el BGG
collection-request-gamenight = Pedir para la próxima Game Night
collection-expansions = Expansiones
