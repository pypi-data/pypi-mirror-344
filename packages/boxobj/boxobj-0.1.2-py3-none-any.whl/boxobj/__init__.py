import math
from dataclasses import dataclass, is_dataclass, asdict, field
from typing import Dict, Tuple, Mapping, List, Union, Protocol, Any

DEFAULT_SCALE = 6


class Dataclass(Protocol):
    # This will validate as an object that has dataclass fields
    __dataclass_fields__: Dict


Number = Union[float, int]
Coordinates = Tuple[Number, Number, Number, Number]
Size = Tuple[Number, Number]


@dataclass(repr=False)
class AttrObject:
    attributes: Union[Dict, Dataclass, None]

    def __init__(self, attributes: Dict = None, **kwargs):
        self.attributes = attributes
        if kwargs:
            if self.attributes is None:
                self.attributes = kwargs
            else:
                self.attributes.update(kwargs)

    def __getattr__(self, item):
        if self.attributes:
            if (
                is_dataclass(self.attributes)
                and item in self.attributes.__dataclass_fields__
            ):
                return getattr(self.attributes, item)
            elif item in self.attributes:
                return self.attributes[item]
        raise AttributeError(
            f"AttributeError: '{self.__class__.__name__}' object has no attribute '{item}'"
        )

    def __getitem__(self, item):
        if self.attributes:
            if (
                is_dataclass(self.attributes)
                and item in self.attributes.__dataclass_fields__
            ):
                return getattr(self.attributes, item)
            elif item in self.attributes:
                return self.attributes[item]
        raise KeyError(f"KeyError: '{item}'")

    def __contains__(self, item):
        return item in self.attributes if self.attributes else False

    def get(self, key, default=None):
        if self.attributes and key in self.attributes:
            return self.attributes[key]
        return default

    def __setitem__(self, key, value):
        if self.attributes is None:
            self.attributes = {}
        if is_dataclass(self.attributes):
            setattr(self.attributes, key, value)
        else:
            self.attributes[key] = value

    def __delattr__(self, item):
        if item == "attributes":
            self.attributes = None
        elif self.attributes and not is_dataclass(self.attributes):
            del self.attributes[item]
        else:
            raise KeyError(f"KeyError: '{item}'")

    def __delitem__(self, key):
        if self.attributes:
            del self.attributes[key]
        else:
            raise KeyError(f"KeyError: '{key}'")

    def pop(self, item):
        if self.attributes is None:
            raise KeyError(f"KeyError: '{item}'")
        return self.attributes.pop(item)

    @property
    def data(self):
        if self.attributes and is_dataclass(self.attributes):
            return asdict(self.attributes)
        else:
            return self.attributes if self.attributes else {}

    def to_dict(self):
        return self.data

    @classmethod
    def serialized_name(cls):
        return f"{cls.__module__}.{cls.__name__}"

    def to_serializable(self):
        value = self.data
        value["cls"] = self.serialized_name()
        return value

    @classmethod
    def from_serialized(cls, obj, **kwargs):
        return cls(obj, **kwargs)


