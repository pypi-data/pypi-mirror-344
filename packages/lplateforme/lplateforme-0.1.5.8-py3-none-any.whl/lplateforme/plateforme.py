from opcode import hasfree

from likeprocessing.processing import *
import pygame
import math
from time import time

class Scroll:
    def __init__(self, player, screen, foreground_image, background_image):
        self.player = player
        self.foreground_image_width = foreground_image.get_width()
        self.foreground_image_height = foreground_image.get_height()
        self.screen_width = screen[0]
        self.screen_height = screen[1]
        self.foreground_image = foreground_image
        self.background_image = background_image
        self.dx = 0
        self.dy = 0

    def draw(self):
        if "droite" in self.player.keyspushed and self.player.x>self.screen_width*2/3 - self.dx:
            self.dx = -max(0, min(self.player.x - self.screen_width * 2 / 3, self.foreground_image_width - self.screen_width))
        elif "gauche" in self.player.keyspushed and self.player.x<self.screen_width/3-self.dx:
            self.dx = -max(0, min(self.player.x - self.screen_width / 3, self.foreground_image_width - self.screen_width))
        if self.player.velocity_y>0 and self.player.y>self.screen_height*2/3-self.dy:
            self.dy = -max(0, min(self.player.y - self.screen_height * 2 / 3, self.foreground_image_height - self.screen_height))
        elif self.player.velocity_y<0 and self.player.y<self.screen_height/3-self.dy:
            self.dy = -max(0, min(self.player.y - self.screen_height / 3, self.foreground_image_height - self.screen_height))
        translate(self.dx/2,self.dy/2)
        image(self.background_image,0,0)
        init_translate(self.dx,self.dy)
        image(self.foreground_image,0,0)

class ImageAnimee:
    def __init__(self):
        self.images = {}
        self.index_animation = 0
        self.compteur_animation = 0
        self.vitesse = 5

    def add_images(self, name, image0: str, fin: int):
        """ajoute une liste d'images à un nom"""
        prefixe = image0.split("0")[0]
        suffixe = image0.split("0")[1]
        self.images[name] = [loadImage(prefixe + str(i) + suffixe) for i in range(fin + 1)]

    def animer(self, name):
        if self.images.get(name) is None:
            name = list(self.images.keys())[0]
            return  self.images[name][0]
        if len(self.images.get(name))==1:
            return self.images[name][0]
        self.compteur_animation += 1
        if self.compteur_animation % self.vitesse == 0:
            self.index_animation = (self.index_animation + 1) % len(self.images[name])
            self.compteur_animation = 0
        return self.images[name][self.index_animation]

    def get_width(self):
        name = list(self.images.keys())[0]
        return self.images[name].get_width()

    def get_height(self):
        name = list(self.images.keys())[0]
        return self.images[name].get_height()


class BoxContainer:
    """Créé un conteneur d'objet"""

    def __init__(self, **kwargs):
        self.objets = []
        self.index = 0
        self.rectangle_englobant = pygame.Rect(0, 0, 0, 0)
        self.name = kwargs.get("name", "")
        self.max_objets = kwargs.get("max_objets", None)
        self.calcul_rectangle_englobant = kwargs.get("c_r_e", False)

    def determine_rectangle_englobant(self):
        """Détermine le rectangle englobant de tous les objets"""
        if len(self.objets) > 0:
            self.rectangle_englobant = pygame.Rect(self.objets[0])
            for objet in self.objets:
                self.rectangle_englobant.union_ip(objet)

    def ajouter(self, objet: ["Box", "BoxContainer"]):
        """
        Ajoute un objet au conteneur.

        :param objet: Objet à ajouter.
        """
        if self.max_objets is not None and len(self.objets) >= self.max_objets:
            return
        if isinstance(objet, BoxContainer):
            for obj in objet:
                if self.max_objets is not None and len(self.objets) >= self.max_objets:
                    return
                self.ajouter(obj)
        else:
            self.objets.append(objet)
            if objet.container is None:
                objet.container = self
        if self.calcul_rectangle_englobant:
            self.determine_rectangle_englobant()

    def ajouter_bords(self, width, height, bord="nseo"):
        """
        Ajoute des box de bords au conteneur.
        """
        largeur = 30
        if "n" in bord:
            self.ajouter(Box(0, -largeur, width, largeur))
        if "s" in bord:
            self.ajouter(Box(0, height, width, largeur))
        if "e" in bord:
            self.ajouter(Box(width, 0, largeur, height))
        if "o" in bord:
            self.ajouter(Box(-largeur, 0, largeur, height))

    def retirer(self, objet, all_container=False):
        """
        Retire un objet du conteneur ou des conteneurs.

        :param objet: Objet à retirer.
        :param all_container: Retirer l'objet de tous les conteneurs.
        """
        try:
            if all_container and objet.container != self:
                try:
                    objet.container.retirer(objet, all_container)
                except:
                    print("erreur retirer container")
            self.objets.remove(objet)
            if self.calcul_rectangle_englobant:
                self.determine_rectangle_englobant()
        except:
            print("erreur retirer")

    def transferer(self, objet: "Box", container: "BoxContainer"):
        """
        Transfère un objet d'un conteneur à un autre.

        :param objet: Objet à transférer.
        :param container: Le conteneur de destination.
        """
        objet.container = None
        self.retirer(objet)
        container.ajouter(objet)

    def draw(self):
        """
        Dessine tous les objets visibles dans le conteneur.
        """
        for objet in self.objets:
            if hasattr(objet, 'draw') and callable(getattr(objet, 'draw')):
                objet.draw()
        if Box.debug and self.rectangle_englobant:
            rect(self.rectangle_englobant.x, self.rectangle_englobant.y, self.rectangle_englobant.width,
                 self.rectangle_englobant.height, no_fill=True, stroke="red")

    def translate(self, dx, dy, exclude=[]):
        """
        Déplace tous les objets du conteneur.

        :param dx: Déplacement horizontal.
        :param dy: Déplacement vertical.
        """
        for objet in self.objets:
            if isinstance(objet, Box) and objet not in exclude:
                objet.x += dx
                objet.y += dy
        if self.calcul_rectangle_englobant:
            self.determine_rectangle_englobant()

    def move(self):
        """
        Commande le déplacement de tous les objets mobiles dans le conteneur.
        """
        list_objet =[]
        for objet in self.objets:
            if isinstance(objet, MovableBox) or isinstance(objet, MovableGravityBox) or isinstance(objet, FollowPathBox):
                list_objet.append(objet)
        while list_objet!=[]:
            o = list_objet.pop()
            o.move()
            if not o.visible:
               self.retirer(o,True)
    def find(self, name):
        """
        Recherche un objet par type.

        :param type: Le type d'objet à rechercher.
        :return: L'objet trouvé ou None.
        """
        for objet in self.objets:
            if hasattr(objet, 'name') and objet.name == name:
                return objet
        return None

    def __iter__(self):
        """
        Retourne l'objet lui-même comme itérateur.
        """
        self.index = 0  # Réinitialise l'index pour une nouvelle itération
        return self

    def __next__(self):
        """
        Retourne l'objet suivant dans l'itération.
        """
        if self.index < len(self.objets):
            result = self.objets[self.index]
            self.index += 1
            return result
        else:
            # Lève une exception StopIteration pour signaler la fin de l'itération
            raise StopIteration

    def __str__(self):
        return self.name + " " + str(self.objets)

    def __len__(self):
        return len(self.objets)

    def isfull(self):
        return self.max_objets != None and len(self.objets) >= self.max_objets


