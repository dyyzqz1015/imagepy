# -*- coding: utf-8 -*-

from core.engines import Simple
from imageplus import ImagePlus
from ui.canvasframe import CanvasFrame
from core.managers import ConfigManager
from ui.panelconfig import ParaDialog
import numpy as np
import IPy

def add(recent, v):
    if v in recent:
        idx = recent.index(v)
        recent.insert(0, recent.pop(idx))
    else: 
        recent.insert(0, v)
    if len(recent)>5:
        del recent[5:]

class ScaleDialog(ParaDialog):
    def para_check(self, para, key):
        if key=='recent' and para[key] != 'Recent':
            k, u = para[key].split(' - ')
            para['k'], para['unit'] = float(k), u
            self.reset()
        return True

class Plugin(Simple):
    title = 'Scale And Unit'
    note = ['all']
    recent = []
    
    para = {'k':1.0, 'unit':'pix', 'kill':False, 'recent':'Recent'}
    view = [(float, (0,1000000), 1, 'per', 'k', 'pix'),
            (str, 'unit', 'unit',''),
            (list, [], str, 'commen', 'recent', ''),
            (bool, 'kill scale', 'kill')]
    
    def show(self):
        self.dialog = ScaleDialog(IPy.get_window(), self.title)
        self.dialog.init_view(self.view, self.para)
        self.dialog.set_handle(lambda x:self.preview(self.para))
        return self.dialog.ShowModal()

    def load(self, ips):
        self.recent = ConfigManager.get('recent-units')
        if self.recent == None : self.recent = ['Recent']
        else: self.recent.insert(0, 'Recent')
        self.view[2] = (list, self.recent, str, 'commen', 'recent', '')
        if ips.unit==None: 
            self.para['K'],self.para['unit'] = (1, 'pix')
        else: self.para['k'], self.para['unit'] = ips.unit
        return True

    #process
    def run(self, ips, imgs, para = None):
        if para['kill'] : ips.unit=None
        else : 
            ips.unit = (para['k'], para['unit'])
            self.recent.pop(0)
            add(self.recent, '%s - %s'%(para['k'], para['unit']))
            ConfigManager.set('recent-units', self.recent)