data = [
    {"discord_language": "id", "google_language": "id",
        "english_name": "Indonesian", "native_name": "Bahasa Indonesia", "flag": "🇮🇩"},
    {"discord_language": "da", "google_language": "da",
        "english_name": "Danish", "native_name": "Dansk", "flag": "🇩🇰"},
    {"discord_language": "de", "google_language": "de",
        "english_name": "German", "native_name": "Deutsch", "flag": "🇩🇪"},
    {"discord_language": "en-GB", "google_language": "en",
        "english_name": "English, UK", "native_name": "English, UK", "flag": "🇬🇧"},
    {"discord_language": "es-ES", "google_language": "es",
        "english_name": "Spanish", "native_name": "Español", "flag": "🇪🇸"},
    {"discord_language": "fr", "google_language": "fr",
        "english_name": "French", "native_name": "Français", "flag": "🇫🇷"},
    {"discord_language": "hr", "google_language": "hr",
        "english_name": "Croatian", "native_name": "Hrvatski", "flag": "🇭🇷"},
    {"discord_language": "it", "google_language": "it",
        "english_name": "Italian", "native_name": "Italiano", "flag": "🇮🇹"},
    {"discord_language": "hu", "google_language": "hu",
        "english_name": "Hungarian", "native_name": "Magyar", "flag": "🇭🇺"},
    {"discord_language": "nl", "google_language": "nl",
        "english_name": "Dutch", "native_name": "Nederlands", "flag": "🇳🇱"},
    {"discord_language": "pl", "google_language": "pl",
        "english_name": "Polish", "native_name": "Polski", "flag": "🇵🇱"},
    {"discord_language": "pt-BR", "google_language": "pt",
        "english_name": "Portuguese, Brazilian", "native_name": "Português do Brasil", "flag": "🇵🇹"},
    {"discord_language": "ro", "google_language": "ro",
        "english_name": "Romanian, Romania", "native_name": "Română", "flag": "🇷🇴"},
    {"discord_language": "fi", "google_language": "fi",
        "english_name": "Finnish", "native_name": " Suomi", "flag": "🇫🇮"},
    {"discord_language": "sv-SE", "google_language": "sv",
        "english_name": "Swedish", "native_name": "Svenska", "flag": "🇸🇻"},
    {"discord_language": "vi", "google_language": "vi",
        "english_name": "Vietnamese", "native_name": "Tiếng Việt", "flag": "🇻🇮"},
    {"discord_language": "tr", "google_language": "tr",
        "english_name": "Turkish", "native_name": "Türkçe", "flag": "🇹🇷"},
    {"discord_language": "cs", "google_language": "cs",
        "english_name": "Czech", "native_name": "Čeština", "flag": "🇨🇿"},
    {"discord_language": "el", "google_language": "el",
        "english_name": "Greek", "native_name": "Ελληνικά", "flag": "🇬🇷"},
    {"discord_language": "bg", "google_language": "bg",
        "english_name": "Bulgarian", "native_name": "български", "flag": "🇧🇬"},
    {"discord_language": "ru", "google_language": "ru",
        "english_name": "Russian", "native_name": "Pусский", "flag": "🇷🇺"},
    {"discord_language": "uk", "google_language": "uk",
        "english_name": "Ukrainian", "native_name": "Українська", "flag": "🇺🇦"},
    {"discord_language": "zh-CN", "google_language": "zh-cn",
        "english_name": "Chinese, Taiwan", "native_name": "繁體中文", "flag": "🇨🇳"},
    {"discord_language": "hi", "google_language": "hi",
        "english_name": "Hindi", "native_name": "हिन्दी", "flag": "🇮🇳"},
    {"discord_language": "th", "google_language": "th",
        "english_name": "Thai", "native_name": "ไทย", "flag": "🇹🇭"},
    {"discord_language": "ja", "google_language": "ja",
        "english_name": "Japanese", "native_name": "日本語", "flag": "🇯🇵"},

    {"discord_language": "no", "google_language": "no",
        "english_name": "Norwegian", "native_name": "Norsk", "flag": "🇳🇴"},
    {"discord_language": "lt", "google_language": "lt",
        "english_name": "Lithuanian", "native_name": "Lietuviškai", "flag": "🇱🇹"},
    {"discord_language": "en-US", "google_language": "en",
        "english_name": "English, US", "native_name": "English, US", "flag": "🇺🇸"},
    {"discord_language": "zh-TW", "google_language": "zh-tw",
        "english_name": "Chinese, China", "native_name": "中文", "flag": "🇹🇼"},
    {"discord_language": "ko", "google_language": "ko",
        "english_name": "Korean", "native_name": "한국어", "flag": "🇰🇷"}
]

