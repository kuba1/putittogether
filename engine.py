#!/usr/bin/python2

import sys
import math
import random
import pygame
from pygame.locals import *
import wx

def get_random_edge():
    if random.random() > 0.5: return Element.CONCAVE
    else: return Element.CONVEX

def distance(p1, p2):
    return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))

def opposite(side):
    if side - 2 < 0:
        return side + 2
    else:
        return side - 2

def neighbouring(side):
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
        self.is_checking = False

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
            e.attach(self, opposite(side))

    def attach_actual(self, e, side, move = False):
        if self.attached_actual[side] != e:
            if move:
                if side is Element.LEFT:
                    self.move(e.rect.centerx + e.rect.width - self.rect.centerx,
                            e.rect.centery - self.rect.centery, True)
                elif side is Element.UP:
                    self.move(e.rect.centerx - self.rect.centerx,
                            e.rect.centery + e.rect.height - self.rect.centery, True)
                elif side is Element.RIGHT:
                    self.move(e.rect.centerx - e.rect.width - self.rect.centerx,
                            e.rect.centery - self.rect.centery, True)
                elif side is Element.DOWN:
                    self.move(e.rect.centerx - self.rect.centerx,
                            e.rect.centery - e.rect.height - self.rect.centery, True)
                else:
                    print('oops... error...')

            self.attached_actual[side] = e
            e.attach_actual(self, opposite(side))

            if move:
                self.check_other_edges(side)

    def detach_actual_all(self):
        for i, e in enumerate(self.attached_actual):
            if e:
                self.attached_actual[i] = None
                e.detach_actual(opposite(i))

    def detach_actual(self, side):
        if self.attached_actual[side]:
            e = self.attached_actual[side]
            self.attached_actual[side] = None
            e.detach_actual(opposite(side))

    def check_other_edges(self, side):
        if not self.is_checking:
            self.is_checking = True
            for i, e in enumerate(self.attached_actual):
                if i is side:
                    continue
                if not e:
                    m = self.group.check_matching_edge(self, i)
                    if m:
                        self.attach_actual(m, i)
                else:
                    e.check_other_edges(opposite(i))

    def verify(self):
        for i, e in enumerate(self.attached):
            if e is not self.attached_actual[i]:
                return False
        return True

    def set_edge(self, edge, side):
        self.edges[side] = edge

    def create_flat_edges(self):
        for i, e in enumerate(self.edges):
            if not e:
                self.edges[i] = Element.FLAT
                if self.attached[i]:
                    self.attached[i].set_edge(Element.FLAT, opposite(i))

    def create_random_edges(self):
        for i, e in enumerate(self.edges):
            if not e:
                if self.attached[i]:
                    self.edges[i] = get_random_edge()
                    self.attached[i].set_edge(-self.edges[i], opposite(i))
                else:
                    self.edges[i] = Element.FLAT

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

    def clear_moved(self):
        for s in self.sprites():
            if s.was_moved:
                s.was_moved = False

    def clear_checking(self):
        for s in self.sprites():
            if s.is_checking:
                s.is_checking = False

    def check_matching_edge(self, e, edge):
        sps = self.sprites()

        for s in sps:
            if s is e:
                continue
            if edge is Element.LEFT:
                dl = distance(e.rect.midleft, s.rect.midright)
            elif edge is Element.UP:
                dl = distance(e.rect.midtop, s.rect.midbottom)
            elif edge is Element.RIGHT:
                dl = distance(e.rect.midright, s.rect.midleft)
            elif edge is Element.DOWN:
                dl = distance(e.rect.midbottom, s.rect.midtop)
            if dl < 0.001:
                return s
        return None

    def find_nearest_by_edge(self, e):
        sps = self.sprites()

        nearest_dist = distance(e.rect.midleft, sps[0].rect.midright)
        nearest_edge = Element.LEFT
        nearest = sps[0]
        for s in sps:
            if s is e or s in e.attached_actual:
                continue
            dl = distance(e.rect.midleft, s.rect.midright)
            du = distance(e.rect.midtop, s.rect.midbottom)
            dr = distance(e.rect.midright, s.rect.midleft)
            db = distance(e.rect.midbottom, s.rect.midtop)
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

