# boxo
`boxo` is a simple library that makes working with computer vision, OCR, and other tools that interact with regions 
of an image or document, simpler and more predictable. 

## Box
The core class in this library is `Box`. It handles many of the common approaches that different 
libraries use to reference the region containing the returned results including:

* **coordinates**: `[x1, y1, x2, y2]`
* a dict containing the **position** defined by `top`, `left`, `width`, `height`
* ***relative* coordinates** or **position** defined as a percentage of the size of the source: `[0.2, 0.5, 0.3, 0.8]`

In addition, it supports conversion from *bottom indexed* boxes like those used in older file types and libraries
such as PDFs.

Box internally represents its coordinates in pixels that are measured from the top-left, but it can return results
using other approaches as needed.

```python
from boxo import Box


tlwh = { 'top': 10, 'left': 10, 'width': 30, 'height': 30 }
coords = [10, 10, 40, 40]
coords_ratio = [0.1, 0.1, 0.4, 0.4]
obj = {
    'coordinates': [10, 10, 40, 40],
    'label': 'green',
    'name': 'my box'
}

box = Box.from_position(tlwh)
box = Box.from_coords(coords)
box = Box.from_position_percentage(coords_ratio, width=100, height=100)
box = Box.from_position_percentage(coords_ratio, top_origin=False, size=(100,100))
box = Box.from_dict(obj)
```

The Box object supports a range of pythonic interactions including sort, addition, subtraction, multiplication, 
division and area calculations.

```python
from boxo import Box


box_a = Box([10, 10, 40, 40])
box_b = Box([15, 10, 30, 50])
boxes = [box_b, box_a]

# sort the boxes vertically
boxes.sort()
# sort the boxes horizontally
boxes.sort(key=lambda x: x.left)

# shift the position of a box
box_a_shifted_down = box_a + [0, 10] # [10, 20, 40, 50]
box_a_shifted_left = box_a - [5, 0] # [5, 10, 35, 40]

# scale up the size of a box
box_a_bigger = box_a * 2 # [20, 20, 80, 80]
box_a_smaller = box_a / 3 # [3.333333, 3.333333, 13.333333, 13.333333]
box_a_smaller = round(box_a_smaller) # [3.3, 3.3, 13.3, 13.3]
box_a_smaller_floor = box_a // 3 # [3, 3, 13, 13]

# Combine two boxes (union)
box_c = box_a + box_b # [10, 10, 40, 50]

# Get the intersection of two boxes
box_i = box_a & box_b # [15, 10, 30, 40]

# Get the area of a box
box_a_area = abs(box_a) # 900
box_b_area = box_a.area # 600
```

Note that to avoid the excessive precision that frequently makes its way into Boxes as they are moved and scaled, the
repr of a Box object limits the output to six digits after the decimal.

Of course, these operands can be combined to perform common operations such as the common *intersection over union*
calculation used to evaluate agreement between two models.

```python
iou = abs(box_a & box_b) / abs(box_a + box_b) # 0.375
```

### Attributes
The `Box` object also supports assigning attributes such as a `label` or `text` to the object to associate it with
a set of values. 

```python
from boxo import Box

cv_box = Box([10, 10, 30, 50], {"label": "cat", "confidence": 0.84})
cv_box_2 = Box({"coordinates": [10, 10, 30, 50], "label": "cat", "confidence": 0.84})
ocr_box = Box([3, 4, 67, 10], text="Boxo is great for working with boxes")
```

As you can see, there are a variety of options for creating a `Box` object from whatever source system produced it. 
Here the `cv_box` value is created by passing the coordinates first, then a dict containing the associated attributes.
`cv_box_2` is the same value, but here the coordinates and attributes are contained in a single dict object. Finally,
the `ocr_box` is created by passing coordinates and using keyword arguments to assign attributes. This flexibility is
intentional to make it easier to handle the varying approaches different tools use to represent data.

Internally the `boxo` classes keep the attributes and coordinate values separate to make them easier to work with.
This shows up in how the objects are represented when printed or displayed in the output. The following is the
representation of the objects above.

```
Box([10, 10, 30, 50], {'label': 'cat', 'confidence': 0.84})
Box([10, 10, 30, 50], {'label': 'cat', 'confidence': 0.84})
Box([3, 4, 67, 10], {'text': 'Boxo is great for working with boxes'})
```

data and serialization

page
pages
page indices
