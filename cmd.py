""""""
""""
import csv
import random
import discord
from discord.ext import commands
from discord.ui import Select, SelectOption

  #システム/ストーリー/テクスチャ/アクション/サウンドのパラーメタを
  #Par変数に格納する。[0][1][2][3][4]それぞれに数値で格納。
  #[0]=sys（システム）
  #[1]=STO（ストーリー）
  #[2]=tex(テクスチャ)
  #[3]=act（アクション）
  #[4]=sou（サウンド）
  #以上で定義するものとする。


#Gameコマンド====================================
# " ?game 技能値 "　コマンドが入力されたら、gameの処理を行う。
bot = commands.Bot(command_prefix="?")
@bot.command()
async def game(ctx, arg):
  skill = int(arg)
    
#最初のコンピュータ技能判定＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
if random.randint(1,100) <= skill:

  #ゲーム種類選択処理＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
  #game.csvを読み込む
  with open('game.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)

  #ドロップダウンメニュー＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
    
  # Viewクラスを継承してButtonを持ったViewを
  class TestView(discord.ui.View):

  # デコレータを使ってSelectオブジェクトをViewのitemsに格納する
    @discord.ui.select(placeholder="制作するゲームの種別を選択してください",         
        options = [
        SelectOption(label='ハウスコンピューター', value='ハウスコンピューター'),
        SelectOption(label='アタレ1500', value='アタレ1500'),
        SelectOption(label='スーパーハウコン', value='スーパーハウコン'),
        SelectOption(label='ギガドライブ', value='ギガドライブ'),
        SelectOption(label='サガリターン', value='サガリターン'),
        SelectOption(label='PlayVerse', value='PlayVerse'),
        SelectOption(label='MANTENDO46', value='MANTENDO46'),
        SelectOption(label='ドリームブロード', value='ドリームブロード'),
        SelectOption(label='PlayVerse2', value='PlayVerse2'),
        SelectOption(label='ゲームブロック', value='ゲームブロック')
        ],
        )
    
  #ドロップダウンメニュー＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿/

    #総合値算出＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
    #初期値設定
    i=0
    x_game=1
    y_game=1

    #合算処理が終わるまでループ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
    while i != 1

      #選択したゲームと一致判定＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
      if select.values[0]  =  values[1][y_game]

          #合算処理____________________________________
          while x_game != 6

            Par[x_game] = values[x_game][y_game] + random.randint(1,100)

            x_game = x_game + 1

          break;
          #合算______________________________________/

        i=1
        y_ygame = y_game + 1

      #選択したゲームと一致判定＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿/
      else:

    break;
    #総合値算出＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿/



#バグ処理＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
dic = random.randint(1,100)

#判定________________________________________
if dic <= skill:

  #クリティカル処理____________________
  if skill-5 <= dic
    bug = 0
  #クリティカル処理＿＿＿＿＿＿＿＿＿＿＿＿/

  #通称成功処理＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
  else:
    bug = random.randint(1,400)/2
  #通常成功処理＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿/

else:
  #ファンブル判定____________________
  if 96 <= dic
    bug = random.randint(1,400) * 4
  #ファンブル判定___________________/

  #通常失敗処理_______________________
  else:
  random.randint(1,400)*2
  #通常失敗処理____________________/

#判定________________________________________/
#バグ処理＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿/

#収入計算＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
#初期値設定
  i = 0
  inc = 0

#パラメーターの値を収入として合算処理
  while i != 6
    inc = Par[i] + inc 
    i = i + 1
  break;
#パラメーターの値を収入として合算処理/

#収入-バグ
inc = (inc * 10) - (bug * 10)
#収入計算＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿/
#最初のコンピューター処理に失敗_____________________________
else:
        send_message = "コンピューター技能に失敗しました。" 
        await message.channel.send(send_message)

#最初のコンピューター処理に失敗_____________________________/
"""
#Gameコマンド====================================//

