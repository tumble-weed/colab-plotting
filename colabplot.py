from matplotlib import pyplot as plt
from collections import defaultdict
import ipywidgets as widgets
from IPython import display

class Display():
    registered_containers = []
    def __init__(self):
        cls = self.__class__
        cls.registered_containers = []
        cls.output = widgets.Output()
    @classmethod
    def register_container(cls,container):
        cls.registered_containers.append(container)
    @classmethod
    def get_displayables(cls,):
        displayables = []
        for c in cls.registered_containers:
            displayables = displayables +  c.get_displayables()
        return displayables
    @classmethod
    def clear(cls):
        # displayables = get_displayables()
        display.clear_output(wait=True)
    @classmethod
    def display(cls):
        displayables = cls.get_displayables()
        display.display(*displayables,cls.output)
        pass
    pass
class Controller():
    # assets = defaultdict(list)
    # buttons = []
    # counters = defaultdict(lambda:[0])
    # pending_updates = {}
    # cb_stack = []
    def __init__(self):
        # print('Here1')
        cls = self.__class__
        
        cls.assets = defaultdict(list)
        cls.buttons = []
        cls.counters = defaultdict(lambda:[0])
        cls.pending_updates = {}
        cls.callbacks = {}
        cls.cb_stack = []
        cls.pointers = {}
        Display.register_container(cls)
        
        pass
    # @classmethod
    # def show(cls,):
    #     Display.clear()
    #     for cb_stack in cls.cb_stack:
    #         cb_stack()
    #     Display.display()
    #     cls.cb_stack = []
    @classmethod
    def flush_cb_stack(cls):
        
        for cb in cls.cb_stack:
            cb()
        Display.clear()
        Display.display()
        cls.cb_stack = []
    @classmethod
    def imshow(cls,imshow_dict):
        # print('Here')
        # import pdb;pdb.set_trace()
        for k,v in imshow_dict.items():
            print(k)
            cls.assets[k].append(v)

            # ctr_k = cls.counters[k]
            # to_show_now = {k:cls.assets[k][cls.counters[k][0]]}
            # cb = lambda to_show_now=to_show_now:PyPlot.imshow(to_show_now)

            # if k not in cls.callbacks:
            if True:
                def cb():
                    print(k,cls.counters[k][0])
                    PyPlot.imshow({k:cls.assets[k][cls.counters[k][0]]})
                    cls.pointers[k] = cls.counters[k][0]
                    pass
                cls.callbacks[k] = cb
    pass
    @classmethod
    def plot(cls,plot_dict):
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
            cls.assets[k].append(v)

            # ctr_k = cls.counters[k]
            # to_show_now = {k:cls.assets[k][cls.counters[k][0]]}
            # cb = lambda to_show_now=to_show_now:PyPlot.imshow(to_show_now)

            # if k not in cls.callbacks:
            if True:
                def cb():
                    print(k,cls.counters[k][0])
                    PyPlot.plot({k:cls.assets[k][cls.counters[k][0]]})
                    cls.pointers[k] = cls.counters[k][0]
                    pass
                cls.callbacks[k] = cb
        pass
    @classmethod
    def attach_controller(cls,names):
        these_counters =[]
        for n in names:
            cls.assets[n]
            these_counters.append(cls.counters[n])
            
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
                            counter = cls.counters[n]
                            asset = cls.assets[n]
                            limit = len(asset)
                            if limit > 0:
                                counter[0] += counter_change
                                counter[0] = counter[0] % limit
                            if n in cls.callbacks:
                                print(f'adding callback for {n}')
                                cls.cb_stack.append(cls.callbacks[n])

                        cls.flush_cb_stack()
                        #------------------------
                    return on_button_clicked
                next.on_click(get_on_button_clicked(1))
                prev.on_click(get_on_button_clicked(-1))
                return next,prev       
        b_prev,b_next = create_iterator_buttons(names)
        cls.buttons.append((b_prev,b_next))
        pass
    @classmethod
    def get_buttons(cls):
        #TODO
        raise NotImplementedError
        pass
    @classmethod
    def get_displayables(cls):
        buttons = []
        for pair in cls.buttons:
            for b in pair:
                buttons.append(b)
        return buttons

class  PyPlot():
    axes_dict = {}
    def __init__(self):
        cls = self.__class__
        cls.axes_dict = {}
        Display.register_container(cls)
        pass
    @classmethod
    def figure(cls,*axes,**kwargs):
        for name in axes:
            '''
            plt.figure()
            ax = plt.gca()
            cls.axes_dict[name] = ax
            '''
            cls.subplots(name,nrows=1,ncols=1,**kwargs)
        pass

    @classmethod
    def subplots(cls,*axes,nrows=None,ncols=None,**kwargs):
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
            cls.axes_dict[n] = ax
        
    @classmethod
    def imshow(cls,imshow_dict):
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
            ax = cls.axes_dict[name]
            ax.clear()
            # plt.figure(ax.figure.number)
            # plt.sca(ax)
            ax.imshow(im)
            # ax.canvas.draw()
            # plt.draw(),**kwargs
            # ax.figure.canvas.draw()
        # !
        # '''
    @classmethod
    def plot(cls,plot_dict):
        for name,im in plot_dict.items():
            ax = cls.axes_dict[name]
            ax.clear()
            # plt.figure(ax.figure.number)
            # plt.sca(ax)
            ax.plot(im)
        pass

    @classmethod
    def get_displayables(cls):
        axes = list(cls.axes_dict.values())
        figures = []
        for ax in axes:
            if ax.figure not in figures:
                figures.append(ax.figure)
        # figures = [ax.figure for ax in axes]
        # print(len(figures))
        return figures
        # return axes

    





