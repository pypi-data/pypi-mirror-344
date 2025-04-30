# -*- coding-utf8 -*-
import numpy as np
from lazylinop.wip.butterfly import clean, ksm


def fuse(ks_values1: np.ndarray, ks_values2: np.ndarray,
         backend: str = 'numpy', batch: int = 64):
    r"""
    Fuse two ``ks_values1, ks_values2`` of shape
    $\left(a_1,~b_1,~c_1,~d_1\right)$ and $\left(a_2,~b_2,~c_2,~d_2\right)$.
    The resulting ``ks_values`` is of shape
    $\left(a_1,~\frac{b_1d_1}{d_2},~\frac{a_2c_2}{a_1},~d_2\right)$ and satisfies
    ``(ksm(ks_values1) @ ksm(ks_values2)).toarray() == ksm(ks_values).toarray()``.

    Args:
        ks_values1: ``np.ndarray``
            First ``ks_values`` of shape $\left(a_1,~b_1,~c_1,~d_1\right)$.
        ks_values2: ``np.ndarray``
            Second ``ks_values`` of shape $\left(a_2,~b_2,~c_2,~d_2\right)$.
        backend: ``str``, ``tuple`` or ``pycuda.driver.Device``, optional
            Use ``backend`` to fuse the two ``ks_values``.
            See :py:func:`ksm` for more details.
        batch: ``int``, optional
            Use a batch to compute ``ks_values`` instead of
            building complete matrix from ``ksèvalues2``.
            It helps to save memory. Default value is 64.

    Returns:
        The resulting ``ks_values`` is a ``np.ndarray`` of shape
        $\left(a_1,~\frac{b_1d_1}{d_2},~\frac{a_2c_2}{a_1},~d_2\right)$.

    .. seealso::
        - :py:func:`ksm`.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.butterfly import ksm, fuse
        >>> a1, b1, c1, d1 = 2, 2, 2, 4
        >>> a2, b2, c2, d2 = 4, 2, 2, 2
        >>> v1 = np.random.randn(a1, b1, c1, d1)
        >>> v2 = np.random.randn(a2, b2, c2, d2)
        >>> v = fuse(v1, v2)
        >>> v.shape
        (2, 4, 4, 2)
        >>> L = ksm(v)
        >>> L1 = ksm(v1)
        >>> L2 = ksm(v2)
        >>> x = np.random.randn(L.shape[1])
        >>> np.allclose(L @ x, L1 @ L2 @ x)
        True
    """
    a1, b1, c1, d1 = ks_values1.shape
    a2, b2, c2, d2 = ks_values2.shape
    a, b, c, d = a1, (b1 * d1) // d2, (a2 * c2) // a1, d2
    dtype = (ks_values1[0, 0, 0, :1] * ks_values2[0, 0, 0, :1]).dtype
    ks_values = np.zeros((a, b, c, d), dtype=dtype)
    # Compute dense representation of L = L1 @ L2.
    L = ksm(ks_values1, backend=backend)
    out2, in2 = a2 * b2 * d2, a2 * c2 * d2
    if batch > in2 or in2 % batch != 0:
        # Compute new batch value.
        batch = 1
        for i in range(8, 1, -1):
            if in2 % i == 0:
                batch = i
                break
    x = np.zeros((out2, batch), dtype=dtype)
    for col in range(0, in2, batch):
        # Input x is ks_values2.
        for off in range(batch):
            i = (col + off) // (c2 * d2)
            k = (col + off - i * c2 * d2) // d2
            l = col + off - i * c2 * d2 - k * d2
            row = np.arange(i * c2 * d2 + l % d2,
                            (i + 1) * c2 * d2, d2)
            j = (row - i * b2 * d2) // d2
            x[row, off] = ks_values2[i, j, k, l]
        # Compute batch of L1 @ L2 @ Id.
        try:
            y = L @ x
        except Exception:
            # Did not find hyper-parameters.
            # Therefore, use OpenCL backend (no grid restrictions).
            try:
                clean(L)
                del L
                L = ksm(ks_values1, backend='opencl-gpu')
                y = L @ x
            except:
                try:
                    clean(L)
                    del L
                    L = ksm(ks_values1, backend='opencl-cpu')
                    y = L @ x
                except:
                    clean(L)
                    del L
                    L = ksm(ks_values1, backend='numpy')
                    y = L @ x
        for off in range(batch):
            # Reset x.
            i = (col + off) // (c2 * d2)
            k = (col + off - i * c2 * d2) // d2
            l = col + off - i * c2 * d2 - k * d2
            row = np.arange(i * c2 * d2 + l % d2,
                            (i + 1) * c2 * d2, d2)
            j = (row - i * b2 * d2) // d2
            x[row, off] = 0
            # Map between 2d and 4d representations.
            # col = i * c * d + k * d + l
            # row = i * b * d + j * d + l
            # Find i, k and l from col value.
            i = (col + off) // (c * d)
            k = (col + off - i * c * d) // d
            l = col + off - i * c * d - k * d
            # Inside the current block.
            # Find i, j and l from row value.
            row = np.arange(i * c * d + l % d,
                            (i + 1) * c * d, d)
            j = (row - i * b * d) // d
            ks_values[i, j, k, l] = y[row, off]
    clean(L)
    del L
    return ks_values
