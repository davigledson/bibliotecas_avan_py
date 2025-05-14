import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from matplotlib.backend_bases import MouseEvent
from PIL import Image
import io
import requests


class InteractiveFloorPlan:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(20, 12))
        self.ax.set_xlim(0, 200)
        self.ax.set_ylim(0, 120)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.fig.suptitle('Setor de Turismo - Layout Linear com Área Verde (Arraste os elementos)', fontsize=16)

        # Elementos arrastáveis
        self.draggable_patches = {}
        self.current_patch = None
        self.start_offset = (0, 0)

        # Estilos
        self.styles = {
            'wall': {'linewidth': 2, 'edgecolor': 'black', 'facecolor': '#f5f5f5'},
            'door': {'linewidth': 1, 'edgecolor': '#8B4513', 'facecolor': '#D2B48C'},
            'window': {'linewidth': 1, 'edgecolor': 'black', 'facecolor': '#87CEEB'},
            'desk': {'linewidth': 1, 'edgecolor': 'black', 'facecolor': '#F5DEB3'},
            'chair': {'linewidth': 1, 'edgecolor': 'black', 'facecolor': '#8B4513'},
            'corridor': {'linewidth': 0, 'facecolor': '#F0F0F0'},
            'text': {'ha': 'center', 'va': 'center', 'fontsize': 9, 'fontweight': 'bold'}
        }

        # Conectar eventos
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)

        self.draw_layout()
        self.setup_legend()

    def draw_layout(self):
        """Desenha o layout linear com corredor único e área verde"""
        # Corredor principal (vertical)
        corridor_width = 15
        corridor_length = 100
        corridor_x = 100
        self.ax.add_patch(patches.Rectangle(
            (corridor_x, 20), corridor_width, corridor_length,
            **self.styles['corridor']))

        # Área verde (mato) no lado direito
        self.draw_green_area(corridor_x + corridor_width + 5, 20, 70, corridor_length)

        # Salas no lado esquerdo do corredor (todas voltadas para a área verde)
        room_width = 40
        room_height = 25
        room_spacing = 5

        # Lista de salas
        rooms = [
            {"name": "Sala 101\nAula", "type": "classroom"},
            {"name": "Sala 102\nAula", "type": "classroom"},
            {"name": "Lab 103\nInformática", "type": "lab"},
            {"name": "Sala 104\nReuniões", "type": "meeting"}
        ]

        for i, room in enumerate(rooms):
            room_x = corridor_x - room_width - 5
            room_y = 25 + i * (room_height + room_spacing)

            # Desenhar sala
            self.draw_room(room_x, room_y, room_width, room_height, room["name"], room["type"])

    def draw_room(self, x, y, width, height, name, room_type):
        """Desenha uma sala completa com mobiliário"""
        # Parede externa
        self.ax.add_patch(patches.Rectangle(
            (x, y), width, height, **self.styles['wall']))

        # Porta para o corredor (parede direita)
        door_width = width / 6
        self.ax.add_patch(patches.Rectangle(
            (x + width - 2, y + height / 2 - door_width / 2),
            2, door_width, **self.styles['door']))

        # Janelas para a área verde (parede esquerda)
        window_height = height / 4
        self.ax.add_patch(patches.Rectangle(
            (x, y + height / 4), 2, window_height, **self.styles['window']))
        self.ax.add_patch(patches.Rectangle(
            (x, y + 3 * height / 4 - window_height / 2),
            2, window_height, **self.styles['window']))

        # Mobiliário conforme o tipo de sala
        if room_type == "classroom":
            self.draw_classroom_furniture(x, y, width, height, name.replace('\n', ''))
        elif room_type == "lab":
            self.draw_lab_furniture(x, y, width, height, name.replace('\n', ''))
        elif room_type == "meeting":
            self.draw_meeting_room(x, y, width, height, name.replace('\n', ''))

        # Nome da sala
        self.ax.text(x + width / 2, y + height + 2, name, **self.styles['text'])

    def draw_classroom_furniture(self, x, y, width, height, room_name):
        """Desenha mobiliário de sala de aula"""
        # Quadro verde
        self.ax.add_patch(patches.Rectangle(
            (x + width / 4, y + height - 5), width / 2, 3,
            facecolor='#2E8B57', edgecolor='black'))

        # Fileiras de mesas (3x2)
        desk_width, desk_height = width / 5, height / 8
        chair_radius = desk_height / 3

        for row in range(2):
            for col in range(3):
                desk_x = x + width / 8 + col * (width / 3.5)
                desk_y = y + height / 4 + row * (height / 3)

                # Mesa
                desk = patches.Rectangle(
                    (desk_x, desk_y), desk_width, desk_height,
                    **self.styles['desk'])
                self.ax.add_patch(desk)

                # Cadeiras
                chair1 = patches.Circle(
                    (desk_x + desk_width / 3, desk_y + desk_height + chair_radius / 2),
                    chair_radius, **self.styles['chair'])
                chair2 = patches.Circle(
                    (desk_x + 2 * desk_width / 3, desk_y + desk_height + chair_radius / 2),
                    chair_radius, **self.styles['chair'])

                self.ax.add_patch(chair1)
                self.ax.add_patch(chair2)

                # Adicionar à lista de elementos arrastáveis
                self.draggable_patches[f"{room_name}_desk_{row}_{col}"] = {
                    'patch': desk, 'type': 'desk', 'x': desk_x, 'y': desk_y,
                    'chairs': [chair1, chair2]
                }

    def draw_lab_furniture(self, x, y, width, height, room_name):
        """Desenha mobiliário de laboratório de informática"""
        # Computadores em U
        desk_width, desk_height = width / 4, height / 6
        for i, pos in enumerate([(x + width / 8, y + height / 3),
                                 (x + width / 2 - desk_width / 2, y + height - desk_height - 5),
                                 (x + width - width / 8 - desk_width, y + height / 3)]):
            desk_x, desk_y = pos

            # Mesa
            desk = patches.Rectangle(
                (desk_x, desk_y), desk_width, desk_height,
                **self.styles['desk'])
            self.ax.add_patch(desk)

            # Monitor
            monitor = patches.Rectangle(
                (desk_x + 1, desk_y + 1), desk_width - 2, desk_height / 3,
                facecolor='black')
            self.ax.add_patch(monitor)

            # Cadeira
            chair = patches.Circle(
                (desk_x + desk_width / 2, desk_y + desk_height + desk_height / 4),
                desk_height / 3, **self.styles['chair'])
            self.ax.add_patch(chair)

            # Adicionar à lista de elementos arrastáveis
            self.draggable_patches[f"{room_name}_pc_{i}"] = {
                'patch': desk, 'type': 'computer', 'x': desk_x, 'y': desk_y,
                'monitor': monitor, 'chair': chair
            }

    def draw_meeting_room(self, x, y, width, height, room_name):
        """Desenha mobiliário de sala de reuniões"""
        # Mesa central
        table = patches.Ellipse(
            (x + width / 2, y + height / 2), width * 0.7, height * 0.6,
            facecolor='#F5DEB3', edgecolor='black')
        self.ax.add_patch(table)

        # Cadeiras ao redor (8 cadeiras)
        chair_radius = height / 12
        for i in range(8):
            angle = 2 * np.pi * i / 8
            chair_x = x + width / 2 + (width * 0.35 + chair_radius * 1.5) * np.cos(angle)
            chair_y = y + height / 2 + (height * 0.3 + chair_radius * 1.5) * np.sin(angle)

            chair = patches.Circle(
                (chair_x, chair_y), chair_radius,
                **self.styles['chair'])
            self.ax.add_patch(chair)

            # Adicionar à lista de elementos arrastáveis
            self.draggable_patches[f"{room_name}_chair_{i}"] = {
                'patch': chair, 'type': 'chair', 'x': chair_x, 'y': chair_y
            }

        self.draggable_patches[f"{room_name}_table"] = {
            'patch': table, 'type': 'table', 'x': x + width / 2, 'y': y + height / 2
        }

    def draw_green_area(self, x, y, width, height):
        """Desenha a área verde com ícone de mato"""
        # Fundo verde
        self.ax.add_patch(patches.Rectangle(
            (x, y), width, height,
            facecolor='#90EE90', edgecolor='#2E8B57', linewidth=2))

        # Texto
        self.ax.text(x + width / 2, y + height / 2, "Área Verde\n(Mato)",
                     ha='center', va='center', fontsize=12, color='#006400')

        # Ícones de plantas/mato
        plant_icon = "🌿"  # Emoji de planta (pode substituir por imagem)
        for i in range(15):
            plant_x = x + width * np.random.uniform(0.1, 0.9)
            plant_y = y + height * np.random.uniform(0.1, 0.9)
            self.ax.text(plant_x, plant_y, plant_icon, fontsize=14, ha='center', va='center')

    def setup_legend(self):
        """Configura a legenda interativa"""
        legend_elements = [
            patches.Patch(facecolor='#F5DEB3', edgecolor='black', label='Mesas'),
            patches.Patch(facecolor='#8B4513', edgecolor='black', label='Cadeiras'),
            patches.Patch(facecolor='#90EE90', edgecolor='#2E8B57', label='Área Verde'),
            patches.Patch(facecolor='#F0F0F0', label='Corredor'),
            patches.Patch(facecolor='#2E8B57', label='Quadro')
        ]

        self.ax.legend(
            handles=legend_elements,
            loc='upper left',
            bbox_to_anchor=(0.01, 0.99),
            fontsize=10,
            title="Legenda:",
            title_fontsize=11
        )

    def on_press(self, event):
        """Evento quando o botão do mouse é pressionado"""
        if event.inaxes != self.ax:
            return

        for name, item in self.draggable_patches.items():
            patch = item['patch']

            if isinstance(patch, patches.Rectangle):
                patch_x, patch_y = patch.get_xy()
                patch_width = patch.get_width()
                patch_height = patch.get_height()

                if (patch_x <= event.xdata <= patch_x + patch_width and
                        patch_y <= event.ydata <= patch_y + patch_height):
                    self.current_patch = name
                    self.start_offset = (event.xdata - patch_x, event.ydata - patch_y)
                    break

            elif isinstance(patch, patches.Circle):
                center = patch.center
                radius = patch.radius

                if ((event.xdata - center[0]) ** 2 + (event.ydata - center[1]) ** 2 <= radius ** 2):
                    self.current_patch = name
                    self.start_offset = (event.xdata - center[0], event.ydata - center[1])
                    break

            elif isinstance(patch, patches.Ellipse):
                # Verificação simplificada para elipse
                center = (item['x'], item['y'])
                width = patch.width
                height = patch.height

                # Transformação para coordenadas normalizadas
                nx = (event.xdata - center[0]) / (width / 2)
                ny = (event.ydata - center[1]) / (height / 2)

                if nx ** 2 + ny ** 2 <= 1:
                    self.current_patch = name
                    self.start_offset = (event.xdata - center[0], event.ydata - center[1])
                    break

    def on_motion(self, event):
        """Evento quando o mouse é movido com o botão pressionado"""
        if self.current_patch is None or event.inaxes != self.ax:
            return

        item = self.draggable_patches[self.current_patch]
        patch = item['patch']

        if isinstance(patch, patches.Rectangle):
            new_x = event.xdata - self.start_offset[0]
            new_y = event.ydata - self.start_offset[1]

            patch.set_xy((new_x, new_y))
            item['x'], item['y'] = new_x, new_y

            # Atualizar componentes associados
            if 'monitor' in item:  # Computador
                item['monitor'].set_xy((new_x + 1, new_y + 1))
            if 'chairs' in item:  # Mesa com cadeiras
                for chair in item['chairs']:
                    chair_center = chair.center
                    chair.center = (
                        chair_center[0] + (new_x - item['x']),
                        chair_center[1] + (new_y - item['y'])
                    )

        elif isinstance(patch, (patches.Circle, patches.Ellipse)):
            new_x = event.xdata - self.start_offset[0]
            new_y = event.ydata - self.start_offset[1]

            if isinstance(patch, patches.Circle):
                patch.center = (new_x, new_y)
            else:  # Ellipse
                patch.center = (new_x, new_y)

            item['x'], item['y'] = new_x, new_y

        self.fig.canvas.draw()

    def on_release(self, event):
        """Evento quando o botão do mouse é liberado"""
        self.current_patch = None

    def show(self):
        """Mostra o plano interativo"""
        plt.tight_layout()
        plt.show()


# Criar e mostrar o plano interativo
floor_plan = InteractiveFloorPlan()
floor_plan.show()