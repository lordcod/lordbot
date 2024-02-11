from typing import List, Dict, TypedDict


class CommandOption(TypedDict):
    name: str
    category: str
    aliases: List[str]
    arguments: List[str]
    descriptrion: Dict[str, str]
    brief_descriptrion: Dict[str, str]
    allowed_disabled: bool


categories_emoji: Dict[str, str] = {
    "economy": "💎",
    "major": "👑",
    "voice": "🎤",
    "moderation": "⚠",
}

categories_name:  Dict[str, Dict[str, str]] = {
    "economy": {
        "ru": "Экономика",
        "en": "Economy",
        "id": "Ekonomi",
        "da": "Økonomi",
        "de": "Wirtschaft",
        "es": "Economía",
        "fr": "Économie",
        "pl": "Gospodarka",
        "tr": "Ekonomi"
    },
    "major": {
        "ru": "Главное",
        "en": "Major",
        "id": "Mayor",
        "da": "Stor",
        "de": "Wichtigsten",
        "es": "Mayor",
        "fr": "Majeur",
        "pl": "Major",
        "tr": "Büyük"
    },
    "voice": {
        "ru": "Голос",
        "en": "Voice",
        "id": "Suara",
        "da": "Stemme",
        "de": "Stimme",
        "es": "Voz",
        "fr": "Voix",
        "pl": "Głos",
        "tr": "Ses"
    },
    "moderation": {
        "ru": "Модерационные",
        "en": "Moderation",
        "id": "Moderasi",
        "da": "Moderation",
        "de": "Moderation",
        "es": "Moderación",
        "fr": "Modération",
        "pl": "Moderacja",
        "tr": "Ilımlılık"
    },
}

