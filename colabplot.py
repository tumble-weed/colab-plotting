

#----------------------------------------
from matplotlib import pyplot as plt
from collections import defaultdict
import ipywidgets as widgets
from IPython import display
global debug_dict
debug_dict = {}
class Display_():
    registered_containers = []
    def __init__(self):
      self.initialize()
    def initialize(self):
        #cls = self.__class__
      self.registered_containers = []
      self.output = widgets.Output()      
      pass
    def register_container(self,container):
        self.registered_containers.append(container)
    def get_displayables(self,):
        displayables = []
        for c in self.registered_containers:
            displayables = displayables +  c.get_displayables()
        return displayables
    def clear(self):
        # displayables = get_displayables()
        display.clear_output(wait=True)

    def display(self):
        displayables = self.get_displayables()
        display.display(*displayables,self.output)
        pass
    pass
Display = Display_()
#-----------------------------------------------
class Controller_():
    # assets = defaultdict(list)
    # buttons = []
    # counters = defaultdict(lambda:[0])
    # pending_updates = {}
    # cb_stack = []
    def __init__(self):
        self.initialize()        
    def initialize(self):
        self.assets = defaultdict(list)
        self.buttons = []
        self.counters = defaultdict(lambda:[0])
        self.pending_updates = {}
        self.callbacks = {}
        self.cb_stack = []
        self.pointers = {}
        Display.register_container(self)
        pass
    # @classmethod
    # def show(cls,):
    #     Display.clear()
    #     for cb_stack in cls.cb_stack:
    #         cb_stack()
    #     Display.display()
    #     cls.cb_stack = []

    def flush_cb_stack(self):
        debug_dict['cb_stack'] = []
        for cbi,cb in enumerate(self.cb_stack):
            debug_dict['cb_stack'].append(cbi)
            cb()
        Display.clear()
        Display.display()
        self.cb_stack = []

    def __getattr__(self,attr):
      if attr in self.__dict__:
        return self.__dict__[attr]
      if hasattr(PyPlot,attr):
        plt_fn_name = attr
        def append_and_register_cb(*args,**kwargs):
          k = args[0]
          args = args[1:]
          self.assets[k].append({'args':args,'kwargs':kwargs})
          #---------------------------
        #   plt_fn = getattr(plt,attr)
          def cb():
            print(k,self.counters[k][0])
            assets_k = self.assets[k][self.counters[k][0]]
            getattr(PyPlot,plt_fn_name)(k,*assets_k['args'],**assets_k['kwargs'])
            self.pointers[k] = self.counters[k][0]
            pass
          self.callbacks[k] = cb
          #---------------------------
        return append_and_register_cb
      raise Exception
      pass
    """
    def imshow(self,imshow_dict):
        # print('Here')
        # import pdb;pdb.set_trace()
        for k,v in imshow_dict.items():
            print(k)
            self.assets[k].append(v)

            # ctr_k = cls.counters[k]
            # to_show_now = {k:cls.assets[k][cls.counters[k][0]]}
            # cb = lambda to_show_now=to_show_now:PyPlot.imshow(to_show_now)

            # if k not in cls.callbacks:
            if True:
                def cb():
                    print(k,self.counters[k][0])
                    PyPlot.imshow({k:self.assets[k][self.counters[k][0]]})
                    self.pointers[k] = self.counters[k][0]
                    pass
                self.callbacks[k] = cb

    def plot(self,plot_dict):
        # for k,v in imshow_dict.items():
        #     cls.assets[k].append(v)
        #     ctr_k = cls.counters[k]
        #     to_show_now = {k:cls.assets[k][cls.counters[k]]}
        #     # cb = lambda to_show_now=to_show_now:PyPlot.plot(to_show_now)
        #     def cb():
        #         print(k,cls.counters[k][0])
        #         PyPlot.plot({k:cls.assets[k][cls.counters[k][0]]})
        #         pass
        #     cls.cb_stack.append(cb)
        for k,v in plot_dict.items():
            print(k)
            self.assets[k].append(v)

            # ctr_k = cls.counters[k]
            # to_show_now = {k:cls.assets[k][cls.counters[k][0]]}
            # cb = lambda to_show_now=to_show_now:PyPlot.imshow(to_show_now)

            # if k not in cls.callbacks:
            if True:
                def cb():
                    print(k,self.counters[k][0])
                    PyPlot.plot({k:self.assets[k][self.counters[k][0]]})
                    self.pointers[k] = self.counters[k][0]
                    pass
                self.callbacks[k] = cb
        pass
		"""
    def attach_controller(self,names):
        these_counters =[]
        for n in names:
            self.assets[n]
            these_counters.append(self.counters[n])
            
        # def get_update_callback():
            # def update_callback():
                # pass
        # these

        def create_iterator_buttons(names):
            with Display.output:
                next = widgets.Button(description="Next")
                prev = widgets.Button(description="Prev")
                
                # counter_list = [-1]
                # assets = AssetManager.assets[nam)
                def get_on_button_clicked(counter_change):
                    def on_button_clicked(b):
                        print(f'button clicked')
                        #------------------------
                        # this_asset = assets[counter_list[0]]
                        # Display.display_callbacks[name](this_asset)
                        # cls.display_callbacks[name](this_asset)
                        for n in names:
                            counter = self.counters[n]
                            asset = self.assets[n]
                            limit = len(asset)
                            if limit > 0:
                                counter[0] += counter_change
                                counter[0] = counter[0] % limit
                            if n in self.callbacks:
                                print(f'adding callback for {n}')
                                self.cb_stack.append(self.callbacks[n])

                        self.flush_cb_stack()
                        #------------------------
                    return on_button_clicked
                next.on_click(get_on_button_clicked(1))
                prev.on_click(get_on_button_clicked(-1))
                return next,prev       
        b_prev,b_next = create_iterator_buttons(names)
        self.buttons.append((b_prev,b_next))
        pass

    def get_buttons(self):
        #TODO
        raise NotImplementedError
        pass

    def get_displayables(self):
        buttons = []
        for pair in self.buttons:
            for b in pair:
                buttons.append(b)
        return buttons
