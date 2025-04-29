import enum
import warnings
from typing import Any

import attrs
from domilite import tags
from domilite.dom_tag import dom_tag
from marshmallow import fields

from bootlace import links
from bootlace.endpoint import Endpoint
from bootlace.nav.schema import NavSchema
from bootlace.util import BootlaceWarning
from bootlace.util import MaybeTaggable
from bootlace.util import Tag
from bootlace.util import as_tag
from bootlace.util import ids as element_id


class NavStyle(enum.Enum):
    """Styles for the nav element"""

    PLAIN = ""
    TABS = "nav-tabs"
    PILLS = "nav-pills"
    UNDERLINE = "nav-underline"


class NavAlignment(enum.Enum):
    """Alignment for the nav element"""

    DEFAULT = ""
    FILL = "nav-fill"
    JUSTIFIED = "nav-justified"


class NavElement:
    """Base class for nav components"""

    Schema: type[NavSchema] = NavSchema
    _NAV_ELEMENT_REGISTRY: dict[str, type["NavElement"]] = {}

    def __init_subclass__(cls) -> None:
        cls._NAV_ELEMENT_REGISTRY[cls.__name__] = cls

    @property
    def active(self) -> bool:
        """Whether the element is active"""
        return False

    @property
    def enabled(self) -> bool:
        """Whether the element is enabled"""
        return True

    def __tag__(self) -> dom_tag:
        warnings.warn(
            BootlaceWarning(f"Unhandled element {self.__class__.__name__}"),
            stacklevel=2,
        )
        return tags.comment(f"unhandled element {self.__class__.__name__}")

    def element_state(self, tag: dom_tag) -> dom_tag:
        """Apply :attr:`active` and :attr:`enabled` states to the tag."""
        if not isinstance(tag, tags.html_tag):
            return tag

        if self.active:
            tag.classes.add("active")
            tag.aria["current"] = "page"

        if not self.enabled:
            tag.classes.add("disabled")
            tag.aria["disabled"] = "true"
        return tag


@attrs.define
class Link(NavElement):
    """A link in the nav bar, either for a view or a literal URL"""

    #: The link to display, either a URL or a view
    link: links.LinkBase

    #: The ID of the element
    id: str = attrs.field(factory=element_id.factory("nav-link"))

    a: Tag = Tag(tags.a, classes={"nav-link"})

    @classmethod
    def with_url(cls, url: str, text: MaybeTaggable, **kwargs: Any) -> "Link":
        """Create a link with a URL."""
        return cls(link=links.Link(url=url, text=text, **kwargs))

    @classmethod
    def with_view(cls, endpoint: str, text: MaybeTaggable, **kwargs: Any) -> "Link":
        """Create a link with a view."""
        return cls(link=links.View(endpoint=Endpoint.from_name(endpoint, **kwargs), text=text))

    @property
    def active(self) -> bool:
        """Whether the link is active."""
        return self.link.active

    @property
    def enabled(self) -> bool:
        """Whether the link is enabled."""
        return self.link.enabled

    @property
    def url(self) -> str:
        """The URL for the link."""
        return self.link.url

    def __tag__(self) -> dom_tag:
        a = as_tag(self.link)
        if isinstance(a, tags.html_tag):
            a["id"] = self.id
            self.a.update(a)

        return self.element_state(a)


@attrs.define
class Separator(NavElement):
    """A separator in dropdown menus"""

    hr: Tag = Tag(tags.hr, classes={"dropdown-divider"})

    def __tag__(self) -> tags.html_tag:
        return self.hr()


@attrs.define
class Text(NavElement):
    """A text element in the nav bar"""

    text: MaybeTaggable

    span: Tag = Tag(tags.span, classes={"nav-link"})

    @property
    def enabled(self) -> bool:
        return False

    def __tag__(self) -> dom_tag:
        tag = self.span(self.text, cls="nav-link")
        return self.element_state(tag)


@attrs.define
class SubGroup(NavElement):
    """Any grouping of items in the nav bar"""

    items: list[NavElement] = attrs.field(factory=list, metadata={"form": fields.List(fields.Nested(NavSchema))})

    @property
    def active(self) -> bool:
        return any(item.active for item in self.items)