class Inventaire(BoxContainer):
    def __init__(self, x=0, y=0, width=60, height=60):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = False

    def draw(self):
        if self.visible and len(self.objets) > 0:
            rect(self.x, self.y, self.width * len(self.objets), self.height, fill="brown", stroke="black", align_h="center",
                 align_v="center")
            for i, objet in enumerate(self.objets):
                objet.x = self.x + (self.width - objet.width) / 2 + i * self.width
                objet.y = self.y + (self.height - objet.height) / 2
                objet.draw()


class InfoContainer(BoxContainer):
    def __init__(self):
        super().__init__()
        self.visible = False

    def ajouter(self, objet):
        super().ajouter(objet)
        if objet.visible:
            self.visible = True

    def unvisible(self):
        self.visible = False
        for objet in self.objets:
            objet.visible = False


class Box(pygame.Rect):
    debug = False

    def __init__(self, x, y, width, height, image=None, collision_behavior=['stop'], **kwargs):
        """
        Initialise une boîte avec une position, des dimensions, une image, une visibilité,
        un état de collision et une couleur.

        :param x: Coordonnée x du coin supérieur gauche de la boîte.
        :param y: Coordonnée y du coin supérieur gauche de la boîte.
        :param width: Largeur de la boîte.
        :param height: Hauteur de la boîte.
        :param image: Image associée à la boîte (par défaut None).
        """
        self.image_name = None
        if isinstance(image, str):
            self.path_image = image
            self.image = loadImage(image)
        elif isinstance(image, pygame.Surface):
            self.image = image
        elif isinstance(image, ImageAnimee):
            self.image = image
            self.image_name = list(self.image.images.keys())[0]
        else:
            self.image = None
            self.path_image = None
        if image is not None and not isinstance(image, ImageAnimee):
            if width == 0:
                width = self.image.get_width()
            else:
                self.image = resize_image(self.image, (width, self.image.get_height()))
            if height == 0:
                height = self.image.get_height()
            else:
                self.image = resize_image(self.image, (self.image.get_width(), height))

        super().__init__(x, y, width, height)

        self.visible = kwargs.get("visible", True)
        self.enable_collide = True
        self.color = "white"
        self.collision_behavior = collision_behavior
        if "bounce" in self.collision_behavior:
            self.collision_behavior.remove("bounce")
            self.collision_behavior.append("bouncey")
            self.collision_behavior.append("bouncex")
        if "stop" in self.collision_behavior:
            self.collision_behavior.remove("stop")
            self.collision_behavior.append("stopy")
            self.collision_behavior.append("stopx")
        self.name = kwargs.get("name", "")
        self.fill = kwargs.get("fill")
        self.container = None
        self.force = kwargs.get("force", float("inf"))
        self.flip_h = kwargs.get("flip_h", False)
        self.flip_v = kwargs.get("flip_v", False)
        self.state = kwargs.get("state")
        self.velocity_x = 0
        self.velocity_y = 0

    def get_position(self):
        """
        Retourne la position (x, y) de la boîte.

        :return: Un tuple (x, y) représentant la position de la boîte.
        """
        return self.x, self.y

    def get_dimensions(self):
        """
        Retourne les dimensions (width, height) de la boîte.

        :return: Un tuple (width, height) représentant les dimensions de la boîte.
        """
        return self.width, self.height

    def set_position(self, x, y):
        """
        Définit une nouvelle position pour la boîte.

        :param x: Nouvelle coordonnée x.
        :param y: Nouvelle coordonnée y.
        """
        self.x = x
        self.y = y

    def set_center_position(self, x, y):
        """
        Définit une nouvelle position pour la boîte en fonction de son centre.

        :param x: Nouvelle coordonnée x du centre.
        :param y: Nouvelle coordonnée y du centre.
        """
        self.centerx = x
        self.centery = y

    def set_dimensions(self, width, height):
        """
        Définit de nouvelles dimensions pour la boîte.

        :param width: Nouvelle largeur.
        :param height: Nouvelle hauteur.
        """
        self.width = width
        self.height = height

    def collides_with(self, other_box):
        """
        Vérifie si cette boîte entre en collision avec une autre boîte.

        :param other_box: Une autre instance de Box.
        :return: True si les boîtes se chevauchent, False sinon.
        """
        # return (self.enable_collide and self.x < other_box.x + other_box.width and
        #         self.x + self.width > other_box.x and
        #         self.y < other_box.y + other_box.height and
        #         self.y + self.height > other_box.y)
        # Calcul de l'intersection
        intersection = self.clip(other_box)

        # Si les rectangles ne se chevauchent pas, retourner None
        if intersection.width * intersection.height < 2:
            return None

        # Déterminer le sens de l'intersection
        if intersection.width > intersection.height:
            # Collision horizontale
            if intersection.top == self.top:
                return "haut"  # self touche other_box par le bas
            if intersection.bottom == self.bottom:
                return "bas"  # self touche other_box par le haut
        else:
            # Collision verticale
            if intersection.left == self.left:
                return "gauche"  # self touche other_box par la droite
            if intersection.right == self.right:
                return "droite"  # self touche other_box par la gauche

        return None

    def __repr_(self):
        """
        Retourne une représentation sous forme de chaîne de caractères de la boîte.

        :return: Une chaîne de caractères représentant la boîte.
        """
        return (f"Box(x={self.x}, y={self.y}, width={self.width}, height={self.height}, "
                f"image={self.path_image if self.image else 'none'}, visible={self.visible}, "
                f"enable_collide={self.enable_collide}, color={self.color})")

    def __str__(self):
        return type(self).__name__ + " " + self.name + " " + str(self.collision_behavior)

    def draw(self):
        """
        Dessine la boîte si elle est visible.
        """
        if self.visible:
            if self.image is None and self.fill is not None:
                rect(self.x, self.y, self.width, self.height, fill=self.fill)

            if isinstance(self.image, ImageAnimee):
                img = self.image.animer(self.image_name)
                image(img, self.x - (img.get_width() - self.width) // 2, self.y, flip_h=self.flip_h, flip_v=self.flip_v)
            elif self.image is not None:
                image(self.image, self.x - (self.image.get_width() - self.width) // 2,
                      self.y - (self.image.get_height() - self.height) // 2, flip_h=self.flip_h, flip_v=self.flip_v)
            if Box.debug:
                rect(self.x, self.y, self.width, self.height, no_fill=True, stroke=self.color)
                text(self.name, self.x, self.y, self.width, self.height, no_stroke=True, no_fill=True, align_h="center",
                     align_v="center")


class LifeBox(Box):
    """Créé une boîte avec une vie"""

    def __init__(self, x, y, width, height, life=1, image=None, value=0, **kwargs):
        super().__init__(x, y, width, height, image, **kwargs)
        self.life = life
        self.collision_behavior = []
        self.owner = kwargs.get("owner", None)

    def set_nb_life(self, life):
        self.life = life

    def draw(self):
        if self.owner is not None:
            self.set_nb_life(self.owner.life)
        if self.visible:
            t = translate()
            init_translate()
            if self.image is None and self.fill is not None:
                for i in range(self.life):
                    rect(self.x + i * self.width, self.y, self.width, self.height, fill=self.fill)
            else:
                for i in range(self.life):
                    image(self.image, self.x + i * self.image.get_width() + 1, self.y)
            translate(*t)

class ChargerBox(Box):
    def __init__(self, x, y, width, height, bullet=1, image=None, value=0, **kwargs):
        super().__init__(x, y, width, height, image, **kwargs)
        self.bullet = bullet
        self.collision_behavior = []
        self.owner = kwargs.get("owner", None)

    def set_nb_bullet(self, bullet):
        self.bullet = bullet

    def draw(self):
        if self.owner is not None:
            self.set_nb_bullet(len(self.owner.magazine))
        if self.visible:
            t = translate()
            init_translate()
            if self.image is None and self.fill is not None:
                for i in range(self.bullet):
                    rect(self.x + i * self.width, self.y, self.width, self.height, fill=self.fill)
            else:
                for i in range(self.bullet):
                    image(self.image, self.x + i * (self.image.get_width() + 2), self.y)
            translate(*t)


class Decors(Box):
    def __init__(self, x, y, width, height, image=None, **kwargs):
        super().__init__(x, y, width, height, image, [], **kwargs)
        self.collision_behavior = []

    def draw(self):
        if self.visible:
            if self.image is None and self.fill is not None:
                rect(self.x, self.y, self.width, self.height, fill=self.fill)
            else:
                image(self.image, self.x, self.y, flip_h=self.flip_h, flip_v=self.flip_v)

    def collides_with(self, other_box):
        return None


class MovableBox(Box):
    def __init__(self, x, y, width, height, image=None, collision_behavior=['stop'], velocity_x=0, velocity_y=0,
                 obstacles: BoxContainer = None, **kwargs):
        """
        Initialise une boîte mobile avec une position, des dimensions, une vélocité et un comportement en cas de collision.

        :param x: Coordonnée x du coin supérieur gauche de la boîte.
        :param y: Coordonnée y du coin supérieur gauche de la boîte.
        :param width: Largeur de la boîte.
        :param height: Hauteur de la boîte.
        :param velocity_x: Vélocité horizontale de la boîte.
        :param velocity_y: Vélocité verticale de la boîte.
        :param collision_behavior: Comportement en cas de collision ('stop', 'bounce', 'stick').
        """
        super().__init__(x, y, width, height, image, collision_behavior, **kwargs)
        self.initial_velocity_x = abs(velocity_x)
        self.initial_velocity_y = abs(velocity_y)
        self.sensx = 1 if velocity_x >= 0 else -1
        self.sensy = 1 if velocity_y >= 0 else -1
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.xf = x
        self.yf = y
        self.collision_zone = None
        self.obstacles = obstacles
        self.voisins = {"haut": None, "bas": None, "gauche": None, "droite": None}
        self.force = kwargs.get("force", 500)
        self.damage = kwargs.get("damage", 0)

    def init_velocity(self):
        if self.velocity_x == 0:
            self.velocity_x = self.initial_velocity_x
        if self.velocity_y == 0:
            self.velocity_y = self.initial_velocity_y

    def set_velocity(self, velocity_x, velocity_y):
        """
        Définit une nouvelle vélocité pour la boîte.

        :param velocity_x: Nouvelle vélocité horizontale.
        :param velocity_y: Nouvelle vélocité verticale.
        """
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def set_x_velocity(self, velocity_x):
        """
        Définit une nouvelle vélocité horizontale pour la boîte.

        :param velocity_x: Nouvelle vélocité horizontale.
        """
        self.velocity_x = velocity_x

    def set_y_velocity(self, velocity_y):
        """
        Définit une nouvelle vélocité verticale pour la boîte.

        :param velocity_y: Nouvelle vélocité verticale.
        """
        self.velocity_y = velocity_y

    def get_x_velocity(self):
        """
        Retourne la vélocité horizontale de la boîte.

        :return: La vélocité horizontale.
        """
        return self.velocity_x

    def get_y_velocity(self):
        """
        Retourne la vélocité verticale de la boîte.

        :return: La vélocité verticale.
        """
        return self.velocity_y

    def move(self):
        """
        Déplace la boîte en fonction de sa vélocité.
        """

        self.voisins = {"haut": None, "bas": None, "gauche": None, "droite": None}
        if abs(self.velocity_x) + abs(self.velocity_y) != 0:
            if self.obstacles is not None:
                for obstacle in self.obstacles:
                    # if obstacle != self and not (isinstance(self, Projectile) and isinstance(obstacle,
                    #                                                                          Projectile) and self.name == obstacle.name):
                    if obstacle != self and not isinstance(obstacle, Decors):
                        collision = self.collides_with(obstacle)
                        if collision :
                            self.voisins[collision] = obstacle
                self.check_collision()
        if "bounce" in self.collision_behavior or "bouncex" in self.collision_behavior or "bouncey" in self.collision_behavior:
            self.init_velocity()
            self.velocity_x = self.sensx * self.initial_velocity_x
            self.velocity_y = self.sensy * self.initial_velocity_y
        self.xf += self.velocity_x
        self.yf += self.velocity_y
        self.x = self.xf
        self.y = self.yf

    def check_collision1(self):
        """
        Vérifie et gère la collision avec les autres boîtes en fonction du comportement défini.
        """
        velocity_x = self.velocity_x
        velocity_y = self.velocity_y
        scale = False
        for obstacle in self.voisins.keys():
            if self.voisins[obstacle] is not None:
                if "scale" in self.voisins[obstacle].collision_behavior:
                    if self.name == "player":
                        scale = True
                if self.voisins[obstacle].name != "player" or self.name != "player":
                    if (obstacle == "gauche" or obstacle == "droite") and ("bouncex" in self.voisins[
                        obstacle].collision_behavior or 'bouncex' in self.collision_behavior and "stopx" in self.voisins[
                                                                               obstacle].collision_behavior):
                        if obstacle == "gauche":
                            self.xf = self.voisins[obstacle].x + self.voisins[obstacle].width + 1
                            self.velocity_x = self.initial_velocity_x
                            if isinstance(self.voisins[obstacle], MovableBox):
                                self.voisins[obstacle].velocity_x = -self.voisins[obstacle].initial_velocity_x
                        else:
                            self.xf = self.voisins[obstacle].x - self.width - 1
                            self.velocity_x = -self.initial_velocity_x
                            if isinstance(self.voisins[obstacle], MovableBox):
                                self.voisins[obstacle].velocity_x = self.voisins[obstacle].initial_velocity_x
                    elif (obstacle == "haut" or obstacle == "bas") and ("bouncey" in self.voisins[
                        obstacle].collision_behavior or 'bouncey' in self.collision_behavior and "stopy" in self.voisins[
                                                                            obstacle].collision_behavior):
                        if obstacle == "haut":
                            self.yf = self.voisins[obstacle].y + self.voisins[obstacle].height + 1
                            self.velocity_y = self.initial_velocity_y
                            if isinstance(self.voisins[obstacle], MovableBox):
                                self.voisins[obstacle].velocity_y = -self.voisins[obstacle].initial_velocity_y
                        else:
                            self.yf = self.voisins[obstacle].y - self.height - 1
                            self.velocity_y = -self.initial_velocity_y
                            if isinstance(self.voisins[obstacle], MovableBox):
                                self.voisins[obstacle].velocity_y = self.voisins[obstacle].initial_velocity_y

                if "life" in self.voisins[obstacle].collision_behavior:
                    self.voisins[obstacle].life -= 1
                    if hasattr(self, 'life'):
                        self.life -= 1
                        if self.life == 0:
                            self.visible = False
                    if hasattr(self, 'player'):
                        self.player.score += self.voisins[obstacle].value
                    if self.voisins[obstacle].life == 0:
                        self.obstacles.retirer(self.voisins[obstacle], True)
                    #     self.voisins[obstacle].visible = False
                elif not scale:
                    if (obstacle == "gauche" or obstacle == "droite") and "stickx" in self.voisins[
                        obstacle].collision_behavior and "mover" in self.collision_behavior:
                        if self.velocity_x != 0:
                            if isinstance(self.voisins["bas"], MovableBox):
                                self.voisins[obstacle].velocity_x = self.velocity_x + self.voisins["bas"].velocity_x
                            else:
                                self.voisins[obstacle].velocity_x = self.velocity_x
                            self.voisins[obstacle].move()
                            self.voisins[obstacle].velocity_x = 0
                    if "stop" in self.voisins[obstacle].collision_behavior:
                        if obstacle == "bas":
                            if isinstance(self.voisins["bas"], MovableBox):
                                if self.velocity_y < 0:
                                    self.velocity_y += self.voisins[obstacle].velocity_y
                                else:
                                    self.velocity_y = self.voisins[obstacle].velocity_y
                            else:
                                if self.velocity_y > 0:
                                    self.velocity_y = 0
                            self.yf = self.voisins[obstacle].y - self.height + 1
                            if isinstance(self.voisins[obstacle], MovableBox):
                                if self.name == "player":
                                    self.velocity_x += self.voisins[obstacle].velocity_x
                                else:
                                    self.velocity_x = self.voisins[obstacle].velocity_x
                        elif obstacle == "haut" and self.velocity_y < 0:
                            self.velocity_y = 0
                            self.yf = self.voisins[obstacle].y + self.voisins[obstacle].height - 1
                        elif obstacle == "droite" and self.velocity_x > 0:
                            self.velocity_x = 0
                            self.xf = self.voisins[obstacle].x - self.width + 1
                        elif obstacle == "gauche" and self.velocity_x < 0:
                            self.velocity_x = 0
                            self.xf = self.voisins[obstacle].x + self.voisins[obstacle].width - 1
                    elif "stopx" in self.voisins[obstacle].collision_behavior:
                        if obstacle == "droite" and self.velocity_x > 0:
                            self.velocity_x = 0
                            self.xf = self.voisins[obstacle].x - self.width + 1
                        elif obstacle == "gauche" and self.velocity_x < 0:
                            self.velocity_x = 0
                            self.xf = self.voisins[obstacle].x + self.voisins[obstacle].width - 1
                    elif "stopy" in self.voisins[obstacle].collision_behavior and isinstance(self, MovableGravityBox):
                        if obstacle == "bas" and self.velocity_y > 0:
                            self.velocity_y = 0
                            if isinstance(self.voisins[obstacle], MovableBox):
                                self.velocity_x += self.voisins[obstacle].velocity_x
                                # self.x += self.velocity_x
                                # self.velocity_x = 0
                            self.yf = self.voisins[obstacle].y - self.height + 1
                        elif obstacle == "haut" and self.velocity_y < 0:
                            self.velocity_y = 0
                            self.yf = self.voisins[obstacle].y + self.voisins[obstacle].height - 1
                if "event" in self.voisins[obstacle].collision_behavior:
                    self.voisins[obstacle].event(self, self.voisins[obstacle])
                if "life" in self.voisins[obstacle].collision_behavior and hasattr(self, 'damage'):
                    self.voisins[obstacle].life -= self.damage
                    if hasattr(self, 'player'):
                        self.player.score += self.voisins[obstacle].value
                    if self.voisins[obstacle].life == 0:
                        self.obstacles.retirer(self.voisins[obstacle], True)
                if hasattr(self, 'life'):
                    self.life -= 1
                    if self.life == 0:
                        self.obstacles.retirer(self, True)
        if self.name == "player":
            if scale:
                self.gravity = 0
            else:
                self.gravity = 0.11

    def check_collision(self):
        """
        Vérifie et gère la collision avec les autres boîtes en fonction du comportement défini.
        """
        velocity_x = self.velocity_x
        velocity_y = self.velocity_y
        scale = False
        if self.name == "projectile":
            pass
        for obstacle in self.voisins.keys():
            if self.voisins[obstacle] is not None:
                if (obstacle == "gauche" or obstacle == "droite") and 'bouncex' in self.collision_behavior and self.voisins[obstacle].force >= self.force:
                    if obstacle == "gauche":
                        self.xf = self.voisins[obstacle].x + self.voisins[obstacle].width + 1
                        self.sensx = 1
                    else:
                        self.xf = self.voisins[obstacle].x - self.width - 1
                        self.sensx = -1
                elif obstacle in ["haut","bas"]  and 'bouncey' in self.collision_behavior and self.voisins[obstacle].force >= self.force:
                    if obstacle == "haut":
                        self.yf = self.voisins[obstacle].y + self.voisins[obstacle].height + 1
                        self.sensy = 1
                    else:
                        self.yf = self.voisins[obstacle].y - self.height - 1
                        self.sensy = -1
                if not 'bouncex' in self.collision_behavior and"stopx" in self.voisins[obstacle].collision_behavior:
                    if obstacle == "droite" and self.force<=self.voisins[obstacle].force:
                        if not isinstance(self.voisins[obstacle],Player):
                            self.velocity_x = min(0, self.velocity_x)
                        self.xf = self.voisins[obstacle].x - self.width + 1
                    elif obstacle == "gauche" and self.force<=self.voisins[obstacle].force:
                        self.velocity_x = max(0, self.velocity_x)
                        self.xf = self.voisins[obstacle].x + self.voisins[obstacle].width - 1
                if "stopy" in self.voisins[obstacle].collision_behavior and isinstance(self, MovableGravityBox):
                    if obstacle == "bas":
                        if isinstance(self.voisins["bas"], MovableBox):
                            if self.velocity_y < 0:
                                self.velocity_y += self.voisins[obstacle].velocity_y
                            else:
                                self.velocity_y = self.voisins[obstacle].velocity_y
                        else:
                            if self.velocity_y > 0:
                                self.velocity_y = 0
                        self.yf = self.voisins[obstacle].y - self.height + 1
                        if isinstance(self.voisins[obstacle], MovableBox):
                            self.velocity_x += self.voisins[obstacle].velocity_x
                    elif obstacle == "haut" and self.velocity_y < 0:
                        self.velocity_y = 0
                        self.yf = self.voisins[obstacle].y + self.voisins[obstacle].height - 1
                if "event" in self.voisins[obstacle].collision_behavior:
                    self.voisins[obstacle].event(self, self.voisins[obstacle])
                # if "life" in self.voisins[obstacle].collision_behavior and hasattr(self, 'damage'):
                #     self.voisins[obstacle].life -= self.damage
                #     if hasattr(self, 'player'):
                #         self.player.score += self.voisins[obstacle].value
                #     if self.voisins[obstacle].life == 0:
                #         self.obstacles.retirer(self.voisins[obstacle], True)
                # if hasattr(self, 'life'):
                #     self.life -= 1
                #     if self.life == 0:
                #         self.obstacles.retirer(self, True)

    def __repr_(self):
        """
        Retourne une représentation sous forme de chaîne de caractères de la boîte mobile.

        :return: Une chaîne de caractères représentant la boîte mobile.
        """
        return (f"MovableBox(x={self.x}, y={self.y}, width={self.width}, height={self.height}, "
                f"velocity_x={self.velocity_x}, velocity_y={self.velocity_y}, "
                f"collision_behavior='{self.collision_behavior}', image={self.path_image if self.image else 'none'})")


class FollowPathBox(MovableBox):
    def __init__(self, x, y, width, height, image=None, path: list[tuple, list] = [], velocity=2,
                 collision_behavior=['stop'], **kwargs):
        super().__init__(x, y, width, height, image, collision_behavior, **kwargs)
        self.path = path
        self.index_path = 0
        self.velocity = velocity
        self.damage = kwargs.get("damage", 0)
        self.mode = kwargs.get("mode", "normal")
        self.sens = 0

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def move(self):
        if self.index_path == len(self.path):
            return
        dx = self.path[self.index_path][0] - self.xf
        dy = self.path[self.index_path][1] - self.yf
        phi = atan2(dy, dx)
        if self.distance(self.xf, self.yf, self.path[self.index_path][0], self.path[self.index_path][1]) > 1:
            self.velocity_x = self.velocity * cos(phi)
            self.velocity_y = self.velocity * sin(phi)
        else:
            self.velocity_x = 0
            self.velocity_y = 0
            self.x = self.path[self.index_path][0]
            self.y = self.path[self.index_path][1]
            self.xf = self.x
            self.yf = self.y
            if self.index_path < len(self.path) and self.sens == 0:
                self.index_path += 1
            elif self.index_path > 0 and self.sens == 1:
                self.index_path -= 1
            if self.index_path == len(self.path) and self.mode == "cycle":
                self.index_path = 0
            elif self.mode == "reverse":
                if self.sens == 1 and self.index_path == 0:
                    self.sens = 0
                elif self.sens == 0 and self.index_path == len(self.path):
                    self.sens = 1
                    self.index_path -= 1

        super().move()
        # self.xf += self.velocity_x
        # self.yf += self.velocity_y
        # self.x=self.xf
        # self.y=self.yf


class MovableGravityBox(MovableBox):
    def __init__(self, x, y, width, height, image=None, collision_behavior=['stop'], velocity_x=0, velocity_y=0,
                 obstacles: BoxContainer = None, gravity=0.11, **kwargs):
        """
        Initialise une boîte mobile avec gravité avec une position, des dimensions, une vélocité,
        un comportement en cas de collision et une gravité.

        :param x: Coordonnée x du coin supérieur gauche de la boîte.
        :param y: Coordonnée y du coin supérieur gauche de la boîte.
        :param width: Largeur de la boîte.
        :param height: Hauteur de la boîte.
        :param velocity_x: Vélocité horizontale de la boîte.
        :param velocity_y: Vélocité verticale de la boîte.
        :param collision_behavior: Comportement en cas de collision ('stop', 'bounce', 'stick').
        :param gravity: Force de gravité appliquée à la boîte.
        """
        super().__init__(x, y, width, height, image, collision_behavior, velocity_x, velocity_y, obstacles, **kwargs)
        self.initial_gravity = gravity
        self.gravity = gravity

    def set_gravity(self, gravity):
        """
        Définit une nouvelle gravité pour la boîte.

        :param gravity: Nouvelle gravité.
        """
        self.initial_gravity = gravity
        self.gravity = gravity

    def move(self):
        """
        Déplace la boîte en fonction de sa vélocité et applique la gravité.
        """
        # Appliquer la gravité à la vélocité verticale
        #self.velocity_x = self.sensx * self.initial_velocity_x
        self.velocity_y += self.gravity
        self.voisins = {"haut": None, "bas": None, "gauche": None, "droite": None}
        if self.velocity_x + self.velocity_y != 0:
            if self.obstacles is not None:
                for obstacle in self.obstacles:
                    if obstacle != self and not isinstance(self, Decors) and not (isinstance(self, Projectile) and isinstance(obstacle,Projectile) and self.name == obstacle.name):
                        collision = self.collides_with(obstacle)
                        if collision :
                            self.voisins[collision] = obstacle
                self.check_collision()
            self.xf += self.velocity_x
            self.yf += self.velocity_y
            self.x = self.xf
            self.y = self.yf

            self.velocity_x = self.sensx * self.initial_velocity_x

    def __repr_(self):
        """
        Retourne une représentation sous forme de chaîne de caractères de la boîte mobile avec gravité.

        :return: Une chaîne de caractères représentant la boîte mobile avec gravité.
        """
        return (f"MovableGravityBox(x={self.x}, y={self.y}, width={self.width}, height={self.height}, "
                f"velocity_x={self.velocity_x}, velocity_y={self.velocity_y}, "
                f"collision_behavior='{self.collision_behavior}', gravity={self.gravity}, "
                f"image={self.path_image if self.image else 'none'})")


class Player(MovableGravityBox):
    def __init__(self, x, y, width, height, image, obstacles, keys={}, **kwargs):
        super().__init__(x, y, width, height, image, ["stop","life"], 2, 2, obstacles, gravity=0.11, **kwargs)
        self.imunity = False
        self.saut = 0
        self.keys = keys
        if "left" not in self.keys:
            self.keys["left"] = K_LEFT
        if "right" not in self.keys:
            self.keys["right"] = K_RIGHT
        if "jump" not in self.keys:
            self.keys["jump"] = K_SPACE
        if "stick" not in self.keys:
            self.keys["stick"] = K_d
        if "catch" not in self.keys:
            self.keys["catch"] = K_c
        if "up" not in self.keys:
            self.keys["up"] = K_UP
        if "down" not in self.keys:
            self.keys["down"] = K_DOWN
        self.name = "player"
        self.sens = "droite"
        self.catch = False
        self.inventaire = Inventaire()
        self.score = 0
        self.life = kwargs.get("vie", 3)
        self.force = kwargs.get("force", 400)
        self.keyspushed = set()
        self.crash = False
        self.maxi_velovity_y = 8

    def scan_keys(self):
        self.keyspushed = set()
        self.velocity_x=0
        self.catch = False
        if keyIsDown(self.keys["left"]):
            self.keyspushed.add("gauche")
            self.velocity_x = -self.initial_velocity_x
            self.sens = "gauche"
        elif keyIsDown(self.keys["right"]):
            self.keyspushed.add("droite")
            self.velocity_x = self.initial_velocity_x
            self.sens = "droite"
        else:
            self.velocity_x = 0
        if keyIsDown(self.keys["up"]):
            self.keyspushed.add("haut")
        elif keyIsDown(self.keys["down"]):
            self.keyspushed.add("bas")
        if keyIsDown(self.keys["jump"]) and self.saut == 0:
            self.saut = 1
            if self.velocity_y == 0:
                self.keyspushed.add("saut")
                self.velocity_y = self.initial_velocity_y * -3
        else:
            self.saut = 0
        if keyIsDown(self.keys["stick"]) and "sticky" not in self.collision_behavior:
            self.keyspushed.add("stick")
            self.force = 600
        else:
            self.collision_behavior = [x for x in self.collision_behavior if x != 'mover']
            self.force=400
        if keyIsDown(self.keys["catch"]):
            self.keyspushed.add("catch")
            self.catch = True

    def move(self):
        self.scan_keys()
        """
        Déplace le personnage.
        """
        # Appliquer la gravité à la vélocité verticale
        self.velocity_y += self.gravity
        self.voisins = {"haut": None, "bas": None, "gauche": None, "droite": None}
        if self.obstacles is not None:
            for obstacle in self.obstacles:
                if not isinstance(obstacle, Decors):
                    if obstacle != self and not (isinstance(self, Projectile) and isinstance(obstacle,
                                                                                             Projectile) and self.name == obstacle.name):
                        collision = self.collides_with(obstacle)
                        if collision:
                            self.voisins[collision] = obstacle
            self.check_collision()
        self.xf += self.velocity_x
        self.yf += self.velocity_y
        self.x = self.xf
        self.y = self.yf
        if self.velocity_y>self.maxi_velovity_y:
            self.crash = True
        if self.crash and self.velocity_y==0:
            self.crash = False
            self.life-=1

    def check_collision(self):
        """
        Vérifie et gère la collision avec les autres boîtes en fonction du comportement défini.
        """
        scale = False
        for obstacle in self.voisins.keys():
            if self.voisins[obstacle] is not None:
                if not isinstance(self.voisins[obstacle], Projectile):
                    if self.force>self.voisins[obstacle].force and (obstacle == "gauche" or obstacle == "droite") and "stickx" in self.voisins[
                        obstacle].collision_behavior:

                        # if self.velocity_x != 0:
                        dec = 1 if obstacle == "gauche" else -1
                        if isinstance(self.voisins["bas"], MovableBox):
                            # self.velocity_x +=
                            self.voisins[obstacle].xf+=self.velocity_x - self.voisins["bas"].velocity_x + dec
                        else:
                            self.voisins[obstacle].xf += self.velocity_x+dec
                            # self.voisins[obstacle].velocity_x += self.velocity_x
                            # self.voisins[obstacle].move()
                            # self.voisins[obstacle].velocity_x = 0
                    elif self.voisins[obstacle].force >= self.force:
                        if obstacle in ["gauche", "droite"] and "stopx" in self.voisins[obstacle].collision_behavior:
                            if obstacle == "gauche":
                                self.xf = self.voisins[obstacle].x + self.voisins[obstacle].width - 1
                                self.velocity_x = max(0, self.voisins[obstacle].velocity_x, self.velocity_x)
                            elif obstacle == "droite":
                                self.xf = self.voisins[obstacle].x - self.width + 1
                                self.velocity_x = min(0, self.voisins[obstacle].velocity_x, self.velocity_x)
                        elif obstacle in ["haut", "bas"]and "stopy" in self.voisins[obstacle].collision_behavior:
                            if obstacle == "haut":
                                self.yf = self.voisins[obstacle].y + self.voisins[obstacle].height + 1
                                self.velocity_y = max(0, self.voisins[obstacle].velocity_y, self.velocity_y)
                            elif obstacle == "bas":
                                self.yf = self.voisins[obstacle].y - self.height +1
                                self.velocity_y = min(0, self.voisins[obstacle].velocity_y, self.velocity_y)
                                if self.voisins[obstacle].name == "caisse 4 s":
                                    ...
                                self.velocity_x +=self.voisins[obstacle].velocity_x
                                self.saut = 0
                    if "scale" in self.voisins[obstacle].collision_behavior:
                        scale = True
                    if "event" in self.voisins[obstacle].collision_behavior:
                        self.voisins[obstacle].event(self, self.voisins[obstacle])
                else:
                    self.life-=1
                    self.voisins[obstacle].visible = False
                    self.obstacles.retirer(self.voisins[obstacle], True)
        if not self.imunity:
            if self.voisins["gauche"] is not None and self.voisins["droite"] is not None:
                 if isinstance(self.voisins["gauche"],MovableBox) and self.voisins["gauche"].damage>0:
                    self.life -= self.voisins["gauche"].damage
                    self.yf = self.voisins["gauche"].y - self.height -1
                    self.xf = self.voisins["gauche"].right - self.width-1
                    self.velocity_y = self.initial_velocity_y * -3
                    self.saut = 1
                    self.imunity = True
                 elif isinstance(self.voisins["droite"],MovableBox) and self.voisins["droite"].damage>0:
                    self.life -= self.voisins["droite"].damage
                    self.yf = self.voisins["droite"].y - self.height - 1
                    self.velocity_y = self.initial_velocity_y*-3
                    self.saut = 1
                    self.imunity = True
            if self.voisins["haut"] is not None and self.voisins["bas"] and  not self.imunity:
                if isinstance(self.voisins["haut"],MovableBox) and self.voisins["haut"].damage>0:
                    self.life -= self.voisins["haut"].damage
                    self.yf = self.voisins["haut"].y + self.voisins["haut"].height + 1
                    self.velocity_y = self.initial_velocity_y
                    self.imunity = True
                elif isinstance(self.voisins["bas"],MovableBox) and self.voisins["bas"].damage>0:
                    self.life -= self.voisins["bas"].damage
                    self.yf = self.voisins["bas"].y - self.height - 1
                    self.velocity_y = self.initial_velocity_y * -3
                    self.saut = 1
                    self.imunity = True
            if isinstance(self.voisins["gauche"],DamageBox) and not self.imunity:
                self.life -= self.voisins["gauche"].damage
                self.xf = self.voisins["gauche"].right + 1
                self.imunity = True
            elif isinstance(self.voisins["droite"],DamageBox) and not self.imunity:
                self.life -= self.voisins["droite"].damage
                self.xf = self.voisins["droite"].x - self.width - 1
            elif isinstance(self.voisins["haut"],DamageBox) and not self.imunity:
                self.life -= self.voisins["haut"].damage
                self.yf = self.voisins["haut"].y + self.voisins["haut"].height + 1
                self.velocity_y = 0
                self.imunity = True
            elif isinstance(self.voisins["bas"],DamageBox) and not self.imunity:
                self.life -= self.voisins["bas"].damage
                self.yf = self.voisins["bas"].y - self.height - 1
                self.velocity_y = self.initial_velocity_y * -3

        elif self.voisins["gauche"] is None and self.voisins["droite"] is None and self.voisins["haut"] is None:
            self.imunity = False

        if scale:
            self.gravity = 0
            self.saut = 0
            if "haut" in self.keyspushed:
                self.velocity_y = -self.initial_velocity_y
            elif "bas" in self.keyspushed:
                self.velocity_y = self.initial_velocity_y
            elif "saut" not in self.keyspushed:
                self.velocity_y = 0
        else:
            self.gravity = self.initial_gravity


    def draw(self):
        if "gauche" in self.keyspushed or "droite" in self.keyspushed:
            self.image_name = "marche"
        elif "saut" in self.keyspushed:
            self.image_name = "marche"
        elif "haut" in self.keyspushed or "bas" in self.keyspushed:
            self.image_name = "grimpe"
        else:
            self.image_name = "idle"
        if self.visible:
            if Box.debug:
                rect(self.x, self.y, self.width, self.height, no_fill=True, stroke=self.color)
            if isinstance(self.image, ImageAnimee):
                img = self.image.animer(self.image_name)
                image(img, self.x - (img.get_width() - self.width) // 2, self.y, flip_h=(self.sens == "gauche"))
            elif self.image is not None:
                image(self.image, self.x - (self.image.get_width() - self.width) // 2, self.y)
        if self.inventaire.visible:
            t = translate()
            init_translate()
            self.inventaire.draw()
            translate(*t)


class MousePlayer(MovableBox):
    def __init__(self, x, y, width, height, image, obstacles, **kwargs):
        super().__init__(x, y, width, height, image, ["stop"], 0, 0, obstacles, **kwargs)
        self.name = kwargs.get("name", "mouseplayer")
        self.movex = kwargs.get("movex", False)
        self.movey = kwargs.get("movey", False)
        if not self.movex and not self.movey:
            self.movex = True
            self.movey = True
        self.lastx = self.x
        self.lasty = self.y
        self.dx = 0
        self.dy = 0
        self.score = 0
        self.life = 3
        self.launch = False

    def setx(self):
        self.xf = mouseX()
        self.dx = self.xf - self.lastx

    def sety(self):
        self.yf = mouseY()
        self.dy = self.yf - self.lasty

    def move(self):
        if self.life > 0:
            if self.movex:
                self.setx()
            if self.movey:
                self.sety()
            if mouse_click_down():
                self.launch = True
            super().move()


class Brique(Box):
    def __init__(self, x, y, width, height, image, fill, **kwargs):
        """Initialise une brique avec une position, des dimensions, une couleur de remplissage et un comportement de collision."""
        super().__init__(x, y, width, height, image, ['stop', 'life'], fill=fill, **kwargs)
        self.life = kwargs.get("life", 1)
        self.value = kwargs.get("value", 1)


class Invaders(Brique):
    def __init__(self, x, y, width, height, image, fill, **kwargs):
        super().__init__(x, y, width, height, image, fill, **kwargs)
        self.damage = kwargs.get("damage", 1)
        self.name = "invader"


class EventBox(Box):
    def __init__(self, x, y, width, height, name, image=None, event=None, **kwargs):
        """ Initialise une boîte événementielle avec une position, des dimensions, un nom, une image et un événement.
        event est une fonction qui prend deux arguments: player et objet.
        player est l'objet qui a déclenché l'événement et objet est l'objet sur lequel l'événement est déclenché."""
        collision_behavior = kwargs.get("collision_behavior", ['event'])
        if "event" not in collision_behavior:
            collision_behavior.append("event")
        super().__init__(x, y, width, height, image, collision_behavior)
        if isinstance(event, str):
            self.event = eval(event)
        else:
            self.event = event
        self.name = name


import json


class Ball(MovableBox):
    def __init__(self, x, y, width, height, image, velocity_x, velocity_y, obstacles, player, **kwargs):
        """Initialise une balle avec une position, des dimensions, une image, une vélocité en x et en y et des obstacles (BoxContainer)."""
        super().__init__(x, y, width, height, image, ["bouncex", "bouncey"], velocity_x, velocity_y, obstacles,
                         **kwargs)
        self.player = player
        self.dead_zone = kwargs.get("dead_zone", (0, 0, processing.width(), processing.height()))
        self.damage = 1
        self.life = float("inf")
        self.velocity_x_max = self.velocity_x
        self.velocity_y_max = self.velocity_y

    def set_x_velocity(self, velocity_x):
        self.velocity_x = borner(velocity_x, -self.velocity_x_max, self.velocity_x_max)

    def set_y_velocity(self, velocity_y):
        self.velocity_y = borner(velocity_y, -self.velocity_y_max, self.velocity_y_max)

    def set_dead_zone(self, dead_zone=None):
        if dead_zone is not None:
            self.dead_zone = dead_zone
        else:
            self.dead_zone = (-3, -3, processing.width() + 3, processing.height())

    def move(self):
        if self.velocity_x == 0 and self.velocity_y == 0 and self.player.life > 0:
            self.x = self.player.x + (self.player.width - self.width) // 2
            self.y = self.player.y - self.height - 2
        if self.x < self.dead_zone[0] or self.x > self.dead_zone[2] or self.y < self.dead_zone[1] or self.y > \
                self.dead_zone[3] or self.life == 0:
            self.velocity_x = 0
            self.velocity_y = 0
            self.player.life -= 1
            self.visible = True
        if self.player.launch:
            self.velocity_y = -2
            self.velocity_x = 2
            self.player.launch = False

        super().move()

    def check_collision(self):
        for obstacle in self.voisins.keys():
            if self.voisins[obstacle] is not None:
                if self.voisins[obstacle] == self.player and obstacle in ["haut", "bas"]:
                    if self.player.dx > 0:
                        self.set_x_velocity(self.velocity_x + 1)
                    elif self.player.dx < 0:
                        self.set_x_velocity(self.velocity_x - 1)
        super().check_collision()

    def draw(self):
        if self.visible:
            if self.image is None:
                ellipse(self.x, self.y, self.width, self.height, fill=self.fill)
            else:
                super().draw()


class Projectile(MovableBox):
    def __init__(self, x, y, width, height, image=None, velocity=5, obstacles=None, damage=1, **kwargs):
        """
        Initialise un projectile avec une position, des dimensions, une image, une vélocité, des obstacles, et des dégâts.

        :param x: Coordonnée x du coin supérieur gauche du projectile.
        :param y: Coordonnée y du coin supérieur gauche du projectile.
        :param width: Largeur du projectile.
        :param height: Hauteur du projectile.
        :param velocity: Vélocité initiale du projectile.
        :param obstacles: Conteneur d'obstacles pour gérer les collisions.
        :param damage: Dégâts infligés par le projectile lors d'une collision.
        """
        super().__init__(x, y, width, height, image, collision_behavior=['stop'], velocity_x=velocity,
                         velocity_y=velocity, obstacles=obstacles, **kwargs)
        self.damage = damage
        self.life = 1
        self.velocity = velocity
        self.name = "projectile"

    def check_collision(self):
        #super().check_collision()
        for obstacle in self.voisins.keys():
            if self.voisins[obstacle] is not None and self.voisins[obstacle].name != self.name:
                if isinstance(self.voisins[obstacle],Player):
                    self.voisins[obstacle].life -= self.damage
                elif isinstance(self.voisins[obstacle],Brique):
                    self.obstacles.retirer(self.voisins[obstacle], True)
                self.life =0
                self.visible = False
                return

    def draw(self):
        if self.visible:
            r = rotate(math.atan2(-self.velocity_y, self.velocity_x), (self.centerx, self.centery))
            # rect(self.x, self.y, self.width, self.height, fill=self.fill,image=self.image)
            image(self.image, self.x, self.y)
            rotate(*r)


class Gun(MovableBox):
    def __init__(self, x, y, width, height, image=None, obstacles=None, angle=0, magazine_capacity=5, bullet_image=None,
                 **kwargs):
        """
        Initialise une arme avec une position, des dimensions, une image, un angle de tir, et un chargeur.

        :param x: Coordonnée x du coin supérieur gauche de l'arme.
        :param y: Coordonnée y du coin supérieur gauche de l'arme.
        :param width: Largeur de l'arme.
        :param height: Hauteur de l'arme.
        :param angle: Angle de tir en degrés (0-360).
        :param magazine_capacity: Capacité du chargeur.
        """
        super().__init__(x, y, width, height, image, ["life", "stop"], 0, 0, obstacles, **kwargs)
        if self.name == "":
            self.name = "gun"
        self.angle = angle
        self.magazine = BoxContainer(name="Magazine")
        self.magazine_capacity = magazine_capacity
        self.max_bullet_launched = kwargs.get("max_bullet_launched", None)
        self.bullet_launched = BoxContainer(max_objets=self.max_bullet_launched, name="Bullets launched")
        self.velocity = kwargs.get("velocity", 2)
        self.bullet_image = bullet_image
        self.reload_auto = kwargs.get("reload_auto", False)
        self.reload()
        self.life = 1
        self.longueur_canon = kwargs.get("longueur_canon", 0)



    def reload(self):
        """
        Recharge le chargeur avec des projectiles.
        """
        self.magazine.objets.clear()
        for _ in range(self.magazine_capacity):
            projectile = Projectile(0, 0, 0, 0, self.bullet_image,obstacles= self.obstacles, damage=1,
                                    fill="orange")  # Initialise les projectiles comme invisibles
            projectile.name = self.name
            self.magazine.ajouter(projectile)

    def fire(self):
        """
        Tire un projectile dans la direction spécifiée par l'angle.
        """
        if len(self.magazine.objets) == 0:
            if self.reload_auto:
                self.reload()
            return

        projectile = self.magazine.objets.pop()
        projectile.visible = True
        radian_angle = math.radians(self.angle)
        projectile.centerx = self.centerx + self.longueur_canon * math.cos(radian_angle)
        projectile.centery = self.centery - self.longueur_canon* math.sin(radian_angle)
        projectile.xf = projectile.x
        projectile.yf = projectile.y
        projectile.obstacles = self.obstacles
        projectile.container = None
        # Calcul de la vélocité en fonction de l'angle

        projectile.velocity_x = self.velocity * math.cos(radian_angle)
        projectile.velocity_y = -self.velocity * math.sin(radian_angle)

        # Ajoute le projectile aux obstacles pour gérer les collisions

        if not self.bullet_launched.isfull():
            self.bullet_launched.ajouter(projectile)
            self.obstacles.ajouter(projectile)
            projectile.visible = True


    def set_angle(self, angle):
        """
        Définit l'angle de tir de l'arme.

        :param angle: Nouvel angle de tir en degrés (0-360).
        """
        self.angle = angle % 360

    def draw(self):
        """
        Dessine l'arme si elle est visible.
        """
        if self.visible:
            super().draw()
            # Optionnel : dessiner une ligne ou une indication visuelle pour montrer la direction de tir

class Canon(Gun):
    def __init__(self, x, y, width, height, image=None, obstacles=None, angle=0, magazine_capacity=5, bullet_image=None,
                 **kwargs):
        kwargs["name"] = kwargs.get("name","canon")
        super().__init__(x, y, width, height, image, obstacles, angle, magazine_capacity, bullet_image, **kwargs)
        self.life = 1

    def draw(self):
        if self.visible:
            r = rotate(math.radians(self.angle), (self.centerx, self.centery))
            super().draw()
            rotate(*r)
    def calcule_angle(self):
        self.angle = -math.degrees(math.atan2(self.enemi.centery - self.centery, self.enemi.centerx - self.centerx))

    def calcule_distance(self):
        return math.sqrt((self.enemi.centerx - self.centerx) ** 2 + (self.enemi.centery - self.centery) ** 2)

    def set_enemi(self, enemi,distance):
        self.enemi = enemi
        self.distance = distance




class Levier(EventBox):
    def __init__(self, x, y, width, height, images: list, event, pos=0):
        """Initialise un levier avec une position, des dimensions, une liste d'images et un événement. Le nombre de positions est défini par le nombre d'images."""
        super().__init__(x, y, width, height, "levier", images[0], event)
        self.images = []
        for img in images:
            if isinstance(img, str):
                self.images.append(loadImage(img))
            else:
                self.images = img
        self.pos = pos
        self.enable = True
        self.time = time()

    def set_pos(self, pos):
        """Définit la position du levier."""
        if self.enable:
            if time()-self.time>0.5:
                self.time = time()
                self.pos = pos % len(self.images)
                self.image = self.images[self.pos]

    def up(self):
        self.set_pos(self.pos + 1)

    def down(self):
        self.set_pos(self.pos - 1)


class CatchBox(EventBox):
    def __init__(self, x, y, width, height, name, image, **kwargs):
        """Initialise une boîte de saisie d'objet avec une position, des dimensions, une image et un événement."""
        super().__init__(x, y, width, height, name, image, self.event)
        self.enable = True
        self.auto = kwargs.get("auto", False)

    def event(self, player, objet):
        if player.name == "player" and (player.catch or self.auto):
            player.inventaire.ajouter(objet)
            player.obstacles_balle.retirer(objet)
            player.inventaire.visible = True


class InfoBox(Box):
    def __init__(self, x, y, width, height, text, image=None, font_size=20, font_color="white", **kwargs):
        """Initialise une boîte d'information avec une position, des dimensions, un texte, une taille de police, une couleur de police et une couleur de fond."""
        super().__init__(x, y, width, height, image, **kwargs)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.center_box = kwargs.get("center", True)
        if self.center_box:
            self.x = (processing.width() - self.width) // 2
            self.y = (processing.height() - self.height) // 2

    def draw(self):
        if self.visible:
            if self.center_box:
                init_translate()
            super().draw()
            text(self.text, self.x, self.y, self.width, self.height, font_size=self.font_size,
                 font_color=self.font_color, align_h="center", align_v="center", no_fill=True, no_stroke=True)

class DamageBox(Box):
    def __init__(self, x, y, width, height, image, damage=1, **kwargs):
        super().__init__(x, y, width, height, image, **kwargs)
        self.damage = damage
        self.name = "damagebox"

class Level:
    def __init__(self, player, config, number=0):
        self.config_all = config
        self.config = self.config_all[number]
        self.number = self.config['number']
        self.player = player
        self.obstacles = BoxContainer()
        self.infos = InfoContainer()
        self.events = events
        self.completed = False
        self.event_fonctions = None

    def setup(self, event_fonctions=None):
        if event_fonctions is None and self.event_fonctions is None:
            raise ValueError("Event functions are not defined.")
        if event_fonctions is not None:
            self.event_fonctions = event_fonctions
        self.player.set_position(*self.config['player_position'])
        background(loadImage(self.config['background']))
        self.obstacles.objets.clear()
        self.infos.objets.clear()
        for obstacle_config in self.config['obstacles']:
            obstacle_type = obstacle_config.pop('type')
            if obstacle_type == "Box":
                self.obstacles.ajouter(Box(**obstacle_config))
            elif obstacle_type == "MovableBox":
                self.obstacles.ajouter(MovableBox(obstacles=self.obstacles, **obstacle_config))
            elif obstacle_type == "EventBox":
                event_name = obstacle_config.pop('event')
                event_function = self.event_fonctions.get(event_name)
                if event_function is not None:
                    self.obstacles.ajouter(EventBox(event=event_function, **obstacle_config))
                else:
                    print(f"Warning: Event function '{event_name}' is not defined.")
            elif obstacle_type == "CatchBox":
                self.obstacles.ajouter(CatchBox(**obstacle_config))
        for obstacle_config in self.config.get('infos') if self.config.get('infos') else []:
            obstacle_type = obstacle_config.pop('type')
            if obstacle_type == "InfoBox":
                self.infos.ajouter(InfoBox(**obstacle_config))
        self.player.obstacles_balle = self.obstacles
        self.player.obstacles = self.obstacles
        self.obstacles.ajouter(self.player)

    def update(self):
        if self.infos.visible:
            if keyIsDown(K_ESCAPE):
                self.infos.unvisible()
        else:
            self.obstacles.move()

    def draw(self):
        self.obstacles.draw()
        self.player.draw()
        self.infos.draw()

    def check_completion(self):
        condition = self.config['completion_condition']
        if condition['type'] == 'position':
            x = condition.get("x", False)
            y = condition.get("y", False)
            if x and y and self.player.x > x and self.player.y > y:
                self.completed = True
            elif x and self.player.x > x:
                self.completed = True
            elif y and self.player.y > y:
                self.completed = True
        elif condition['type'] == 'inventory':
            if any(objet.name == condition['item'] for objet in self.player.inventaire.objets):
                self.completed = True

    def next_level(self):
        if self.completed:
            if self.number < len(self.config_all):
                level = Level(self.player, self.config_all, number=self.number)
                level.setup(self.event_fonctions)
                return level
        return self
