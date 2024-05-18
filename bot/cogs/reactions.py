from typing import Literal, Optional
import typing
import nextcord
from nextcord.ext import commands
from bot.databases import GuildDateBases
from bot.misc.lordbot import LordBot


class GreedyUser(str):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}['{self}']"

    def __class_getitem__(cls, param: str) -> 'GreedyUser':
        return cls(param)


reactions_list = {
    "with_user": {
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
    },
    "no_user": {
        "angrystare": "{author} сердито смотрит куда-то.",
        "bleh": "{author} выражает отвращение.",
        "blush": "{author} краснеет.",
        "brofist": "{author} подает кулак.",
        "celebrate": "{author} радостно празднует.",
        "cheers": "{author} поднимает бокал.",
        "clap": "{author} аплодирует.",
        "confused": "{author} озадачен.",
        "cry": "{author} горько плачет.",
        "dance": "{author} весело танцует.",
        "drool": "{author} слюнит.",
        "evillaugh": "{author} злобно смеется.",
        "facepalm": "{author} делает facepalm.",
        "happy": "{author} радостно улыбается.",
        "headbang": "{author} качает головой.",
        "laugh": "{author} смеется.",
        "mad": "{author} сердится.",
        "nervous": "{author} нервничает.",
        "no": "{author} решительно отрицает.",
        "nom": "{author} удовлетворенно жует.",
        "nosebleed": "{author} начинает кровоточить из носа.",
        "nyah": "{author} мурлычет.",
        "peek": "{author} заглядывает.",
        "pout": "{author} хмурится.",
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
        "smile": "{author} улыбается.",
        "smug": "{author} выглядит довольным.",
        "sneeze": "{author} чихает.",
        "stare": "{author} смотрит внимательно.",
        "stop": "{author} останавливается.",
        "surprised": "{author} удивлен.",
        "sweat": "{author} потеет.",
        "thumbsup": "{author} поднимает большой палец вверх.",
        "tired": "{author} уставший.",
        "woah": "{author} восклицает 'Вау!'",
        "yawn": "{author} зевает.",
        "yay": "{author} восклицает 'Ура!'",
        "yes": "{author} утвердительно кивает головой."
    }
}

AllReactionsType = Literal[GreedyUser['airkiss'], 'angrystare', GreedyUser['bite'], 'bleh', 'blush', 'brofist', 'celebrate', 'cheers', 'clap', 'confused', GreedyUser['cool'], 'cry', GreedyUser['cuddle'], 'dance', 'drool', 'evillaugh', 'facepalm', GreedyUser['handhold'], 'happy', 'headbang', GreedyUser['hug'], GreedyUser['kiss'], 'laugh', GreedyUser['lick'], GreedyUser['love'], 'mad', 'nervous', 'no', 'nom', 'nosebleed',  # type: ignore
                           GreedyUser['nuzzle'], 'nyah', GreedyUser['pat'], 'peek', GreedyUser['pinch'], GreedyUser['poke'], 'pout', GreedyUser['punch'], 'roll', 'run', 'sad', 'scared', 'shout', 'shrug', 'shy', 'sigh', 'sip', 'slap', 'sleep', 'slowclap', GreedyUser['smack'], 'smile', 'smug', 'sneeze', GreedyUser['sorry'], 'stare', 'stop', 'surprised', 'sweat', 'thumbsup', GreedyUser['tickle'], 'tired', GreedyUser['wave'], GreedyUser['wink'], 'woah', 'yawn', 'yay', 'yes']  # type: ignore


class ReactionsCommand(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot

        for react_type in typing.get_args(AllReactionsType):
            self.register_command(react_type)

    def register_command(self, react_type: AllReactionsType) -> None:
        @commands.command(name=react_type)
        async def _react_type_callback(ctx: commands.Context, user: Optional[nextcord.Member] = None, *, comment: Optional[str] = None):
            await self.reactions(ctx, react_type, user, comment=comment)
        self.bot.add_command(_react_type_callback)

    async def get_gif_with_react(self, react_type: AllReactionsType) -> str:
        params = {
            'reaction': react_type,
            'format': 'gif'
        }
        async with self.bot.session.get('https://api.otakugifs.xyz/gif', params=params) as responce:
            responce.raise_for_status()
            json = await responce.json()
            return json['url']

    @commands.command()
    async def reactions(self, ctx: commands.Context, react_type: AllReactionsType, user: Optional[nextcord.Member] = None, *, comment: Optional[str] = None) -> None:
        gdb = GuildDateBases(ctx.guild.id)
        color = await gdb.get('color')

        if user is None and isinstance(react_type, GreedyUser):
            await ctx.send("You must specify the user")
            return

        if user is None:
            embed = nextcord.Embed(
                description=reactions_list['no_user'].get(react_type).format(
                    author=ctx.author.mention),
                color=color
            )
        else:
            embed = nextcord.Embed(
                description=reactions_list['with_user'].get(react_type).format(
                    author=ctx.author.mention, user=user.mention),
                color=color
            )
        if comment:
            embed.add_field(
                name='Comment',
                value=comment
            )
        embed.set_image(await self.get_gif_with_react(react_type))

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ReactionsCommand(bot))