current = [
    {"locale": "en", "english_name": "English",
     "native_name": "English", "flag": "🇬🇧"},
    {"locale": "ru", "english_name": "Russian",
     "native_name": "Pусский", "flag": "🇷🇺"},
    {"locale": "id", "english_name": "Indonesian",
     "native_name": "Bahasa Indonesia", "flag": "🇮🇩"},
    {"locale": "da", "english_name": "Danish",
     "native_name": "Dansk", "flag": "🇩🇰"},
    {"locale": "de", "english_name": "German",
     "native_name": "Deutsch", "flag": "🇩🇪"},
    {"locale": "es", "english_name": "Spanish",
     "native_name": "Español", "flag": "🇪🇸"},
    {"locale": "fr", "english_name": "French",
     "native_name": "Français", "flag": "🇫🇷"},
    {"locale": "pl", "english_name": "Polish",
     "native_name": "Polski", "flag": "🇵🇱"},
    {"locale": "tr", "english_name": "Turkish",
     "native_name": "Türkçe", "flag": "🇹🇷"},
]


class BotInfo:
    title = {
        'en': 'this is a multifunctional bot',
        'ru': 'это многофункциональный бот',
        'id': 'Ini adalah bot multifungsi',
        'da': 'Dette er en multifunktionel bot',
        'de': 'dies ist ein multifunktionaler Bot',
        'es': 'es un bot multifuncional',
        'fr': 'c\'est un bot multifonctionnel',
        'pl': 'to wielofunkcyjny Bot',
        'tr': 'bu çok işlevli bir bot'
    }
    description = {
        'en': 'The bot is designed to facilitate server management and is equipped with various automation tools',
        'ru': 'Бот предназначен для облегчения управления сервером и оснащен различными средствами автоматизации',
        'id': 'Bot dirancang untuk memfasilitasi manajemen server dan dilengkapi dengan berbagai alat otomatisasi',
        'da': 'Botten er designet til at lette serverstyring og er udstyret med forskellige automatiseringsværktøjer',
        'de': 'Der Bot wurde entwickelt, um die Serververwaltung zu erleichtern und ist mit verschiedenen Automatisierungsfunktionen ausgestattet',
        'es': 'El bot está diseñado para facilitar la administración del servidor y está equipado con varias herramientas de automatización',
        'fr': 'Le bot est conçu pour faciliter la gestion du serveur et est équipé de divers outils d\'automatisation',
        'pl': 'Bot ma na celu ułatwienie zarządzania serwerem i jest wyposażony w różne Narzędzia automatyzacji',
        'tr': 'Bot, sunucunun yönetimini kolaylaştırmak için tasarlanmıştır ve çeşitli otomasyon araçlarıyla donatılmıştır'
    }

    info_server = {
        'en': 'Information about the server',
        'ru': 'Информация о сервере',
        'id': 'Informacje o serwerze',
        'da': 'Oplysninger om serveren',
        'de': 'Informationen zum Server',
        'es': 'Información del servidor',
        'fr': 'Informations sur le serveur',
        'pl': 'Informacje o serwerze',
        'tr': 'Sunucu Bilgileri'
    }
    prefix_server = {
        'en': 'Server prefix',
        'ru': 'Префикс сервера',
        'id': 'Awalan server',
        'da': 'Serverpræfiks',
        'de': 'Server-Präfix',
        'es': 'Prefijo del servidor',
        'fr': 'Préfixe du serveur',
        'pl': 'Prefiks serwera',
        'tr': 'Sunucu öneki'
    }


