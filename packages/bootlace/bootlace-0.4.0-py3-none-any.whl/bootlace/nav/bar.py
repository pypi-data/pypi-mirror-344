import attrs
from domilite import tags
from domilite.dom_tag import dom_tag
from domilite.util import container
from marshmallow import fields

from bootlace.size import SizeClass
from bootlace.style import ColorClass
from bootlace.util import Tag
from bootlace.util import as_tag
from bootlace.util import ids as element_id

from .core import Link
from .core import NavElement
from .core import SubGroup
from .nav import Nav
from .schema import NavSchema


@attrs.define
class NavBar(NavElement):
    """A navigation bar, typically at the top of the page

    This is usually the primary navigation for a site.
    """

    #: The ID of the navbar
    id: str = attrs.field(factory=element_id.factory("navbar"))

    #: The elements in the navbar
    items: list[NavElement] = attrs.field(factory=list, metadata={"form": fields.List(fields.Nested(NavSchema))})

    #: The size of the navbar, if any, used to select when it
    #: should expand or collapse
    expand: SizeClass | None = attrs.field(
        default=SizeClass.LARGE,
        metadata={"form": fields.Enum(SizeClass, allow_none=True)},
    )

    #: The color of the navbar, if using a bootstrap color class
    color: ColorClass | None = attrs.field(
        default=ColorClass.TERTIARY,
        metadata={"form": fields.Enum(ColorClass, allow_none=True)},
    )

    #: Whether the navbar should be fluid (e.g. full width)
    fluid: bool = True

    nav: Tag = Tag(tags.nav, classes={"navbar"})
    container: Tag = Tag(tags.div, classes={"container"})

    def __tag__(self) -> tags.html_tag:
        nav = self.nav()
        if self.expand:
            nav.classes.add(self.expand.add_to_class("navbar-expand"))
        if self.color:
            nav.classes.add(self.color.add_to_class("bg"))

        container = self.container()
        if self.fluid:
            container.classes.add("container-fluid")
            container.classes.discard("container")
        else:
            container.classes.add("container")

        nav.add(container)

        for item in self.items:
            container.add(as_tag(item))

        return nav


@attrs.define
class Brand(Link):
    """The brand for the navbar, typically the site's logo or name

    You can pass :class:`~bootlace.links.Link` or :class:`~bootlace.links.View`
    as the source link, and
    """

    #: The ID of the brand
    id: str = attrs.field(factory=element_id.factory("navbar-brand"))

    def __tag__(self) -> dom_tag:
        a = as_tag(self.link)
        a["class"] = "navbar-brand"
        a["id"] = self.id
        return self.element_state(a)


@attrs.define
class NavBarCollapse(SubGroup):
    """A collection of nav elements that can be collapsed"""

    id: str = attrs.field(factory=element_id.factory("navbar-collapse"))

    button: Tag = Tag(tags.button, classes={"navbar-toggler"}, attributes={"type": "button"})
    icon: Tag = Tag(tags.span, classes={"navbar-toggler-icon"})
    container: Tag = Tag(tags.div, classes={"collapse", "navbar-collapse"})

    def __tag__(self) -> dom_tag:
        button = self.button()
        button.data["bs-toggle"] = "collapse"
        button.data["bs-target"] = f"#{self.id}"
        button.aria["controls"] = f"{self.id}"
        button.aria["expanded"] = "false"
        button.aria["label"] = "Toggle navigation"

        button.add(self.icon())
        div = self.container(id=self.id)
        for item in self.items:
            div.add(as_tag(item))
        return container(button, div)


@attrs.define
class NavBarNav(Nav):
    """Primary grouping of nav elements in the navbar"""

    id: str = attrs.field(factory=element_id.factory("navbar-nav"))

    ul: Tag = Tag(tags.ul, classes={"navbar-nav"})
    li: Tag = Tag(tags.li, classes={"nav-item"})

    def __tag__(self) -> tags.html_tag:
        ul = self.ul(id=self.id)
        for item in self.items:
            ul.add(self.li(as_tag(item), __pretty=False))
        return ul


@attrs.define
class NavBarSearch(NavElement):
    """A search bar for the navbar"""

    id: str = attrs.field(factory=element_id.factory("navbar-search"))

    placeholder: str = "Search"
    action: str = "#"
    method: str = "GET"
    button: str | None = None

    form: Tag = Tag(tags.form, classes={"d-flex"}, attributes={"role": "search"})
    input: Tag = Tag(tags.input, classes={"form-control", "me-2"}, attributes={"type": "search"})
    button_tag: Tag = Tag(tags.button, classes={"btn", "btn-success"}, attributes={"type": "submit"})

    def __tag__(self) -> dom_tag:
        form = self.form(id=self.id)

        input = self.input(
            placeholder=self.placeholder,
        )
        input.aria["label"] = self.placeholder
        form.add(input)
        form.add(self.button_tag(self.button or self.placeholder))
        return self.element_state(form)
