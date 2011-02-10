from gtk import DrawingArea
from lib.graph.Graph import Graph
import gtk

class DrawArea(DrawingArea):
    def __init__(self, changed_method, complete=False):
        DrawingArea.__init__(self)
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.add_events(gtk.gdk.MOTION_NOTIFY)
        self.add_events(gtk.gdk.BUTTON1_MOTION_MASK)
        self.add_events(gtk.gdk.KEY_PRESS_MASK)
         
        self.connect('expose-event', self.expose)
        self.connect('button-press-event', self.mouse_press)
        self.connect('button-release-event',self.mouse_release)
        self.connect('motion-notify-event',self.mouse_motion) 
        
        self.action = None
        self.select = []
        self.graph = Graph(complete)
        self.cairo = None
        self.changed = False
        self.path = None
        
        self.set_double_buffered(True)
           
        self.changed_method = changed_method

    def set_changed(self, value):
        if self.changed != value:
            self.changed = value
            self.changed_method(self)
        
    def add_vertex(self, event):
        position = event.get_coords()
        self.graph.add_vertex(position)
        self.action = None
    
    def remove_vertex(self, event):
        position = event.get_coords()
        self.graph.remove_vertex(position)
        self.action = None
        
    def add_edge(self, event):
        if self.select:
            position = event.get_coords()
            vertex = self.graph.get_vertex_position(position)
            if vertex != None:
                self.graph.add_edge(self.select, vertex)
                self.deselect_all_vertex()
                #self.action = None
                return True
        else:
            self.select_vertex(event)
        return False
            
    def remove_edge(self, event):
        if self.select:
            position = event.get_coords()
            vertex = self.graph.get_vertex_position(position)
            if vertex != None:
                self.graph.remove_edge(self.select, vertex)
                self.deselect_all_vertex()
                #self.action = None
                return True
        else:
            self.select_vertex(event)
        return False
        
    def move_vertex(self, event):
        #Comment here to take this code cool
        #if len(self.select) > 0:
        #    self.deselect_all_vertex()
        ###
        self.select_vertex(event)
            
    def select_vertex(self, event):
        position = event.get_coords()
        vertex = self.graph.get_vertex_position(position)
        
        if vertex:
            vertex.select(True)
            if self.select.count(vertex) == 1:
                self.select.remove(vertex)
            self.select.append(vertex)
        else:
            self.deselect_all_vertex()
    
    def deselect_all_vertex(self):
        if len(self.select) > 0:
            for vertex in self.select:
                vertex.select(False)
            self.select  = []
        
    def mouse_press(self, widget, event):
        if self.action != None:
            self.set_changed(True)
        if self.action == None:
            self.move_vertex(event)
        elif self.action == "add_vertex":
            self.add_vertex(event)
        elif self.action == "remove_vertex":
            self.remove_vertex(event)
        elif self.action == "add_edge":
            self.add_edge(event)
        elif self.action == "remove_edge":
            self.remove_edge(event)
            
        self.draw()
        
    def mouse_release(self, widget, event):
        pass
    
    def mouse_motion(self, widget, event):
        if len(self.select) > 0:
            start_position = self.select[-1].position
            end_position = event.get_coords()
            
            delta_x = end_position[0] - start_position[0]
            delta_y = end_position[1] - start_position[1]
                        
            self.set_changed(True)
            for vertex in self.select:
                new_position = [vertex.position[0] + delta_x, vertex.position[1] + delta_y]
                vertex.position = new_position
            
            self.draw()
            self.queue_draw()

