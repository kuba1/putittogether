#!/usr/bin/python2

import sys
import math
import random
import pygame
from pygame.locals import *

def GetRandomEdge():
    if random.random() > 0.5: return Element.CONCAVE
    else: return Element.CONVEX

def Distance(p1, p2):
    return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))

def Opposite(side):
    if side - 2 < 0:
        return side + 2
    else:
        return side - 2

def Neighbouring(side):
    n = [side - 1, side + 1]
    if n[0] is -1:
        n[0] = 3
    if n[1] is 4:
        n[1] = 0

class Element(pygame.sprite.Sprite):
    CONVEX = -1
    FLAT = 0
    CONCAVE = 1

    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

    def __init__(self, image = None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = None
        if self.image:
            self.rect = image.get_rect()

        # [left, up, right, down]
        self.attached = [None, None, None, None]
        self.attached_actual = [None, None, None, None]
        self.edges = [None, None, None, None]

        self.group = None

        self.was_moved = False

    def move(self, dx, dy, move_att = False):
        if not self.was_moved:
            self.was_moved = True
            x = self.rect.center[0]
            y = self.rect.center[1]
            self.rect.center = (x + dx, y + dy)
            if move_att:
                for e in self.attached_actual:
                    if e:
                        e.move(dx, dy, True)
            #self.was_moved = False

    def attach(self, e, side):
        if self.attached[side] != e:
            self.attached[side] = e
            e.attach(self, Opposite(side))

    def attachActual(self, e, side, move = False):
        if self.attached_actual[side] != e:
            if move:
                if side is Element.LEFT:
                    #self.rect.center = (e.rect.centerx + e.rect.width, e.rect.centery)
                    self.move(e.rect.centerx + e.rect.width - self.rect.centerx,
                            e.rect.centery - self.rect.centery, True)
                elif side is Element.UP:
                    self.rect.center = (e.rect.centerx, e.rect.centery + e.rect.height)
                elif side is Element.RIGHT:
                    self.rect.center = (e.rect.centerx - e.rect.width, e.rect.centery)
                elif side is Element.DOWN:
                    self.rect.center = (e.rect.centerx, e.rect.centery - e.rect.height)
                else:
                    print('oops... error...')

            self.attached_actual[side] = e
            e.attachActual(self, Opposite(side))

            if move:
                self.checkOtherEdges(side)

    def detachActualAll(self):
        for i, e in enumerate(self.attached_actual):
            if e:
                self.attached_actual[i] = None
                e.detachActual(Opposite(i))

    def detachActual(self, side):
        if self.attached_actual[side]:
            e = self.attached_actual[side]
            self.attached_actual[side] = None
            e.detachActual(Opposite(side))

    def checkOtherEdges(self, side):
        for i, e in enumerate(self.attached_actual):
            if i is side:
                continue
            if not e:
                m = self.group.checkMatchingEdge(self, i)
                if m:
                    self.attachActual(m, i)
            else:
                e.checkOtherEdges(Opposite(i))

    def verify(self):
        for i, e in enumerate(self.attached):
            print(i, e, self.attached_actual[i])
            if e is not self.attached_actual[i]:
                return False
        return True

    def setEdge(self, edge, side):
        self.edges[side] = edge

    def createFlatEdges(self):
        for i, e in enumerate(self.edges):
            if not e:
                self.edges[i] = Element.FLAT
                if self.attached[i]:
                    self.attached[i].setEdge(Element.FLAT, Opposite(i))

    def createRandomEdges(self):
        for i, e in enumerate(self.edges):
            if not e:
                if self.attached[i]:
                    self.edges[i] = GetRandomEdge()
                    self.attached[i].setEdge(-self.edges[i], Opposite(i))
                else:
                    self.edges[i] = Element.FLAT

    def debugDump(self):
        print(self.edges[0], self.edges[1], self.edges[2], self.edges[3])

class EnhancedLayeredUpdates(pygame.sprite.LayeredUpdates):
    def __init__(self, elements):
        pygame.sprite.LayeredUpdates.__init__(self, *elements)
        for e in elements:
            e.group = self

    def verify(self):
        for s in self.sprites():
            if not s.verify():
                return False
        return True

    def clearMoved(self):
        for s in self.sprites():
            if s.was_moved:
                s.was_moved = False

    def checkMatchingEdge(self, e, edge):
        sps = self.sprites()

        for s in sps:
            if s is e:
                continue
            if edge is Element.LEFT:
                dl = Distance(e.rect.midleft, s.rect.midright)
            elif edge is Element.UP:
                dl = Distance(e.rect.midtop, s.rect.midbottom)
            elif edge is Element.RIGHT:
                dl = Distance(e.rect.midright, s.rect.midleft)
            elif edge is Element.DOWN:
                dl = Distance(e.rect.midbottom, s.rect.midtop)
            if dl < 0.001:
                return s
        return None

    def findNearestByEdge(self, e):
        sps = self.sprites()

        nearest_dist = Distance(e.rect.midleft, sps[0].rect.midright)
        nearest_edge = Element.LEFT
        nearest = sps[0]
        for s in sps:
            if s is e or s in e.attached_actual:
                continue
            dl = Distance(e.rect.midleft, s.rect.midright)
            du = Distance(e.rect.midtop, s.rect.midbottom)
            dr = Distance(e.rect.midright, s.rect.midleft)
            db = Distance(e.rect.midbottom, s.rect.midtop)
            if dl < nearest_dist:
                nearest_dist = dl
                nearest_edge = Element.LEFT
                nearest = s
            if du < nearest_dist:
                nearest_dist = du
                nearest_edge = Element.UP
                nearest = s
            if dr < nearest_dist:
                nearest_dist = dr
                nearest_edge = Element.RIGHT
                nearest = s
            if db < nearest_dist:
                nearest_dist = db
                nearest_edge = Element.DOWN
                nearest = s
        return (nearest, nearest_edge, nearest_dist)

pygame.init()
screen = pygame.display.set_mode((800,600), DOUBLEBUF)
clock = pygame.time.Clock()

#number of columns
n = 3
#number of rows
m = 3
#number of elements
e = n*m
elements = []

#slice the picture
puzzle = pygame.image.load('Lenna.png')
ew = puzzle.get_rect().width / n
eh = puzzle.get_rect().height / m
print(ew, eh)

#generate definition table for the edges
for i in range(0,e):
    r = math.floor(i / n)
    c = i % n
    rect = pygame.Rect(c * ew, r * eh, ew, eh)
    new = Element(puzzle.subsurface(rect))
    new.move(random.random() * (800 - ew), random.random() * (600 - eh))
    elements.append(new)
    if i is not 0:
        if i % n > 0:
            new.attach(elements[i-1], Element.LEFT)
        if i >= n:
            new.attach(elements[i-n], Element.UP)

for e in elements:
    e.createFlatEdges()
    #e.createRandomEdges()
    e.debugDump()

print('midleft', elements[0].rect.midleft)

elements_group = EnhancedLayeredUpdates(elements)
mouse_last = (0,0)
update = True
selected = None
dragging = False
while True:
    deltat = clock.tick(30)
    for e in pygame.event.get():
        if e.type is KEYDOWN:
            if e.key is K_ESCAPE:
                sys.exit(0)
            elif e.key is K_f:
                screen = pygame.display.set_mode((0,0),FULLSCREEN)

        elif e.type is MOUSEBUTTONDOWN:
            if e.button is 1:
                mouse_last = e.pos
                sels = elements_group.get_sprites_at(e.pos)
                num = len(sels)
                if num > 0:
                    selected = sels[num - 1]
                    selected.detachActualAll()
                    elements_group.move_to_front(selected)
                    update = True
                else:
                    selected = None
            elif e.button is 3:
                mouse_last = e.pos
                sels = elements_group.get_sprites_at(e.pos)
                num = len(sels)
                if num > 0:
                    selected = sels[num - 1]
                    elements_group.move_to_front(selected)
                    update = True
                else:
                    selected = None
            elif e.button is 2:
                sels = elements_group.get_sprites_at(e.pos)
                #print(sels[len(sels) - 1].attached_actual)
                print(sels[len(sels) - 1].verify())

        elif e.type is MOUSEMOTION:
            if e.buttons[0] is 1:
                if selected:
                    selected.move(e.pos[0] - mouse_last[0], e.pos[1] - mouse_last[1])
                    mouse_last = e.pos
                    update = True
                    dragging = True
                    elements_group.clearMoved()
            elif e.buttons[2] is 1:
                if selected:
                    selected.move(e.pos[0] - mouse_last[0], e.pos[1] - mouse_last[1], True)
                    mouse_last = e.pos
                    update = True
                    dragging = True
                    elements_group.clearMoved()

        elif e.type is MOUSEBUTTONUP:
            if dragging:
                dragging = False
                elem, edge, dist = elements_group.findNearestByEdge(selected)
                print(elem, edge, dist)
                if dist < 20.0:
                    selected.attachActual(elem, edge, True)
                    #elem.attachActual(selected, Opposite(edge), True)
                    update = True
                    elements_group.clearMoved()
                    if elements_group.verify():
                        print("ZWYCIESTWO!!!!!!!!!!")
                    else:
                        print("jeszcze nie")

    if update:
        update = False
        screen.fill((255,255,255))
        elements_group.update()
        elements_group.draw(screen)
        pygame.display.flip()