@dataclass
class Box(AttrObject):
    """
    A representation of a box that can handle the various coordinate systems as source data and convert them
    to a common, coordinate-based object.
    """

    coordinates: Coordinates
    output_scale: int = 6
    container_size: Size = None

    def __init__(
        self,
        value,
        attributes: Union[Dict, Dataclass] = None,
        output_scale=None,
        container_size=None,
        **kwargs,
    ):

        # Handle creating a Box from another Box
        if isinstance(value, Box):
            self.coordinates = tuple(value.coordinates)
            attr = value.attributes.copy() if value.attributes else None

        # Handle value representing a list of coordinates
        elif isinstance(value, list) or isinstance(value, tuple):
            self.coordinates = tuple(value)
            attr = attributes

        # Handle a dict containing the components of the box
        elif isinstance(value, Dict):
            value = value.copy()
            self.coordinates = _case_insensitive_pop(
                value, "coordinates", raise_if_missing=False
            )
            if not self.coordinates:
                self.coordinates = self.position_to_coordinates(
                    _case_insensitive_pop(value, "left"),
                    _case_insensitive_pop(value, "top"),
                    _case_insensitive_pop(value, "width"),
                    _case_insensitive_pop(value, "height"),
                )

            rel_coord = _case_insensitive_pop(
                value, "rel_coordinates", raise_if_missing=False
            )
            if not rel_coord:
                rel_coord = _case_insensitive_pop(
                    value, "relative_coordinates", raise_if_missing=False
                )
            if rel_coord:
                c_pair = zip(self.coordinates, rel_coord)
                dim_pair = [
                    (i, c[0] / c[1])
                    for i, c in enumerate(c_pair)
                    if c[0] > 0 and c[1] > 0
                ]
                w_vals = [c for i, c in dim_pair if i in [0, 2]]
                h_vals = [c for i, c in dim_pair if i in [1, 3]]
                self.container_size = (
                    sum(w_vals) / len(w_vals),
                    sum(h_vals) / len(h_vals),
                )

            # Get any remaining attributes on the value that aren't associated with location or serialization
            attr = {
                k: v
                for k, v in value.items()
                if k.lower()
                not in ["coordinates", "left", "top", "width", "height", "cls"]
            }

            if attributes:
                # If the attributes are a dataclass but there are other keys in the value, append the dataclass
                # attributes to the base, else use the dataclass
                if is_dataclass(attributes):
                    if attr:
                        attr.update(asdict(attributes))
                    else:
                        attr = attributes
                else:
                    attr.update(attributes)
        else:
            raise ValueError("The value parameter must contain coordinate values")
        if len(self.coordinates) != 4:
            raise ValueError("Box coordinates must have exactly four values")
        if output_scale is not None:
            self.output_scale = output_scale
        if container_size is not None:
            self.container_size = container_size
        AttrObject.__init__(self, attr, **kwargs)

    @property
    def left(self) -> Number:
        return self.coordinates[0]

    @property
    def top(self) -> Number:
        return self.coordinates[1]

    @property
    def width(self) -> Number:
        return self.coordinates[2] - self.coordinates[0]

    @property
    def height(self) -> Number:
        return self.coordinates[3] - self.coordinates[1]

    @property
    def center(self) -> (Number, Number):
        return (
            (self.coordinates[2] - self.coordinates[0]) / 2 + self.coordinates[0],
            (self.coordinates[3] - self.coordinates[1]) / 2 + self.coordinates[1],
        )

    @property
    def bottom(self) -> Number:
        return self.coordinates[3]

    @property
    def right(self) -> Number:
        return self.coordinates[2]

    @property
    def relative_coordinates(self) -> Coordinates:
        if self.container_size is None:
            raise ValueError("container_size must be set")
        return (
            self.coordinates[0] / self.container_size[0],
            self.coordinates[1] / self.container_size[1],
            self.coordinates[2] / self.container_size[0],
            self.coordinates[3] / self.container_size[1],
        )

    @property
    def area(self) -> Number:
        """
        Returns the area of the Box in square pixels
        """
        return abs(self)

    def copy(self, location_only: bool = False) -> "Box":
        return Box(
            tuple(self.coordinates),
            self.attributes.copy() if self.attributes and not location_only else None,
        )

    def with_attributes(self, additional_attributes: dict) -> "Box":
        attr = self.attributes.copy()
        attr.update(additional_attributes)
        return Box(tuple(self.coordinates), attr)

    @classmethod
    def from_dict(cls, obj: Dict) -> "Box":
        """
        Creates a Box object containing contents of the dict that is passed. It's expected that
        the dict passed contains either position information as top/left/width/height elements or
        an element containing coordinates.

        :param obj: The source dict to build the Box from
        :return: A Box object
        """
        return cls(obj)

    @classmethod
    def from_position_percentage(
        cls,
        position: Dict[str, Number],
        size: Size = None,
        width: Number = None,
        height: Number = None,
        scale: Number = 1,
        **kwargs,
    ):
        """
        Creates a Box object containing contents of the dict that is passed as a position that is defined as
        a percentage of the image size.

        :param position: The source dict to build the Box from
        :param size: The size of the image as a tuple (width, height)
        :param width: The width of the image in pixels
        :param height: The height of the image in pixels
        :param scale: The number of digits to the right of the decimal point to include in the calculated coordinates
        :param kwargs: Additional keyword attributes that should be included in the Box attributes
        :return: A Box object
        """
        (width, height) = size if size else (width, height)
        if width is None or height is None:
            raise ValueError("Image dimensions must be provided")
        p = position.copy()
        coordinates = cls.position_to_coordinates(
            round(cls.__case_insensitive_pop(p, "left") * width, scale),
            round(cls.__case_insensitive_pop(p, "top") * height, scale),
            round(cls.__case_insensitive_pop(p, "width") * width, scale),
            round(cls.__case_insensitive_pop(p, "height") * height, scale),
        )
        if kwargs:
            p.update(kwargs)
        return cls(coordinates, p, container_size=(width, height))

    @staticmethod
    def __normalize_bottom_origin(
        coordinates: Coordinates, height: Number
    ) -> Coordinates:
        if height is None:
            raise ValueError(
                "Image height must be provided when the origin is bottom-left"
            )
        return (
            coordinates[0],
            height - coordinates[3],
            coordinates[2],
            height - coordinates[1],
        )

    @classmethod
    def from_coordinates(
        cls,
        coordinates: Coordinates,
        top_origin: bool = True,
        height: Number = None,
        **kwargs,
    ) -> "Box":
        """
        Creates a Box object using coordinates of the box in pixels.

        :param coordinates: The coordinates of the box (x1, y1, x2, y2)
        :param top_origin: Indicates the origin from which the coordinates are calculated, False if bottom origin
        :param height: The height of the image in pixels (required for bottom origin coordinates)
        :param kwargs: Additional keyword attributes that should be included in the Box attributes
        :return: A Box object
        """
        if len(coordinates) != 4:
            raise ValueError("Coordinates must have exactly four values")
        if not top_origin:
            coordinates = cls.__normalize_bottom_origin(coordinates, height)
        return cls(coordinates, kwargs)

    @classmethod
    def from_coordinates_percentage(
        cls, coordinates, top_origin=True, size=None, width=None, height=None, **kwargs
    ) -> "Box":
        """
        Creates a Box object using coordinates of the box as a percentage of the box size.

        :param coordinates: The coordinates of the box (x1, y1, x2, y2)
        :param top_origin: Indicates the origin from which the coordinates are calculated, False if bottom origin
        :param size: The size of the image as a tuple (width, height)
        :param width: The width of the image in pixels
        :param height: The height of the image in pixels
        :param kwargs: Additional keyword attributes that should be included in the attributes
        :return: A Box object
        """
        (width, height) = size if size else (width, height)
        if len(coordinates) != 4:
            raise ValueError("Coordinates must have exactly four values")
        if width is None or height is None:
            raise ValueError(
                "Image dimensions must be provided if the coordinates are defined as a ratio"
            )
        coordinates[0] = width * coordinates[0]
        coordinates[1] = height * coordinates[1]
        coordinates[2] = width * coordinates[2]
        coordinates[3] = height * coordinates[3]
        if not top_origin:
            coordinates = cls.__normalize_bottom_origin(coordinates, height)
        return cls(coordinates, kwargs)

    @staticmethod
    def position_to_coordinates(
        left: float, top: float, width: float, height: float
    ) -> Tuple[float, float, float, float]:
        return left, top, left + width, top + height

    @staticmethod
    def is_box(obj: Any) -> bool:
        """
        Returns true or false if the dict that is provided contains the keys or coordinates necessary to be a box
        in the pattern required by this class.

        :param obj: The dict or array to check
        """
        return (
            isinstance(obj, Mapping)
            and (
                ("top" in obj and "left" in obj and "width" in obj and "height" in obj)
                or ("coordinates" in obj and len(obj["coordinates"]) == 4)
            )
        ) or ((isinstance(obj, list) or isinstance(obj, tuple)) and len(obj) == 4)

    def __abs__(self):
        return self.width * self.height

    def __mul__(self, scalar):
        return Box([x * scalar for x in self.coordinates], self.attributes)

    def __truediv__(self, factor):
        return Box([x / factor for x in self.coordinates], self.attributes)

    def __floordiv__(self, factor):
        return Box([x // factor for x in self.coordinates], self.attributes)

    def __add__(self, other):
        # TODO: Consider how to combine attributes if at all
        if isinstance(other, Box):
            other = other.coordinates
        if isinstance(other, list) or isinstance(other, tuple):
            if len(other) == 4:
                pairs = list(zip(self.coordinates, other))
                return Box(
                    [min(pairs[0]), min(pairs[1]), max(pairs[2]), max(pairs[3])],
                    self.attributes,
                )
            elif len(other) == 2:
                c = self.coordinates
                x = other[0]
                y = other[1]
                return Box([c[0] + x, c[1] + y, c[2] + x, c[3] + y], self.attributes)
        raise ValueError("Invalid value to add to a Box")

    def __sub__(self, other):
        if (isinstance(other, list) or isinstance(other, tuple)) and len(other) == 2:
            c = self.coordinates
            x = other[0]
            y = other[1]
            return Box([c[0] - x, c[1] - y, c[2] - x, c[3] - y], self.attributes)
        raise ValueError("Invalid value to subtract from a Box")

    def __gt__(self, other):
        if self.top == other.top:
            return self.left > other.left
        else:
            return self.top > other.top

    def __lt__(self, other):
        if self.top == other.top:
            return self.left < other.left
        else:
            return self.top < other.top

    def __radd__(self, other):
        return self.copy(True) if other == 0 else self + other

    def scale(self, scale: float | int) -> "Box":
        width = self.width * math.sqrt(scale)
        height = self.height * math.sqrt(scale)
        w2 = width / 2
        h2 = height / 2
        coords = [
            max(self.center[0] - w2, 0),
            max(self.center[1] - h2, 0),
            (
                min(self.center[0] + w2, self.container_size[0])
                if self.container_size
                else self.center[0] + w2
            ),
            (
                min(self.center[1] + h2, self.container_size[1])
                if self.container_size
                else self.center[1] + h2
            ),
        ]
        return Box(coords, self.attributes, container_size=self.container_size)

    def offset(self, x: Number = 0, y: Number = 0) -> "Box":
        """
        Offset the position of the box as a percentage of the image dimensions.
        Can only be used if the `container_size` attribute is set.
        :param x: Horizontal offset of the box, a value of 0 will result in no change
        :param y: Vertical offset of the box, a value of 0 will result in no change
        :return: A Box object
        """
        if self.container_size is None:
            raise ValueError(
                "Container size must be set to perform a percentage offset"
            )
        xx = self.container_size[0] * (1 + x) - self.container_size[0]
        yy = self.container_size[1] * (1 + y) - self.container_size[1]
        coords = [
            max(self.coordinates[0] + xx, 0),
            max(self.coordinates[1] + yy, 0),
            min(self.coordinates[2] + xx, self.container_size[0]),
            min(self.coordinates[3] + yy, self.container_size[1]),
        ]
        return Box(coords, self.attributes, container_size=self.container_size)

    def intersecting_boxes(self, boxes, min_overlap=0):
        return [
            box
            for box in boxes
            if self & box and abs(self & box) > abs(box) * min_overlap
        ]

    def __and__(self, other):
        a = self.coordinates
        b = other.coordinates
        intersection = (
            max(a[0], b[0]),
            max(a[1], b[1]),
            min(a[2], b[2]),
            min(a[3], b[3]),
        )
        if intersection[2] < intersection[0] or intersection[3] < intersection[1]:
            return None
        else:
            return Box(intersection)

    def __round__(self, n=None):
        return Box([round(x, n) for x in self.coordinates], self.attributes)

    def __repr__(self):
        if is_dataclass(self.attributes):
            attr = self.attributes
        else:
            attr = (
                {k: v for k, v in self.attributes.items() if k != "cls"}
                if self.attributes
                else None
            )
        coords = [round(c, self.output_scale) for c in self.coordinates]
        if attr:
            return f"Box({coords}, {repr(attr)})"
        else:
            return f"Box({coords})"

    @property
    def data(self) -> Dict:
        if self.attributes and is_dataclass(self.attributes):
            d = asdict(self.attributes)
        else:
            d = self.attributes if self.attributes else {}
        d["coordinates"] = [round(c, self.output_scale) for c in self.coordinates]
        return d

    @property
    def expanded_data(self) -> Dict:
        d = self.data
        d["left"] = round(self.left, self.output_scale)
        d["top"] = round(self.top, self.output_scale)
        d["width"] = round(self.width, self.output_scale)
        d["height"] = round(self.height, self.output_scale)
        d["rel_coordinates"] = [
            round(c, self.output_scale) for c in self.relative_coordinates
        ]
        return d

    @staticmethod
    def intersection_over_union(a: "Box", b: "Box") -> float:
        intersection = a & b
        if intersection:
            return abs(intersection) / (abs(a) + abs(b) - abs(intersection))
        else:
            return 0


@dataclass
class Page(AttrObject):
    """
    A representation of a "page" of Boxes and the relevant information about the page
    source to support operations on the contents.
    """

    width: float
    height: float
    index: int = None
    identifier: Union[str, int] = None
    contents: List[Box] = field(default_factory=list)

    def __init__(
        self,
        width: float,
        height: float,
        index: int = None,
        identifier: Union[str, int] = None,
        contents: List[Box] = None,
        attributes: Union[Dict, Dataclass] = None,
        **kwargs,
    ):
        self.width = width
        self.height = height
        self.index = index
        self.identifier = identifier
        self.contents = contents if contents else []
        AttrObject.__init__(self, attributes, **kwargs)

    @property
    def size(self) -> Size:
        return self.width, self.height

    def __repr__(self):
        first_line = "<Page "
        if self.identifier:
            first_line += f"{self.identifier} "
        if self.contents:
            first_line += "containing {len(self._contents)} items"
        lines = [
            first_line,
            f"  - width: {self.width}",
            f"  - height: {self.height}",
        ]
        if self.attributes:
            for k, v in self.attributes.items():
                lines.append(f"  - {k}: {v}")
        if self.contents:
            lines.append("  - contents:")
            lines.extend(["    " + repr(b) for b in self.contents[:10]])
            if len(self.contents) > 10:
                lines.append("    ...")
        lines.append(">")
        return "\n".join(lines)


@dataclass
class Pages(AttrObject):
    """
    A set of Page objects
    """

    pages: List[Page] = field(default_factory=list)
    orientation_vertical: bool = True

    def __init__(
        self,
        pages: List[Page] = None,
        orientation_vertical: bool = True,
        attributes: Union[Dict, Dataclass] = None,
        **kwargs,
    ):
        self.pages = pages if pages else []
        self.orientation_vertical = orientation_vertical
        AttrObject.__init__(self, attributes, **kwargs)

    @classmethod
    def from_indices(cls, indices: List[Coordinates]) -> "Pages":
        # TODO: Fix the class so that it handles scenarios with indexes that don't abut each other
        return cls(
            [
                Page(ind[2] - ind[0], ind[3] - ind[1], index=i, identifier=i)
                for i, ind in enumerate(indices)
            ]
        )

    def __len__(self):
        return len(self.pages)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self) -> Page:
        if self.n < len(self.pages):
            result = self.pages[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    def __getitem__(self, item):
        return self.pages[item]

    def append(self, page: Page):
        self.pages.append(page)

    @property
    def width(self) -> Number:
        if self.orientation_vertical:
            return max([page.width for page in self.pages])
        else:
            return sum([page.width for page in self.pages])

    @property
    def height(self) -> Number:
        if self.orientation_vertical:
            return sum([page.height for page in self.pages])
        else:
            return max([page.height for page in self.pages])

    @property
    def page_offsets(self) -> List[List[Number]]:
        """
        Retrieves the relative offsets for the top-left corner of each page of content when stacked end-to-end
        in the orientation specified.
        """
        offsets = []
        index = 0
        for page in self.pages:
            if self.orientation_vertical:
                offsets.append([0, index])
                index += page.height
            else:
                offsets.append([index, 0])
                index += page.width
        return offsets

    @property
    def page_indices(self) -> List[Coordinates]:
        """
        Retrieves the coordinates of each page of content when stacked end-to-end
        in the orientation specified.
        """
        return [
            (indices[0], indices[1], indices[0] + page.width, indices[1] + page.height)
            for page, indices in zip(self, self.page_offsets)
        ]

    def consolidate_content(
        self, target: "Pages", max_dimension_variance: float = 0.01
    ):
        if len(self) != len(target):
            raise ValueError("Page counts don't match")
        if self.orientation_vertical != target.vertical:
            raise ValueError("The target orientation doesn't match")

        # Adjust the coordinates to align with the target
        # Scale the content to match the dimensions of the target
        width_ratio = target.width / self.width
        height_ratio = target.height / self.height

        # Confirm the ratio of width and height are reasonably close
        if abs(width_ratio / height_ratio - 1) > max_dimension_variance:
            raise ValueError(
                f"Mismatched width and height ratios: ({width_ratio}, {height_ratio})"
            )

        box: Box
        return [
            (box * height_ratio) + offset
            for page, offset in zip(self, target.page_offsets)
            for box in page.contents
        ]

    def __repr__(self):
        lines = [
            f"<PageSet containing {len(self.pages)} pages",
            f"  - width: {self.width}",
            f"  - height: {self.height}",
        ]
        if self.attributes:
            for k, v in self.attributes.items():
                lines.append(f"  - {k}: {v}")
        if self.pages:
            lines.append("  - pages:")
            lines.extend(["    " + s for p in self.pages for s in repr(p).split("\n")])
        lines.append(">")
        return "\n".join(lines)


def _case_insensitive_pop(d, key, default=None, raise_if_missing=True):
    if key in d:
        return d.pop(key)
    else:
        for k in d.keys():
            if k.lower() == key.lower():
                return d.pop(k)
    if raise_if_missing:
        raise KeyError(f"Value for {key} is missing")
    else:
        return default
