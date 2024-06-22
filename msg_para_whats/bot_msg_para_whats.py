import pyautogui as bot

#necessario está em outra aba
bot.click('brave.png') #print do icone do navegador
bot.click('whats.png') #icone do what na guia do navegador
bot.click('bp.png') #barra de pesquisa principal
bot.write("arquivo") #nome do grupo
bot.press("enter")
bot.write("Bom dia a todos")
bot.press("enter")
