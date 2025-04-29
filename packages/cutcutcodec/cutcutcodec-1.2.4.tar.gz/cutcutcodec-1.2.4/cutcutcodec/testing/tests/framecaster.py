#!/usr/bin/env python3

"""Disjonction of alla cases of framecaster."""

import time

import numpy as np

from cutcutcodec.core.io.framecaster import normalize_video_frame


TVH, TVL = 219.0/255.0, 16.0/255.0


def naive_converter(frame: np.ndarray, is_yuv: bool, is_tv: bool) -> np.ndarray:
    """Pure numpy implementation."""
    if frame.ndim == 2:
        frame = frame[:, :, None]
    if frame.dtype != np.float32:
        maxi = float(1 << (8 * frame.itemsize)) - 1.0
        frame = frame.astype(np.float32)
        frame /= maxi
    if is_tv:
        frame -= 16.0 / 255.0
        frame *= 255.0 / (219.0 - 16.0)
    if is_yuv:
        frame[:, :, 1:3] -= 0.5
    return frame


def timer(frame: np.ndarray, name: str, *args):
    """Ensure C implementation is faster than pure numpy."""
    t_naive, t_c = [], []
    for _ in range(64):
        frame_copy = frame.copy()
        t_i = time.time()
        naive_converter(frame_copy, *args)
        t_naive.append(time.time() - t_i)
        frame_copy = frame.copy()
        t_i = time.time()
        normalize_video_frame(frame_copy, *args)
        t_c.append(time.time() - t_i)
    t_naive = np.median(t_naive)
    t_c = np.median(t_c)
    print(f"{name} naive:{1000*t_naive:.2f}ms vs c:{1000*t_c:.2f}ms ({t_naive/t_c:.2f} x faster)")
    assert t_c < t_naive


def test_float32_y_pc():
    """Test this convertion."""
    frame = np.array([[0.0, 1.0]], dtype=np.float32)
    is_yuv, is_tv = True, False
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv),
    )
    timer(np.empty((1080, 1920), dtype=np.float32), "float32-y-pc", is_yuv, is_tv)


def test_float32_y_tv():
    """Test this convertion."""
    frame = np.array([[TVL, TVH]], dtype=np.float32)
    is_yuv, is_tv = True, True
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv),
    )
    timer(np.empty((1080, 1920), dtype=np.float32), "float32-y-tv", is_yuv, is_tv)


def test_float32_yuv_pc():
    """Test this convertion."""
    frame = np.array([[[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]]], dtype=np.float32)
    is_yuv, is_tv = True, False
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv),
    )
    timer(np.empty((1080, 1920, 3), dtype=np.float32), "float32-yuv-pc", is_yuv, is_tv)


def test_float32_yuv_tv():
    """Test this convertion."""
    frame = np.array([[[TVL, TVL, TVL], [TVH, TVH, TVH]]], dtype=np.float32)
    is_yuv, is_tv = True, True
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv),
    )
    timer(np.empty((1080, 1920, 3), dtype=np.float32), "float32-yuv-tv", is_yuv, is_tv)


def test_float32_yuva_pc():
    """Test this convertion."""
    frame = np.array([[[0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 1.0, 1.0]]], dtype=np.float32)
    is_yuv, is_tv = True, False
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv),
    )
    timer(np.empty((1080, 1920, 4), dtype=np.float32), "float32-yuva-pc", is_yuv, is_tv)


def test_float32_yuva_tv():
    """Test this convertion."""
    frame = np.array([[[TVL, TVL, TVL, TVL], [TVH, TVH, TVH, TVH]]], dtype=np.float32)
    is_yuv, is_tv = True, True
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv),
    )
    timer(np.empty((1080, 1920, 4), dtype=np.float32), "float32-yuva-tv", is_yuv, is_tv)


def test_uint8_y_pc():
    """Test this convertion."""
    frame = np.array([[0, 255]], dtype=np.uint8)
    is_yuv, is_tv = True, False
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv),
    )
    timer(np.empty((1080, 1920), dtype=np.uint8), "u8-y-pc", is_yuv, is_tv)


def test_uint8_y_tv():
    """Test this convertion."""
    frame = np.array([[16, 219]], dtype=np.uint8)
    is_yuv, is_tv = True, True
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv),
    )
    timer(np.empty((1080, 1920), dtype=np.uint8), "u8-y-tv", is_yuv, is_tv)


def test_uint8_yuv_pc():
    """Test this convertion."""
    frame = np.array([[[0, 0, 0], [255, 255, 255]]], dtype=np.uint8)
    is_yuv, is_tv = True, False
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv)
    )
    timer(np.empty((1080, 1920, 3), dtype=np.uint8), "u8-yuv-pc", is_yuv, is_tv)


def test_uint8_yuv_tv():
    """Test this convertion."""
    frame = np.array([[[16, 16, 16], [219, 219, 219]]], dtype=np.uint8)
    is_yuv, is_tv = True, True
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv)
    )
    timer(np.empty((1080, 1920, 3), dtype=np.uint8), "u8-yuv-tv", is_yuv, is_tv)


