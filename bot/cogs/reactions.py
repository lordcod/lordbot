from typing import Literal, Optional
import typing
import nextcord
from nextcord.ext import commands
from bot.misc.lordbot import LordBot

reactions_list = [{
    "airkiss": "{author} легко прижал губы к щеке {user}, отправляя воздушный поцелуй.",
    "angrystare": "{author} сердито посмотрел на {user}, выражая свое недовольство.",
    "bite": "{author} нежно укусил {user}, проявляя свою привязанность.",
    "bleh": "{author} отвратительно коснулся {user}, выражая свое неприятие.",
    "blush": "{author} краснеет, глядя на {user}, ощущая нежные чувства.",
    "brofist": "{author} сочувственно дает кулаком по кулаку {user}, выражая дружескую поддержку.",
    "celebrate": "{author} радостно празднует с {user}, выражая свою радость.",
    "cheers": "{author} поднимает бокал в честь {user}, знаком приветствия и уважения.",
    "clap": "{author} аплодирует {user}, выражая свою признательность.",
    "confused": "{author} с удивлением смотрит на {user}, не понимая что происходит.",
    "cool": "{author} подмигивает {user}, показывая что все в порядке.",
    "cry": "{author} плачет с {user}, выражая свою поддержку и сочувствие.",
    "cuddle": "{author} нежно прижимается к {user}, ища утешение и ласку.",
    "dance": "{author} весело танцует с {user}, погружаясь в ритм музыки.",
    "drool": "{author} слюнит, глядя на {user}, испытывая голод.",
    "evillaugh": "{author} злобно смеется над {user}, выражая свою злость и насмешку.",
    "facepalm": "{author} делает facepalm из-за {user}, выражая свое разочарование или удивление.",
    "handhold": "{author} берет руку {user}, демонстрируя свою поддержку и привязанность.",
    "happy": "{author} радостно улыбается {user}, показывая свое счастье.",
    "headbang": "{author} качает головой в такт музыке вместе с {user}.",
    "hug": "{author} крепко обнимает {user}, выражая свою любовь и поддержку.",
    "kiss": "{author} страстно целует {user}, погружаясь в любовь и страсть.",
    "laugh": "{author} смеется с {user}, испытывая радость и веселье.",
    "lick": "{author} ласково лижет {user}, проявляя свою нежность и привязанность.",
    "love": "{author} глубоко любит {user}, выражая свои искренние чувства.",
    "mad": "{author} сердито смотрит на {user}, выражая свое раздражение.",
    "nervous": "{author} нервно ковыряет пальцы вместе с {user}, испытывая беспокойство.",
    "no": "{author} решительно отрицает {user}, выражая свое недовольство или несогласие.",
    "nom": "{author} удовлетворенно жует вместе с {user}, наслаждаясь вкусом.",
    "nosebleed": "{author} замечает {user} и начинает кровоточить из носа, испытывая возбуждение.",
    "nuzzle": "{author} ласково прижимается к {user}, ища нежность и ласку.",
    "nyah": "{author} мило мурлычет в ответ на {user}, выражая свое согласие или одобрение.",
    "pat": "{author} ласково поглаживает {user}, проявляя свою заботу и привязанность.",
    "peek": "{author} быстро заглядывает взглядом вместе с {user}, прятаясь от кого-то или что-то.",
    "pinch": "{author} остро пожимает {user}, выражая свое раздражение или недовольство.",
    "poke": "{author} легко тычет пальцем в {user}, привлекая внимание.",
    "pout": "{author} грустно губами тянет к {user}, выражая свое разочарование.",
    "punch": "{author} с силой бьет кулаком {user}, выражая свою ярость или агрессию.",
    "roll": "{author} крутит глазами в ответ на {user}, выражая свое недовольство или усталость.",
    "run": "{author} бегает вокруг {user}, испытывая веселье и радость.",
    "sad": "{author} грустно смотрит на {user}, выражая свою печаль или тоску.",
    "scared": "{author} испуганно смотрит на {user}, испытывая страх или тревогу.",
    "shout": "{author} кричит на {user}, выражая свою ярость или недовольство.",
    "shrug": "{author} пожимает плечами в ответ на {user}, выражая свое непонимание или безразличие.",
    "shy": "{author} стеснительно улыбается {user}, испытывая смущение.",
    "sigh": "{author} вздыхает в ответ на {user}, выражая свое разочарование или усталость.",
    "sip": "{author} с удовольствием глотает напиток вместе с {user}, наслаждаясь вкусом.",
    "slap": "{author} жестко хлопает {user}, выражая свое недовольство или раздражение.",
    "sleep": "{author} зевает и идет спать рядом с {user}, испытывая сонливость.",
    "slowclap": "{author} медленно хлопает в ладоши в ответ на {user}, выражая свое недовольство или сарказм.",
    "smack": "{author} бьет ладонью по губам {user}, выражая свое удивление или восхищение.",
    "smile": "{author} дружелюбно улыбается {user}, выражая свою радость и доброжелательность.",
    "smug": "{author} выглядит довольным рядом с {user}, испытывая гордость или удовлетворение.",
    "sneeze": "{author} чихает вместе с {user}, испытывая небольшое недомогание.",
    "sorry": "{author} извиняется перед {user}, выражая свое сожаление и раскаяние.",
    "stare": "{author} смотрит на {user} с вниманием и интересом, ожидая ответа.",
    "stop": "{author} останавливает {user}, выражая свое недовольство или требуя прекратить действие.",
    "surprised": "{author} удивленно смотрит на {user}, испытывая шок или удивление.",
    "sweat": "{author} потеет, глядя на {user}, испытывая стресс или тревогу.",
    "thumbsup": "{author} поднимает большой палец вверх перед {user}, показывая свое одобрение.",
    "tickle": "{author} щекочет {user}, вызывая смех и веселье.",
    "tired": "{author} уставленно моргает в ответ на {user}, испытывая усталость.",
    "wave": "{author} машет рукой {user}, прощаясь или приветствуя.",
    "wink": "{author} подмигивает {user}, выражая свое одобрение или заинтересованность.",
    "woah": "{author} восклицает 'Вау!' в ответ на {user}, выражая свое удивление или восхищение.",
    "yawn": "{author} зевает рядом с {user}, испытывая сонливость или усталость.",
    "yay": "{author} восклицает 'Ура!' вместе с {user}, выражая свою радость и веселье.",
    "yes": "{author} утвердительно кивает головой перед {user}, выражая свое согласие или одобрение."
}, {
    "airkiss": "{author} отправляет воздушный поцелуй.",
    "angrystare": "{author} сердито смотрит куда-то.",
    "bite": "{author} нежно укусил.",
    "bleh": "{author} выражает отвращение.",
    "blush": "{author} краснеет.",
    "brofist": "{author} подает кулак.",
    "celebrate": "{author} радостно празднует.",
    "cheers": "{author} поднимает бокал.",
    "clap": "{author} аплодирует.",
    "confused": "{author} озадачен.",
    "cool": "{author} подмигивает.",
    "cry": "{author} горько плачет.",
    "cuddle": "{author} прижимается.",
    "dance": "{author} весело танцует.",
    "drool": "{author} слюнит.",
    "evillaugh": "{author} злобно смеется.",
    "facepalm": "{author} делает facepalm.",
    "handhold": "{author} берет за руку.",
    "happy": "{author} радостно улыбается.",
    "headbang": "{author} качает головой.",
    "hug": "{author} крепко обнимает.",
    "kiss": "{author} страстно целует.",
    "laugh": "{author} смеется.",
    "lick": "{author} лижет.",
    "love": "{author} глубоко любит.",
    "mad": "{author} сердится.",
    "nervous": "{author} нервничает.",
    "no": "{author} решительно отрицает.",
    "nom": "{author} удовлетворенно жует.",
    "nosebleed": "{author} начинает кровоточить из носа.",
    "nuzzle": "{author} прижимается.",
    "nyah": "{author} мурлычет.",
    "pat": "{author} ласково гладит.",
    "peek": "{author} заглядывает.",
    "pinch": "{author} остро пожимает.",
    "poke": "{author} тычет пальцем.",
    "pout": "{author} хмурится.",
    "punch": "{author} с силой бьет кулаком.",
    "roll": "{author} крутит глазами.",
    "run": "{author} бегает вокруг.",
    "sad": "{author} грустит.",
    "scared": "{author} испуган.",
    "shout": "{author} кричит.",
    "shrug": "{author} пожимает плечами.",
    "shy": "{author} стесняется.",
    "sigh": "{author} вздыхает.",
    "sip": "{author} глотает напиток.",
    "slap": "{author} жестко хлопает.",
    "sleep": "{author} идет спать.",
    "slowclap": "{author} медленно хлопает в ладоши.",
    "smack": "{author} бьет ладонью по губам.",
    "smile": "{author} улыбается.",
    "smug": "{author} выглядит довольным.",
    "sneeze": "{author} чихает.",
    "sorry": "{author} извиняется.",
    "stare": "{author} смотрит внимательно.",
    "stop": "{author} останавливается.",
    "surprised": "{author} удивлен.",
    "sweat": "{author} потеет.",
    "thumbsup": "{author} поднимает большой палец вверх.",
    "tickle": "{author} щекочет.",
    "tired": "{author} уставший.",
    "wave": "{author} машет рукой.",
    "wink": "{author} подмигивает.",
    "woah": "{author} восклицает 'Вау!'",
    "yawn": "{author} зевает.",
    "yay": "{author} восклицает 'Ура!'",
    "yes": "{author} утвердительно кивает головой."
}
]
all_reactions_type = Literal["airkiss", "angrystare", "bite", "bleh", "blush", "brofist", "celebrate", "cheers", "clap", "confused", "cool", "cry", "cuddle", "dance", "drool", "evillaugh", "facepalm", "handhold", "happy", "headbang", "hug", "kiss", "laugh", "lick", "love", "mad", "nervous", "no", "nom", "nosebleed", "nuzzle",
                             "nyah", "pat", "peek", "pinch", "poke", "pout", "punch", "roll", "run", "sad", "scared", "shout", "shrug", "shy", "sigh", "sip", "slap", "sleep", "slowclap", "smack", "smile", "smug", "sneeze", "sorry", "stare", "stop", "surprised", "sweat", "thumbsup", "tickle", "tired", "wave", "wink", "woah", "yawn", "yay", "yes"]


