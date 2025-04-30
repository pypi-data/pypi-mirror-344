# -*- coding: utf-8 -*-

from lazylinop.wip.butterfly.GB_param_generate import DebflyGen
import numpy as np


class Chain():

    def __init__(self, ks_patterns: list = None):
        """
        A ``Chain`` instance is built by calling the
        constructor ``Chain(ks_patterns)``.

        Args:
            ks_patterns: ``list``
                List of tuples $((a_l,~b_l,~c_l,~d_l))^n$
                each being called a pattern.

        Attributes:
            ks_patterns: ``list``
                List of patterns $(a_i,~b_i,~c_i,~d_i)$.
            n_patterns: ``int``
                Equal to ``len(ks_patterns)``.
            shape: ``tuple``
                ``shape`` is equal to $(a_1b_1d_1,~a_nc_nd_n)$
                when ``n = n_patterns``.
            chainable: ``bool``
                ``True`` if for each $i$:

                .. - $M=a_0b_0d_0$ is ``True``
                - $a_ic_id_i=a_{i+1}c_{i+1}d_{i+1}$ is ``True``
                - and $a_{i+1}$ divides $a_i$
                - and $d_i$ divides $d_{i+1}$
                .. - and $N=a_{n-1}c_{n-1}d_{n-1}$ is ``True``
                See [1] for more details.

        Return:
            ``chain`` with ``ks_patterns``, ``n_patterns``, ``shape``
            and ``chainable`` attributes.

        Examples:
            >>> from lazylinop.wip.butterfly.ksd import Chain
            >>> chain = Chain.smallest_monotone((2, 2), n_patterns=2)
            >>> chain.ks_patterns
            [(1, 1, 1, 2), (1, 2, 2, 1)]
            >>> chain = Chain(ks_patterns=[(2, 1, 1, 2), (2, 1, 1, 2)])
            >>> chain.ks_patterns
            [(2, 1, 1, 2), (2, 1, 1, 2)]
            >>> # Concatenation of two chains.
            >>> chain1 = Chain.smallest_monotone((2, 3), n_patterns=2)
            >>> chain2 = Chain.smallest_monotone((3, 4), n_patterns=2)
            >>> chain = chain1 @ chain2
            >>> chain.shape
            (2, 4)
            >>> chain.n_patterns
            4
            >>> chain.ks_patterns
            [(1, 1, 1, 2), (1, 2, 3, 1), (1, 1, 1, 3), (1, 3, 4, 1)]

        References:
            [1] Butterfly Factorization with Error Guarantees.
            Léon Zheng, Quoc-Tung Le, Elisa Riccietti, and Rémi Gribonval
            https://hal.science/hal-04763712v1/document
        """
        if ks_patterns is not None and not isinstance(ks_patterns, list) \
           and not isinstance(ks_patterns, tuple):
            raise TypeError("ks_patterns must be a list.")
        if ks_patterns is None:
            self.shape = None
            self.n_patterns = None
            self.ks_patterns = None
            self.chainable = False
            self.rank = None
            self._chain_type = 'custom'
        else:
            for k in ks_patterns:
                if not isinstance(k, tuple):
                    raise TypeError("ks_patterns must be a list of tuples.")
            a, b, c, d = ks_patterns[0]
            out = a * b * d
            a, b, c, d = ks_patterns[-1]
            self.shape = (out, a * c * d)
            self.n_patterns = len(ks_patterns)
            self.ks_patterns = ks_patterns
            # Keep track of the rank.
            self._abcdpq = []
            for k in ks_patterns:
                self._abcdpq.append((k[0], k[1], k[2], k[3], 1, 1))
            self.chainable = self._is_chainable()
            self._rank = 1
            self._chain_type = 'custom'

    def _is_chainable(self):
        """
        Check if ``self`` is chainable.
        The following conditions must be true:

        - $M=a_0b_0d_0$
        - $a_ic_id_i=a_{i+1}c_{i+1}d_{i+1}$
        - $a_{i+1}$ divides $a_i$
        - $d_i$ divides $d_{i+1}$
        - $N=a_{n-1}c_{n-1}d_{n-1}$
        See [1] for more details.

        References:
            [1] Butterfly Factorization with Error Guarantees.
            Léon Zheng, Quoc-Tung Le, Elisa Riccietti, and Rémi Gribonval
            https://hal.science/hal-04763712v1/document
        """
        # a_1 * b_1 * d_1 must be equal to the number
        # of rows of the input matrix.
        a, b, c, d = self.ks_patterns[0]
        if a * b * d != self.shape[0]:
            return False
        # a_F * c_F * d_F must be equal to the number
        # of columns of the input matrix.
        F = self.n_patterns
        a, b, c, d = self.ks_patterns[F - 1]
        if a * c * d != self.shape[1]:
            return False
        for i in range(F - 1):
            a1, b1, c1, d1 = self.ks_patterns[i]
            a2, b2, c2, d2 = self.ks_patterns[i + 1]
            if a1 % a2 != 0:
                return False
            if d2 % d1 != 0:
                return False
        # Number of columns of the current factor must
        # be equal to the number of rows of the next factor.
        for i in range(F - 1):
            a, b, c, d = self.ks_patterns[i]
            col = a * c * d
            a, b, c, d = self.ks_patterns[i + 1]
            row = a * b * d
            if col != row:
                return True
        return True

    @classmethod
    def square_dyadic(cls, shape):
        """
        Build a square-dyadic chain from shape.

        Matrix must be square ``shape[0] = shape[1] = N``
        with $N=2^n$ a power of two.
        Number of ``ks_patterns`` is equal to $n$.
        The l-th pattern is given by
        ``(2 ** (l - 1), 2, 2, shape[0] // 2 ** l)`` where
        ``1 <= l <= n``.

        We can draw the square-dyadic decomposition for $N=16$:

        .. image:: _static/dft_16x16_square_dyadic.svg

        Args:
            shape: ``tuple``
                Shape of the input matrix must be $(N,~N)$ with $N=2^n$.
        """
        m, n = shape
        if m != n:
            raise Exception("Matrix must be square shape[0]=shape[1].")
        ok = ((m & (m - 1)) == 0) and m > 0
        ok = ok and (((n & (n - 1)) == 0) and n > 0)
        if not ok:
            raise Exception("shape of the matrix must be power of two.")
        n_patterns = int(np.log2(m))
        ks_patterns = []
        for i in range(1, n_patterns + 1):
            ks_patterns.append((2 ** (i - 1), 2, 2, m // 2 ** i))
        tmp = cls(ks_patterns)
        tmp._chain_type = 'square dyadic'
        return tmp

    @classmethod
    def random(cls, shape: tuple, n_patterns: int):
        """
        Build a random chain from ``shape``.

        Args:
            shape: ``tuple``
                Shape of the input matrix, expect a tuple $(M,~N)$.
                ``M`` is equal to the
                number of rows $a_0b_0d_0$ of the first factor while
                ``N`` is equal to the number of
                columns $a_{n-1}c_{n-1}d_{n-1}$ of the last factor.
            n_patterns: ``int``, optional
                Number of patterns of the chain.
                It corresponds to the number of
                factors $n$ of the decomposition.
        """
        if n_patterns < 2:
            raise Exception("n_patterns must be >= 2.")
        rank = np.random.randint(
            1, high=min(shape[0], shape[1]) // 2 + 1)
        test = DebflyGen(shape[0], shape[1], rank)
        tmp = test.random_debfly_chain(n_patterns, format="abcdpq")
        # Convert to 'abcdpq' format with p=q=1.
        ks_patterns = []
        for t in tmp:
            ks_patterns.append((t[0], t[1], t[2], t[3]))
        tmp = cls(ks_patterns)
        tmp._chain_type = 'random'
        return tmp

    @classmethod
    def smallest_monotone(cls, shape: tuple, n_patterns: int):
        """
        Build the smallest monotone chain possible from ``shape``.

        :octicon:`alert-fill;1em;sd-text-danger` Be aware that
        ``Chain.smallest_monotone(...)`` uses a lot of memory when
        values of ``shape`` are large.

        Args:
            shape: ``tuple``
                Shape of the input matrix, expect a tuple $(M,~N)$.
                ``M`` is equal to the
                number of rows $a_0b_0d_0$ of the first factor while
                ``N`` is equal to the number of
                columns $a_{n-1}c_{n-1}d_{n-1}$ of the last factor.
            n_patterns: ``int``, optional
                Number of patterns of the chain.
                It corresponds to the number of
                factors $n$ of the decomposition.
        """
        if n_patterns < 2:
            raise Exception("n_patterns must be >= 2.")
        rank = 1
        test = DebflyGen(shape[0], shape[1], rank)
        _, tmp = test.smallest_monotone_debfly_chain(
            n_patterns, format="abcdpq")
        # Convert to 'abcd' format.
        ks_patterns = []
        for t in tmp:
            ks_patterns.append((t[0], t[1], t[2], t[3]))
        tmp = cls(ks_patterns)
        tmp._chain_type = 'smallest monotone'
        return tmp

    def __matmul__(self, chain):
        """
        Return the concatenation of two chains.

        Args:
            chain: ``Chain``
                An instance of ``Chain``
                to concatenate with ``self``.

        Returns:
            An instance of ``Chain`` that is the
            concatenation of ``chain`` and ``self``.

        Examples:
            >>> from lazylinop.wip.butterfly.ksd import Chain
            >>> chain1 = Chain.smallest_monotone((2, 3), n_patterns=2)
            >>> chain1.ks_patterns
            [(1, 1, 1, 2), (1, 2, 3, 1)]
            >>> chain2 = Chain.smallest_monotone((3, 4), n_patterns=2)
            >>> chain2.ks_patterns
            [(1, 1, 1, 3), (1, 3, 4, 1)]
            >>> chain = chain1 @ chain2
            >>> chain.shape
            (2, 4)
            >>> chain.n_patterns
            4
            >>> chain.ks_patterns
            [(1, 1, 1, 2), (1, 2, 3, 1), (1, 1, 1, 3), (1, 3, 4, 1)]
        """
        M, K = self.shape
        if K != chain.shape[0]:
            raise Exception("self.shape[1] must be equal to chaine.shape[0].")
        return Chain(ks_patterns=self.ks_patterns + chain.ks_patterns)

    def __len__(self):
        """"
        Return length of ``self``.
        """
        return len(self.ks_patterns)
