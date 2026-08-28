partners-title = Parceiros
partners-description = Parceiros do GEST.
partners-intro = O GEST agradece aos parceiros que tornam possível a realização das nossas atividades e iniciativas. Conhece as entidades que apoiam a nossa comunidade e ajudam a levar mais jogos e eventos ao IST.
partner-galp-thanks = Patrocinador do Board Game Café em 2026 através do Prémio CA2EC.
partner-jogonamesa-thanks = Obrigado ao Jogo na Mesa pelo apoio para a
partner-santander-thanks = Patrocinador do Board Game Café em 2025 através do Prémio CA2EC.
partner-aeist-thanks = Obrigado à AEIST pelo apoio através do programa P3A para a realização do RPGIST e as renovações da ludoteca do GEST.
partner-newborn-games-thanks = Obrigado à Newborn Games pelo apoio para a realização do RPGIST.
partner-games-omnivorous-thanks = Obrigado à Games Omnivorous pelo apoio para a realização do RPGIST.

home-hero-alt = Banner do GEST
home-description = Grupo de jogos do Instituto Superior Técnico: Game Nights, D&D, torneios, convenções e comunidade.

home-about-title = Sobre nós
home-about-body-1 = Somos um grupo de estudantes do IST que promove o convívio através de todo o tipo de jogos, desde jogos de tabuleiro e jogos narrativos, a jogos de cartas, videojogos, e mais. Organizamos eventos como as Game Nights, Campanhas e One-Shots de TTRPGs, torneios, e outras atividades ao longo do ano. Para além disso, procuramos cultivar uma comunidade acolhedora e inclusiva, na qual todos são bem-vindos a partilhar o gosto pelos diversos jogos. Junta-te à nossa comunidade no Discord e segue-nos no Instagram para estares a par dos nossos eventos! Se tiveres alguma dúvida, contacta-nos por mail ou pelas nossas redes sociais.
home-discord-invite = Junta-te a nós no Discord para conversar, participar em actividades e interagir com a comunidade!
home-whatsapp-invite = Junta-te ao nosso grupo de WhatsApp para receber novidades sobre eventos e sobre a comunidade!

home-events-title = Eventos recorrentes
home-gamenights-title = Game Nights
home-gamenights-body =
  Aparece nas nossas Game Nights semanais! Marca no calendário a próxima data e vem jogar Catan, HEAT: Pedal to the Metal, Cat in the Box, Wavelength e muito mais. Não é necessária inscrição, e podes trazer o teu grupo ou vir individualmente. Este evento é aberto tanto a veteranos como a principiantes (ou sem experiência nenhuma!).
  Consulta a nossa ludoteca carregando no botão abaixo.
home-game-collection = Colecção de jogos
home-oneshots-title = One-Shots de D&D
home-oneshots-body =
  Os eventos de One-Shots de Dungeons & Dragons (D&D) realizam-se trimestralmente e dirigem-se a jogadores de todos os níveis de experiência, desde iniciantes curiosos até veteranos experientes. Cada sessão é independente, dando aos participantes uma aventura completa sem compromisso a longo prazo. As inscrições podem ser feitas individualmente ou em grupo.
home-sign-up = Inscrições
home-oneshots-closed = De momento não temos inscrições a decorrer.

home-calendar-title = Calendário
home-calendar-frame-title = Calendário do GEST
calendar-unavailable = Calendário ainda indisponível. Tenta novamente dentro de momentos.
calendar-previous-month = Mês anterior
calendar-next-month = Mês seguinte
calendar-weekday-mon = Seg
calendar-weekday-tue = Ter
calendar-weekday-wed = Qua
calendar-weekday-thu = Qui
calendar-weekday-fri = Sex
calendar-weekday-sat = Sáb
calendar-weekday-sun = Dom
calendar-view-label = Vista do calendário
calendar-agenda-label = Lista de eventos do mês
calendar-agenda-empty-prefix = Sem eventos em
calendar-origin-link = Ver calendário completo

home-gallery-title = Galeria
home-gallery-label = Fotografias de eventos
home-gallery-previous = Fotografias anteriores
home-gallery-next = Fotografias seguintes
home-gallery-close = Fechar fotografia

