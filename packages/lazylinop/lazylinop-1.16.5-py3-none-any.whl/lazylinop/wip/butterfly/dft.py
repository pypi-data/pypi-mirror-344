import numpy as np
from lazylinop.signal import fft
from lazylinop.wip.butterfly import fuse
from lazylinop.wip.butterfly import clean, ksm
from lazylinop.wip.butterfly.ksm import _multiple_ksm
from lazylinop.basicops import bitrev


def dft_square_dyadic_ks_values(N: int, dense: bool = False,
                                dtype: str = 'complex64'):
    r"""
    Return a list of ``ks_values`` that corresponds
    to the ``F @ P.T`` matrix decomposition into
    ``p = int(np.log2(N))`` factors, where ``F`` is the DFT matrix
    and ``P`` the bit-reversal permutation matrix.
    The size $N=2^p$ of the DFT must be a power of $2$.

    We can draw the square-dyadic decomposition for $N=16$:

    .. image:: _static/dft_16x16_square_dyadic.svg

    Args:
        N: ``int``
            DFT of size $N=2^p$.
        dense: ``bool``, optional
            If ``dense=True`` compute and return
            2d representation of the factors.
            Default value is ``False``.
        dtype: ``str``, optional
            It could be either ``'complex64'`` (default) or ``'complex128'``.

    Returns:
        List of 4d ``np.ndarray`` corresponding to ``ks_values``.
        If ``dense=True`` it also returns a list of
        2d ``np.ndarray`` corresponding to the ``p = int(np.log2(N))`` factors.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.butterfly import dft_square_dyadic_ks_values
        >>> from lazylinop.wip.butterfly import ksm
        >>> from lazylinop.signal import fft
        >>> from lazylinop.basicops import bitrev
        >>> N = 2 ** 10
        >>> ks_values = dft_square_dyadic_ks_values(N)
        >>> x = np.random.randn(N)
        >>> L = ksm(ks_values, backend='scipy')
        >>> P = bitrev(N)
        >>> np.allclose(fft(N) @ x, L @ P @ x)
        True

    References:
        - Learning Fast Algorithms for Linear Transforms Using Butterfly Factorizations.
          Dao T, Gu A, Eichhorn M, Rudra A, Re C.
          Proc Mach Learn Res. 2019 Jun;97:1517-1527. PMID: 31777847; PMCID: PMC6879380.
    """
    if not (((N & (N - 1)) == 0) and N > 0):
        raise ValueError("N must be a power of two.")
    inv_sqrt2 = 1.0 / np.sqrt(2.0)
    p = int(np.log2(N))
    if dense:
        factors = [None] * p
    ks_values = [None] * p
    for n in range(p):
        if n == (p - 1):
            f2 = (fft(2) @ np.eye(2)).astype(dtype)
            if dense:
                factors[n] = np.kron(np.eye(N // 2, dtype=dtype), f2)
            a = N // 2
            b, c = 2, 2
            d = 1
            ks_values[n] = np.empty((a, b, c, d), dtype=dtype)
            for i in range(a):
                ks_values[n][i, :, :, 0] = f2
        else:
            s = N // 2 ** (p - n)
            t = N // 2 ** (n + 1)
            w = np.exp(2.0j * np.pi / (2 * t))
            omega = (w ** (-np.arange(t))).astype(dtype)
            if dense:
                diag_omega = np.diag(omega)
                factors[n] = np.kron(
                    np.eye(s, dtype=dtype) * inv_sqrt2,
                    np.vstack((
                        np.hstack((np.eye(t, dtype=dtype), diag_omega)),
                        np.hstack((np.eye(t, dtype=dtype), -diag_omega)))))
            a = s
            b, c = 2, 2
            d = t
            ks_values[n] = np.empty((a, b, c, d), dtype=dtype)
            # Map between 2d and 4d representations.
            # col = i * c * d + k * d + l
            # row = i * b * d + j * d + l
            # Loop over the a blocks.
            for i in range(a):
                for u in range(t):
                    for v in range(4):
                        if v == 0:
                            # Identity.
                            sub_col = u
                            sub_row = u
                            tmp = inv_sqrt2
                        elif v == 1:
                            # diag(omega).
                            sub_col = u + t
                            sub_row = u
                            tmp = omega[u] * inv_sqrt2
                        elif v == 2:
                            # Identity.
                            sub_col = u
                            sub_row = u + t
                            tmp = inv_sqrt2
                        else:
                            # -diag(omega)
                            sub_col = u + t
                            sub_row = u + t
                            tmp = -omega[u] * inv_sqrt2
                        j = sub_row // d
                        k = sub_col // d
                        ks_values[n][i, j, k, sub_col - k * d] = tmp
    if dense:
        return ks_values, factors
    else:
        return ks_values


def dft_ks_values(N: int, n_factors: int, dtype: str = 'complex64'):
    r"""
    Return a list of ``ks_values`` that corresponds
    to the ``F @ P.T`` matrix decomposition into ``n_factors`` factors,
    where ``F`` is the DFT matrix and
    ``P`` the bit-reversal permutation matrix.
    The size $N$ of the DFT must be power of $2$.
    See :ref:`[1] <dec>` for more details.

    Args:
        N: ``int``
            DFT of size $N$. $N$ must be a power of two.
        n_factors: ``int``
            Number of factors of the DFT decomposition.
        dtype: ``str``, optional
            It could be either ``'complex64'`` (default) or ``'complex128'``.

    Returns:
        List of 4d ``np.ndarray`` corresponding to ``ks_values``.
        The length of the list is equal to ``n_factors``.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.butterfly import dft_ks_values
        >>> from lazylinop.wip.butterfly import ksm
        >>> from lazylinop.signal import fft
        >>> from lazylinop.basicops import bitrev
        >>> N = 2 ** 10
        >>> ks_values = dft_ks_values(N, 2)
        >>> x = np.random.randn(N)
        >>> L = ksm(ks_values, backend='scipy')
        >>> P = bitrev(N)
        >>> np.allclose(fft(N) @ x, L @ P @ x)
        True
    """
    if not (((N & (N - 1)) == 0) and N > 0):
        raise ValueError("N must be a power of two.")
    p = int(np.log2(N))
    if n_factors == p:
        return dft_square_dyadic_ks_values(p, False, dtype)
    if n_factors < 2 or n_factors > p:
        raise Exception("n_factors must be >= 2 and <= p.")

    inv_sqrt2 = 1.0 / np.sqrt(2.0)
    ks_values = [None] * n_factors
    a, b, c, d = 1, 2, 2, N // 2
    for n in range(n_factors):
        if n < (n_factors - 1):
            w = np.exp(2.0j * np.pi / (2 * d))
            omega = (w ** (-np.arange(d))).astype(dtype)
            ks_values[n] = np.empty((a, b, c, d), dtype=dtype)
            # Map between 2d and 4d representations.
            # col = i * c * d + k * d + l
            # row = i * b * d + j * d + l
            # Loop over the a blocks.
            for i in range(a):
                for u in range(d):
                    for v in range(4):
                        if v == 0:
                            # Identity.
                            sub_col = u
                            sub_row = u
                            tmp = inv_sqrt2
                        elif v == 1:
                            # diag(omega).
                            sub_col = u + d
                            sub_row = u
                            tmp = omega[u] * inv_sqrt2
                        elif v == 2:
                            # Identity.
                            sub_col = u
                            sub_row = u + d
                            tmp = inv_sqrt2
                        else:
                            # -diag(omega)
                            sub_col = u + d
                            sub_row = u + d
                            tmp = -omega[u] * inv_sqrt2
                        j = sub_row // d
                        k = sub_col // d
                        ks_values[n][i, j, k, sub_col - k * d] = tmp
            a *= 2
            d //= 2
        else:
            p2 = 2 ** (n_factors - 1)
            k = N // p2
            a, b, c, d = p2, k, k, 1
            # Compute DFT matrix.
            batch = 1
            for i in range(8, 1, -1):
                if k % i == 0:
                    batch = i
                    break
            x = np.zeros((k, batch), dtype=dtype)
            ks_values[n] = np.empty((a, b, c, d), dtype=dtype)
            for col in range(0, k, batch):
                for off in range(batch):
                    x[col + off, off] = 1.0
                # Compute DFT matrix per batch.
                fx = (fft(k) @ x).astype(dtype)
                # Fill ks_values per batch.
                for i in range(a):
                    ks_values[n][i, :, col:(col + batch), 0] = fx
                for off in range(batch):
                    x[col + off, off] = 0.0
                del fx
            del x
        print(n, ks_values[n].nbytes)
    return ks_values


def dft(N: int, backend: str = 'numpy', dtype: str = 'complex64'):
    r"""
    Return a :class:`LazyLinOp` `L` with the Butterfly structure
    corresponding to the Discrete-Fourier-Transform (DFT).

    The number of factors $p$ of the square-dyadic decomposition
    is given by $p=\log_2\left(N\right)$.

    Shape of ``L`` is $\left(N,~N\right)$ where
    $N=2^p$ must be a power of two.

    Args:
        N: ``int``
            DFT of size $N$. $N$ must be a power of two.
        backend: ``str``, ``tuple`` or ``pycuda.driver.Device``, optional
            See :py:func:`ksm` for more details.
        dtype: ``str``, optional
            It could be either ``'complex64'`` (default) or ``'complex128'``.

    Returns:
        :class:`LazyLinOp` `L` corresponding to the DFT.

    .. seealso::
        :py:func:`dft_helper`

    .. _dec:

        **References:**

        [1] Learning Fast Algorithms for Linear Transforms Using Butterfly Factorizations.
        Dao T, Gu A, Eichhorn M, Rudra A, Re C.
        Proc Mach Learn Res. 2019 Jun;97:1517-1527. PMID: 31777847; PMCID: PMC6879380.
    """
    return dft_helper(N, int(np.log2(N)), backend=backend, dtype=dtype)


def dft_helper(N: int, n_factors: int, backend: str = 'numpy',
               strategy: str = 'memory', dtype: str = 'complex64'):
    r"""
    Return a :class:`LazyLinOp` `L` corresponding to
    the Discrete-Fourier-Transform (DFT).

    Shape of ``L`` is $\left(N,~N\right)$ where
    $N=2^p$ must be a power of two.

    Args:
        N: ``int``
            DFT of size $N$. $N$ must be a power of two.
        n_factors: ``int``
            Number of factors ``n_factors <= p``.
            If ``n_factors = p``, return the square-dyadic decomposition.
            The performance of the algorithm depends on
            the number of factors, the size of the DFT
            as-well-as the strategy.
            Our experimentation shows that square-dyadic decomposition
            is always the worse choice.
            The best choice is two, three or four factors.
        backend: ``str``, ``tuple`` or ``pycuda.driver.Device``, optional
            See :py:func:`ksm` for more details.
        strategy: ``str``, optional
            It could be:

            - ``'l2r'`` fuse from left to right.
            - ``balanced`` fuse from left to right and right to left ($p>3$).

              - Case ``p = 6`` and ``n_factors = 2``:

                - step 0: 0 1 2 3 4 5
                - step 1: 01 2 3 45
                - step 2: 012 345
              - Case ``p = 7`` and ``n_factors = 2``:

                - step 0: 0 1 2 3 4 5 6
                - step 1: 01 2 3 4 56
                - step 2: 012 3 456
                - step 3: 0123 456
              - Case ``p = 7`` and ``n_factors = 3``:

                - step 0: 0 1 2 3 4 5 6
                - step 1: 01 2 3 4 56
                - step 2: 012 3 456
            - ``'memory'`` find the two consecutive ``ks_values`` that
              minimize the memory of the fused ``ks_values``.
              It is the default value.
            - ``'decomposition'`` uses :ref:`[1] <dec>`.
        dtype: ``str``, optional
            It could be either ``'complex64'`` (default) or ``'complex128'``.

    Benchmark of our DFT implementation is
    (we use default hyper-parameters here):

    .. image:: _static/default_dft_batch_size512_complex64.svg

    Returns:
        :class:`LazyLinOp` `L` corresponding to the DFT.

    .. _dec:

        **References:**

        [1] Learning Fast Algorithms for Linear Transforms Using Butterfly Factorizations.
        Dao T, Gu A, Eichhorn M, Rudra A, Re C.
        Proc Mach Learn Res. 2019 Jun;97:1517-1527. PMID: 31777847; PMCID: PMC6879380.
    """
    if not (((N & (N - 1)) == 0) and N > 0):
        raise ValueError("N must be a power of two.")
    p = int(np.log2(N))
    if n_factors > p or n_factors < 1:
        raise ValueError("n_factors must be positive and less or equal to p.")
    if dtype != 'complex64' and dtype != 'complex128':
        raise Exception("dtype must be either 'complex64' or 'complex128'.")

    # FIXME
    if n_factors == 7:
        params = None
    elif n_factors == 8:
        params = None
    elif n_factors == 9:
        params = None
    elif n_factors == 10:
        params = None
    elif n_factors == 11:
        params = None
    elif n_factors == 12:
        params = None
    elif n_factors == 13:
        params = None
    elif n_factors == 14:
        params = None
    else:
        params = None

    ks_values = dft_square_dyadic_ks_values(N, dtype=dtype)
    if p == n_factors:
        # Nothing to fuse.
        L = ksm(ks_values, backend='numpy')
    else:
        tmp = [None] * (p // 2 + p % 2)
        m, target = p, p
        if strategy == 'l2r':
            # Fuse from left to right (in-place modification of ks_values).
            while True:
                for i in range(0, m - m % 2 - 1, 2):
                    if target > n_factors:
                        ks_values[i // 2] = fuse(ks_values[i],
                                                 ks_values[i + 1],
                                                 backend=backend)
                        target -= 1
                if target == n_factors:
                    break
                if m % 2 == 1:
                    ks_values[m // 2 + m % 2 - 1] = ks_values[m - 1]
                    # target -= 1
                if target == n_factors:
                    break
                m = m // 2 + m % 2
                target = m
            L = ksm(ks_values[:n_factors], backend='numpy')
        elif strategy == 'balanced':
            if p <= 3:
                raise Exception("strategy 'balanced' does" +
                                " not work when p <= 3.")
            # Fuse from left to right and from right to left.
            step = 0
            idx = [str(i) for i in range(p)]
            print(f"      ", idx)
            lpos, rpos, n_left, n_right = 0, m - 1, 0, 0
            while True:
                if target > n_factors:
                    # From left to right.
                    idx[lpos + 1] = idx[lpos] + idx[lpos + 1]
                    target -= 1
                    lpos += 1
                    n_left += 1
                if target > n_factors:
                    # From right to left.
                    idx[rpos - 1] = idx[rpos - 1] + idx[rpos]
                    target -= 1
                    rpos -= 1
                    n_right += 1
                if lpos + 1 >= m / 2:
                    lpos, rpos = n_left, m - 1 - n_right
                print(f"step={step}", idx[n_left:(p - n_right)])
                step += 1
                if target == n_factors:
                    break
            # if n_left != n_right:
            #     raise Exception("Cannot fuse from left to right and right to left" +
            #                     " for the given values of p and n_factors.")
            m, target = p, p
            lpos, rpos, n_left, n_right = 0, m - 1, 0, 0
            while True:
                if target > n_factors:
                    # From left to right.
                    ks_values[lpos + 1] = fuse(ks_values[lpos],
                                               ks_values[lpos + 1],
                                               backend=backend)
                    target -= 1
                    lpos += 1
                    n_left += 1
                if target > n_factors:
                    # From right to left.
                    ks_values[rpos - 1] = fuse(ks_values[rpos - 1],
                                               ks_values[rpos],
                                               backend=backend)
                    target -= 1
                    rpos -= 1
                    n_right += 1
                if lpos + 1 >= m // 2:
                    lpos, rpos = n_left, m - 1 - n_right
                if target == n_factors:
                    break
            L = ksm(ks_values[n_left:(n_left + n_factors)], backend='numpy')
        elif strategy == 'memory':
            step = 0
            idx = [str(i) for i in range(p)]
            print(f"      ", idx)
            n_fuses = 0
            while True:
                # Build memory list.
                memory = np.full(p - n_fuses - 1, 0)
                for i in range(p - n_fuses - 1):
                    a1, b1, c1, d1 = ks_values[i].shape
                    a2, b2, c2, d2 = ks_values[i + 1].shape
                    memory[i] = a1 * ((b1 * d1) // d2) * ((a2 * c2) // a1) * d2
                # Find argmin.
                argmin = np.argmin(memory)
                # Fuse argmin and argmin + 1.
                ks_values[argmin] = fuse(ks_values[argmin],
                                         ks_values[argmin + 1],
                                         backend=backend)
                idx[argmin] = idx[argmin] + idx[argmin + 1]
                n_fuses += 1
                # Delete argmin + 1.
                ks_values.pop(argmin + 1)
                idx.pop(argmin + 1)
                target -= 1
                print(f"step={step}", idx)
                step += 1
                if target == n_factors:
                    break
            L = ksm(ks_values, backend='numpy')
        elif strategy == 'decomposition':
            L = ksm(dft_ks_values(p, n_factors, dtype=dtype),
                    backend='numpy')
        else:
            raise Exception("strategy must be either 'l2r'," +
                            " 'balanced' or 'memory'.")

    if backend in ('numpy', 'scipy'):
        F = ksm(L.ks_values, backend=backend) @ bitrev(2 ** p)
        F.ks_values = L.ks_values
    else:
        F = _multiple_ksm(L.ks_values, backend=backend,
                          params=params, perm=True)
        F.ks_values = L.ks_values
    clean(L)
    del L
    return F