class translate:
    placeholder = {
        'ru': 'Выберете подходящий язык:',
        'en': 'Will choose the appropriate language:',
        'id': 'Pilih bahasa yang sesuai:',
        'da': 'Vælg det relevante sprog:',
        'de': 'Wählen Sie die entsprechende Sprache aus:',
        'es': 'Seleccione el idioma apropiado:',
        'fr': 'Seleccione el idioma apropiado:',
        'pl': 'Wybierz odpowiedni język:',
        'tr': 'Doğru dili seçin:'
    }


class captcha:
    congratulation = {
        'ru': 'Поздравляю, вы ввели капчу!',
        'en': 'Congratulations you have passed the captcha!',
        'id': 'Selamat, Anda telah memperkenalkan captcha!',
        'da': 'Tillykke, du har introduceret captcha!',
        'de': 'Herzlichen Glückwunsch, Sie haben Captcha eingeführt!',
        'es': '¡Felicitaciones, has introducido captcha!',
        'fr': 'Félicitations, vous avez saisi le captcha!',
        'pl': 'Gratulacje, wprowadziłeś kodowanie!',
        'tr': 'Tebrikler, kodlamayı girdiniz!'
    }
    enter = {
        'ru': 'У вас есть 30 секунд чтобы решить капчу!',
        'en': 'You have 30 seconds to solve the captcha!',
        'id': 'Anda memiliki waktu 30 detik untuk menyelesaikan captcha!',
        'da': 'Du har 30 sekunder til at løse captcha!',
        'de': 'Sie haben 30 Sekunden Zeit, um das Captcha zu lösen!',
        'es': '¡Tienes 30 segundos para resolver el captcha!',
        'fr': 'Vous avez 30 secondes pour résoudre le captcha!',
        'pl': 'Masz 30 sekund na rozwikłanie kodowania!',
        'tr': 'Kodlamayı çözmek için 30 saniyeniz var!'
    }
    failed = {
        'ru': 'Капча не пройдена',
        'en': 'Captcha failed',
        'id': 'Captcha belum dilewati',
        'da': 'Captcha er ikke bestået',
        'de': 'Captcha wird nicht übergeben',
        'es': 'Captcha no se pasa',
        'fr': 'Le captcha n\'est pas passé',
        'pl': 'Captcha nie przeszła',
        'tr': 'Captcha geçmedi'
    }