home-contact-title = Contacto
home-contact-intro = Fala connosco se tiveres dúvidas sobre eventos, a ludoteca, ou o grupo.

gestcon-title = GESTCon — Convenção de Jogos de Tabuleiro
gestcon-description = Convenção de jogos de tabuleiro organizada pelo GEST no Instituto Superior Técnico.
gestcon-hero-alt = Banner da GESTCon
gestcon-about-body =
  A GESTCon é uma convenção de Jogos de Tabuleiro organizada pelo GEST, um grupo de estudantes do IST dedicado aos jogos de mesa e aos demais tipos de jogos.
  A primeira edição deste evento realizou-se a 9, 10 e 11 de Janeiro de 2026 e foi o primeiro evento deste tipo em Lisboa desde 2019! Tivemos centenas de jogos de tabuleiro, clássicos e novidades, jogados entre amigos e família ao longo de três dias de convenção!
gestcon-gallery-title = Galeria
gestcon-ludoteca-left-alt = Ludoteca da GESTCon
gestcon-ludoteca-right-alt = Ludoteca da GESTCon
gestcon-ludoteca-caption = Com uma ludoteca com mais de 300 jogos selecionados, houve diversão para todas as idades e níveis de experiência!
gestcon-root-alt = Jogo Root numa mesa da GESTCon
gestcon-cubitos-alt = Jogo Cubitos numa mesa da GESTCon
gestcon-cubitos-caption = Cubitos!
gestcon-gesticieiro-alt = GESTiceiro na GESTCon
gestcon-gallery-cta = À procura de mais momentos?
gestcon-gallery-button = Vê a galeria completa
gestcon-gallery-url = /pt/gestcon/2026/galeria/
gestcon-gallery-page-title = GESTCon — Galeria
gestcon-gallery-description = Fotografias e momentos da GESTCon 2026.
gestcon-gallery-label = Fotografias da GESTCon

collection-title = Ludoteca
collection-description = Jogos de tabuleiro e material de TTRPG disponíveis na ludoteca do GEST.
collection-about =
  Eis a nossa ludoteca! Aqui podes ver todos os jogos e material de TTRPG que temos disponíveis.
  De momento, temos <strong>{ $bg_count }</strong> { collection-about.boardgames }{ collection-about.bg-unavailable } e <strong>{ $rpg_count }</strong> { collection-about.rpg-items }{ collection-about.rpg-unavailable }.
  .boardgames =
    { $bg_count ->
      [one] jogo de tabuleiro
     *[other] jogos de tabuleiro
    }
  .rpg-items =
    { $rpg_count ->
      [one] item de RPG
     *[other] itens de RPG
    }
  .bg-unavailable =
    { $bg_unavailable ->
      [0] {""}
     *[other] { $bg_count ->
        [one] { " " }(do qual { $bg_unavailable } { $bg_unavailable ->
          [one] não está disponível
         *[other] não estão disponíveis
        })
       *[other] { " " }(dos quais { $bg_unavailable } { $bg_unavailable ->
          [one] não está disponível
         *[other] não estão disponíveis
        })
      }
    }
  .rpg-unavailable =
    { $rpg_unavailable ->
      [0] {""}
     *[other] { $rpg_count ->
        [one] { " " }(do qual { $rpg_unavailable } { $rpg_unavailable ->
          [one] não está disponível
         *[other] não estão disponíveis
        })
       *[other] { " " }(dos quais { $rpg_unavailable } { $rpg_unavailable ->
          [one] não está disponível
         *[other] não estão disponíveis
        })
      }
    }
collection-boardgames-title = Jogos de tabuleiro
collection-ttrpg-title = Narrativos
collection-empty = Ainda não há itens públicos nesta categoria.
collection-modal-close = Fechar detalhes
collection-no-image = Sem imagem
collection-available = Disponível
collection-ceded-to-gest = (cedido ao GEST)
collection-unavailable = Indisponível
collection-tags = Etiquetas
collection-year = Ano
collection-system = Sistema
collection-weight = Complexidade
collection-rating = Classificação
collection-players = Jogadores
collection-best-with = (melhor a { $count })
collection-duration = Duração
collection-bgg-link = Ver no BGG
collection-request-gamenight = Pedir para a próxima Game Night
collection-expansions = Expansões
