# 📑 Change Log

## Alpha/v0.2.1

17.02.2024

### What's Changed
1. Added the leaderboard command.
2. Updated economy settings.
3. Added the ability to add custom emojis for the economy.
4. Now the server is automatically added to the database, and also deleted from the database if the bot was kicked out of the server and was not added back within 1 day.
5. There is a limit on the commands `gift`, `take` now the maximum amount can be 1 million.
6. The help command has been updated, new services present in the update have been added.
7. Fixed the perception of commands for further rights verification.
8. New command execution rules have been added: cooldown, allowed roles, allowed channels. 
9. A new temporary roles service has been added.
10. Database acquisition time is accelerated.
11. The idea service has been added.
12. The return of the music service in a new form.
13. The settings of the greeting service have been disclosed and are now in the general me.
14. The translation function has been updated.

### Languages added
* Indonesia 🇮🇩
* Danish 🇩🇰
* German 🇩🇪
* Spanish 🇪🇸
* French 🇫🇷
* Polish 🇵🇱
* Turkish 🇹🇷


## Alpha/v0.1.2

09.12.2023

### What's Changed

* **`/activity`** - Fixed the work of the team
* Updated emojis in economy and settings
* The music module has been completely removed
* Added the command `/clone role`&#x20;
* Changed the type of auto-reaction settings
* Changing the appearance of the `l.help` command
* Added the welcome module:&#x20;
  * Automatic roles
  * Automatic greeting for newbies
* Added a translation to the message when the bot is mentioned
* Reduced command processing time

## Release - Alpha/v0.1.1

26.11.2023

### Main functions:

* **Moderation**: The ability to send messages on behalf of the bot and clean up the chat from messages.
* **Music**: The ability to listen to music, the presence of temporary pause and full mute functions, as well as the ability to adjust the volume - all these are provided as functions available for use.
* **Translator**: When selecting a message, all languages available in the discord are provided. After selecting one of them, the translation into the selected language takes place.
* **Activity**: To create an activity in a channel, you must first select the desired channel, and then the activity itself. The bot displays the available activities and displays their name, as well as the maximum number of participants.
* **Settings**: You can change the prefix, language, disable commands, change the color of system messages, as well as set automatic messages in branches and forums, and set automatic reactions.
* **Embed-buidler**: The ability to send embed messages without using a webhook.
* **Available languages:**
  * English(English)
  * Russian(Русский)