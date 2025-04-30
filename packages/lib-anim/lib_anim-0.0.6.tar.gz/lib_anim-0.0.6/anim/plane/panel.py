"""
Simple tools for displaying 2D animations

Animation2d
-----------

The :class:`Animation2d` wraps a  ``QGraphicsView`` and ``QGraphicsScene``
as well as all necessary tools for display (scene limits, antialiasing, etc.)
Groups of elements can be formed for easier manipulation, and user interaction 
is possible (drag, click, etc.). It contains a timer triggering the 
:py:meth:`Animation2d.update` method at a regular pace. In subclasses, this 
allows to change elements' positions or features (color, size, etc.) to create
animations.

Items
--------

The items are the elements displayed in the scene (*e.g.* circles, lines, ...).
They derive both from the generic class :class:`item` and from their corresponding 
``QGraphicsItem``. They are incorporaeted in the animation *via* 
:py:meth:`Animation2d.add`.

Simple animation window
-----------------------

The :class:`Window` class creates a simple window containing the 
:py:meth:`Animation2d.Qview` widget. It manages the ``QApplication``, size 
on screen, shortcuts and timer trig. If an :class:`Animation2d` object is
created without parent (``QWidget`` or :class:`Window`), the default 
:class:`Window` is automatically created.
"""

from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPen, QColorConstants
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem

import anim

# ==========================================================================

class GraphicsView(QGraphicsView):
  
  def __init__(self, scene, *args, **kwargs):

    super().__init__(*args, *kwargs)
    self.setScene(scene)
    self.padding = 0
    self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

  def fit(self):
    
    rect = self.scene().itemsBoundingRect()
    rect.setLeft(rect.left() - self.padding)
    rect.setTop(rect.top() - self.padding)
    rect.setBottom(rect.bottom() + self.padding)
    self.fitInView(rect, Qt.AspectRatioMode.KeepAspectRatio)

  def showEvent(self, E):

    self.fit()    
    super().showEvent(E)

  def resizeEvent(self, E):
    
    self.fit()
    super().resizeEvent(E)

# ==========================================================================

