# python -m venv venv
#venv\Scripts\activate

#só com teclas
import pyautogui as bot

bot.PAUSE = 1

bot.press('win')
bot.PAUSE = 1
bot.write('teste.xlsx')
bot.PAUSE = 1
bot.press('enter')
bot.click(x=183,y=70)
bot.click(x=60,y=254)

bot.PAUSE = 1
bot.write("Teste 1")
bot.PAUSE = 1
bot.press('tab')
bot.PAUSE = 1
bot.write("Teste 2")

