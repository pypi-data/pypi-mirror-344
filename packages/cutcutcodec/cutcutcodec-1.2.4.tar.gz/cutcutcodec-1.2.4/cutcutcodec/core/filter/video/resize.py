#!/usr/bin/env python3

"""Resize an image."""

from fractions import Fraction
import numbers
import typing

import cv2
import numpy as np
import torch

from cutcutcodec.core.classes.filter import Filter
from cutcutcodec.core.classes.frame_video import FrameVideo
from cutcutcodec.core.classes.stream import Stream
from cutcutcodec.core.classes.stream_video import StreamVideoWrapper
from .pad import pad_keep_ratio


def _resize(image: np.ndarray, shape: tuple[int, int], copy: bool) -> np.ndarray:
    """Help ``resize``.

    Notes
    -----
    * No verifications are performed for performance reason.
    * The output tensor can be a reference to the provided tensor if copy is False.
    """
    if image.shape[:2] == shape:  # optional optimization
        return image.copy() if copy else image
    height, width = shape
    enlarge = height >= image.shape[0] or width >= image.shape[1]
    image = np.ascontiguousarray(image)  # cv2 needs it
    image = cv2.resize(  # 10 times faster than torchvision.transforms.v2.functional.resize
        image,
        dsize=(width, height),
        interpolation=(cv2.INTER_LANCZOS4 if enlarge else cv2.INTER_AREA),  # for antialiasing
    )
    if enlarge and np.issubdtype(image.dtype, np.floating):
        image = np.clip(image, 0.0, 1.0, out=image)
    return image


def resize(
    image: FrameVideo | torch.Tensor | np.ndarray,
    shape: tuple[numbers.Integral, numbers.Integral] | list[numbers.Integral],
    copy: bool = True,
) -> FrameVideo | torch.Tensor | np.ndarray:
    """Reshape the image, can introduce a deformation.

    Parameters
    ----------
    image : cutcutcodec.core.classes.image_video.FrameVideo or torch.Tensor or numpy.ndarray
        The image to be resized, of shape (height, width, channels).
        It has to match with the video image specifications.
    shape : int and int
        The pixel dimensions of the returned image.
        The convention adopted is the numpy convention (height, width).
    copy : boolean, default=True
        If True, ensure that the returned tensor doesn't share the data of the input tensor.

    Returns
    -------
    resized_image
        The resized image homogeneous with the input.
        The underground data are not shared with the input. A safe copy is done.

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.classes.frame_video import FrameVideo
    >>> from cutcutcodec.core.filter.video.resize import resize
    >>> ref = FrameVideo(0, torch.empty(480, 720, 3))
    >>> resize(ref, (720, 1080)).shape  # upscaling
    (720, 1080, 3)
    >>> resize(ref, (480, 360)).shape  # downscaling
    (480, 360, 3)
    >>>
    """
    # case cast homogeneous
    if isinstance(image, FrameVideo):
        return FrameVideo(image.time, resize(torch.Tensor(image), shape, copy=copy))
    if isinstance(image, torch.Tensor):
        return torch.as_tensor(
            resize(image.numpy(force=True), shape, copy=copy), device=image.device
        )

    # verif case np.ndarray
    assert isinstance(image, np.ndarray), image.__class__.__name__
    assert image.ndim == 3, image.shape
    assert image.shape[0] >= 1, image.shape
    assert image.shape[1] >= 1, image.shape
    assert image.shape[2] in {1, 2, 3, 4}, image.shape
    assert image.dtype.type in {np.uint8, np.float32}
    assert isinstance(shape, (tuple, list)), shape.__class__.__name__
    assert len(shape) == 2, len(shape)
    assert all(isinstance(s, numbers.Integral) and s >= 1 for s in shape), shape
    shape = (int(shape[0]), int(shape[1]))
    assert isinstance(copy, bool), copy.__class__.__name__

    # resize
    return _resize(image, shape, copy=copy)


