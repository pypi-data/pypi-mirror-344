from rest_framework.exceptions import PermissionDenied
from rules import test_rule


def enforce_permission(rule: str, *args) -> None:
    """Raise PermissionDenied if the rule test fails."""
    if not test_rule(rule, *args):
        msg = "You do not have permission to perform this action."
        raise PermissionDenied(msg)