class ReactionsCommand(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot

        for react_type in typing.get_args(all_reactions_type):
            self.register_reaction_command(react_type)

    async def get_gif_with_react(self, react_type: all_reactions_type) -> str:
        params = {
            'reaction': react_type,
            'format': 'gif'
        }
        async with self.bot.session.get('https://api.otakugifs.xyz/gif', params=params) as responce:
            responce.raise_for_status()
            json = await responce.json()
            return json['url']

    def register_reaction_command(self, react_type: all_reactions_type) -> str:
        @commands.command(name=react_type)
        async def _react_command(ctx: commands.Context, user: Optional[nextcord.Member] = None):
            embed = nextcord.Embed(
                description=reactions_list[0 if user else 1].get(react_type).format(
                    author=ctx.author.mention, user=user.mention if user else None),

            )
            embed.set_image(await self.get_gif_with_react(react_type))

            await ctx.send(embed=embed)
        self.bot.add_command(_react_command)

    @commands.command()
    async def reactions(self, ctx: commands.Context, react_type: all_reactions_type, user: Optional[nextcord.Member] = None) -> None:
        embed = nextcord.Embed(
            description=reactions_list[0 if user else 1].get(react_type).format(
                author=ctx.author.mention, user=user.mention if user else None),

        )
        embed.set_image(await self.get_gif_with_react(react_type))

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ReactionsCommand(bot))
