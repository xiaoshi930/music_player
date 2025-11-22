from __future__ import annotations

import logging
import os
import time
import shutil
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.frontend import add_extra_js_url

try:
    from homeassistant.components.http.static import StaticPathConfig
except ImportError:
    try:
        from homeassistant.components.http import StaticPathConfig
    except ImportError:
        class StaticPathConfig:
            def __init__(self, url_path, path, cache_headers):
                self.url_path = url_path
                self.path = path
                self.cache_headers = cache_headers

from .const import DOMAIN
from .api import NeteaseLyricsView

_LOGGER = logging.getLogger(__name__)

async def async_setup_lyrics_card(hass: HomeAssistant) -> bool:
    state_lyrics_card_path = '/netease_lyrics-local'
    await hass.http.async_register_static_paths([
        StaticPathConfig(state_lyrics_card_path, hass.config.path('custom_components/ha_cloud_music/www'), False)
    ])
    _LOGGER.debug(f"register_static_path: {state_lyrics_card_path + ':custom_components/ha_cloud_music/www'}")
    add_extra_js_url(hass, state_lyrics_card_path + f"/music-player-card.js")
    return True
  
async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    hass.data.setdefault(DOMAIN, {})
    await async_setup_lyrics_card(hass)
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data[DOMAIN][entry.entry_id] = entry.data

    hass.http.register_view(NeteaseLyricsView(hass))
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if DOMAIN in hass.data:
        hass.data[DOMAIN].pop(entry.entry_id)
    return True 