def test_uint8_yuva_pc():
    """Test this convertion."""
    frame = np.array([[[0, 0, 0, 0], [255, 255, 255, 255]]], dtype=np.uint8)
    is_yuv, is_tv = True, False
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv)
    )
    timer(np.empty((1080, 1920, 4), dtype=np.uint8), "u8-yuva-pc", is_yuv, is_tv)


def test_uint8_yuva_tv():
    """Test this convertion."""
    frame = np.array([[[16, 16, 16, 16], [219, 219, 219, 219]]], dtype=np.uint8)
    is_yuv, is_tv = True, True
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv)
    )
    timer(np.empty((1080, 1920, 4), dtype=np.uint8), "u8-yuva-tv", is_yuv, is_tv)


def test_uint16_y_pc_10b():
    """Test this convertion."""
    frame = np.array([[0, 1023]], dtype=np.uint16) << 6
    is_yuv, is_tv = True, False
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv),
    )
    timer(np.empty((1080, 1920), dtype=np.uint16), "u16-y-pc-10b", is_yuv, is_tv)


def test_uint16_y_pc_12b():
    """Test this convertion."""
    frame = np.array([[0, 4095]], dtype=np.uint16) << 4
    is_yuv, is_tv = True, False
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv),
    )
    timer(np.empty((1080, 1920), dtype=np.uint16), "u16-y-pc-12b", is_yuv, is_tv)


def test_uint16_y_tv_10b():
    """Test this convertion."""
    frame = np.array([[64, 876]], dtype=np.uint16) << 6
    is_yuv, is_tv = True, True
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv),
    )
    timer(np.empty((1080, 1920), dtype=np.uint16), "u16-y-tv-10b", is_yuv, is_tv)


def test_uint16_y_tv_12b():
    """Test this convertion."""
    frame = np.array([[256, 3504]], dtype=np.uint16) << 4
    is_yuv, is_tv = True, True
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv),
    )
    timer(np.empty((1080, 1920), dtype=np.uint16), "u16-y-tv-12b", is_yuv, is_tv)


def test_uint16_yuv_pc_10b():
    """Test this convertion."""
    frame = np.array([[[0, 0, 0], [1023, 1023, 1023]]], dtype=np.uint16) << 6
    is_yuv, is_tv = True, False
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv)
    )
    timer(np.empty((1080, 1920, 3), dtype=np.uint16), "u16-yuv-pc_10b", is_yuv, is_tv)


def test_uint16_yuv_pc_12b():
    """Test this convertion."""
    frame = np.array([[[0, 0, 0], [4095, 4095, 4095]]], dtype=np.uint16) << 4
    is_yuv, is_tv = True, False
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv)
    )
    timer(np.empty((1080, 1920, 3), dtype=np.uint16), "u16-yuv-pc_12b", is_yuv, is_tv)


def test_uint16_yuv_tv_10b():
    """Test this convertion."""
    frame = np.array([[[64, 64, 64], [876, 876, 876]]], dtype=np.uint16) << 6
    is_yuv, is_tv = True, True
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv)
    )
    timer(np.empty((1080, 1920, 3), dtype=np.uint16), "u16-yuv-tv-10b", is_yuv, is_tv)


def test_uint16_yuv_tv_12b():
    """Test this convertion."""
    frame = np.array([[[256, 256, 256], [3504, 3504, 3504]]], dtype=np.uint16) << 4
    is_yuv, is_tv = True, True
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv)
    )
    timer(np.empty((1080, 1920, 3), dtype=np.uint16), "u16-yuv-tv-12b", is_yuv, is_tv)


def test_uint16_yuva_pc_10b():
    """Test this convertion."""
    frame = np.array([[[0, 0, 0, 0], [1023, 1023, 1023, 1023]]], dtype=np.uint16) << 6
    is_yuv, is_tv = True, False
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv)
    )
    timer(np.empty((1080, 1920, 4), dtype=np.uint16), "u16-yuva-pc-10b", is_yuv, is_tv)


def test_uint16_yuva_pc_12b():
    """Test this convertion."""
    frame = np.array([[[0, 0, 0, 0], [4095, 4095, 4095, 4095]]], dtype=np.uint16) << 4
    is_yuv, is_tv = True, False
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv)
    )
    timer(np.empty((1080, 1920, 4), dtype=np.uint16), "u16-yuva-pc-12b", is_yuv, is_tv)


def test_uint16_yuva_tv_10b():
    """Test this convertion."""
    frame = np.array([[[64, 64, 64, 64], [876, 876, 876, 876]]], dtype=np.uint16) << 6
    is_yuv, is_tv = True, True
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv)
    )
    timer(np.empty((1080, 1920, 4), dtype=np.uint16), "u16-yuva-tv-10b", is_yuv, is_tv)


def test_uint16_yuva_tv_12b():
    """Test this convertion."""
    frame = np.array([[[256, 256, 256, 256], [3504, 3504, 3504, 3504]]], dtype=np.uint16) << 4
    is_yuv, is_tv = True, True
    assert np.allclose(
        normalize_video_frame(frame.copy(), is_yuv, is_tv),
        naive_converter(frame.copy(), is_yuv, is_tv)
    )
    timer(np.empty((1080, 1920, 4), dtype=np.uint16), "u16-yuva-tv-12b", is_yuv, is_tv)
