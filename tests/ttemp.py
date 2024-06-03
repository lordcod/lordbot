all_reactions_type = ["airkiss", "angrystare", "bite", "bleh", "blush", "brofist", "celebrate", "cheers", "clap", "confused", "cool", "cry", "cuddle", "dance", "drool", "evillaugh", "facepalm", "handhold", "happy", "headbang", "hug", "kiss", "laugh", "lick", "love", "mad", "nervous", "no", "nom", "nosebleed", "nuzzle",
                      "nyah", "pat", "peek", "pinch", "poke", "pout", "punch", "roll", "run", "sad", "scared", "shout", "shrug", "shy", "sigh", "sip", "slap", "sleep", "slowclap", "smack", "smile", "smug", "sneeze", "sorry", "stare", "stop", "surprised", "sweat", "thumbsup", "tickle", "tired", "wave", "wink", "woah", "yawn", "yay", "yes"]


cmd = """
    @commands.command()
    async def {react_type}(ctx: commands.Context, user: Optional[nextcord.Member] = None):
        embed = nextcord.Embed(
            description=reactions_list[0 if user else 1].get('{react_type}').format(
                author=ctx.author.mention, user=user.mention if user else None),

        )
        embed.set_image(await self.get_gif_with_react('{react_type}'))

        await ctx.send(embed=embed)
"""
for rt in all_reactions_type:
    print(cmd.format(react_type=rt))