categories: Dict[str, List[CommandOption]] = {
    "economy": [
        {
            "name": "balance",
            "category": "economy",
            "aliases": ["bal"],
            "arguments": ["[member]"],
            "descriptrion": {
                "en": (
                    "Displays the participant\"s balance as well as possible rewards that can be collected\n\n"
                    "If no participant is specified, the value is taken by the one who started the command"
                ),
                "ru": (
                    "Отображает баланс участника, а также возможные вознаграждения, которые можно получить\n\n"
                    "Если участник не указан, значение принимает тот, кто запустил команду"
                ),
                "id": (
                    "Menampilkan saldo peserta serta kemungkinan hadiah yang dapat dikumpulkan \ n \ n"
                    "Jika tidak ada peserta yang ditentukan, nilainya diambil oleh orang yang memulai perintah"
                ),
                "da": (
                    "Viser deltagerens balance samt mulige belønninger, der kan indsamles\n\n"
                    "Hvis der ikke er angivet nogen deltager, tages værdien af den, der startede kommandoen"
                ),
                "de": (
                    "Zeigt das Guthaben des Teilnehmers sowie mögliche Belohnungen an, die gesammelt werden können\n \n"
                    "Wenn kein Teilnehmer angegeben ist, wird der Wert von demjenigen übernommen, der den Befehl gestartet hat."
                ),
                "es": (
                    "Muestra el saldo del participante, así como las posibles recompensas que se pueden cobrar\n\n"
                    "Si no se especifica ningún participante, el valor lo toma quien inició el comando"
                ),
                "fr": (
                    "Affiche le solde du participant ainsi que les éventuelles récompenses pouvant être collectées\n \ n"
                    "Si aucun participant n'est spécifié, la valeur est prise par celui qui a lancé la commande"
                ),
                "pl": (
                    "Wyświetla saldo uczestnika, a także możliwe nagrody, które można zebrać\n\n"
                    "Jeśli żaden uczestnik nie jest określony, wartość jest pobierana przez tego, który uruchomił polecenie"
                ),
                "tr": (
                    "Katılımcının bakiyesini ve toplanabilecek olası ödülleri görüntüler\n\n"
                    "Katılımcı belirtilmezse, değer komutu başlatan kişi tarafından alınır"
                ),
            },
            "brief_descriptrion": {
                "en": "Participant's balance",
                "ru": "Баланс участника",
                "id": "Saldo peserta",
                "da": "Deltagerens balance",
                "de": "Guthaben des Teilnehmers",
                "es": "Saldo del participante",
                "fr": "Solde du participant",
                "pl": "Saldo uczestnika",
                "tr": "Katılımcının bakiyesi"
            },
            "allowed_disabled": True
        },
        {
            "name": "leaderboard",
            "category": "economy",
            "aliases": [],
            "arguments": [],
            "descriptrion": {
                "en": "Shows statistics of the top 10 server participants by balance",
                "ru": "Показывает статистику по 10 лучшим участникам сервера по балансу",
                "id": "Menampilkan statistik dari 10 peserta server teratas berdasarkan saldo",
                "da": "Viser statistik over de 10 bedste serverdeltagere efter balance",
                "de": "Zeigt Statistiken der Top 10 Serverteilnehmer nach Saldo an",
                "es": "Muestra estadísticas de los 10 mejores participantes del servidor por saldo",
                "fr": "Affiche les statistiques des 10 meilleurs participants au serveur par solde",
                "pl": "Pokazuje statystyki 10 najlepszych uczestników serwera według salda",
                "tr": "En iyi 10 sunucu katılımcısının istatistiklerini bakiyeye göre gösterir"
            },
            "brief_descriptrion": {
                "en": "Top server participants by balance",
                "ru": "Лучшие участники сервера по балансу",
                "id": "Peserta server teratas berdasarkan saldo",
                "da": "Top server deltagere efter balance",
                "de": "Top-Serverteilnehmer nach Saldo",
                "es": "Principales participantes del servidor por saldo",
                "fr": "Principaux participants au serveur par solde",
                "pl": "Najlepsi uczestnicy serwera według salda",
                "tr": "Bakiyeye göre en iyi sunucu katılımcıları"
            },
            "allowed_disabled": True
        },
        {
            "name": "pay",
            "category": "economy",
            "aliases": [],
            "arguments": ["<member>", "<amount>"],
            "descriptrion": {
                "en": "Transfers the specified amount to the selected participant",
                "ru": "Переводит указанную сумму выбранному участнику",
                "id": "Mentransfer jumlah yang ditentukan ke peserta yang dipilih",
                "da": "Overfører det angivne beløb til den valgte deltager",
                "de": "Überweist den angegebenen Betrag an den ausgewählten Teilnehmer",
                "es": "Transfiere la cantidad especificada al participante seleccionado",
                "fr": "Transfère le montant spécifié au participant sélectionné",
                "pl": "Przekazuje określoną kwotę wybranemu Uczestnikowi",
                "tr": "Belirtilen tutarı seçilen katılımcıya aktarır"
            },
            "brief_descriptrion": {
                "en": "Transfers money",
                "ru": "Переводит деньги",
                "id": "Transfer uang",
                "da": "Overfører penge",
                "de": "Überweisungen Geld",
                "es": "Transferencias de dinero",
                "fr": "Transferts d'argent",
                "pl": "Przelewy pieniądze",
                "tr": "Para transferi"
            },
            "allowed_disabled": True
        },

        {
            "name": "daily",
            "category": "economy",
            "aliases": [],
            "arguments": [],
            "descriptrion": {
                "en": "Issues a cash reward once a day",
                "ru": "Выдает денежное вознаграждение один раз в день",
                "id": "Mengeluarkan hadiah uang tunai sekali sehari",
                "da": "Udsteder en kontant belønning en gang om dagen",
                "de": "Gibt einmal täglich eine Geldprämie aus",
                "es": "Emite una recompensa en efectivo una vez al día",
                "fr": "Émet une récompense en espèces une fois par jour",
                "pl": "Wydaje nagrodę pieniężną raz dziennie",
                "tr": "Günde bir kez nakit ödül verir"
            },
            "brief_descriptrion": {
                "en": "Daily cash rewards",
                "ru": "Ежедневные денежные вознаграждения",
                "id": "Hadiah uang tunai harian",
                "da": "Daglige kontante belønninger",
                "de": "Tägliche Geldprämien",
                "es": "Recompensas diarias en efectivo",
                "fr": "Récompenses quotidiennes en espèces",
                "pl": "Codzienne nagrody pieniężne",
                "tr": "Günlük nakit ödüller"
            },
            "allowed_disabled": True
        },
        {
            "name": "weekly",
            "category": "economy",
            "aliases": [],
            "arguments": [],
            "descriptrion": {
                "en": "Issues a cash reward once a week",
                "ru": "Выдает денежное вознаграждение раз в неделю",
                "id": "Mengeluarkan hadiah uang tunai seminggu sekali",
                "da": "Udsteder en kontant belønning en gang om ugen",
                "de": "Gibt einmal pro Woche eine Geldprämie aus",
                "es": "Emite una recompensa en efectivo una vez a la semana",
                "fr": "Émet une récompense en espèces une fois par semaine",
                "pl": "Wydaje nagrodę pieniężną raz w tygodniu",
                "tr": "Haftada bir kez nakit ödül verir"
            },
            "brief_descriptrion": {
                "en": "Weekly cash rewards",
                "ru": "Еженедельные денежные вознаграждения",
                "id": "Hadiah uang tunai mingguan",
                "da": "Ugentlige kontante belønninger",
                "de": "Wöchentliche Geldprämien",
                "es": "Recompensas semanales en efectivo",
                "fr": "Récompenses hebdomadaires en espèces",
                "pl": "Cotygodniowe nagrody pieniężne",
                "tr": "Haftalık nakit ödüller"
            },
            "allowed_disabled": True
        },
        {
            "name": "monthly",
            "category": "economy",
            "aliases": [],
            "arguments": [],
            "descriptrion": {
                "en": "Issues a cash reward once a month",
                "ru": "Выдает денежное вознаграждение раз в месяц",
                "id": "Mengeluarkan hadiah uang tunai sebulan sekali",
                "da": "Udsteder en kontant belønning en gang om måneden",
                "de": "Gibt einmal im Monat eine Geldprämie aus",
                "es": "Emite una recompensa en efectivo una vez al mes",
                "fr": "Émet une récompense en espèces une fois par mois",
                "pl": "Wydaje nagrodę pieniężną raz w miesiącu",
                "tr": "Ayda bir kez nakit ödül verir"
            },
            "brief_descriptrion": {
                "en": "Monthly cash rewards",
                "ru": "Ежемесячное денежное вознаграждение",
                "id": "Hadiah uang tunai bulanan",
                "da": "Månedlige kontantbelønninger",
                "de": "Monatliche Geldprämien",
                "es": "Recompensas mensuales en efectivo",
                "fr": "Récompenses mensuelles en espèces",
                "pl": "Miesięczne nagrody pieniężne",
                "tr": "Aylık nakit ödüller"
            },
            "allowed_disabled": True
        },

        {
            "name": "deposit",
            "category": "economy",
            "aliases": ["dep"],
            "arguments": ["<amount>"],
            "descriptrion": {
                "en": "Transfers the entered amount of money to the bank protecting your funds from robbery",
                "ru": "Переводит введенную сумму денег в банк, защищая ваши средства от ограбления",
                "id": "Mentransfer jumlah uang yang dimasukkan ke bank melindungi dana Anda dari perampokan",
                "da": "Overfører det indtastede beløb til banken, der beskytter dine midler mod røveri",
                "de": "Überweist den eingegebenen Geldbetrag an die Bank, um Ihr Geld vor Raub zu schützen",
                "es": "Transfiere la cantidad de dinero ingresada al banco protegiendo sus fondos contra robos",
                "fr": "Transfère le montant d'argent saisi à la banque protégeant vos fonds contre le vol",
                "pl": "Przekazuje wprowadzoną kwotę pieniędzy do banku chroniącego twoje środki przed rabunkiem",
                "tr": "Girilen para miktarını, paranızı soygundan koruyan bankaya aktarır"
            },
            "brief_descriptrion": {
                "en": "Transfers the entered amount of money to the bank",
                "ru": "Переводит введенную сумму денег в банк",
                "id": "Mentransfer jumlah uang yang dimasukkan ke bank",
                "da": "Overfører det indtastede beløb til banken",
                "de": "Überweist den eingegebenen Geldbetrag an die Bank",
                "es": "Transfiere la cantidad de dinero ingresada al banco",
                "fr": "Transfère le montant saisi à la banque",
                "pl": "Przekazuje wprowadzoną kwotę pieniędzy do banku",
                "tr": "Girilen para miktarını bankaya aktarır"
            },
            "allowed_disabled": True
        },
        {
            "name": "withdraw",
            "category": "economy",
            "aliases": ["wd"],
            "arguments": ["<amount>"],
            "descriptrion": {
                "en": (
                    "Redirects your funds from the bank back to your account\n\n"
                    "Please note that if you lose your funds, it is not possible to return them"
                ),
                "ru": (
                    "Перенаправляет ваши средства из банка обратно на ваш счет\n\n"
                    "Пожалуйста, обратите внимание, что если вы потеряете свои средства, вернуть их будет невозможно"
                ),
                "id": (
                    "Mengalihkan dana Anda dari bank kembali ke rekening Anda\n\n"
                    "Harap dicatat bahwa jika Anda kehilangan dana, tidak mungkin mengembalikannya"
                ),
                "da": (
                    "Omdirigerer dine penge fra banken tilbage til din konto\n\n"
                    "Bemærk, at hvis du mister dine penge, er det ikke muligt at returnere dem"
                ),
                "de": (
                    "Leitet Ihr Geld von der Bank zurück auf Ihr Konto\n\n"
                    "Bitte beachten Sie, dass es bei Verlust Ihres Geldes nicht möglich ist, es zurückzugeben."
                ),
                "es": (
                    "Redirige sus fondos del banco a su cuenta\n\n"
                    "Tenga en cuenta que si pierde sus fondos, no es posible devolverlos"
                ),
                "fr": (
                    "Redirige vos fonds de la banque vers votre compte\n\n"
                    "Veuillez noter que si vous perdez vos fonds, il n'est pas possible de les restituer"
                ),
                "pl": (
                    "Przekierowuje środki z banku z powrotem na twoje konto\n\n"
                    "Pamiętaj, że jeśli stracisz środki, nie możesz ich zwrócić"
                ),
                "tr": (
                    "Przekierowuje środki z banku z powrotem na twoje konto\n\n"
                    "Pamiętaj, że jeśli stracisz środki, nie możesz ich zwrócić"
                ),
            },
            "brief_descriptrion": {
                "en": "Transfers the amount back to the account",
                "ru": "Переводит сумму обратно на счет",
                "id": "Mentransfer jumlah tersebut kembali ke rekening",
                "da": "Overfører beløbet tilbage til kontoen",
                "de": "Überweist den Betrag zurück auf das Konto",
                "es": "Transfiere el importe de vuelta a la cuenta",
                "fr": "Transfère le montant sur le compte",
                "pl": "Przelewa kwotę z powrotem na konto",
                "tr": "Tutarı hesaba geri aktarır"
            },
            "allowed_disabled": True
        },

        {
            "name": "gift",
            "category": "economy",
            "aliases": [],
            "arguments": ["[member]", "<amount>"],
            "descriptrion": {
                "en": (
                    "Adds a certain amount to the selected participant\n"
                    "If the participant is not selected, the team performer acts instead"
                ),
                "ru": (
                    "Добавляет определенную сумму выбранному участнику\n"
                    "Если участник не выбран, вместо него действует исполнитель команды"
                ),
                "id": (
                    "Menambahkan jumlah tertentu ke peserta yang dipilih\n"
                    "Jika peserta tidak dipilih, pemain tim bertindak sebagai gantinya"
                ),
                "da": (
                    "Tilføjer et bestemt beløb til den valgte deltager\n"
                    "Hvis deltageren ikke er valgt, handler holdudøveren i stedet"
                ),
                "de": (
                    "Fügt dem ausgewählten Teilnehmer einen bestimmten Betrag hinzu\n"
                    "Wenn der Teilnehmer nicht ausgewählt wird, handelt stattdessen der Team Performer"
                ),
                "es": (
                    "Agrega una cierta cantidad al participante seleccionado\n"
                    "Si el participante no es seleccionado, el ejecutante del equipo actúa en su lugar"
                ),
                "fr": (
                    "Ajoute un certain montant au participant sélectionné\n"
                    "Si le participant n'est pas sélectionné, l'interprète de l'équipe agit à la place"
                ),
                "pl": (
                    "Dodaje określoną kwotę do wybranego uczestnika\n"
                    "Jeśli uczestnik nie zostanie wybrany, wykonawca zespołu działa zamiast tego"
                ),
                "tr": (
                    "Seçilen katılımcıya belirli bir miktar ekler\n"
                    "Katılımcı seçilmezse, bunun yerine takım oyuncusu hareket eder"
                ),
            },
            "brief_descriptrion": {
                "en": "Adds the amount to the participant",
                "ru": "Добавляет сумму участнику",
                "id": "Menambahkan jumlah tersebut ke peserta",
                "da": "Tilføjer beløbet til deltageren",
                "de": "Fügt dem Teilnehmer den Betrag hinzu",
                "es": "Agrega la cantidad al participante",
                "fr": "Ajoute le montant au participant",
                "pl": "Dodaje kwotę do uczestnika",
                "tr": "Tutarı katılımcıya ekler"
            },
            "allowed_disabled": True
        },
        {
            "name": "take",
            "category": "economy",
            "aliases": [],
            "arguments": ["[member]", "<amount>"],
            "descriptrion": {
                "en": (
                    "Takes a certain amount to the selected participant\n"
                    "If the participant is not selected, the team performer acts instead"
                ),
                "ru": (
                    "Выплачивает определенную сумму выбранному участнику\n"
                    "Если участник не выбран, вместо него действует исполнитель команды"
                ),
                "id": (
                    "Mengambil jumlah tertentu untuk peserta yang dipilih\n"
                    "Jika peserta tidak dipilih, pemain tim bertindak sebagai gantinya"
                ),
                "da": (
                    "Tager et vist beløb til den valgte deltager\n"
                    "Hvis deltageren ikke er valgt, handler holdudøveren i stedet"
                ),
                "de": (
                    "Nimmt dem ausgewählten Teilnehmer einen bestimmten Betrag\n"
                    "Wenn der Teilnehmer nicht ausgewählt wird, handelt stattdessen der Team Performer"
                ),
                "es": (
                    "Toma una cierta cantidad para el participante seleccionado\n"
                    "Si el participante no es seleccionado, el ejecutante del equipo actúa en su lugar"
                ),
                "fr": (
                    "Prend un certain montant au participant sélectionné\n"
                    "Si le participant n'est pas sélectionné, l'interprète de l'équipe agit à la place"
                ),
                "pl": (
                    "Pobiera określoną kwotę wybranemu Uczestnikowi\n"
                    "Jeśli uczestnik nie zostanie wybrany, wykonawca zespołu działa zamiast tego"
                ),
                "tr": (
                    "Seçilen katılımcıya belirli bir miktar alır\n"
                    "Katılımcı seçilmezse, bunun yerine takım oyuncusu hareket eder"
                ),
            },
            "brief_descriptrion": {
                "en": "Takes the amount to the participant",
                "ru": "Забирает сумму у участнику",
                "id": "Membawa jumlah tersebut ke peserta",
                "da": "Tager beløbet til deltageren",
                "de": "Überweist den Betrag an den Teilnehmer",
                "es": "Lleva la cantidad al participante",
                "fr": "Remet le montant au participant",
                "pl": "Przyjmuje kwotę do uczestnika",
                "tr": "Tutarı katılımcıya alır"
            },
            "allowed_disabled": True
        },
    ],
    "major": [
        {
            "name": "help",
            "category": "major",
            "aliases": [],
            "arguments": ["[command]"],
            "descriptrion": {
                "en": "A command describing the bot's functions",
                "ru": "Команда, описывающая функции бота",
                "id": "Perintah yang menjelaskan fungsi bot",
                "da": "En kommando, der beskriver botens funktioner",
                "de": "Ein Befehl, der die Funktionen des Bots beschreibt",
                "es": "Un comando que describe las funciones del bot",
                "fr": "Une commande décrivant les fonctions du bot",
                "pl": "Polecenie opisujące funkcje bota",
                "tr": "Botun işlevlerini açıklayan bir komut"
            },
            "brief_descriptrion": {
                "en": "Current command",
                "ru": "Текущая команда",
                "id": "Tim saat ini",
                "da": "Det nuværende hold",
                "de": "Aktueller Befehl",
                "es": "Equipo actual",
                "fr": "Équipe actuelle",
                "pl": "Obecny zespół",
                "tr": "Mevcut takım"
            },
            "allowed_disabled": False,
        },
        {
            "name": "ping",
            "category": "major",
            "aliases": [],
            "arguments": [],
            "descriptrion": {
                "en": "Shows the performance and current status of the bot",
                "ru": "Показывает производительность и текущее состояние бота",
                "id": "Menunjukkan kinerja dan status bot saat ini",
                "da": "Viser botens ydeevne og aktuelle status",
                "de": "Zeigt die Leistung und den aktuellen Status des Bots an",
                "es": "Muestra el rendimiento y el estado actual del bot",
                "fr": "Affiche les performances et l'état actuel du bot",
                "pl": "Pokazuje wydajność i aktualny stan bota",
                "tr": "Botun performansını ve mevcut durumunu gösterir"
            },
            "brief_descriptrion": {
                "en": "Current bot delay",
                "ru": "Текущая задержка бота",
                "id": "Penundaan bot saat ini",
                "da": "Aktuel bot forsinkelse",
                "de": "Aktuelle Bot-Verzögerung",
                "es": "Retraso actual del bot",
                "fr": "Délai actuel du bot",
                "pl": "Aktualne opóźnienie bota",
                "tr": "Geçerli bot gecikmesi"
            },
            "allowed_disabled": False,
        },
        {
            "name": "invite",
            "category": "major",
            "aliases": [],
            "arguments": [],
            "descriptrion": {
                "en": "Issues a link inviting the bot to the server",
                "ru": "Выдает ссылку, приглашающую бота на сервер",
                "id": "Menerbitkan tautan yang mengundang bot ke server",
                "da": "Udsteder et link, der inviterer bot til serveren",
                "de": "Gibt einen Link aus, der den Bot zum Server einlädt",
                "es": "Emite un enlace que invita al bot al servidor",
                "fr": "Émet un lien invitant le bot sur le serveur",
                "pl": "Wystawia link zapraszający bota na serwer",
                "tr": "Botu sunucuya davet eden bir bağlantı verir"
            },
            "brief_descriptrion": {
                "en": "Bot invitation link",
                "ru": "Ссылка на приглашение бота",
                "id": "Tautan undangan bot",
                "da": "Bot invitation link",
                "de": "Bot-Einladungslink",
                "es": "Enlace de invitación de bots",
                "fr": "Lien d'invitation de bot",
                "pl": "Link do zaproszenia bota",
                "tr": "Bot davet bağlantısı"
            },
            "allowed_disabled": False,
        },
        {
            "name": "captcha",
            "category": "major",
            "aliases": [],
            "arguments": [],
            "descriptrion": {
                "en": "Shows a picture on which the text is encrypted within 30 seconds the user must solve the captcha",
                "ru": "Показывает картинку, на которой зашифрован текст, в течение 30 секунд пользователь должен разгадать капчу",
                "id": "Menampilkan gambar di mana teks dienkripsi dalam waktu 30 detik pengguna harus menyelesaikan captcha",
                "da": "Viser et billede, hvor teksten er krypteret inden for 30 sekunder brugeren skal løse captcha",
                "de": "Zeigt ein Bild an, auf dem der Text verschlüsselt ist Innerhalb von 30 Sekunden muss der Benutzer das Captcha lösen",
                "es": "Muestra una imagen en la que el texto está cifrado en 30 segundos el usuario debe resolver el captcha",
                "fr": "Affiche une image sur laquelle le texte est crypté dans les 30 secondes, l'utilisateur doit résoudre le captcha",
                "pl": "Pokazuje obraz, na którym tekst jest szyfrowany w ciągu 30 sekund użytkownik musi rozwiązać captcha",
                "tr": "Kullanıcının captcha'yı çözmesi gereken metnin 30 saniye içinde şifrelendiği bir resmi gösterir"
            },
            "brief_descriptrion": {
                "en": "Test command",
                "ru": "Тестовая команда",
                "id": "Perintah uji",
                "da": "Testkommando",
                "de": "Befehl testen",
                "es": "Comando de prueba",
                "fr": "Commande de test",
                "pl": "Polecenie testowe",
                "tr": "Test komutu"
            },
            "allowed_disabled": True,

        },
    ],
    "voice": [
        {
            "name": "join",
            "category": "voice",
            "aliases": [],
            "arguments": [],
            "descriptrion": {
                "en": "Enters the channel with the user who called the command",
                "ru": "",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "brief_descriptrion": {
                "en": "Enters the channel"
            },
            "allowed_disabled": True,
        },
        {
            "name": "leave",
            "category": "voice",
            "aliases": [],
            "arguments": [],
            "descriptrion": {
                "en": "Comes out the channel with the user who called the command",
                "ru": "",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "brief_descriptrion": {
                "en": "Comes out the channel",
                "ru": "",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "allowed_disabled": True,
        },
        {
            "name": "play",
            "category": "voice",
            "aliases": [],
            "arguments": ["<title/url>"],
            "descriptrion": {
                "en": (
                    "Starts playing the music set by the user\n"
                    "As a cloud with music is **Yandex Music**"
                ),
                "ru": "",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "brief_descriptrion": {
                "en": "Starts playing music",
                "ru": "",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "allowed_disabled": True,
        },
        {
            "name": "stop",
            "category": "voice",
            "aliases": [],
            "arguments": [],
            "descriptrion": {
                "en": "Stops the current music stream",
                "ru": "",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "brief_descriptrion": {
                "en": "Stops the music",
                "ru": "",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "allowed_disabled": True,
        },
        {
            "name": "pause",
            "category": "voice",
            "aliases": [],
            "arguments": [],
            "descriptrion": {
                "en": "Stops the current music stream in the future which can be continued",
                "ru": "",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "brief_descriptrion": {
                "en": "Assigns a pause for music",
                "ru": "",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "allowed_disabled": True,
        },
        {
            "name": "resume",
            "category": "voice",
            "aliases": [],
            "arguments": [],
            "descriptrion": {
                "en": "Resumes the music stream that was completed by the necessary means in order to continue in the future",
                "ru": "",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "brief_descriptrion": {
                "en": "Resumes music",
                "ru": "",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "allowed_disabled": True,
        },
        {
            "name": "volume",
            "category": "voice",
            "aliases": [],
            "arguments": ["<volume>"],
            "descriptrion": {
                "en": "Set the volume to the current music stream from 1 to 100",
                "ru": "",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "brief_descriptrion": {
                "en": "Sets the volume",
                "ru": "",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "allowed_disabled": True,
        },
    ],
    "moderation": [
        {
            "name": "purge",
            "category": "moderation",
            "aliases": [],
            "arguments": [],
            "descriptrion": {
                "en": "Subcommands that help clean the chat",
                "ru": "Подкоманды, которые помогают очистить чат",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "brief_descriptrion": {
                "en": "Commands to clear the chat",
                "ru": "Команды для очистки чата",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "allowed_disabled": True,
        },
        {
            "name": "temp-role",
            "category": "moderation",
            "aliases": [],
            "arguments": ["<member>", "<roles>", "[time]"],
            "descriptrion": {
                "en": (
                    "Adds roles to a certain participant for a while or forever\n"
                    "If the role is not specified, the role will be assigned forever\n"
                    "You can summarize the roles\n"
                    "The time is indicated in the format `1d1h1m1s` the values can be combined and also duplicated, for example `1d2h1d`\n\n"
                    "Example: "
                    "l.temp-role **@lordcode** **@role1** **@role2** _12h_"
                ),
                "ru": (
                    "Добавляет роли определенному участнику на некоторое время или навсегда\n"
                    "Если роль не указана, она будет назначена навсегда\n"
                    "Вы можете суммировать роли\n"
                    "Время указано в формате `1d1h1m1s` значения могут комбинироваться, а также дублироваться, например `1d2h1d`\n\n"
                    "Пример: "
                    "l.temp-role **@lordcode** **@role1** **@role2** _12h_"
                ),
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "brief_descriptrion": {
                "en": "Adds roles to a certain participant for a while or forever",
                "ru": "Добавляет роли определенному участнику на некоторое время или навсегда",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "allowed_disabled": True,
        },
        {
            "name": "temp-role list",
            "category": "moderation",
            "aliases": [],
            "arguments": ["[member]"],
            "descriptrion": {
                "en": (
                    "Provides a list of temporary roles for the server or member.\n"
                    "If `member` is n2ot specified, it shows a list of all temporary roles on the server.\n"
                    "If specified, it shows only those roles that belong to the participant.\n"
                    "The roles assigned to are always not shown in the list."
                ),
                "ru": (
                    "Предоставляет список временных ролей для сервера или участника.\n"
                    "Если `member` не указан, то отображается список всех временных ролей на сервере.\n"
                    "Если указано, то отображаются только те роли, которые принадлежат участнику.\n"
                    "Роли назначенные на всегда не отображаются в списке."
                ),
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "brief_descriptrion": {
                "en": "Provides a list of temporary roles for the server or member",
                "ru": "Предоставляет список временных ролей для сервера или участника",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "allowed_disabled": True,
        },
        {
            "name": "say",
            "category": "moderation",
            "aliases": [],
            "arguments": ["<text/json>"],
            "descriptrion": {
                "en": (
                    "Sends a message on behalf of the bot using a unique "
                    "[**embed builder**](<https://lordcord.fun/embed-builder>) or plain text"
                ),
                "ru": (
                    "Отправляет сообщение от имени бота, используя уникальный "
                    "[**embed конструктор**](<https://lordcord.fun/embed-builder>) или обычный текст"
                ),
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "brief_descriptrion": {
                "en": "Sends a message",
                "ru": "Отправляет сообщение",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "allowed_disabled": True,
        },
        {
            "name": "settings",
            "category": "moderation",
            "aliases": ["set", "setting"],
            "arguments": [],
            "descriptrion": {
                "en": "Opens special bot management settings as well as its extensions",
                "ru": "Открывает специальные настройки управления ботом, а также его расширения",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "brief_descriptrion": {
                "en": "Opens the bot settings",
                "ru": "Открывает настройки бота",
                "id": "",
                "da": "",
                "de": "",
                "es": "",
                "fr": "",
                "pl": "",
                "tr": ""
            },
            "allowed_disabled": False,
        },
    ],
}


commands: List[CommandOption] = [com for cat in categories.values()
                                 for com in cat]


class Embed:
    title = {
        "ru": "Справочник",
        "en": "Help Book",
        "id": "",
        "da": "",
        "de": "",
        "es": "",
        "fr": "",
        "pl": "",
        "tr": ""
    }

    description = {
        "ru": "Справка по командам бота",
        "en": "Help on bot commands",
        "id": "",
        "da": "",
        "de": "",
        "es": "",
        "fr": "",
        "pl": "",
        "tr": ""
    }

    footer = {
        "ru": "[] = Необязательно | <> = Обязательно",
        "en": "[] = Optional | <> = Required",
        "id": "",
        "da": "",
        "de": "",
        "es": "",
        "fr": "",
        "pl": "",
        "tr": ""
    }


class CommandEmbed:
    name = {
        "ru": "Имя команды",
        "en": "Command name",
        "id": "",
        "da": "",
        "de": "",
        "es": "",
        "fr": "",
        "pl": "",
        "tr": ""
    }
    category = {
        "ru": "Категория",
        "en": "Category",
        "id": "",
        "da": "",
        "de": "",
        "es": "",
        "fr": "",
        "pl": "",
        "tr": ""
    }
    aliases = {
        "ru": "Псевдонимы",
        "en": "Aliases",
        "id": "",
        "da": "",
        "de": "",
        "es": "",
        "fr": "",
        "pl": "",
        "tr": ""
    }
    arguments = {
        "ru": "Аргументы",
        "en": "Arguments",
        "id": "",
        "da": "",
        "de": "",
        "es": "",
        "fr": "",
        "pl": "",
        "tr": ""
    }
    disable_command = {
        "ru": "Можно отключить?",
        "en": "Can I turn it off?",
        "id": "",
        "da": "",
        "de": "",
        "es": "",
        "fr": "",
        "pl": "",
        "tr": ""
    }
    connection_disabled = {
        0: {
            "ru": "Да",
            "en": "Yeah",
            "id": "",
            "da": "",
            "de": "",
            "es": "",
            "fr": "",
            "pl": "",
            "tr": ""
        },
        1: {
            "ru": "Нет",
            "en": "Nope",
            "id": "",
            "da": "",
            "de": "",
            "es": "",
            "fr": "",
            "pl": "",
            "tr": ""
        }
    }
    description = {
        "ru": "Описание",
        "en": "Descriptrion",
        "id": "",
        "da": "",
        "de": "",
        "es": "",
        "fr": "",
        "pl": "",
        "tr": ""
    }


class CommandNotFound:
    title = {
        "en": "Command Not Found",
        "ru": "Команда не найдена",
        "id": "",
        "da": "",
        "de": "",
        "es": "",
        "fr": "",
        "pl": "",
        "tr": ""
    }
    description = {
        "en": "When searching for command, we did not find it, look at it again in the general list of commands",
        "ru": "При поиске команды мы ее не нашли, посмотрите на нее еще раз в общем списке команд",
        "id": "",
        "da": "",
        "de": "",
        "es": "",
        "fr": "",
        "pl": "",
        "tr": ""
    }


class CommandNotValid:
    title = {
        "en": "The command is invalid",
        "ru": "Команда недействительна",
        "id": "",
        "da": "",
        "de": "",
        "es": "",
        "fr": "",
        "pl": "",
        "tr": ""
    }
    description = {
        "en": "Most likely you entered the name of the team incorrectly, perhaps it contains some strange characters",
        "ru": "Скорее всего, вы неправильно ввели название команды, возможно, оно содержит какие-то странные символы",
        "id": "",
        "da": "",
        "de": "",
        "es": "",
        "fr": "",
        "pl": "",
        "tr": ""
    }
