# Copyright (c) 2025 Zun Yang, (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import annotations
from typing import Callable, Optional, Tuple, Any, Dict


def is_full_arm_id(val: Any) -> bool:
    """Return True if `val` is a string that looks like a full Azure ARM resource ID."""
    return isinstance(val, str) and val.strip().startswith('/subscriptions/')


def as_id_dict(val: str) -> Dict[str, str]:
    """Wrap an ARM ID string into {'id': <id>}."""
    return {'id': val}


def split_rg_name_shorthand(s: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Split a shorthand 'rg/name' reference into (rg, name).

    Returns (None, None) if `s` isn't shorthand or is malformed.
    """
    if isinstance(s, str) and '/' in s and not s.startswith('/subscriptions/'):
        rg, name = s.split('/', 1)
        if rg and name:
            return rg.strip(), name.strip()
    return None, None


def classify_ref(val: Any) -> Tuple[str, Any]:
    """
    Classify a reference value to guide normalization.

    Returns:
      ('id', <id>)         for a full ARM id string
      ('dict_id', <id>)    for {'id': '<full-id>'}
      ('rgname', (name, rg)) for 'rg/name' shorthand (returned as (name, rg))
      ('dict_name', (name, rg_or_None)) for {'name': ..., 'resource_group': optional}
      ('name', <name>)     for bare name string
      ('unknown', val)     otherwise
    """
    if val is None:
        return 'unknown', val

    if isinstance(val, dict):
        if 'id' in val and isinstance(val['id'], str) and is_full_arm_id(val['id']):
            return 'dict_id', val['id']
        if 'name' in val and isinstance(val['name'], str):
            rg = val.get('resource_group')
            return 'dict_name', (val['name'], rg)
        return 'unknown', val

    if isinstance(val, str):
        s = val.strip()
        if is_full_arm_id(s):
            return 'id', s
        rg, name = split_rg_name_shorthand(s)
        if rg and name:
            return 'rgname', (name, rg)
        return 'name', s

    return 'unknown', val


def normalize_cross_rg_ref(
    val: Any,
    *,
    subscription_id: str,
    default_rg: str,
    build_with: Callable[[str, str, str], str],
) -> Dict[str, str] | Any:
    """
    Normalize a *top-level* Azure resource reference to {'id': '<ARM-ID>'}.

    Intended for resources that can live outside the current RG (e.g., Public IP).
    - If `val` is a full ID (string) or dict with `id`, returns {'id': <same>}.
    - If `val` is a dict with `name` (+ optional `resource_group`), or 'rg/name' shorthand,
      builds an id using that group.
    - If `val` is a bare name, builds an id using `default_rg`.
    - Otherwise returns `val` unchanged (fail-fast at the caller if it is invalid).

    Args:
      val:              The raw reference (str or dict).
      subscription_id:  Current subscription id.
      default_rg:       Resource group to use if the user passed only a bare name.
      build_with:       Callable(subscription_id, resource_group, name) -> id string.

    Returns:
      dict {'id': '<ARM-ID>'} or the original value if unrecognized.
    """
    kind, data = classify_ref(val)

    if kind in ('id', 'dict_id'):
        return as_id_dict(data)

    if kind == 'dict_name':
        name, rg = data
        return as_id_dict(build_with(subscription_id, rg or default_rg, name))

    if kind == 'rgname':
        name, rg = data
        return as_id_dict(build_with(subscription_id, rg, name))

    if kind == 'name':
        return as_id_dict(build_with(subscription_id, default_rg, data))

    return val


def normalize_agw_child_ref(
    val: Any,
    *,
    subscription_id: str,
    resource_group: str,
    appgw_name: str,
    build_child_id: Callable[[str, str, str, str], str],
) -> Dict[str, str] | Any:
    """
    Normalize an *Application Gateway child* reference to {'id': '<ARM-ID>'}.

    Intended for child resources that always live under the given App GW:
      - frontend IP configuration, frontend port, SSL certificate
      - backend address pool, backend HTTP settings
      - HTTP listener, redirect configuration, URL path map
      - probe, rewrite rule set, etc.

    - If `val` is a full id (string) or dict with `id`, returns {'id': <same>}.
    - If `val` is a dict with `name` or a bare name, builds an id under the specified App GW.
    - Otherwise returns `val` unchanged.

    Args:
      val:             The raw reference (str or dict).
      subscription_id: Current subscription id.
      resource_group:  App Gateway's resource group.
      appgw_name:      App Gateway's name.
      build_child_id:  Callable(subscription_id, resource_group, appgw_name, child_name) -> id.

    Returns:
      dict {'id': '<ARM-ID>'} or the original value if unrecognized.
    """
    kind, data = classify_ref(val)

    if kind in ('id', 'dict_id'):
        return as_id_dict(data)

    if kind == 'dict_name':
        name, _rg_ignored = data
        return as_id_dict(build_child_id(subscription_id, resource_group, appgw_name, name))

    if kind == 'name':
        return as_id_dict(build_child_id(subscription_id, resource_group, appgw_name, data))

    return val
