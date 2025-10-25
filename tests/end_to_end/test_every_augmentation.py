import uuid
from pathlib import Path
import time

from fastapi import status
from app.schemas.image import (
    AugmentationRequestBody,
    BrightenArguments,
    ChannelSwapArguments,
    CutoutArguments,
    DarkenArguments,
    EdgeFilterArguments, FlipArguments, InvertArguments, MaxFilterArguments, MinFilterArguments,
    ShiftArguments, GaussianBlurArguments, MuteChannelArguments, PepperNoiseArguments, RainbowNoiseArguments,
    PercentileFilterArguments, RotateArguments, SaltNoiseArguments, UniformBlurArguments, ZoomArguments, TintArguments,
)
import pytest

pytestmark = pytest.mark.asyncio

async def test_every_augmentation(http_client):
    """
    This test creates an augmented version of each image.
    1. Create a user
    2. Upload an image
    3. Augment the image in every single permitted way.
    """
    external_id = str(uuid.uuid4())
    headers = {
        "X-External-User-ID": external_id
    }
    responses_map = {}
    # --- CREATE A USER ---
    response = await http_client.post(
        url="/users-api/sign-up",
        headers=headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    # --- UPLOAD AN IMAGE ---
    image_path = Path("/image-augmentation-service/tests/data/colour-scribbles-256x256.png")
    assert image_path.exists()
    with open(image_path, "rb") as image_file:
        upload_response = await http_client.post(
            headers=headers,
            url="/image-api/upload",
            files={"image": ("test.png", image_file, "image/png")},
        )
    assert upload_response.status_code == status.HTTP_201_CREATED
    responses_map.update({'unprocessed_image': upload_response.json()})
    # --- CREATE AUGMENTATIONS ---
    # --- brighten
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=BrightenArguments(
                processing='brighten',
                amount=30
            )
        ).model_dump()
    )
    responses_map.update({'brighten': augment_response.json()})
    # --- channel_swap
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=ChannelSwapArguments(
                processing='channel_swap',
                a='r',
                b='b'
            )
        ).model_dump()
    )
    responses_map.update({'channel_swap': augment_response.json()})
    # --- cutout
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=CutoutArguments(
                processing='cutout',
                amount=33
            )
        ).model_dump()
    )
    responses_map.update({'cutout': augment_response.json()})
    # --- darken
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=DarkenArguments(
                processing='darken',
                amount=30
            )
        ).model_dump()
    )
    responses_map.update({'darken': augment_response.json()})
    # --- edge_filter
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=EdgeFilterArguments(
                processing='edge_filter',
                image_type='edge_enhanced'
            )
        ).model_dump()
    )
    responses_map.update({'edge_filter': augment_response.json()})
    # --- flip
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=FlipArguments(
                processing='flip',
                axis='y'
            )
        ).model_dump()
    )
    responses_map.update({'flip': augment_response.json()})
    # --- gaussian_blur
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=GaussianBlurArguments(
                processing='gaussian_blur',
                amount=100
            )
        ).model_dump()
    )
    responses_map.update({'gaussian_blur': augment_response.json()})
    # --- invert
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=InvertArguments(
                processing='invert'
            )
        ).model_dump()
    )
    responses_map.update({'invert': augment_response.json()})
    # --- max_filter
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=MaxFilterArguments(
                processing='max_filter',
                size=5
            )
        ).model_dump()
    )
    responses_map.update({'max_filter': augment_response.json()})
    # --- min_filter
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=MinFilterArguments(
                processing='min_filter',
                size=5
            )
        ).model_dump()
    )
    responses_map.update({'min_filter': augment_response.json()})
    # --- mute_channel
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=MuteChannelArguments(
                processing='mute_channel',
                channel='g'
            )
        ).model_dump()
    )
    responses_map.update({'mute_channel': augment_response.json()})
    # --- pepper_noise
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=PepperNoiseArguments(
                processing='pepper_noise',
                amount=33
            )
        ).model_dump()
    )
    responses_map.update({'pepper_noise': augment_response.json()})
    # --- percentile_filter
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=PercentileFilterArguments(
                processing='percentile_filter',
                percentile=50,
                size=5,
            )
        ).model_dump()
    )
    responses_map.update({'percentile_filter': augment_response.json()})
    # --- rainbow_noise
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=RainbowNoiseArguments(
                processing='rainbow_noise',
                amount=33
            )
        ).model_dump()
    )
    responses_map.update({'rainbow_noise': augment_response.json()})
    # --- rotate
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=RotateArguments(
                processing='rotate',
                angle=30
            )
        ).model_dump()
    )
    responses_map.update({'rotate': augment_response.json()})
    # --- salt_noise
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=SaltNoiseArguments(
                processing='salt_noise',
                amount=33
            )
        ).model_dump()
    )
    responses_map.update({'salt_noise': augment_response.json()})
    # --- shift
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=ShiftArguments(
                processing='shift',
                direction='left',
                distance=128,
            )
        ).model_dump()
    )
    responses_map.update({'shift': augment_response.json()})
    # --- tint
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=TintArguments(
                processing='tint',
                channel='b',
                amount=33
            )
        ).model_dump()
    )
    responses_map.update({'tint': augment_response.json()})
    # --- uniform_blur
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=UniformBlurArguments(
                processing='uniform_blur',
                size=33
            )
        ).model_dump()
    )
    responses_map.update({'uniform_blur': augment_response.json()})
    # --- zoom
    augment_response = await http_client.post(
        headers=headers,
        url=f"/image-api/augment/{str(upload_response.json()['unprocessed_image_id'])}",
        json=AugmentationRequestBody(
            arguments=ZoomArguments(
                processing='zoom',
                amount=50
            )
        ).model_dump()
    )
    responses_map.update({'zoom': augment_response.json()})
    # # --- FAIL THIS IF YOU WANT THE PRINTOUT
    # print('-'*100)
    # for k, v in responses_map.items():
    #     print(k, v)
    # print('-'*100)
    # pytest.fail()