class panel(QObject):
  """
  2D Animation

  Base class for two-dimensional animations.

  The :py:attr:`Animation2d.Qview` attribute is a ``QGraphicsView`` and can thus
  be used directly as a QWidget in any Qt application. For rapid display, the
  companion class :class:`Window` allows to easily create a new window for
  the animation.

  .. note:: Two times are at play in an animation: the *display* time, whose 
    increments are approximately the inverse of the :py:attr:`Animation2d.fps`
    attribute, and the *animation* time, which is a virtual quantity unrelated 
    to the actual time. This way, slow motion or fast-forward animations can
    be displayed. The :py:attr:`Animation2d.dt` attibute controls the increment
    of animation time between two display updates.
  
  Attributes:
    
    item ({:class:`item` *subclass*}): All items in the scene.

    boundaries ({'x', 'y', 'width', 'height'}): Limits of the scene.

    margin (float): Margin around the scene (pix).

    timeHeight (float): Position of the time display relative to the top of the
      scene (pix).

    fps (float): Display framerate (1/s). Default is 25.

    t (float): Current animation time (s).

    dt (float): Animation time increment (s) between two updates.

    disp_time (bool): If true, the animation time is overlaid to the animation.

    disp_boundaries (bool): If true, a thin grey rectanle is overlaid to 
      indicate the boundaries.

    parent (``QWidget`` or :class:`Window`): If not None (default), a simple
      window containing the animation is created.

    Qscene (``QGraphicsScene``): ``QGraphicsScene`` containing the elements.

    Qview (``QGraphicsView``): ``QGraphicsView`` widget representing the scene.

    timer (``QElapsedTimer``): Timer storing the display time since the 
      animation start.

    Qtimer (``QTimer``): Timer managing the display updates.
  """

  # Events
  updated = pyqtSignal()

  # ========================================================================
  def __init__(self, W, 
               viewHeight=None, 
               boundaries=None, 
               disp_boundaries=True, 
               boundaries_color=QColorConstants.Gray):
    """
    Animation constructor

    Defines all the attributes of the animation, especially the ``QGraphicsScene`` and ``QGraphicsView`` necessary for rendering.

    Args:

      viewHeight (float): Height of the ``QGraphicsView``.

      boundaries ([[float,float],[float,float]]): Limits of the scene to display.
        The first element sets the *x*-limits and the second the *y*-limits. 
        Default is [[0,1],[0,1]].

      disp_boundaries (bool): If true, a thin grey rectanle is overlaid to 
        indicate the boundaries.

      disp_time (bool): If true, the animation time is overlaid to the animation.

      dt (float): Animation time increment (s) between two updates. Default: 0.04.
    """

    super().__init__()

    self.window = W

    # --- Size settings

    if viewHeight is None:
      self.viewHeight = self.window.height
    elif viewHeight<=1:
      self.viewHeight = QApplication.desktop().screenGeometry().height()*viewHeight
    else:
      self.viewHeight = viewHeight
    
     # --- Scene & view

    # Scene limits
    self.boundaries = {'x':[0,1], 'y':[0,1], 'width':None, 'height':None}
    if boundaries is not None:
      self.boundaries['x'] = list(boundaries[0])
      self.boundaries['y'] = list(boundaries[1])
    self.boundaries['width'] = self.boundaries['x'][1]-self.boundaries['x'][0]
    self.boundaries['height'] = self.boundaries['y'][1]-self.boundaries['y'][0]

    # Scale factor
    self.factor = self.viewHeight/self.boundaries['height']

    # Aspect ratio
    self.aspect_ratio = self.boundaries['width']/self.boundaries['height']
    
    # Scene
    self.scene = QGraphicsScene()
    self.view = GraphicsView(self.scene)

    # Style management
    match self.window.style:

      case 'dark':
        if boundaries_color is None: boundaries_color = QColorConstants.Black

      case 'light':
        self.view.setStyleSheet("border: 0px; background-color:#efefef;")
        if boundaries_color is None: boundaries_color = QColor('#efefef')

      case 'white':
        self.view.setStyleSheet("border: 0px; background-color:white;")
        if boundaries_color is None: boundaries_color = Qt.white

    # Scene boundaries display
    self.disp_boundaries = disp_boundaries
    if self.disp_boundaries:
      self.box = QGraphicsRectItem(0,0,
        self.factor*self.boundaries['width'],
        -self.factor*self.boundaries['height'])
      self.box.setPen(QPen(boundaries_color, 2))
      self.scene.addItem((self.box))

    # --- Display items

    self.item = {}
    self.composite = {}

    # --- Display

    # Antialiasing
    self.view.setRenderHints(QPainter.RenderHint.Antialiasing)

    # Stack
    self.stack = {'vpos': self.boundaries['y'][1], 
                  'vmin': self.boundaries['y'][0],
                  'vpadding': 0.02}
    
  # ========================================================================
  def add(self, type, name, **kwargs):
    """
    Add an item to the scene.

    args:
      item (:class:`item` *subclass*): The item to add.
    """

    # Stack
    if 'stack' in kwargs:
      stack = kwargs['stack']
      del kwargs['stack']
    else:
      stack = False

    height = kwargs['height'] if 'height' in kwargs else None

    if height=='fill':
      height = self.stack['vpos']-self.boundaries['y'][0]
      kwargs['height'] = height
      
    # Add items
    if issubclass(type, anim.plane.composite):

      # Let composite elements create items
      self.composite[name] = type(self, name, **kwargs)

    else:

      # Create item
      self.item[name] = type(self, name, **kwargs)

      # Add item to the scene
      if self.item[name].parent is None:
        self.scene.addItem(self.item[name])
    
    # --- Stack

    if stack:

      x = 0
      y = self.stack['vpos']

      if height is None:
        self.stack['vpos'] -= self.item[name].height()
      else:
        self.stack['vpos'] -= height
        y -= height

      # Set position
      self.item[name].position = [x, y]

      # Bottom padding
      self.stack['vpos'] -= kwargs['vpadding'] if 'vpadding' in kwargs else self.stack['vpadding']

  # ========================================================================
  def setPadding(self, padding):

    self.view.padding = padding*self.factor

  # ========================================================================
  def update(self, t=None):
    """
    Update animation state
    """

    # Repaint
    self.view.viewport().repaint()

    # Confirm update
    self.updated.emit()

  # ========================================================================
  def receive(self, event):
    """
    Event reception
    """

    match event['type']:

      case 'show':
        
        for name in self.composite:
          if isinstance(self.composite[name], anim.plane.arrow):
            self.composite[name].points = self.composite[name].points

      case 'update':

        # Update dispay
        self.update(event['time'])

      case 'stop':
        self.stop()

      case _:
        pass
        # print(event)

  # ========================================================================
  def change(self, type, item):
    """
    Change notification

    This method is triggered whenever an item is changed.
    It does nothing and has to be reimplemented in subclasses.

    .. Note::
      To catch motion an item has to be declared as ``movable``,
      which is not the default.

    args:
      type (str): Type of change (``move``).
      item (:class:`item` *subclass*): The changed item.
    """

    pass
  
  # ========================================================================
  def stop(self):
    """
    Stop notification

    This method is triggered when the window is closed.
    It does nothing and has to be reimplemented in subclasses.
    """

    pass
