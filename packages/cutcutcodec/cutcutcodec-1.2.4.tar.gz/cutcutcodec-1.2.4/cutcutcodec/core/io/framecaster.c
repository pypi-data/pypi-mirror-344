/* Fast frame normalization. */

#define PY_SSIZE_T_CLEAN
#include <numpy/arrayobject.h>
#include <omp.h>
#include <Python.h>
#include "cutcutcodec/core/opti/parallel/threading.h"


#pragma omp declare simd
inline npy_float32 tv2pc(npy_float32 value) {
  /* from range [16/255, 219/255] -> [0, 1] */
  // # see l111 libavfilter/opencl/colorspace_common.cl
  return (value - (16.0f / 255.0f)) * (255.0f / (219.0f - 16.0f));
}


static PyObject* py_normalize_video_frame(PyObject* Py_UNUSED(self), PyObject* args) {
  PyArrayObject *frame, *out = NULL;
  int is_yuv, is_tv, error = 0;
  long int threads = 0;
  npy_float32 factor, yuv_shift;

  // parse input
  if ( !PyArg_ParseTuple(
    args, "O!pp|ll",
    &PyArray_Type, &frame, &is_yuv, &is_tv, &threads
    )
  ) {
    return NULL;
  }

  // case grayscale, add a leading channel dimension
  if ( PyArray_NDIM(frame) == 2 ) {
    npy_intp ptr[] = {PyArray_DIM(frame, 0), PyArray_DIM(frame, 1), 1};
    PyArray_Dims shape = {ptr, 3};
    if ( PyArray_Resize(frame, &shape, 0, NPY_ANYORDER) == NULL ) {
      return PyErr_NoMemory();
    }
    is_yuv = 1;
  } else {
    if ( PyArray_NDIM(frame) != 3 ) {
      PyErr_SetString(PyExc_ValueError, "'frame' requires 3 dimensions");
      return NULL;
    }
  }

  // set context
  threads = get_num_threads(threads);
  yuv_shift = is_yuv ? -0.5 : 0.0;

  // cast and convert
  out = frame;
  int out_inplace = 1;
  switch ( PyArray_TYPE(frame) ) {
    case NPY_FLOAT32:
      Py_BEGIN_ALLOW_THREADS
      switch ( PyArray_DIM(frame, 2) ) {
        case 1:
          if ( is_tv ) {
            #pragma omp parallel for schedule(static) num_threads(threads)
            for ( npy_intp i = 0; i < PyArray_DIM(frame, 0); ++i ) {  // float32, y, tv
            #pragma GCC ivdep
            for ( npy_intp j = 0; j < PyArray_DIM(frame, 1); ++j ) {
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 0) = tv2pc(*(npy_float32 *)PyArray_GETPTR3(frame, i, j, 0));
            }}
          }
          break;
        case 3:
          if ( is_tv ) {
            #pragma omp parallel for schedule(static) num_threads(threads)
            for ( npy_intp i = 0; i < PyArray_DIM(frame, 0); ++i ) {  // float32, yuv, tv
            #pragma GCC ivdep
            for ( npy_intp j = 0; j < PyArray_DIM(frame, 1); ++j ) {
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 0) = tv2pc(*(npy_float32 *)PyArray_GETPTR3(frame, i, j, 0));
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 1) = tv2pc(*(npy_float32 *)PyArray_GETPTR3(frame, i, j, 1)) + yuv_shift;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 2) = tv2pc(*(npy_float32 *)PyArray_GETPTR3(frame, i, j, 2)) + yuv_shift;
            }}
          } else {
            #pragma omp parallel for schedule(static) num_threads(threads)
            for ( npy_intp i = 0; i < PyArray_DIM(frame, 0); ++i ) {  // float32, yuv, pc
            #pragma GCC ivdep
            for ( npy_intp j = 0; j < PyArray_DIM(frame, 1); ++j ) {
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 1) = *(npy_float32 *)PyArray_GETPTR3(frame, i, j, 1) + yuv_shift;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 2) = *(npy_float32 *)PyArray_GETPTR3(frame, i, j, 2) + yuv_shift;
            }}
          }
          break;
        case 4:
          if ( is_tv ) {
            #pragma omp parallel for schedule(static) num_threads(threads)
            for ( npy_intp i = 0; i < PyArray_DIM(frame, 0); ++i ) {  // float32, yuva, tv
            #pragma GCC ivdep
            for ( npy_intp j = 0; j < PyArray_DIM(frame, 1); ++j ) {
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 0) = tv2pc(*(npy_float32 *)PyArray_GETPTR3(frame, i, j, 0));
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 1) = tv2pc(*(npy_float32 *)PyArray_GETPTR3(frame, i, j, 1)) + yuv_shift;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 2) = tv2pc(*(npy_float32 *)PyArray_GETPTR3(frame, i, j, 2)) + yuv_shift;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 3) = tv2pc(*(npy_float32 *)PyArray_GETPTR3(frame, i, j, 3));
            }}
          } else {
            #pragma omp parallel for schedule(static) num_threads(threads)
            for ( npy_intp i = 0; i < PyArray_DIM(frame, 0); ++i ) {  // float32, yuva, pc
            #pragma GCC ivdep
            for ( npy_intp j = 0; j < PyArray_DIM(frame, 1); ++j ) {
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 1) = *(npy_float32 *)PyArray_GETPTR3(frame, i, j, 1) + yuv_shift;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 2) = *(npy_float32 *)PyArray_GETPTR3(frame, i, j, 2) + yuv_shift;
            }}
          }
      }
      Py_END_ALLOW_THREADS
      break;
    case NPY_UINT8:
      out = (PyArrayObject *)PyArray_EMPTY(3, PyArray_SHAPE(frame), NPY_FLOAT32, 0);
      if ( out == NULL ) {
        error = 1;
        break;
      }
      Py_BEGIN_ALLOW_THREADS
      factor = 1.0 / 255.0;
      out_inplace = 0;
      switch ( PyArray_DIM(frame, 2) ) {
        case 1:
          if ( is_tv ) {
            #pragma omp parallel for schedule(static) num_threads(threads)
            for ( npy_intp i = 0; i < PyArray_DIM(frame, 0); ++i ) {  // uint8, y, tv
            #pragma GCC ivdep
            for ( npy_intp j = 0; j < PyArray_DIM(frame, 1); ++j ) {
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 0) = tv2pc((npy_float32)(*(npy_uint8 *)PyArray_GETPTR3(frame, i, j, 0)) * factor);
            }}
          } else {
            #pragma omp parallel for schedule(static) num_threads(threads)
            for ( npy_intp i = 0; i < PyArray_DIM(frame, 0); ++i ) {  // uint8, y, pc
            #pragma GCC ivdep
            for ( npy_intp j = 0; j < PyArray_DIM(frame, 1); ++j ) {
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 0) = (npy_float32)(*(npy_uint8 *)PyArray_GETPTR3(frame, i, j, 0)) * factor;
            }}
          }
          break;
        case 3:
          if ( is_tv ) {
            #pragma omp parallel for schedule(static) num_threads(threads)
            for ( npy_intp i = 0; i < PyArray_DIM(frame, 0); ++i ) {  // uint8, yuv, tv
            #pragma GCC ivdep
            for ( npy_intp j = 0; j < PyArray_DIM(frame, 1); ++j ) {
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 0) = tv2pc((npy_float32)(*(npy_uint8 *)PyArray_GETPTR3(frame, i, j, 0)) * factor);
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 1) = tv2pc((npy_float32)(*(npy_uint8 *)PyArray_GETPTR3(frame, i, j, 1)) * factor) + yuv_shift;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 2) = tv2pc((npy_float32)(*(npy_uint8 *)PyArray_GETPTR3(frame, i, j, 2)) * factor) + yuv_shift;
            }}
          } else {
            #pragma omp parallel for schedule(static) num_threads(threads)
            for ( npy_intp i = 0; i < PyArray_DIM(frame, 0); ++i ) {  // uint8, yuv, pc
            #pragma GCC ivdep
            for ( npy_intp j = 0; j < PyArray_DIM(frame, 1); ++j ) {
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 0) = (npy_float32)(*(npy_uint8 *)PyArray_GETPTR3(frame, i, j, 0)) * factor;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 1) = (npy_float32)(*(npy_uint8 *)PyArray_GETPTR3(frame, i, j, 1)) * factor + yuv_shift;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 2) = (npy_float32)(*(npy_uint8 *)PyArray_GETPTR3(frame, i, j, 2)) * factor + yuv_shift;
            }}
          }
          break;
        case 4:
          if ( is_tv ) {
            #pragma omp parallel for schedule(static) num_threads(threads)
            for ( npy_intp i = 0; i < PyArray_DIM(frame, 0); ++i ) {  // uint8, yuva, tv
            #pragma GCC ivdep
            for ( npy_intp j = 0; j < PyArray_DIM(frame, 1); ++j ) {
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 0) = tv2pc((npy_float32)(*(npy_uint8 *)PyArray_GETPTR3(frame, i, j, 0)) * factor);
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 1) = tv2pc((npy_float32)(*(npy_uint8 *)PyArray_GETPTR3(frame, i, j, 1)) * factor) + yuv_shift;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 2) = tv2pc((npy_float32)(*(npy_uint8 *)PyArray_GETPTR3(frame, i, j, 2)) * factor) + yuv_shift;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 3) = tv2pc((npy_float32)(*(npy_uint8 *)PyArray_GETPTR3(frame, i, j, 3)) * factor);
            }}
          } else {
            #pragma omp parallel for schedule(static) num_threads(threads)
            for ( npy_intp i = 0; i < PyArray_DIM(frame, 0); ++i ) {  // uint8, yuva, pc
            #pragma GCC ivdep
            for ( npy_intp j = 0; j < PyArray_DIM(frame, 1); ++j ) {
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 0) = (npy_float32)(*(npy_uint8 *)PyArray_GETPTR3(frame, i, j, 0)) * factor;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 1) = (npy_float32)(*(npy_uint8 *)PyArray_GETPTR3(frame, i, j, 1)) * factor + yuv_shift;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 2) = (npy_float32)(*(npy_uint8 *)PyArray_GETPTR3(frame, i, j, 2)) * factor + yuv_shift;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 3) = (npy_float32)(*(npy_uint8 *)PyArray_GETPTR3(frame, i, j, 3)) * factor;
            }}
          }
          break;
      }
      Py_END_ALLOW_THREADS
      break;
    case NPY_UINT16:
      out = (PyArrayObject *)PyArray_EMPTY(3, PyArray_SHAPE(frame), NPY_FLOAT32, 0);
      if ( out == NULL ) {
        error = 1;
        break;
      }
      Py_BEGIN_ALLOW_THREADS
      factor = 1.0 / 65535.0;
      out_inplace = 0;
      switch ( PyArray_DIM(frame, 2) ) {
        case 1:
          if ( is_tv ) {
            #pragma omp parallel for schedule(static) num_threads(threads)
            for ( npy_intp i = 0; i < PyArray_DIM(frame, 0); ++i ) {  // uint8, y, tv
            #pragma GCC ivdep
            for ( npy_intp j = 0; j < PyArray_DIM(frame, 1); ++j ) {
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 0) = tv2pc((npy_float32)(*(npy_uint16 *)PyArray_GETPTR3(frame, i, j, 0)) * factor);
            }}
          } else {
            #pragma omp parallel for schedule(static) num_threads(threads)
            for ( npy_intp i = 0; i < PyArray_DIM(frame, 0); ++i ) {  // uint8, y, pc
            #pragma GCC ivdep
            for ( npy_intp j = 0; j < PyArray_DIM(frame, 1); ++j ) {
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 0) = (npy_float32)(*(npy_uint16 *)PyArray_GETPTR3(frame, i, j, 0)) * factor;
            }}
          }
          break;
        case 3:
          if ( is_tv ) {
            #pragma omp parallel for schedule(static) num_threads(threads)
            for ( npy_intp i = 0; i < PyArray_DIM(frame, 0); ++i ) {  // uint8, yuv, tv
            #pragma GCC ivdep
            for ( npy_intp j = 0; j < PyArray_DIM(frame, 1); ++j ) {
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 0) = tv2pc((npy_float32)(*(npy_uint16 *)PyArray_GETPTR3(frame, i, j, 0)) * factor);
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 1) = tv2pc((npy_float32)(*(npy_uint16 *)PyArray_GETPTR3(frame, i, j, 1)) * factor) + yuv_shift;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 2) = tv2pc((npy_float32)(*(npy_uint16 *)PyArray_GETPTR3(frame, i, j, 2)) * factor) + yuv_shift;
            }}
          } else {
            #pragma omp parallel for schedule(static) num_threads(threads)
            for ( npy_intp i = 0; i < PyArray_DIM(frame, 0); ++i ) {  // uint8, yuv, pc
            #pragma GCC ivdep
            for ( npy_intp j = 0; j < PyArray_DIM(frame, 1); ++j ) {
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 0) = (npy_float32)(*(npy_uint16 *)PyArray_GETPTR3(frame, i, j, 0)) * factor;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 1) = (npy_float32)(*(npy_uint16 *)PyArray_GETPTR3(frame, i, j, 1)) * factor + yuv_shift;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 2) = (npy_float32)(*(npy_uint16 *)PyArray_GETPTR3(frame, i, j, 2)) * factor + yuv_shift;
            }}
          }
          break;
        case 4:
          if ( is_tv ) {
            #pragma omp parallel for schedule(static) num_threads(threads)
            for ( npy_intp i = 0; i < PyArray_DIM(frame, 0); ++i ) {  // uint8, yuva, tv
            #pragma GCC ivdep
            for ( npy_intp j = 0; j < PyArray_DIM(frame, 1); ++j ) {
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 0) = tv2pc((npy_float32)(*(npy_uint16 *)PyArray_GETPTR3(frame, i, j, 0)) * factor);
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 1) = tv2pc((npy_float32)(*(npy_uint16 *)PyArray_GETPTR3(frame, i, j, 1)) * factor) + yuv_shift;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 2) = tv2pc((npy_float32)(*(npy_uint16 *)PyArray_GETPTR3(frame, i, j, 2)) * factor) + yuv_shift;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 3) = tv2pc((npy_float32)(*(npy_uint16 *)PyArray_GETPTR3(frame, i, j, 3)) * factor);
            }}
          } else {
            #pragma omp parallel for schedule(static) num_threads(threads)
            for ( npy_intp i = 0; i < PyArray_DIM(frame, 0); ++i ) {  // uint8, yuva, pc
            #pragma GCC ivdep
            for ( npy_intp j = 0; j < PyArray_DIM(frame, 1); ++j ) {
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 0) = (npy_float32)(*(npy_uint16 *)PyArray_GETPTR3(frame, i, j, 0)) * factor;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 1) = (npy_float32)(*(npy_uint16 *)PyArray_GETPTR3(frame, i, j, 1)) * factor + yuv_shift;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 2) = (npy_float32)(*(npy_uint16 *)PyArray_GETPTR3(frame, i, j, 2)) * factor + yuv_shift;
              *(npy_float32 *)PyArray_GETPTR3(out, i, j, 3) = (npy_float32)(*(npy_uint16 *)PyArray_GETPTR3(frame, i, j, 3)) * factor;
            }}
          }
          break;
      }
      Py_END_ALLOW_THREADS
      break;
  }

  // finalyse
  if ( error ) {
    Py_DECREF(out);
    return PyErr_NoMemory();
  }
  if ( out_inplace ) {
    Py_INCREF(out);
  }

  return (PyObject*)out;
}


