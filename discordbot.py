
from discord.ext import commands
import discord

from os import getenv
import time
import traceback
import re

# white by kaiyade
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

scoremathuser = []


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    global scoremathuser

    try:
        if str(message.content)[0:2] == "tl":
            tlmsg = message.content
            tlsplit = tlmsg.split("\n")

            tlsp1 = tlsplit[0]

            try:
                tltime = re.sub(r"\D", "", tlsp1)
                if int(tltime) >= 21 and int(tltime) <= 90:
                    del tlsplit[0]
                    lp = 0
                    minus = False
                    delist = 0
                    for tlline in tlsplit:
                        if ":" in tlline:
                            linesplit = tlline.split(":")
                            lpt = 0
                            for i in range(len(linesplit) - 1):
                                up = str(linesplit[lpt])[-1]
                                down = str(linesplit[lpt + 1])[0:2]
                                try:
                                    up2 = str(linesplit[lpt])[-2]
                                except:
                                    up2 = ""

                                tmath = 0

                                tmath = int(up) * 60 + int(down)

                                tmath = int(tmath) - (90 - int(tltime))

                                if minus == False:
                                    if tmath <= 0:
                                        minus = True
                                        delist = lp

                                up = tmath // 60

                                if len(str(up)) == 2:
                                    up = str(up)[1:]

                                down = tmath % 60

                                try:
                                    if int(up2) == 0:
                                        up2 = ""
                                except:
                                    pass

                                down = "{0:02}".format(int(down))

                                linesplit[lpt] = linesplit[lpt][:-2] + str(up2) + str(up)
                                linesplit[lpt + 1] = str(down) + linesplit[lpt + 1][2:]

                                lpt += 1

                            tlsplit[lp] = ':'.join(linesplit)
                        lp += 1
                    if delist != 0:
                        for i in range(len(tlsplit) - delist):
                            del tlsplit[len(tlsplit) - 1]
                    endtl = '\n'.join(tlsplit)
                    if tltime != 90:
                        endtl = await message.channel.send("```" + "持ち越し" + tltime + "秒\n\n" + endtl + "```")
                    else:
                        endtl = await message.channel.send("```" + endtl + "```")

                    await endtl.add_reaction("📩")

                else:
                    sentmsg = await message.channel.send("エラー: 持ち越し時間")
                    await message.delete(delay=5)
                    await sentmsg.delete(delay=5)
            except:
                pass



        elif str(message.content)[0:1] == "=":
            try:
                if "スコア計算" in message.content:
                    spl = message.content.split()
                    await message.channel.send("```<段階> <ボス(整数)> <ダメージ>```")
                    if int(message.author.id) in scoremathuser:
                        pass
                    else:
                        scoremathuser.append(int(message.author.id))

                elif "sc" in message.content:
                    spl = message.content[4:].split()
                    d = await scoremag(int(spl[0]), int(spl[1]))
                    score = spl[2].replace(",", "")
                    score = float(d) * int(score)
                    score = '{:,}'.format(int(score))
                    await message.channel.send(score)

                elif "m" in message.content:
                    if "-" in message.content:
                        await message.channel.send("正の整数を入力してください")
                        return
                    if "s" not in message.content:
                        spl = message.content[3:].split()
                        ans = ((int(spl[1]) - int(spl[0])) / int(spl[1])) * 90 + 20

                        if "." in str(ans):
                            anssp = str(ans).split(".")
                            ans = int(anssp[0])
                            if int(anssp[1]) != 0:
                                ans += 1

                        if ans > 90:
                            ans = 90

                        if ans < 21:
                            await message.channel.send("持ち越し不可能です")
                        else:
                            await message.channel.send(str(ans) + " 秒の持ち越しが可能です")

                    else:
                        spl = message.content[3:].split()
                        if int(spl[1][:2]) <= 90 and int(spl[1][:2]) > 20:

                            ans = int(spl[0]) / (1 - (((int(spl[1][:2]) - 0.99999999) - 20) / 90))

                            if "." in str(ans):
                                anssp = str(ans).split(".")
                                ans = int(anssp[0])
                                if int(anssp[1]) != 0:
                                    ans += 1

                            await message.channel.send(str(spl[1][:2]) + " 秒持ち越すための最低ダメージは " + str(ans) + " です")
                        else:
                            await message.channel.send("持ち越し時間は21～90の間で指定してください")

                else:
                    temp = message.content[1:].replace('×', '*')
                    temp = temp.replace('x', '*')
                    temp = temp.replace('÷', '/')
                    math = await message.channel.send(eval(temp))
            except:
                pass



        elif str(message.content)[0:6] == ";;help":
            try:
                await message.channel.send(
                    "```tl <秒数> - TLを変換\n" + "= <計算式> - 計算\n" + "=スコア計算 - クラバトのスコアの計算(複数同時計算用)\n" + "=sc <段階> <ボス(整数)> <ダメージ> - スコア計算\n" + "=m <残りHP> <与ダメージ> - 持ち越し秒数の計算\n" + "=m <残りHP> <持ち越し時間>s - 指定した持ち越し時間に必要な最低ダメージを計算```")

            except:
                pass

        elif str(message.content)[0:16] == "deploymentserver":
            try:
                guildlist = ""
                for item in bot.guilds:
                    guildlist = str(guildlist) + str(item) + ", "

                await message.channel.send("サーバー数: " + str(len(bot.guilds)) + "\n" + "一覧: " + str(guildlist))
            except:
                pass

        else:
            if int(message.author.id) in scoremathuser:
                msg = message.content

                msg = msg.replace(",", "")
                scorelist = []

                if "\n" in msg:
                    spline = msg.split("\n")
                else:
                    spline = [msg]
                amount = 0

                for line in spline:
                    item = line.split()

                    d = await scoremag(int(item[0]), int(item[1]))

                    score = d * int(item[2])
                    score = int(score)

                    score = '{:,}'.format(score)

                    scorelist.append(str(score))

                    amount += int(d * int(item[2]))

                if len(scorelist) == 1:
                    scores = scorelist[0]
                    await message.channel.send(scores)
                else:
                    scores = '\n'.join(scorelist)

                    await message.channel.send(scores + "\n\n" + "{:,}".format(amount))

                looptime = 0
                for item in scoremathuser:
                    if str(item) == str(message.author.id):
                        del scoremathuser[looptime]
                        break

                    looptime += 1

        logchannel = bot.get_channel(893860509902856202)
        msg_id = 893860755785547836
        datamsg = await logchannel.fetch_message(msg_id)
        data = str(datamsg.content).replace("[", "")
        data = data.replace("]", "")
        data = data.replace("'", "")
        try:
            data = data.split(", ")
        except:
            pass

        if str(message.guild.id) not in str(data):
            guild = datamsg.guild
            category = guild.get_channel(893860113717293107)
            ch = await category.create_text_channel(name=message.guild.name)
            data.append(str(message.guild.id) + " " + str(ch.id))
            await datamsg.edit(content=data)

        if str(message.guild.id) in str(data):
            for item in data:
                if str(message.guild.id) in str(item):
                    item = item.split()
                    sendchannel = bot.get_channel(int(item[1]))
                    author = str(message.author).split("#")
                    try:
                        global name
                        if str(name) == str(message.author):
                            await sendchannel.send("\n>> " + message.content)
                        else:
                            await sendchannel.send(str(author[0]) + "\n>> " + message.content)
                    except:
                        pass
                    name = str(message.author)
                    for item in message.attachments:
                        await sendchannel.send(item)

        # await datamsg.edit(content="['707068450866069544 893873726477697035', '646245538022293512 893877531160219688']")

    except:
        pass


