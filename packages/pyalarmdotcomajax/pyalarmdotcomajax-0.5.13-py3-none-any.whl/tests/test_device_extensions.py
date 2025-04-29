"""Test device extensions."""

import aiohttp
import pytest
from aioresponses import aioresponses

from pyalarmdotcomajax import AlarmController
from pyalarmdotcomajax import const as c
from pyalarmdotcomajax.cli import _print_element_tearsheet
from pyalarmdotcomajax.devices.camera import Camera
from pyalarmdotcomajax.extensions import (
    CameraSkybellControllerExtension,
    ConfigurationOptionType,
    ExtendedProperties,
)

from .responses import get_http_body_html


@pytest.mark.asyncio
async def test__extension_camera_skybellhd__fetch(
    all_base_ok_responses: str,
    adc_client: AlarmController,
) -> None:
    """Ensures that ExtendedProperties objects are created from server response data."""

    async with aiohttp.ClientSession() as websession:
        extension = CameraSkybellControllerExtension(websession=websession, headers={"foo": "bar"})
        configs: list[ExtendedProperties] = await extension.fetch()

    assert configs[0].device_name == "Front Doorbell"
    assert configs[0].config_id == "2048"
    assert configs[0].settings["indoor-chime"].current_value is CameraSkybellControllerExtension.ChimeOnOff.ON
    assert (
        configs[0].settings["outdoor-chime"].current_value
        is CameraSkybellControllerExtension.ChimeAdjustableVolume.MEDIUM
    )
    assert configs[0].raw_attribs


@pytest.mark.asyncio
async def test__extension_camera_skybellhd__via_alarm_controller(
    all_base_ok_responses: str,
    adc_client: AlarmController,
) -> None:
    """Test whether pyalarmdotcomajax camera objects are properly built when encountering Skybell HD cameras."""

    await adc_client.async_update()

    assert adc_client.devices.cameras["id-camera-skybell"]

    skybell = adc_client.devices.cameras["id-camera-skybell"]

    assert skybell.name == "Front Doorbell"
    assert skybell.settings["indoor-chime"].current_value is CameraSkybellControllerExtension.ChimeOnOff.ON
    assert (
        skybell.settings["outdoor-chime"].current_value
        is CameraSkybellControllerExtension.ChimeAdjustableVolume.MEDIUM
    )
    assert skybell.settings["indoor-chime"].option_type is ConfigurationOptionType.BINARY_CHIME


@pytest.mark.asyncio
async def test__extension_camera_skybellhd__cli_tearsheet(
    all_base_ok_responses: str,
    adc_client: AlarmController,
) -> None:
    """_print_element_tearsheet will throw exception on failure."""

    await adc_client.async_update()

    assert adc_client.devices.cameras["id-camera-skybell"]

    _print_element_tearsheet(adc_client.devices.cameras["id-camera-skybell"])


# @pytest.mark.asyncio # type: ignore
# async def test__extension_camera_skybellhd__change_indoor_chime(
#     all_base_ok_responses: str,
#
#     adc_client: AlarmController,
# ) -> None:
#     """_print_element_tearsheet will throw exception on failure."""


@pytest.mark.asyncio
async def test__extension_camera_skybellhd__submit_change(
    all_base_ok_responses: str,
    response_mocker: aioresponses,
    adc_client: AlarmController,
) -> None:
    """Test changing configuration option."""

    response_mocker.get(
        url=CameraSkybellControllerExtension.ENDPOINT.format(c.URL_BASE),
        status=200,
        body=get_http_body_html("camera_settings_skybell"),
        repeat=True,
    )

    response_mocker.post(
        url=CameraSkybellControllerExtension.ENDPOINT.format(c.URL_BASE),
        status=200,
        body=get_http_body_html("camera_settings_skybell_changed"),
    )

    await adc_client.async_update()

    camera: Camera = adc_client.devices.cameras["id-camera-skybell"]

    assert camera.settings["indoor-chime"].current_value == CameraSkybellControllerExtension.ChimeOnOff.ON

    await camera.async_change_setting("indoor-chime", CameraSkybellControllerExtension.ChimeOnOff.OFF)

    assert camera.settings["indoor-chime"].current_value == CameraSkybellControllerExtension.ChimeOnOff.OFF


@pytest.mark.asyncio
async def test__extension_camera_skybellhd__missing_field(
    skybell_missing_video_quality_field: str,
    adc_client: AlarmController,
) -> None:
    """Ensures that pyalarmdotcomajax skips loading data from Skybell HD if Skybell HD config page has unexpected structure."""

    await adc_client.async_update()

    assert adc_client.devices.cameras is not None

    skybell = adc_client.devices.cameras["id-camera-skybell"]

    assert skybell.name == "Front Doorbell"
    assert skybell.settings["indoor-chime"].current_value is CameraSkybellControllerExtension.ChimeOnOff.ON
    assert (
        skybell.settings["outdoor-chime"].current_value
        is CameraSkybellControllerExtension.ChimeAdjustableVolume.MEDIUM
    )
    assert skybell.settings["indoor-chime"].option_type is ConfigurationOptionType.BINARY_CHIME
