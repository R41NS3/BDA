from _typeshed import Incomplete
from typing import IO, Final

from reportlab.graphics.renderbase import Renderer
from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Flowable

__version__: Final[str]

def draw(drawing: Drawing, canvas: Canvas, x: float, y: float, showBoundary=...) -> None: ...

class _PDFRenderer(Renderer):
    def __init__(self) -> None: ...
    def drawNode(self, node) -> None: ...
    def drawRect(self, rect) -> None: ...
    def drawImage(self, image) -> None: ...
    def drawLine(self, line) -> None: ...
    def drawCircle(self, circle) -> None: ...
    def drawPolyLine(self, polyline) -> None: ...
    def drawWedge(self, wedge) -> None: ...
    def drawEllipse(self, ellipse) -> None: ...
    def drawPolygon(self, polygon) -> None: ...
    def drawString(self, stringObj) -> None: ...
    def drawPath(self, path) -> None: ...
    def setStrokeColor(self, c) -> None: ...
    def setFillColor(self, c) -> None: ...
    def applyStateChanges(self, delta, newState) -> None: ...

class GraphicsFlowable(Flowable):
    drawing: Incomplete
    width: Incomplete
    height: Incomplete
    def __init__(self, drawing) -> None: ...
    def draw(self) -> None: ...

def drawToFile(d: Drawing, fn: str | IO[bytes], msg: str = "", showBoundary=..., autoSize: int = 1, **kwds) -> None: ...
def drawToString(d: Drawing, msg: str = "", showBoundary=..., autoSize: int = 1, **kwds) -> str: ...
def test(outDir: str = "pdfout", shout: bool = False) -> None: ...