@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if reaction.emoji == ("📩"):
        if ":" in reaction.message.content and reaction.message.author.bot:
            channel = await user.create_dm()
            await channel.send(reaction.message.content)


async def scoremag(a, b):
    if int(a) == 1:
        if int(b) == 1:
            c = 1.2
        elif int(b) == 2:
            c = 1.2
        elif int(b) == 3:
            c = 1.3
        elif int(b) == 4:
            c = 1.4
        elif int(b) == 5:
            c = 1.5

    elif int(a) == 2:
        if int(b) == 1:
            c = 1.6
        elif int(b) == 2:
            c = 1.6
        elif int(b) == 3:
            c = 1.8
        elif int(b) == 4:
            c = 1.9
        elif int(b) == 5:
            c = 2.0

    elif int(a) == 3:
        if int(b) == 1:
            c = 2.0
        elif int(b) == 2:
            c = 2.0
        elif int(b) == 3:
            c = 2.4
        elif int(b) == 4:
            c = 2.4
        elif int(b) == 5:
            c = 2.6

    elif int(a) == 4 or int(a) == 5:
        if int(b) == 1:
            c = 3.5
        elif int(b) == 2:
            c = 3.5
        elif int(b) == 3:
            c = 3.7
        elif int(b) == 4:
            c = 3.8
        elif int(b) == 5:
            c = 4.0

    return c


@bot.event
async def on_ready():
    count = len(bot.guilds)
    await bot.change_presence(activity=discord.Game(name=";;help", type=1))


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