Controller = Controller_()
#-----------------------------------------------
class  PyPlot_():
    axes_dict = {}
    def __init__(self):
        self.initialize()
        
    def initialize(self):
        self.axes_dict = {}
        Display.register_container(self)
        pass      

    def figure(self,*axes,**kwargs):
        for name in axes:
            '''
            plt.figure()
            ax = plt.gca()
            cls.axes_dict[name] = ax
            '''
            self.subplots(name,nrows=1,ncols=1,**kwargs)
        pass


    def subplots(self,*axes,nrows=None,ncols=None,**kwargs):
        axes_names = axes
        if nrows is None and ncols is None:
            nrows,ncols = 1,len(axes_names)
            pass
        
        f,axes = plt.subplots(nrows,ncols,**kwargs)
        try:
            axes[0]
        except TypeError:
            axes = [axes]
        for n,ax in zip(axes_names,axes):
            # ax.imshow(np.zeros((227,227)))
            self.axes_dict[n] = ax

    def wrap_pyplot_method(self,plt_fn_name):
        def wrapped(*args,**kwargs):
          name = args[0]
          args = args[1:]
          ax = self.axes_dict[name]
          ax.clear()
          # plt.figure(ax.figure.number)
        #   plt.sca(ax)
          plt_fn = getattr(ax,plt_fn_name)
          plt_fn(*args,**kwargs)
          plt.draw()
          #ax.imshow(*stuff)
        return wrapped
      
    def __getattr__(self,attr):
      if attr in self.__dict__:
        return self.__dict__[attr]
      if hasattr(plt,attr):
        plt_fn_name = attr
        # plt_fn = plt.__dict__[attr]
        
        return self.wrap_pyplot_method(attr)
      raise Exception
      pass
    """
    def imshow(self,imshow_dict):
        '''
        all_axes = list(cls.axes_dict.values())
        figures = [ax.figure for ax in all_axes]
        unique_figures = list(set(figures))
        figures_to_axes = {}
        for f in unique_figures:
            for gi,g in enumerate(figures):
                if g == f:
                    ax = all_axes[gi]
                    ax.imshow(im)
            f.canvas.draw()
        '''
        # '''
        for name,im in imshow_dict.items():
            ax = self.axes_dict[name]
            ax.clear()
            # plt.figure(ax.figure.number)
            # plt.sca(ax)
            ax.imshow(im)
            # ax.canvas.draw()
            # plt.draw(),**kwargs
            # ax.figure.canvas.draw()
        # !
        # '''

    def plot(self,plot_dict):
        for name,im in plot_dict.items():
            ax = self.axes_dict[name]
            ax.clear()
            # plt.figure(ax.figure.number)
            # plt.sca(ax)
            ax.plot(im)
        pass
        
		"""
    def get_displayables(self):
        axes = list(self.axes_dict.values())
        figures = []
        for ax in axes:
            if ax.figure not in figures:
                figures.append(ax.figure)
        # figures = [ax.figure for ax in axes]
        # print(len(figures))
        return figures
        # return axes
PyPlot = PyPlot_()


#--------------------
# imshow(im)
# PyPlot.scatter('xy',x,y)
# #scatter({'xy':x,y})
# #Controller['xy'].scatter(x,y,)
# #PyPlot['xy'].scatter(x,y)
# #Pyplot.scatter('xy',...
#               'xy2',...)
# #Pyplot['xy','xy1','xy2'].scatter()...

# def wrapped():
#   pass


