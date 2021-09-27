from discord.ext import commands
import discord


from os import getenv
import time
import traceback
import re

#white by kaiyade
intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(command_prefix='/', intents=intents)




scoremathuser = []
d = 0

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    global scoremathuser, d

    try:
        if str(message.content)[0:2] == "tl":
            tlmsg = message.content
            tlsplit = tlmsg.split("\n")

            tlsp1 = tlsplit[0]
            
            
            try:
                tltime = re.sub(r"\D", "", tlsp1)
                if int(tltime) >= 21 and int(tltime) <= 89:
                    del tlsplit[0]
                    lp = 0
                    minus = False
                    delist = 0
                    for tlline in tlsplit:
                        if ":" in tlline:
                            linesplit = tlline.split(":")
                            lpt = 0
                            for i in range(len(linesplit)-1):
                                up2 = str(linesplit[lpt])[-2]
                                up = str(linesplit[lpt])[-1]
                                down = str(linesplit[lpt+1])[0:2]
    
                            
                                tmath = 0

                                tmath = int(up)*60 + int(down)

                                tmath = int(tmath) - (90-int(tltime))

                                if minus == False:
                                    if tmath <= 0:
                                        minus = True
                                        delist = lp

                                up = tmath // 60

                                if len(str(up)) == 2:
                                    up = str(up)[1:]

   
                                down = tmath % 60


                                down = "{0:02}".format(int(down))

                                try:
                                    if int(up2) == 0:
                                        up2 = ""
                                except:
                                    pass

                                linesplit[lpt] = linesplit[lpt][:-2] + str(up)
                                linesplit[lpt+1] = str(down) + linesplit[lpt+1][2:]

                                lpt+=1

                            


                            tlsplit[lp] = ':'.join(linesplit)
                        lp+=1 
                    if delist != 0:
                        for i in range(len(tlsplit)-delist):
                            del tlsplit[len(tlsplit)-1]
                    endtl= '\n'.join(tlsplit)
                    endtl = await message.channel.send("```"+"持ち越し"+ tltime +"秒\n\n"+endtl+"```")

            
                else:
                    sentmsg = await message.channel.send("エラー: 持ち越し時間")
                    await message.delete(delay=5)
                    await sentmsg.delete(delay=5)
            except:
                pass

        

        elif str(message.content)[0:2] == "= ":
            try:
                if "スコア計算" in message.content:
                    spl = message.content.split()
                    await message.channel.send("```<段階> <ボス(整数)> <ダメージ>```")
                    if int(message.author.id) in scoremathuser:
                        pass
                    else:
                        scoremathuser.append(int(message.author.id))
                else:
                    temp = message.content[2:].replace('×', '*')
                    temp = temp.replace('x', '*')
                    temp = temp.replace('÷', '/')
                    math = await message.channel.send(eval(temp))
            except:
                pass

        elif str(message.content)[0:16] == "deploymentserver":
            try:
                guildlist = ""
                for item in bot.guilds:
                    guildlist = str(guildlist) + str(item) + ", " 

                await message.channel.send("サーバー数: "+ str(len(bot.guilds))+ "\n" + "一覧: " + str(guildlist))
            except:
                pass

        elif str(message.content)[0:6] == ";;help":
            try:
                await message.channel.send("```tl <秒数> - TLを変換\n" + "= <計算式> - 計算\n" + "= スコア計算 - クラバトのスコアの計算```")
                
            except:
                pass

        else:
            if int(message.author.id) in scoremathuser:
                msg = message.content

                msg = msg.replace(",", "")
                scorelist = []

                if "\n" in  msg:
                    spline = msg.split("\n")
                else:
                    spline = [msg]
                amount = 0
                
                for line in spline:
                    item = line.split()

                    if int(item[0]) == 1:
                        if int(item[1]) == 1:
                            d = 1.2
                        elif int(item[1]) == 2:
                            d = 1.2
                        elif int(item[1]) == 3:
                            d = 1.3
                        elif int(item[1]) == 4:
                            d = 1.4
                        elif int(item[1]) == 5:
                            d = 1.5

                    elif int(item[0]) == 2:
                        if int(item[1]) == 1:
                            d = 1.6
                        elif int(item[1]) == 2:
                            d = 1.6
                        elif int(item[1]) == 3:
                            d = 1.8
                        elif int(item[1]) == 4:
                            d = 1.9 
                        elif int(item[1]) == 5:
                            d = 2.0

                    elif int(item[0]) == 3:
                        if int(item[1]) == 1:
                            d = 2.0
                        elif int(item[1]) == 2:
                            d = 2.0
                        elif int(item[1]) == 3:
                            d = 2.4
                        elif int(item[1]) == 4:
                            d = 2.4
                        elif int(item[1]) == 5:
                            d = 2.6

                    elif int(item[0]) == 4 or int(item[0]) == 5:
                        if int(item[1]) == 1:
                            d = 3.5
                        elif int(item[1]) == 2:
                            d = 3.5
                        elif int(item[1]) == 3:
                            d = 3.7
                        elif int(item[1]) == 4:
                            d = 3.8
                        elif int(item[1]) == 5:
                            d = 4.0

                    score = d *int(item[2])
                    score = int(score)
                    
                    score = '{:,}'.format(score)

                    scorelist.append (str(score))

                    amount += int(d*int(item[2]))

                    

                if len(scorelist) == 1:
                    scores = scorelist[0]
                    await message.channel.send(scores)
                else:
                    scores= '\n'.join(scorelist)
                    
                    await message.channel.send(scores + "\n\n" + "{:,}".format(amount))

                looptime = 0
                for item in scoremathuser:
                    if str(item) == str(message.author.id):
                        del scoremathuser[looptime]
                        break

                    looptime += 1
                    
    except:
        pass

@bot.event
async def on_ready():
    count = len(bot.guilds)
    await bot.change_presence(activity=discord.Game(name=";;help", type=1))


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
