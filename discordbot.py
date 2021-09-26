from discord.ext import commands
import discord
import time
import re

from os import getenv
import traceback


intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(command_prefix='/', intents=intents)




@bot.event
async def on_message(message):
    if message.author.bot:
        return

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

                                linesplit[lpt] = linesplit[lpt][:-1] + str(up)
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
                await message.channel.send("```tl <秒数> - TLを変換\n" + "= <計算式> - 計算```")
                
            except:
                pass
        
    except:
        pass



@bot.event
async def on_ready():
    print('{0.user}がログインしました'.format(bot))
    count = len(bot.guilds)
    await bot.change_presence(activity=discord.Game(name=";;help", type=1))


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