class activiti:
    failed = {
        'ru': 'Это активность недоступна или не работает',
        'en': 'This activity is unavailable or does not work',
        'id': 'Aktivitas ini tidak tersedia atau tidak berfungsi',
        'da': 'Denne aktivitet er ikke tilgængelig eller fungerer ikke',
        'de': 'Diese Aktivität ist nicht verfügbar oder funktioniert nicht',
        'es': 'Esta actividad no está disponible o no funciona',
        'fr': 'Cette activité n\'est pas disponible ou ne fonctionne pas',
        'pl': 'Ta akcja jest niedostępna lub nie działa',
        'tr': 'Bu işlem kullanılamıyor veya çalışmıyor'
    }
    embed_title = {
        'ru': 'Активность успешно создана!',
        'en': 'The activity has been successfully created!',
        'id': 'Aktivitas telah berhasil dibuat!',
        'da': 'Aktivitet er blevet oprettet med succes!',
        'de': 'Aktivität wurde erfolgreich erstellt!',
        'es': '¡La actividad fue creada con éxito!',
        'fr': 'L\'activité a été créée avec succès!',
        'pl': 'Wydarzenie zostało pomyślnie utworzone!',
        'tr': 'Etkinlik başarıyla oluşturuldu!'
    }
    embed_description = {
        'ru': 'Однако некоторые виды активностей могут быть недоступны для вашего сервера, если уровень бустов не соответствует требованиям активности.',
        'en': 'However, some types of activities may not be available for your server if the boost level does not meet the activity requirements.',
        'id': 'Namun, beberapa jenis aktivitas mungkin tidak tersedia untuk server Anda jika level peningkatan tidak memenuhi persyaratan aktivitas.',
        'da': 'Nogle aktivitetstyper er dog muligvis ikke tilgængelige for din server, hvis opgraderingsniveauet ikke opfylder Aktivitetskravene.',
        'de': 'Einige Aktivitätstypen sind jedoch möglicherweise für Ihren Server nicht verfügbar, wenn die Upgrade-Stufe die Aktivitätsanforderungen nicht erfüllt.',
        'es': 'Sin embargo, es posible que algunos tipos de actividad no estén disponibles para su servidor si el nivel de actualización no cumple con los requisitos de actividad.',
        'fr': 'Cependant, certains types d\'activité peuvent ne pas être disponibles pour votre serveur si le niveau de mise à niveau ne répond pas aux exigences d\'activité.',
        'pl': 'Jednak niektóre rodzaje działań mogą nie być dostępne dla Twojego serwera, jeśli poziom aktualizacji nie spełnia wymagań dotyczących działań.',
        'tr': 'Ancak, güncelleme düzeyi eylem gereksinimlerini karşılamıyorsa sunucunuz için bazı eylem türleri kullanılamayabilir.'
    }
    fields_label = {
        'ru': 'Название активности',
        'en': 'Activity name',
        'id': 'Nama aktivitas',
        'da': 'Aktivitetsnavn',
        'de': 'Name der Aktivität',
        'es': 'Nombre de la actividad',
        'fr': 'Nom de l\'activité',
        'pl': 'Nazwa działalności',
        'tr': 'Faaliyetin adı'
    }
    fields_max_user = {
        'ru': 'Максимальное кол-во пользователей',
        'en': 'Maximum number of users',
        'id': 'Jumlah maksimum pengguna',
        'da': 'Maksimalt antal brugere',
        'de': 'Maximale Anzahl von Benutzern',
        'es': 'Número máximo de usuarios',
        'fr': 'Nombre maximum d\'utilisateurs',
        'pl': 'Maksymalna liczba użytkowników',
        'tr': 'Maksimum kullanıcı sayısı'
    }