class PuzzleFrame(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.elements_group = []

        pygame.init()
        self.size = self.GetSize()
        self.resize = False

        self.screen = pygame.Surface(self.size, 0, 32)
        self.clock = pygame.time.Clock()

        self.mouse_last = (0,0)
        self.selected = None
        self.dragging = False
        self.resize = False
        self.do_update = False

        self.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)
        self.Bind(wx.EVT_RIGHT_DOWN, self._on_right_down)
        self.Bind(wx.EVT_LEFT_UP, self._on_up)
        self.Bind(wx.EVT_RIGHT_UP, self._on_up)
        self.Bind(wx.EVT_MOTION, self._on_motion)
        self.Bind(wx.EVT_SIZE, self._on_resize)
        self.Bind(wx.EVT_PAINT, self._on_paint)

    def _on_paint(self, e):
        self._redraw()
        e.Skip()

    def _on_left_down(self, e):
        self.mouse_last = e.GetPosition()
        sels = self.elements_group.get_sprites_at(e.GetPosition())
        num = len(sels)
        if num > 0:
            self.selected = sels[num - 1]
            self.selected.detach_actual_all()
            self.elements_group.move_to_front(self.selected)
            self.do_update = True
        else:
            self.selected = None

    def _on_right_down(self, e):
        self.mouse_last = e.GetPosition()
        sels = self.elements_group.get_sprites_at(e.GetPosition())
        num = len(sels)
        if num > 0:
            self.selected = sels[num - 1]
            self.elements_group.move_to_front(self.selected)
            self.do_update = True
        else:
            self.selected = None

    def _on_up(self, e):
        if self.dragging:
            self.dragging = False
            elem, edge, dist = self.elements_group.find_nearest_by_edge(self.selected)
            if dist < 20.0:
                self.selected.attach_actual(elem, edge, True)
                #elem.attach_actual(selected, opposite(edge), True)
                self.do_update = True
                self.elements_group.clear_moved()
                self.elements_group.clear_checking()
                if self.elements_group.verify():
                    wx.MessageBox('Gratuluje! Jestes mistrzem!', 'Info', wx.OK | wx.ICON_INFORMATION);

    def _on_motion(self, e):
        if e.Dragging():
            if self.selected:
                if e.LeftIsDown():
                    self.selected.move(e.GetX() - self.mouse_last[0], e.GetY() - self.mouse_last[1])
                    self.mouse_last = e.GetPosition()
                    self.dragging = True
                    self.elements_group.clear_moved()
                    self.do_update = True
                if e.RightIsDown():
                    self.selected.move(e.GetX() - self.mouse_last[0], e.GetY() - self.mouse_last[1], True)
                    self.mouse_last = e.GetPosition()
                    self.dragging = True
                    self.elements_group.clear_moved()
                    self.do_update = True

    def _on_resize(self, e):
        self.size = self.GetSize()
        self.resize = True
        self._redraw()

    def update(self):
        if self.do_update:
            self.do_update = False
            self._redraw()

    def _redraw(self):
        if self.resize:
            self.resize = False
            self.screen = pygame.Surface(self.size, 0, 32)

        #TODO: fill with wx.Window background color
        self.screen.fill((255,255,255))
        if self.elements_group:
            self.elements_group.draw(self.screen)
        s = pygame.image.tostring(self.screen, 'RGB')
        img = wx.ImageFromData(self.size[0], self.size[1], s)
        bmp = wx.BitmapFromImage(img)
        dc = wx.ClientDC(self)
        dc.DrawBitmap(bmp, 0, 0)
        del dc

    def load_puzzle(self, path):
        #number of columns
        n = 5
        #number of rows
        m = 5
        #number of elements
        e = n*m
        self.elements = []

        #load a picture and rescale it to fit the display
        image = wx.Image(path)

        xscale = float(self.size[0]) * 3.0 / 4.0 / float(image.GetSize()[0])
        yscale = float(self.size[1]) * 3.0 / 4.0 / float(image.GetSize()[1])

        if xscale < yscale:
            image.Rescale(xscale * float(image.GetSize()[0]), xscale * float(image.GetSize()[1]))
        else:
            image.Rescale(yscale * float(image.GetSize()[0]), yscale * float(image.GetSize()[1]))

        puzzle = pygame.image.fromstring(image.GetData(), image.GetSize(), "RGB")
        #slice the picture
        ew = puzzle.get_rect().width / n
        eh = puzzle.get_rect().height / m

        #generate definition table for the edges
        for i in range(0,e):
            r = math.floor(i / n)
            c = i % n
            rect = pygame.Rect(c * ew, r * eh, ew, eh)
            new = Element(puzzle.subsurface(rect))

            #TODO: change hardcoded values
            new.move(random.random() * self.size[0] - ew, self.size[1] - random.random() * self.size[1]/4 - eh)
            self.elements.append(new)
            if i is not 0:
                if i % n > 0:
                    new.attach(self.elements[i-1], Element.LEFT)
                if i >= n:
                    new.attach(self.elements[i-n], Element.UP)

        for e in self.elements:
            e.create_flat_edges()
            #e.create_random_edges()

        self.elements_group = EnhancedLayeredUpdates(self.elements)
        self.do_update = True