static PyMethodDef framecasterMethods[] = {
  {
    "normalize_video_frame", (PyCFunction)py_normalize_video_frame, METH_VARARGS,
    R"(Normalize a raw video frame.

    * add 1 leading channel to grayscale frame (h x w -> h x w x 1)
    * shift bit because libav convertion is only bit shift
    * cast into float32
    * convert limited range to full range (based on UIT-R)

    Parameters
    ----------
    frame : np.ndarray
        The float32, uint8 or uint16 video frame of shape (height, width, [channels]),
        with optional channel dimension in {1, 3, 4}.
    is_yuv : bool
        If False, consider frame in rgb in [0, 1]**3, otherwise, yuv in [0, 1] x [-1/2, 1/2]**2.
    is_tv : bool
        If True, apply limited range convertion (219*x+16) * 2**(n-8).
    threads : int, default=0
        Number of threads used.

    Notes
    -----
    It is optimized for C contiguous array.
    )"
  },
  {NULL, NULL, 0, NULL}
};


static struct PyModuleDef framecaster = {
  PyModuleDef_HEAD_INIT,
  "framecaster",
  "This module, implemented in C, offers functions to normalize frames.",
  -1,
  framecasterMethods
};


PyMODINIT_FUNC PyInit_framecaster(void)
{
  import_array();
  if ( PyErr_Occurred() ) {
    return NULL;
  }
  return PyModule_Create(&framecaster);
}