def resize_keep_ratio(
    image: FrameVideo | torch.Tensor | np.ndarray,
    shape: tuple[numbers.Integral, numbers.Integral] | list[numbers.Integral],
    copy: bool = True,
) -> FrameVideo | torch.Tensor | np.ndarray:
    """Reshape the image, keep the aspact ratio and pad with transparent pixels.

    Parameters
    ----------
    image : cutcutcodec.core.classes.image_video.FrameVideo or torch.Tensor or numpy.ndarray
        Transmitted to ``cutcutcodec.core.filter.video.resize.resize``.
    shape : int and int
        Transmitted to ``cutcutcodec.core.filter.video.resize.resize``.
    copy : boolean, default=True
        Transmitted to ``cutcutcodec.core.filter.video.resize.resize``.

    Returns
    -------
    resized_image
        The resized (and padded) image homogeneous with the input.
        The underground data are not shared with the input. A safe copy is done.

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.classes.frame_video import FrameVideo
    >>> from cutcutcodec.core.filter.video.resize import resize_keep_ratio
    >>> ref = FrameVideo(0, torch.full((4, 8, 1), 0.5))
    >>>
    >>> # upscale
    >>> resize_keep_ratio(ref, (8, 9))[..., 1]  # alpha layer
    tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [1., 1., 1., 1., 1., 1., 1., 1., 1.],
            [1., 1., 1., 1., 1., 1., 1., 1., 1.],
            [1., 1., 1., 1., 1., 1., 1., 1., 1.],
            [1., 1., 1., 1., 1., 1., 1., 1., 1.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0.]])
    >>> resize_keep_ratio(ref, (8, 9)).convert(1)[..., 0]  # as gray
    tensor([[0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000],
            [0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000],
            [0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000],
            [0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000]])
    >>>
    >>> # downscale
    >>> resize_keep_ratio(ref, (4, 4))[..., 1]  # alpha layer
    tensor([[0., 0., 0., 0.],
            [1., 1., 1., 1.],
            [1., 1., 1., 1.],
            [0., 0., 0., 0.]])
    >>> resize_keep_ratio(ref, (4, 4)).convert(1)[..., 0]  # as gray
    tensor([[0.0000, 0.0000, 0.0000, 0.0000],
            [0.5000, 0.5000, 0.5000, 0.5000],
            [0.5000, 0.5000, 0.5000, 0.5000],
            [0.0000, 0.0000, 0.0000, 0.0000]])
    >>>
    >>> # mix
    >>> resize_keep_ratio(ref, (6, 6))[..., 1]  # alpha layer
    tensor([[0., 0., 0., 0., 0., 0.],
            [1., 1., 1., 1., 1., 1.],
            [1., 1., 1., 1., 1., 1.],
            [1., 1., 1., 1., 1., 1.],
            [0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0.]])
    >>> resize_keep_ratio(ref, (6, 6)).convert(1)[..., 0]  # as gray
    tensor([[0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000],
            [0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000],
            [0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000]])
    >>>
    """
    # minimalist verifications
    assert isinstance(image, (FrameVideo, torch.Tensor, np.ndarray)), image.__class__.__name__
    assert image.ndim >= 2, image.shape
    assert image.shape[0] >= 1, image.shape
    assert image.shape[1] >= 1, image.shape
    assert isinstance(shape, (tuple, list)), shape.__class__.__name__
    assert len(shape) == 2, len(shape)
    assert all(isinstance(s, numbers.Integral) and s >= 1 for s in shape), shape

    # find the shape for keeping proportion
    dw_sh, dh_sw = shape[1]*image.shape[0], shape[0]*image.shape[1]
    if dw_sh < dh_sw:  # need vertical padding
        height, width = (round(dw_sh/image.shape[1]), shape[1])  # keep width unchanged
    elif dw_sh > dh_sw:  # need horizontal padding
        height, width = (shape[0], round(dh_sw/image.shape[0]))  # keep height unchanged
    else:  # if the proportion is the same
        return resize(image, shape, copy=copy)

    # resize and pad
    image = resize(image, (height, width), copy=copy)
    image = pad_keep_ratio(image, shape, copy=False)
    return image