#    def keyboard_press(self, widget, event):
#        keyname = gtk.gdk.keyval_name(event.keyval)
#        print "Key %s (%d) was pressed" % (keyname, event.keyval)
#        if event.state & gtk.gdk.CONTROL_MASK:
#            print "Control was being held down"
#        if event.state & gtk.gdk.MOD1_MASK:
#            print "Alt was being held down"
#        if event.state & gtk.gdk.SHIFT_MASK:
#            print "Shift was being held down"

    def move_select_right(self):
        if len(self.select) == 1:
            order_x = sorted(self.graph.vertex, key=lambda vertex: vertex.position[0])
            index_x = order_x.index(self.select[0]) + 1
            order_x = order_x[index_x:]
            
            next_vertex = self.get_shortest_neighbor(self.select[0], order_x, 1)

            if next_vertex:                
                self.deselect_all_vertex()
                next_vertex.select(True)
                self.select.append(next_vertex)
                self.draw()            
                self.draw()
            
    def move_select_left(self):
        if len(self.select) == 1:
            order_x = sorted(self.graph.vertex, key=lambda vertex: vertex.position[0])
            index_x = order_x.index(self.select[0]) - 1
            order_x = order_x[:index_x]

            next_vertex = self.get_shortest_neighbor(self.select[0], order_x, 1)

            if next_vertex:
                self.deselect_all_vertex()
                next_vertex.select(True)
                self.select.append(next_vertex)
                self.draw() 
         
    def move_select_up(self):
        if len(self.select) == 1:
            order_y = sorted(self.graph.vertex, key=lambda vertex: vertex.position[1])
            index_y = order_y.index(self.select[0]) - 1
            order_y = order_y[:index_y]
                        
            next_vertex = self.get_shortest_neighbor(self.select[0], order_y, 0)

            if next_vertex:
                self.deselect_all_vertex()
                next_vertex.select(True)
                self.select.append(next_vertex)
                self.draw()
            
    def move_select_down(self):
        if len(self.select) == 1:
            order_y = sorted(self.graph.vertex, key=lambda vertex: vertex.position[1])
            index_y = order_y.index(self.select[0]) + 1
            order_y = order_y[index_y:]
                        
            next_vertex = self.get_shortest_neighbor(self.select[0], order_y, 0)
            
            if next_vertex:
                self.deselect_all_vertex()
                next_vertex.select(True)
                self.select.append(next_vertex)
                self.draw()

    def get_shortest_neighbor(self, vertex, neighbor, dot):
        next_vertex = None
        if len(neighbor) > 0:
            point_max = vertex.position[dot]
            point_min = vertex.position[dot]
            while not next_vertex:
                for current in neighbor:
                    if current.position[dot] == point_max:
                        next_vertex = current
                        break
                    elif current.position[dot] == point_min:
                        next_vertex = current
                        break
                point_max = point_max + 1
                point_min = point_min - 1
        return next_vertex    
    
        
    def get_shortest_euclidian_neighbor(self, vertex, neighbor):
        #Please, optimize this method..
        #Its using brute force!
        
        if neighbor.count(vertex) == 1:
            neighbor.remove(vertex)
        shortest_vertex = vertex
        shortest_distance = None
        for vertex in neighbor:
            delta_x = self.select[0].position[0] - vertex.position[0]
            delta_y = self.select[0].position[1] - vertex.position[1]
            distance = ((delta_x ** 2) + (delta_y ** 2)) ** 0.5
            if not shortest_distance or distance < shortest_distance:
                shortest_distance = distance
                shortest_vertex = vertex
                
        return shortest_vertex
          
    def create_area(self, widget, event):
        self.area = widget.get_allocation()
        
        self.cairo = widget.window.cairo_create()
        
        self.cairo.rectangle(0, 0, self.area.width, self.area.height)
        self.cairo.clip()
        
    def expose(self, widget, event):
        self.create_area(widget, event)
        self.cairo.rectangle(0, 0, self.area.width, self.area.height)
        self.cairo.set_source_rgb(1, 1, 1)     
        self.cairo.fill()
        
        self.graph.draw(self.cairo, self.area)
        
    def draw(self):
        self.cairo.save()
        self.queue_draw_area(0, 0, self.area.width, self.area.height)
        self.cairo.restore()
