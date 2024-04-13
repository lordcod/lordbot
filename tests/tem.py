import orjson

data = [
    {
        "name": "giveaway",
        "category": "major",
        "aliases": [],
        "arguments": [],
        "descriptrion": {'en': 'Opens the menu for creating a giveaway!', 'da': 'Åbner menuen til oprettelse af en gave!', 'de': 'Öffnet das Menü zum Erstellen eines Werbegeschenks!', 'es': '¡Abre el menú para crear un sorteo!', 'fr': 'Ouvre le menu pour créer un cadeau!', 'id': 'Membuka menu untuk membuat hadiah!', 'pl': 'Otwiera menu do tworzenia rozdania!', 'ru': 'Открывает меню для создания раздачи!', 'tr': 'Bir hediye oluşturmak için menüyü açar!'},
        "brief_descriptrion": {'en': 'Opens the menu for creating a giveaway!', 'da': 'Åbner menuen til oprettelse af en gave!', 'de': 'Öffnet das Menü zum Erstellen eines Werbegeschenks!', 'es': '¡Abre el menú para crear un sorteo!', 'fr': 'Ouvre le menu pour créer un cadeau!', 'id': 'Membuka menu untuk membuat hadiah!', 'pl': 'Otwiera menu do tworzenia rozdania!', 'ru': 'Открывает меню для создания раздачи!', 'tr': 'Bir hediye oluşturmak için menüyü açar!'},
        "allowed_disabled": True
    },
    {
        "name": "skip",
        "category": "voice",
        "aliases": [],
        "arguments": [],
        "descriptrion": {'en': 'Stops playing the current song and starts playing the next one.', 'da': 'Stop med at spille den aktuelle sang og begynder at spille den næste.', 'de': 'Hört auf, das aktuelle Lied zu spielen und beginnt das nächste zu spielen.', 'es': 'Deja de tocar la canción actual y comienza a tocar la siguiente.', 'fr': 'Arrête de jouer la chanson actuelle et commence à jouer le suivant.', 'id': 'Berhenti memainkan lagu saat ini dan mulai memainkan yang berikutnya.', 'pl': 'Przestaje odtwarzać obecną piosenkę i zaczyna odtwarzać następną.', 'ru': 'Прекращает играть в текущую песню и начинает играть следующую.', 'tr': 'Mevcut şarkıyı oynamayı durdurur ve bir sonraki şarkıyı çalmaya başlar.'},
        "brief_descriptrion": {'en': 'Stops playing the current song and starts playing the next one.', 'da': 'Stop med at spille den aktuelle sang og begynder at spille den næste.', 'de': 'Hört auf, das aktuelle Lied zu spielen und beginnt das nächste zu spielen.', 'es': 'Deja de tocar la canción actual y comienza a tocar la siguiente.', 'fr': 'Arrête de jouer la chanson actuelle et commence à jouer le suivant.', 'id': 'Berhenti memainkan lagu saat ini dan mulai memainkan yang berikutnya.', 'pl': 'Przestaje odtwarzać obecną piosenkę i zaczyna odtwarzać następną.', 'ru': 'Прекращает играть в текущую песню и начинает играть следующую.', 'tr': 'Mevcut şarkıyı oynamayı durdurur ve bir sonraki şarkıyı çalmaya başlar.'},
        "allowed_disabled": True
    },

    {
        "name": "shop",
        "category": "economy",
        "aliases": [],
        "arguments": [],
        "descriptrion": {'en': 'Opens the Server Role Store', 'da': 'Åbner serverrollebutikken', 'de': 'Öffnet den Serverrollenspeicher', 'es': 'Abre el almacén de roles del servidor', 'fr': 'Ouvre le magasin de rôle du serveur', 'id': 'Membuka Toko Peran Server', 'pl': 'Otwiera sklep z serwerami', 'ru': 'Открывает хранилище ролей сервера', 'tr': 'Sunucu rol mağazasını açar'},
        "brief_descriptrion": {'en': 'Opens the Server Role Store', 'da': 'Åbner serverrollebutikken', 'de': 'Öffnet den Serverrollenspeicher', 'es': 'Abre el almacén de roles del servidor', 'fr': 'Ouvre le magasin de rôle du serveur', 'id': 'Membuka Toko Peran Server', 'pl': 'Otwiera sklep z serwerami', 'ru': 'Открывает хранилище ролей сервера', 'tr': 'Sunucu rol mağazasını açar'},
        "allowed_disabled": True
    },

    {
        "name": "avatar",
        "category": "major",
        "aliases": [],
        "examples": [
            ["avatar @lordcode", {'en': 'It will show the avatar of the participant with the username lordcode', 'da': 'Det viser deltagerens avatar med brugernavnet Lordcode', 'de': 'Es wird den Avatar des Teilnehmers mit dem Benutzernamen Lordcode zeigen', 'es': 'Mostrará el avatar del participante con el nombre de usuario Lordcode',
                                  'fr': "Il montrera l'avatar du participant avec le nom d'utilisateur Lordcode", 'id': 'Itu akan menunjukkan avatar peserta dengan nama pengguna lordcode', 'pl': 'Pokaże awatara uczestnika w lordcode nazwy użytkownika', 'ru': 'Он покажет аватар участника с именем пользователя LordCode', 'tr': 'Lordcode kullanıcı adı ile katılımcının avatarını gösterecek'}],
            ["avatar 636824998123798531", {'en': 'It will show the avatar of the participant with the id 636824998123798531', 'da': 'Det viser deltagerens avatar med ID 636824998123798531', 'de': 'Es wird den Avatar des Teilnehmers mit der ID 636824998123798531 zeigen', 'es': 'Mostrará el avatar del participante con la ID 636824998123798531',
                                           'fr': "Il montrera l'avatar du participant avec l'ID 636824998123798531", 'id': 'Ini akan menunjukkan avatar peserta dengan ID 636824998123798531', 'pl': 'Pokaże awatara uczestnika z ID 636824998123798531', 'ru': 'Он покажет аватар участника с ID 636824998123798531', 'tr': '636824998123798531 ile katılımcının avatarını gösterecek'}]
        ],
        "arguments": [
            {
                "en": "[member]",
                "da": "[medlem]",
                "de": "[Mitglied]",
                "es": "[miembro]",
                "fr": "[membre]",
                "id": "[anggota]",
                "pl": "[członek]",
                "ru": "[участник]",
                "tr": "[üye]"
            }],
        "descriptrion": {'en': "Shows the participant's avatar!", 'da': 'Viser deltagerens avatar!', 'de': 'Zeigt den Avatar des Teilnehmers!', 'es': '¡Muestra el avatar del participante!', 'fr': "Montre l'avatar du participant!", 'id': 'Menunjukkan avatar peserta!', 'pl': 'Pokazuje awatar uczestnika!', 'ru': 'Показывает аватар участника!', 'tr': 'Katılımcının avatarını gösterir!'},
        "brief_descriptrion": {'en': "Shows the participant's avatar!", 'da': 'Viser deltagerens avatar!', 'de': 'Zeigt den Avatar des Teilnehmers!', 'es': '¡Muestra el avatar del participante!', 'fr': "Montre l'avatar du participant!", 'id': 'Menunjukkan avatar peserta!', 'pl': 'Pokazuje awatar uczestnika!', 'ru': 'Показывает аватар участника!', 'tr': 'Katılımcının avatarını gösterir!'},
        "allowed_disabled": True
    },
    {
        "name": "invites",
        "category": "major",
        "aliases": [],
        "examples": [
            ["invites", {'en': 'Shows the latest invitations from the entire server', 'da': 'Viser de nyeste invitationer fra hele serveren', 'de': 'Zeigt die neuesten Einladungen vom gesamten Server an', 'es': 'Muestra las últimas invitaciones de todo el servidor',
                         'fr': "Affiche les dernières invitations de l'ensemble du serveur", 'id': 'Menunjukkan undangan terbaru dari seluruh server', 'pl': 'Pokazuje najnowsze zaproszenia z całego serwera', 'ru': 'Показывает последние приглашения с всего сервера', 'tr': 'Tüm sunucudan en son davetiyeleri gösterir'}],
            ["invites @lordcode", {'en': 'It will show the latest invitations of the participant with the nickname @lordcode', 'da': 'Det viser de seneste invitationer fra deltageren med kaldenavnet @lordcode', 'de': 'Es wird die neuesten Einladungen des Teilnehmers mit dem Spitznamen @lordcode zeigen', 'es': 'Mostrará las últimas invitaciones del participante con el apodo @lordcode',
                                   'fr': 'Il montrera les dernières invitations du participant avec le surnom @lordcode', 'id': 'Ini akan menunjukkan undangan terbaru dari peserta dengan nama panggilan @lordcode', 'pl': 'Pokaże najnowsze zaproszenia uczestnika z pseudonimem @LordCode', 'ru': 'Он покажет последние приглашения участника с прозвищем @lordcode', 'tr': '@Lordcode takma adıyla katılımcının en son davetlerini gösterecek'}],
            ["invites 636824998123798531", {'en': 'It will show the latest invitations of the participant with the id 636824998123798531', 'da': 'Det viser de seneste invitationer af deltageren med ID 636824998123798531', 'de': 'Es wird die neuesten Einladungen des Teilnehmers mit der ID 636824998123798531 zeigen', 'es': 'Mostrará las últimas invitaciones del participante con la ID 636824998123798531',
                                            'fr': "Il montrera les dernières invitations du participant avec l'ID 636824998123798531", 'id': 'Ini akan menunjukkan undangan terbaru dari peserta dengan ID 636824998123798531', 'pl': 'Pokazuje najnowsze zaproszenia uczestnika z ID 636824998123798531', 'ru': 'Он покажет последние приглашения участника с ID 636824998123798531', 'tr': '636824998123798531 ile katılımcının en son davetlerini gösterecektir.'}]
        ],
        "arguments": [
            {
                "en": "[member]",
                "da": "[medlem]",
                "de": "[Mitglied]",
                "es": "[miembro]",
                "fr": "[membre]",
                "id": "[anggota]",
                "pl": "[członek]",
                "ru": "[участник]",
                "tr": "[üye]"
            }],
        "descriptrion": {'en': "Shows the participant's avatar!", 'da': 'Viser deltagerens avatar!', 'de': 'Zeigt den Avatar des Teilnehmers!', 'es': '¡Muestra el avatar del participante!', 'fr': "Montre l'avatar du participant!", 'id': 'Menunjukkan avatar peserta!', 'pl': 'Pokazuje awatar uczestnika!', 'ru': 'Показывает аватар участника!', 'tr': 'Katılımcının avatarını gösterir!'},
        "brief_descriptrion": {'en': "Shows the participant's avatar!", 'da': 'Viser deltagerens avatar!', 'de': 'Zeigt den Avatar des Teilnehmers!', 'es': '¡Muestra el avatar del participante!', 'fr': "Montre l'avatar du participant!", 'id': 'Menunjukkan avatar peserta!', 'pl': 'Pokazuje awatar uczestnika!', 'ru': 'Показывает аватар участника!', 'tr': 'Katılımcının avatarını gösterir!'},
        "allowed_disabled": True
    },
    {
        "name": "move",
        "category": "voice",
        "aliases": [],
        "arguments": [{'en': '<index>', 'da': '<indeks>', 'de': '<Index>', 'es': '<índice>', 'fr': '<indice>', 'id': '<indeks>', 'pl': '<indeks>', 'ru': '<индекс>', 'tr': '<indeks>'}],
        "examples": [
            ["move 5", {'en': 'Will start producing 5 tracks in the queue', 'da': 'Begynder at producere 5 numre i køen', 'de': 'Werde 5 Tracks in der Warteschlange produzieren', 'es': 'Comenzará a producir 5 pistas en la cola',
                        'fr': "Commencera à produire 5 pistes dans la file d'attente", 'id': 'Akan mulai memproduksi 5 trek dalam antrian', 'pl': 'Zacznie produkować 5 utworów w kolejce', 'ru': 'Начнет производить 5 треков в очереди', 'tr': 'Kuyrukta 5 parça üretmeye başlayacak'}]
        ],
        "descriptrion": {'en': 'Will switch to the track in the queue', 'da': 'Skifter til banen i køen', 'de': 'Wechselt zur Spur in der Warteschlange', 'es': 'Cambiará a la pista en la cola', 'fr': "Passera à la piste dans la file d'attente", 'id': 'Akan beralih ke trek di antrian', 'pl': 'Przełączy się na tor w kolejce', 'ru': 'Переключится на дорожку в очереди', 'tr': 'Kuyrukta piste geçecek'},
        "brief_descriptrion": {'en': 'Will switch to the track in the queue', 'da': 'Skifter til banen i køen', 'de': 'Wechselt zur Spur in der Warteschlange', 'es': 'Cambiará a la pista en la cola', 'fr': "Passera à la piste dans la file d'attente", 'id': 'Akan beralih ke trek di antrian', 'pl': 'Przełączy się na tor w kolejce', 'ru': 'Переключится на дорожку в очереди', 'tr': 'Kuyrukta piste geçecek'},
        "allowed_disabled": True
    },

    {
        "name": "reminder",
        "category": "major",
        "aliases": [],
        "arguments": [{'en': '<time>', 'da': '<tid>', 'de': '<Time>', 'es': '<Time>', 'fr': '<Time>', 'id': '<lima>', 'pl': '<czasu>', 'ru': '<время>', 'tr': '<Time>'}, {'en': '<text>', 'da': '<tekst>', 'de': '<text>', 'es': '<Exto>', 'fr': '<Text>', 'id': '<text>', 'pl': '<ext>', 'ru': '<Текст>', 'tr': '<Text>'}],
        "examples": [
            ["reminder 14d daily reward", {'en': 'To remind you after 14 days about the daily reward', 'da': 'At minde dig efter 14 dage om den daglige belønning', 'de': 'Um Sie nach 14 Tagen an die tägliche Belohnung zu erinnern', 'es': 'Para recordarle después de 14 días sobre la recompensa diaria',
                                           'fr': 'Pour vous rappeler après 14 jours la récompense quotidienne', 'id': 'Untuk mengingatkan Anda setelah 14 hari tentang hadiah harian', 'pl': 'Przypomnij ci po 14 dniach o codziennej nagrody', 'ru': 'Чтобы напомнить вам после 14 дней о ежедневной награде', 'tr': '14 gün sonra günlük ödül hakkında hatırlatmak için'}]
        ],
        "descriptrion": {'en': 'It reminds you of the specified text at a certain time', 'da': 'Det minder dig om den specificerede tekst på et bestemt tidspunkt', 'de': 'Es erinnert Sie zu einem bestimmten Zeitpunkt an den angegebenen Text', 'es': 'Le recuerda el texto especificado en un momento determinado', 'fr': 'Il vous rappelle le texte spécifié à un certain moment', 'id': 'Itu mengingatkan Anda pada teks yang ditentukan pada waktu tertentu', 'pl': 'Przypomina ci określony tekst w określonym czasie', 'ru': 'Это напоминает вам указанный текст в определенное время', 'tr': 'Belirli bir zamanda belirtilen metni hatırlatır'},
        "brief_descriptrion": {'en': 'It reminds you of the specified text at a certain time', 'da': 'Det minder dig om den specificerede tekst på et bestemt tidspunkt', 'de': 'Es erinnert Sie zu einem bestimmten Zeitpunkt an den angegebenen Text', 'es': 'Le recuerda el texto especificado en un momento determinado', 'fr': 'Il vous rappelle le texte spécifié à un certain moment', 'id': 'Itu mengingatkan Anda pada teks yang ditentukan pada waktu tertentu', 'pl': 'Przypomina ci określony tekst w określonym czasie', 'ru': 'Это напоминает вам указанный текст в определенное время', 'tr': 'Belirli bir zamanda belirtilen metni hatırlatır'},
        "allowed_disabled": True
    }
]
print(orjson.dumps(data).decode())