class FilterVideoResize(Filter):
    """Frozen the shape of the input stream.

    Attributes
    ----------
    keep_ratio : boolean
        True if the aspect ratio is keep, False otherwise (readonly).
    shape : tuple[int, int]
        The pixel dimensions of the incoming frames (readonly).
        The convention adopted is the numpy convention (height, width).

    Examples
    --------
    >>> from cutcutcodec.core.generation.video.noise import GeneratorVideoNoise
    >>> from cutcutcodec.core.filter.video.resize import FilterVideoResize
    >>> (stream_in,) = GeneratorVideoNoise(0).out_streams
    >>>
    >>> # keep ratio
    >>> (stream_out,) = FilterVideoResize([stream_in], (4, 6), keep_ratio=True).out_streams
    >>> stream_out.snapshot(0, (8, 9)).convert(1)[..., 0]
    tensor([[0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [0.5235, 0.3225, 0.2517, 0.4637, 0.4967, 0.3389, 0.1788, 0.1682, 0.2504],
            [0.4382, 0.5387, 0.5730, 0.4529, 0.4138, 0.4805, 0.5094, 0.4846, 0.4545],
            [0.4194, 0.6593, 0.7861, 0.5694, 0.4670, 0.6399, 0.7877, 0.7278, 0.5980],
            [0.5754, 0.4871, 0.5062, 0.6876, 0.7017, 0.6122, 0.5992, 0.5289, 0.4502],
            [0.7454, 0.4579, 0.2027, 0.4286, 0.7173, 0.6183, 0.3378, 0.3964, 0.6148],
            [0.9088, 0.5593, 0.1404, 0.1291, 0.5980, 0.6734, 0.2591, 0.4383, 0.8964],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000]])
    >>> stream_out.snapshot(0, (4, 3)).convert(1)[..., 0]
    tensor([[0.0000, 0.0000, 0.0000],
            [0.5060, 0.4730, 0.4557],
            [0.5078, 0.5852, 0.4931],
            [0.0000, 0.0000, 0.0000]])
    >>> stream_out.snapshot(0, (6, 5)).convert(1)[..., 0]
    tensor([[0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [0.4672, 0.4393, 0.4528, 0.3705, 0.3279],
            [0.5374, 0.5901, 0.5939, 0.6267, 0.5536],
            [0.6929, 0.2912, 0.5406, 0.4344, 0.6335],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.0000]])
    >>>
    >>> # deformation
    >>> (stream_out,) = FilterVideoResize([stream_in], (4, 6), keep_ratio=False).out_streams
    >>> stream_out.snapshot(0, (8, 9))[..., 0]
    tensor([[0.5186, 0.2040, 0.1217, 0.6263, 1.0000, 0.8228, 0.4027, 0.5082, 0.8317],
            [0.5837, 0.4015, 0.2937, 0.5282, 0.8607, 0.8669, 0.5844, 0.4760, 0.5484],
            [0.6039, 0.6970, 0.5962, 0.3657, 0.5604, 0.9367, 0.8844, 0.4597, 0.1515],
            [0.4040, 0.7688, 0.7883, 0.2821, 0.3852, 0.9566, 1.0000, 0.5497, 0.1524],
            [0.1668, 0.6130, 0.7582, 0.3105, 0.4186, 0.9009, 0.9197, 0.6914, 0.5459],
            [0.2929, 0.5605, 0.6228, 0.3390, 0.4971, 0.8122, 0.7501, 0.7327, 0.8138],
            [0.7253, 0.6989, 0.5109, 0.3182, 0.5178, 0.7448, 0.6579, 0.6546, 0.7545],
            [1.0000, 0.8142, 0.4661, 0.2942, 0.5099, 0.7171, 0.6343, 0.5901, 0.6479]])
    >>> stream_out.snapshot(0, (4, 3))[..., 0]
    tensor([[0.2721, 0.9769, 0.4960],
            [0.7737, 0.4440, 0.4901],
            [0.5577, 0.4625, 0.7313],
            [0.7737, 0.5130, 0.6131]])
    >>> stream_out.snapshot(0, (6, 5))[..., 0]
    tensor([[0.4298, 0.1972, 1.0000, 0.4729, 0.7146],
            [0.6007, 0.4248, 0.7106, 0.7914, 0.3603],
            [0.5545, 0.6820, 0.3978, 1.0000, 0.2288],
            [0.2864, 0.6698, 0.4334, 0.9205, 0.6380],
            [0.5371, 0.5082, 0.5150, 0.7171, 0.7786],
            [0.9398, 0.4087, 0.5103, 0.6623, 0.6369]])
    >>>
    """

    def __init__(
        self,
        in_streams: typing.Iterable[Stream],
        shape: tuple[numbers.Integral, numbers.Integral] | list[numbers.Integral],
        keep_ratio: bool = False,
    ):
        """Initialise and create the class.

        Parameters
        ----------
        in_streams : typing.Iterable[Stream]
            Transmitted to ``cutcutcodec.core.classes.filter.Filter``.
        shape : tuple[int, int]
            The pixel dimensions of the incoming frames.
            The convention adopted is the numpy convention (height, width).
        keep_ratio : boolean, default=False
            If True, the returned frame is padded to keep the proportion of the incoming frame.
        """
        assert isinstance(shape, (tuple, list)), shape.__class__.__name__
        assert len(shape) == 2, len(shape)
        assert all(isinstance(s, numbers.Integral) and s >= 1 for s in shape), shape
        assert isinstance(keep_ratio, bool), keep_ratio.__class__.__name__
        self._shape = (int(shape[0]), int(shape[1]))
        self._keep_ratio = keep_ratio

        super().__init__(in_streams, in_streams)
        super().__init__(
            in_streams, [_StreamVideoResize(self, index) for index in range(len(in_streams))]
        )

    def _getstate(self) -> dict:
        return {
            "keep_ratio": self.keep_ratio,
            "shape": list(self.shape),
        }

    def _setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        assert state.keys() == {"keep_ratio", "shape"}, set(state)
        FilterVideoResize.__init__(self, in_streams, state["shape"], keep_ratio=state["keep_ratio"])

    @property
    def keep_ratio(self) -> bool:
        """Return True if the aspect ratio is keep, False otherwise."""
        return self._keep_ratio

    @property
    def shape(self) -> tuple[int, int]:
        """Return The pixel dimensions of the incoming frames."""
        return self._shape


class _StreamVideoResize(StreamVideoWrapper):
    """Translate a video stream from a certain delay."""

    def _snapshot(self, timestamp: Fraction, mask: torch.Tensor) -> torch.Tensor:
        in_mask = torch.full(self.node.shape, True, dtype=bool)
        src = self.stream._snapshot(timestamp, in_mask)  # pylint: disable=W0212
        dst = (
            resize_keep_ratio(src, mask.shape)
            if self.node.keep_ratio else
            resize(src, mask.shape)
        )
        return dst
