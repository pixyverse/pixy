import logging

logger = logging.getLogger(__name__)


def prop_to_string(props: dict[str, str]):
    op = ""
    for k in props.keys():
        v = props[k]
        if v:
            op += f" {k}='{props[k]}'"
        else:
            op += f" {k}"
    return op.replace('"', "")


def createElement(elem: str | tuple, props: dict[str, str] = {}, children=[]):
    logger.debug(elem)
    logger.debug(
        f"""Create Element '{elem}' with {props}
        please and {len(children) if children else 0} children too"""
    )
    if isinstance(elem, tuple):
        return "".join(elem)
    if len(children) == 0:
        return elem
    children_output = "".join(createElement(child) for child in children)
    logger.debug(f"Children: {children_output}")
    return (
        f"<{elem} {prop_to_string(props)}>{children_output}</{elem}>"
        if (isinstance(elem, str) and not elem.istitle())
        else children_output
    )
