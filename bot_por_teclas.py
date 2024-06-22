# python -m venv venv
#venv\Scripts\activate

#só com teclas
import pyautogui as bot
1
bot.PAUSE = 1

bot.press('win')
bot.write('teste.xlsx')
bot.press('enter')
bot.click(x=183,y=70)
bot.click(x=60,y=254)
for numero in range(0,5):
    bot.write("Teste 1")
    bot.press('tab')
    bot.write("Teste 2")