class errors:
    MissingPermissions = {
        'en': 'You don\'t have enough rights',
        'ru': 'У вас недостаточно прав',
        'id': '',
        'da': '',
        'de': '',
        'es': '',
        'fr': '',
        'pl': '',
        'tr': ''
    }
    BotMissingPermissions = {
        'en': 'The bot does not have enough rights to perform this action, most likely you took it away when adding the bot to the server',
        'ru': 'У бота недостаточно прав для выполнения этого действия, скорее всего, вы убрали их при добавлении бота на сервер',
        'id': 'Anda tidak memiliki cukup hak',
        'da': 'Du har ikke nok rettigheder',
        'de': 'Du hast nicht genug Rechte',
        'es': 'No tienes suficientes derechos',
        'fr': 'Vous n\'avez pas assez de droits',
        'pl': 'Nie masz wystarczających praw',
        'tr': 'Yeterli hakkınız yok'
    }
    MissingRole = {
        'en': 'You don\'t have a suitable role to execute the command',
        'ru': 'У вас нет нужной роли для выполнения команды',
        'id': 'Anda tidak memiliki peran yang tepat untuk menjalankan perintah',
        'da': 'Du har ikke den rigtige rolle til at køre kommandoen',
        'de': 'Sie haben nicht die richtige Rolle, um den Befehl auszuführen',
        'es': 'No tiene el rol adecuado para ejecutar el comando',
        'fr': 'N\'a pas le rôle approprié pour exécuter la commande',
        'pl': 'Nie ma odpowiedniej roli do wykonania polecenia',
        'tr': 'Komutu yerine getirmek için uygun bir rol yoktur'
    }
    MissingChannel = {
        'en': 'You cannot execute this command in this channel',
        'ru': 'Вы не можете выполнить эту команду в этом канале',
        'id': 'Anda tidak dapat menjalankan perintah ini di saluran ini',
        'da': 'Du kan ikke køre denne kommando på denne kanal',
        'de': 'Sie können diesen Befehl auf diesem Kanal nicht ausführen',
        'es': 'No puede ejecutar este comando en este canal',
        'fr': 'Vous ne pouvez pas exécuter cette commande sur ce canal',
        'pl': 'Nie możesz uruchomić tego polecenia na tym kanale',
        'tr': 'Bu komutu bu kanalda çalıştıramazsınız'
    }

    NotOwner = {
        'en': 'This command is intended for the bot owner',
        'ru': 'Эта команда предназначена для владельца бота',
        'id': 'Perintah ini ditujukan untuk pemilik bot',
        'da': 'Denne kommando er beregnet til bot ejere',
        'de': 'Dieser Befehl ist für Bot-Besitzer gedacht',
        'es': 'Este comando está destinado a propietarios de bots',
        'fr': 'Cette commande est destinée aux propriétaires de robots',
        'pl': 'To polecenie jest przeznaczone dla właścicieli robotów',
        'tr': 'Bu komut bot sahibine yöneliktir'
    }
    CommandNotFound = {
        'en': 'There is no such command',
        'ru': 'Такой команды нет',
        'id': 'Tidak ada perintah seperti itu',
        'da': 'Der er ingen sådan kommando',
        'de': 'Es gibt keinen solchen Befehl',
        'es': 'No hay tal comando',
        'fr': 'Il n\'y a pas une telle commande',
        'pl': 'Nie ma takiego polecenia',
        'tr': 'Böyle bir takım yok'
    }
    CheckFailure = {
        'en': 'You don\'t fulfill all the conditions',
        'ru': 'Вы не выполняете всех условий',
        'id': 'Anda tidak memenuhi semua persyaratan',
        'da': 'Du opfylder ikke alle kravene',
        'de': 'Erfüllt nicht alle Anforderungen',
        'es': 'No cumple con todos los requisitos',
        'fr': 'Ne répondent pas à toutes les exigences',
        'pl': 'Nie spełniają wszystkich wymagań',
        'tr': 'Tüm gereksinimleri karşılamıyor'
    }
    BadArgument = {
        'en': 'Invalid argument entered',
        'ru': 'Введен недопустимый аргумент',
        'id': 'Argumen yang tidak valid telah dimasukkan',
        'da': 'Et ugyldigt argument er blevet indtastet',
        'de': 'Ein ungültiges Argument wurde eingegeben',
        'es': 'Se ha introducido un argumento no válido',
        'fr': 'Un argument invalide a été saisi',
        'pl': 'Wprowadzono nieprawidłowy argument',
        'tr': 'Yanlış argüman tanıtıldı'
    }
    DisabledCommand = {
        'en': 'This command is disabled on the server',
        'ru': 'Эта команда отключена на сервере',
        'id': 'Perintah ini dinonaktifkan di server',
        'da': 'Denne kommando er deaktiveret på serveren',
        'de': 'Dieser Befehl ist auf dem Server deaktiviert',
        'es': 'Este comando está deshabilitado en el servidor',
        'fr': 'Cette commande est désactivée sur le serveur',
        'pl': 'To polecenie jest wyłączone na serwerze',
        'tr': 'Bu komut sunucuda devre dışı bırakıldı'
    }
    MissingRequiredArgument = {
        'en': 'You didn\'t enter a required argument',
        'ru': 'Вы не ввели обязательный аргумент',
        'id': 'Anda tidak memasukkan argumen yang diperlukan',
        'da': 'Du indtastede ikke de krævede argumenter',
        'de': 'Sie haben die erforderlichen Argumente nicht eingegeben',
        'es': 'No ha introducido los argumentos requeridos',
        'fr': 'Vous n\'avez pas saisi les arguments requis',
        'pl': 'Nie wprowadziłeś wymaganych argumentów',
        'tr': 'Gerekli argümanları girmediniz'
    }
    NotActivateEconomy = {
        'en': 'The economy system is disabled on the server',
        'ru': 'Система экономики отключена на сервере',
        'id': 'Sistem ekonomi dinonaktifkan di server',
        'da': 'Økonomisk system deaktiveret på serveren',
        'de': 'Finanzsystem auf dem Server deaktiviert',
        'es': 'Deshabilitó el sistema financiero en el servidor',
        'fr': 'Désactivé le système financier sur le serveur',
        'pl': 'Wyłączony system finansowy na serwerze',
        'tr': 'Sunucudaki devre dışı bırakılmış finansal sistem'
    }
    OnlyTeamError = {
        'en': 'This command can only be used by the bot team',
        'ru': 'Эта команда может быть использована только командой бота',
        'id': 'Perintah ini hanya dapat digunakan oleh tim bot',
        'da': 'Denne kommando kan kun bruges af bot teams',
        'de': 'Dieser Befehl kann nur von Bot-Teams verwendet werden',
        'es': 'Este comando solo puede ser utilizado por equipos de bots',
        'fr': 'Cette commande ne peut être utilisée que par les équipes de robots',
        'pl': 'To polecenie może być używane tylko przez polecenia robotów',
        'tr': 'Bu komut yalnızca robot komutları tarafından kullanılabilir'
    }
    MemberNotFound = {
        'en': 'The participant could not be found',
        'ru': 'Участника не удалось найти',
        'id': 'Tidak ada peserta yang ditemukan',
        'da': 'Ingen deltagere fundet',
        'de': 'Keine Teilnehmer gefunden',
        'es': 'No se encontraron participantes',
        'fr': 'Aucun participant n\'a été trouvé',
        'pl': 'Nie znaleziono żadnego uczestnika',
        'tr': 'Katılımcı bulunamadı'
    }

    class CommandOnCooldown:
        title = {
            'en': 'The command is on hold',
            'ru': 'Команда находится в режиме ожидания',
            'id': 'Perintah dalam mode siaga',
            'da': 'Kommandoer i standbytilstand',
            'de': 'Befehle im Standby-Modus',
            'es': 'Comandos en modo de espera',
            'fr': 'Commandes en mode veille',
            'pl': 'Polecenie jest w trybie gotowości',
            'tr': 'Komut bekleme modunda'
        }
        description = {
            'en': 'Try again after',
            'ru': 'Повторите попытку через',
            'id': 'Coba lagi',
            'da': 'Prøv igen',
            'de': 'Versuchen Sie es erneut',
            'es': 'Inténtalo de nuevo',
            'fr': 'Veuillez réessayer.',
            'pl': 'Spróbuj ponownie przez',
            'tr': 'Tekrar deneyin'
        }


class selector_music:
    placeholder = {
        'en': 'Select a track',
        'ru': 'Выберите трек',
        'id': 'Pilih trek',
        'da': 'Vælg et spor',
        'de': 'Wählen Sie eine Spur',
        'es': 'Seleccione una pista',
        'fr': 'Sélectionnez une piste',
        'pl': 'Wybierz ścieżkę',
        'tr': 'Bir parça seçin'
    }
    title = {
        'en': 'Choose the track you are interested in!',
        'ru': 'Выберите интересующий вас трек!',
        'id': 'Pilih trek yang Anda minati!',
        'da': 'Vælg det spor, du er interesseret i!',
        'de': 'Wählen Sie die Strecke, die Sie interessiert!',
        'es': '¡Elige la pista que te interesa!',
        'fr': 'Choisissez la piste qui vous intéresse!',
        'pl': 'Wybierz utwór, który Cię interesuje!',
        'tr': 'İlgilendiğiniz parçayı seçin!'
    }
