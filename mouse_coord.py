import pyautogui as auto  # captura da coordenada do mouse
from PySimpleGUI import PySimpleGUI as sg  # criação da interface gráfica
from datetime import datetime  # data e horário local
import os.path  # import necessário para verificar existência do log.txt no diretório do script

data_hora = datetime.now().strftime('%d/%m/%Y %H:%M')


# captura resolução da tela e retorna os valores de X e Y
resolucao = auto.size()
x = resolucao[0]
y = resolucao[1]


def usa_multimonitor(coordx, coordy):
    if coordy == 1080 and coordx > 1920:
        return True
    elif coordy == 1080 and coordx == 1920:
        return False
    elif coordy == 1440 and coordx > 2560:
        return True
    elif coordy == 1440 and coordx == 2560:
        return False


def obter_resolucao_tela(teste):
    if teste:
        x_real = int(x / 2)
        return x_real, y
    else:
        return x, y


teste_monitores = usa_multimonitor(x, y)


def criar_log():
    log_existente = os.path.exists('log.txt')  # confere existência do log no diretório do script
    if log_existente:
        print('Log já existe.')
    else:
        with open('log.txt', 'x') as log:
            print('Log não existe.\nCriando agora...')
            log.write(f'{data_hora} - Resolução do monitor: {obter_resolucao_tela(teste_monitores)}')


def registrar_coord(data, locx, locy):
    # append de novas coordenadas capturadas no arquivo log
    with open('log.txt', 'a+') as log:
        log.write(f'\n{data}: {locx}, {locy}')


def obter_mouse_coord():
    # captura coordenadas do mouse
    coord_agora = auto.position()
    x_agora = coord_agora[0]
    y_agora = coord_agora[1]
    # return x_agora, y_agora
    if teste_monitores:
        if x_agora < x / 2:
            registrar_coord(data_hora, x_agora, y_agora)  # salva coordenada no log externo
            return x_agora, y_agora
        elif x_agora > x / 2:
            dif_x = int(x_agora - x / 2)  # correção para o valor de x, caso esteja capturando coord no monitor 2
            registrar_coord(data_hora, dif_x, y_agora)  # salva coordenada no log externo
            return dif_x, y_agora
    elif not teste_monitores:
        registrar_coord(data_hora, x_agora, y_agora)  # salva coordenada no log externo
        return x_agora, y_agora


def hotkey():
    obter_mouse_coord()


def res_total():
    if teste_monitores:
        return f'Resolução total: ({x},{y})\n'
    else:
        pass


sg.theme('Reddit')
criar_log()
layout = [[sg.Text('Aperte F10 para capturar as coordenadas da posição do mouse.\nAs coordendas serão salvas no arquivo'
                   ' log.txt.')],
          [sg.Text('Últimas coordendas salvas:')],
          [sg.Multiline(f'Resolução do monitor: {obter_resolucao_tela(True)}\n{res_total()}',
                        size=(60, 5), key='multiline-box', auto_refresh=True)]]

window = sg.Window('Log das Coordenadas do Mouse', layout, keep_on_top=True, finalize=True, location=(960, 540))
window.bind('<F10>', hotkey)

while True:  # Event Loop
    evento, valores = window.read()
    window['multiline-box'].Update(f'{data_hora}: {obter_mouse_coord()}\n', append=True,
                                   autoscroll=True)
    if evento in (sg.WIN_CLOSED, 'Quit'):
        break

window.close()
