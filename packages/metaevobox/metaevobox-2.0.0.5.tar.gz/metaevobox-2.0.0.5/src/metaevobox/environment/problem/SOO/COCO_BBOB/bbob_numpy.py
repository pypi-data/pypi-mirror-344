from ....problem.basic_problem import Basic_Problem
import numpy as np


class BBOB_Numpy_Problem(Basic_Problem):
    """
    # Introduction
    BBOB-Surrogate investigates the integration of surrogate modeling techniques into MetaBBO , enabling data-driven approximation of expensive objective functions while maintaining optimization fidelity.
    # Original paper
    "[Surrogate Learning in Meta-Black-Box Optimization: A Preliminary Study](https://arxiv.org/abs/2503.18060)." arXiv preprint arXiv:2503.18060 (2025).
    # Official Implementation
    [BBOB-Surrogate](https://github.com/GMC-DRL/Surr-RLDE)
    # License
    None
    # Problem Suite Composition
    BBOB-Surrogate contains a total of 72 optimization problems, corresponding to three dimensions (2, 5, 10), each dimension contains 24 problems. Each problem consists of a trained KAN or MLP network, which is used to fit 24 black box functions in the COCO-BBOB benchmark. The network here is a surrogate model of the original function.
    # Args:
    - dim (int): Dimensionality of the problem.
    - shift (np.ndarray): Shift vector applied to the input space.
    - rotate (np.ndarray): Rotation matrix applied to the input space.
    - bias (float): Bias added to the objective function value.
    - lb (float or np.ndarray): Lower bound(s) of the search space.
    - ub (float or np.ndarray): Upper bound(s) of the search space.
    # Attributes:
    - dim (int): Problem dimensionality.
    - shift (np.ndarray): Shift vector.
    - rotate (np.ndarray): Rotation matrix.
    - bias (float): Objective function bias.
    - lb (float or np.ndarray): Lower bound(s) of the search space.
    - ub (float or np.ndarray): Upper bound(s) of the search space.
    - FES (int): Function evaluation count.
    - opt (np.ndarray): Optimal solution (shift vector).
    - optimum (float): Objective value at the optimal solution.
    # Methods:
    - get_optimal(): Returns the optimal solution (shift vector).
    - func(x): Abstract method to evaluate the objective function at input `x`. Must be implemented by subclasses.
    # Raises:
    - NotImplementedError: If `func` is not implemented in a subclass.
    """
    
    def __init__(self, dim, shift, rotate, bias, lb, ub):
        self.dim = dim
        self.shift = shift
        self.rotate = rotate
        self.bias = bias
        self.lb = lb
        self.ub = ub
        self.FES = 0
        self.opt = self.shift
        # self.optimum = self.eval(self.get_optimal())
        self.optimum = self.func(self.get_optimal().reshape(1, -1))[0]

    def get_optimal(self):
        return self.opt

    def func(self, x):
        raise NotImplementedError

class NoisyProblem:
    def noisy(self, ftrue):
        raise NotImplementedError

    def eval(self, x):
        ftrue = super().eval(x)
        return self.noisy(ftrue)

    def boundaryHandling(self, x):
        return 100. * pen_func(x, self.ub)

class GaussNoisyProblem(BBOB_Numpy_Problem):
    """
    Attribute 'gause_beta' need to be defined in subclass.
    """

    def noisy(self, ftrue):
        if not isinstance(ftrue, np.ndarray):
            ftrue = np.array(ftrue)
        bias = self.optimum
        ftrue_unbiased = ftrue - bias
        fnoisy_unbiased = ftrue_unbiased * np.exp(self.gauss_beta * np.random.randn(*ftrue_unbiased.shape))
        return np.where(ftrue_unbiased >= 1e-8, fnoisy_unbiased + bias + 1.01 * 1e-8, ftrue)

class UniformNoisyProblem(NoisyProblem):
    """
    Attributes 'uniform_alpha' and 'uniform_beta' need to be defined in subclass.
    """

    def noisy(self, ftrue):
        if not isinstance(ftrue, np.ndarray):
            ftrue = np.array(ftrue)
        bias = self.optimum
        ftrue_unbiased = ftrue - bias
        fnoisy_unbiased = ftrue_unbiased * (np.random.rand(*ftrue_unbiased.shape) ** self.uniform_beta) * \
                          np.maximum(1., (1e9 / (ftrue_unbiased + 1e-99)) ** (
                                      self.uniform_alpha * (0.49 + 1. / self.dim) * np.random.rand(
                                  *ftrue_unbiased.shape)))
        return np.where(ftrue_unbiased >= 1e-8, fnoisy_unbiased + bias + 1.01 * 1e-8, ftrue)

class CauchyNoisyProblem(NoisyProblem):
    """
    Attributes 'cauchy_alpha' and 'cauchy_p' need to be defined in subclass.
    """

    def noisy(self, ftrue):
        if not isinstance(ftrue, np.ndarray):
            ftrue = np.array(ftrue)
        bias = self.optimum
        ftrue_unbiased = ftrue - bias
        fnoisy_unbiased = ftrue_unbiased + self.cauchy_alpha * np.maximum(0.,
                                                                          1e3 + (np.random.rand(
                                                                              *ftrue_unbiased.shape) < self.cauchy_p) * np.random.randn(
                                                                              *ftrue_unbiased.shape) / (np.abs(
                                                                              np.random.randn(
                                                                                  *ftrue_unbiased.shape)) + 1e-199))
        return np.where(ftrue_unbiased >= 1e-8, fnoisy_unbiased + bias + 1.01 * 1e-8, ftrue)

class _Sphere(BBOB_Numpy_Problem):
    """
    Abstract Sphere
    """
    def __init__(self, dim, shift, rotate, bias, lb, ub):
        super().__init__(dim, shift, rotate, bias, lb, ub)

    def func(self, x):
        self.FES += x.shape[0]
        z = sr_func(x, self.shift, self.rotate)
        return np.sum(z ** 2, axis=-1) + self.bias + self.boundaryHandling(x)

def sr_func(x, Os, Mr):  # shift and rotate
    y = x[:, :Os.shape[-1]] - Os
    return np.matmul(Mr, y.transpose()).transpose()


def rotate_gen(dim):  # Generate a rotate matrix
    random_state = np.random
    H = np.eye(dim)
    D = np.ones((dim,))
    for n in range(1, dim):
        mat = np.eye(dim)
        x = random_state.normal(size=(dim - n + 1,))
        D[n - 1] = np.sign(x[0])
        x[0] -= D[n - 1] * np.sqrt((x * x).sum())
        # Householder transformation
        Hx = (np.eye(dim - n + 1) - 2. * np.outer(x, x) / (x * x).sum())
        mat[n - 1:, n - 1:] = Hx
        H = np.dot(H, mat)
    # Fix the last sign such that the determinant is 1
    D[-1] = (-1) ** (1 - (dim % 2)) * D.prod()
    # Equivalent to np.dot(np.diag(D), H) but faster, apparently
    H = (D * H.T).T
    return H

def osc_transform(x):
    """
    Implementing the oscillating transformation on objective values or/and decision values.

    :param x: If x represents objective values, x is a 1-D array in shape [NP] if problem is single objective,
              or a 2-D array in shape [NP, number_of_objectives] if multi-objective.
              If x represents decision values, x is a 2-D array in shape [NP, dim].
    :return: The array after transformation in the shape of x.
    """
    y = x.copy()
    idx = (x > 0.)
    y[idx] = np.log(x[idx]) / 0.1
    y[idx] = np.exp(y[idx] + 0.49 * (np.sin(y[idx]) + np.sin(0.79 * y[idx]))) ** 0.1
    idx = (x < 0.)
    y[idx] = np.log(-x[idx]) / 0.1
    y[idx] = -np.exp(y[idx] + 0.49 * (np.sin(0.55 * y[idx]) + np.sin(0.31 * y[idx]))) ** 0.1
    return y


def asy_transform(x, beta):
    """
    Implementing the asymmetric transformation on decision values.

    :param x: Decision values in shape [NP, dim].
    :param beta: beta factor.
    :return: The array after transformation in the shape of x.
    """
    NP, dim = x.shape
    idx = (x > 0.)
    y = x.copy()
    y[idx] = y[idx] ** (1. + beta * np.linspace(0, 1, dim).reshape(1, -1).repeat(repeats=NP, axis=0)[idx] * np.sqrt(y[idx]))
    return y


def pen_func(x, ub):
    """
    Implementing the penalty function on decision values.

    :param x: Decision values in shape [NP, dim].
    :param ub: the upper-bound as a scalar.
    :return: Penalty values in shape [NP].
    """
    return np.sum(np.maximum(0., np.abs(x) - ub) ** 2, axis=-1)

class F1(_Sphere):
    def boundaryHandling(self, x):
        return 0.

    def __str__(self):
        return 'Sphere'

class F101(GaussNoisyProblem, _Sphere):
    gauss_beta = 0.01
    def __str__(self):
        return 'Sphere_moderate_gauss'

class F102(UniformNoisyProblem, _Sphere):
    uniform_alpha = 0.01
    uniform_beta = 0.01
    def __str__(self):
        return 'Sphere_moderate_uniform'

class F103(CauchyNoisyProblem, _Sphere):
    cauchy_alpha = 0.01
    cauchy_p = 0.05
    def __str__(self):
        return 'Sphere_moderate_cauchy'

class F107(GaussNoisyProblem, _Sphere):
    gauss_beta = 1.
    def __str__(self):
        return 'Sphere_gauss'

class F108(UniformNoisyProblem, _Sphere):
    uniform_alpha = 1.
    uniform_beta = 1.
    def __str__(self):
        return 'Sphere_uniform'

class F109(CauchyNoisyProblem, _Sphere):
    cauchy_alpha = 1.
    cauchy_p = 0.2
    def __str__(self):
        return 'Sphere_cauchy'

class F2(BBOB_Numpy_Problem):
    """
    Ellipsoidal
    """
    def __init__(self, dim, shift, rotate, bias, lb, ub):
        super().__init__(dim, shift, rotate, bias, lb, ub)

    def __str__(self):
        return 'Ellipsoidal'

    def func(self, x):
        self.FES += x.shape[0]
        nx = self.dim
        z = sr_func(x, self.shift, self.rotate)
        z = osc_transform(z)
        i = np.arange(nx)
        return np.sum(np.power(10, 6 * i / (nx - 1)) * (z ** 2), -1) + self.bias

class F3(BBOB_Numpy_Problem):
    """
    Rastrigin
    """
    def __init__(self, dim, shift, rotate, bias, lb, ub):
        self.scales = (10. ** 0.5) ** np.linspace(0, 1, dim)
        super().__init__(dim, shift, rotate, bias, lb, ub)

    def __str__(self):
        return 'Rastrigin'

    def func(self, x):
        self.FES += x.shape[0]
        z = self.scales * asy_transform(osc_transform(sr_func(x, self.shift, self.rotate)), beta=0.2)
        return 10. * (self.dim - np.sum(np.cos(2. * np.pi * z), axis=-1)) + np.sum(z ** 2, axis=-1) + self.bias

class F4(BBOB_Numpy_Problem):
    """
    Buche_Rastrigin
    """
    def __init__(self, dim, shift, rotate, bias, lb, ub):
        shift[::2] = np.abs(shift[::2])
        self.scales = ((10. ** 0.5) ** np.linspace(0, 1, dim))
        BBOB_Numpy_Problem.__init__(self, dim, shift, rotate, bias, lb, ub)

    def __str__(self):
        return 'Buche_Rastrigin'

    def func(self, x):
        self.FES += x.shape[0]
        z = sr_func(x, self.shift, self.rotate)
        z = osc_transform(z)
        even = z[:, ::2]
        even[even > 0.] *= 10.
        z *= self.scales
        return 10 * (self.dim - np.sum(np.cos(2 * np.pi * z), axis=-1)) + np.sum(z ** 2, axis=-1) + 100 * pen_func(x, self.ub) + self.bias

class F5(BBOB_Numpy_Problem):
    """
    Linear_Slope
    """
    def __init__(self, dim, shift, rotate, bias, lb, ub):
        shift = np.sign(shift)
        shift[shift == 0.] = np.random.choice([-1., 1.], size=(shift == 0.).sum())
        shift = shift * ub
        BBOB_Numpy_Problem.__init__(self, dim, shift, rotate, bias, lb, ub)

    def __str__(self):
        return 'Linear_Slope'

    def func(self, x):
        self.FES += x.shape[0]
        z = x.copy()
        exceed_bound = (x * self.shift) > (self.ub ** 2)
        z[exceed_bound] = np.sign(z[exceed_bound]) * self.ub  # clamp back into the domain
        s = np.sign(self.shift) * (10 ** np.linspace(0, 1, self.dim))
        return np.sum(self.ub * np.abs(s) - z * s, axis=-1) + self.bias

class F6(BBOB_Numpy_Problem):
    """
    Attractive_Sector
    """
    def __init__(self, dim, shift, rotate, bias, lb, ub):
        scales = (10. ** 0.5) ** np.linspace(0, 1, dim)
        rotate = np.matmul(np.matmul(rotate_gen(dim), np.diag(scales)), rotate)
        BBOB_Numpy_Problem.__init__(self, dim, shift, rotate, bias, lb, ub)

    def __str__(self):
        return 'Attractive_Sector'

    def func(self, x):
        self.FES += x.shape[0]
        z = sr_func(x, self.shift, self.rotate)
        idx = (z * self.get_optimal()) > 0.
        z[idx] *= 100.
        return osc_transform(np.sum(z ** 2, -1)) ** 0.9 + self.bias

class _Step_Ellipsoidal(BBOB_Numpy_Problem):
    """
    Abstract Step_Ellipsoidal
    """
    def __init__(self, dim, shift, rotate, bias, lb, ub):
        scales = (10. ** 0.5) ** np.linspace(0, 1, dim)
        rotate = np.matmul(np.diag(scales), rotate)
        self.Q_rotate = rotate_gen(dim)
        BBOB_Numpy_Problem.__init__(self, dim, shift, rotate, bias, lb, ub)

    def func(self, x):
        self.FES += x.shape[0]
        z_hat = sr_func(x, self.shift, self.rotate)
        z = np.matmul(np.where(np.abs(z_hat) > 0.5, np.floor(0.5 + z_hat), np.floor(0.5 + 10. * z_hat) / 10.), self.Q_rotate.T)
        return 0.1 * np.maximum(np.abs(z_hat[:, 0]) / 1e4, np.sum(100 ** np.linspace(0, 1, self.dim) * (z ** 2), axis=-1)) + \
               self.boundaryHandling(x) + self.bias

class F7(_Step_Ellipsoidal):
    def boundaryHandling(self, x):
        return pen_func(x, self.ub)

    def __str__(self):
        return 'Step_Ellipsoidal'

class F113(GaussNoisyProblem, _Step_Ellipsoidal):
    gauss_beta = 1.
    def __str__(self):
        return 'Step_Ellipsoidal_gauss'

class F114(UniformNoisyProblem, _Step_Ellipsoidal):
    uniform_alpha = 1.
    uniform_beta = 1.
    def __str__(self):
        return 'Step_Ellipsoidal_uniform'

class F115(CauchyNoisyProblem, _Step_Ellipsoidal):
    cauchy_alpha = 1.
    cauchy_p = 0.2
    def __str__(self):
        return 'Step_Ellipsoidal_cauchy'

class _Rosenbrock(BBOB_Numpy_Problem):
    """
    Abstract Rosenbrock_original
    """
    def __init__(self, dim, shift, rotate, bias, lb, ub):
        shift *= 0.75  # range_of_shift=0.8*0.75*ub=0.6*ub
        rotate = np.eye(dim)
        BBOB_Numpy_Problem.__init__(self, dim, shift, rotate, bias, lb, ub)

    def func(self, x):
        self.FES += x.shape[0]
        z = max(1., self.dim ** 0.5 / 8.) * sr_func(x, self.shift, self.rotate) + 1
        return np.sum(100 * (z[:, :-1] ** 2 - z[:, 1:]) ** 2 + (z[:, :-1] - 1) ** 2, axis=-1) + self.bias + self.boundaryHandling(x)

class F8(_Rosenbrock):
    def boundaryHandling(self, x):
        return 0.

    def __str__(self):
        return 'Rosenbrock_original'

class F104(GaussNoisyProblem, _Rosenbrock):
    gauss_beta = 0.01
    def __str__(self):
        return 'Rosenbrock_moderate_gauss'

class F105(UniformNoisyProblem, _Rosenbrock):
    uniform_alpha = 0.01
    uniform_beta = 0.01
    def __str__(self):
        return 'Rosenbrock_moderate_uniform'

class F106(CauchyNoisyProblem, _Rosenbrock):
    cauchy_alpha = 0.01
    cauchy_p = 0.05
    def __str__(self):
        return 'Rosenbrock_moderate_cauchy'

class F110(GaussNoisyProblem, _Rosenbrock):
    gauss_beta = 1.
    def __str__(self):
        return 'Rosenbrock_gauss'

class F111(UniformNoisyProblem, _Rosenbrock):
    uniform_alpha = 1.
    uniform_beta = 1.
    def __str__(self):
        return 'Rosenbrock_uniform'

class F112(CauchyNoisyProblem, _Rosenbrock):
    cauchy_alpha = 1.
    cauchy_p = 0.2
    def __str__(self):
        return 'Rosenbrock_cauchy'

class F9(BBOB_Numpy_Problem):
    """
    Rosenbrock_rotated
    """
    def __init__(self, dim, shift, rotate, bias, lb, ub):
        scale = max(1., dim ** 0.5 / 8.)
        self.linearTF = scale * rotate
        shift = np.matmul(0.5 * np.ones(dim), self.linearTF) / (scale ** 2)
        BBOB_Numpy_Problem.__init__(self, dim, shift, rotate, bias, lb, ub)

    def __str__(self):
        return 'Rosenbrock_rotated'

    def func(self, x):
        self.FES += x.shape[0]
        z = np.matmul(x, self.linearTF.T) + 0.5
        return np.sum(100 * (z[:, :-1] ** 2 - z[:, 1:]) ** 2 + (z[:, :-1] - 1) ** 2, axis=-1) + self.bias

class _Ellipsoidal(BBOB_Numpy_Problem):
    """
    Abstract Ellipsoidal
    """
    condition = None

    def __init__(self, dim, shift, rotate, bias, lb, ub):
        BBOB_Numpy_Problem.__init__(self, dim, shift, rotate, bias, lb, ub)

    def func(self, x):
        self.FES += x.shape[0]
        nx = self.dim
        z = sr_func(x, self.shift, self.rotate)
        z = osc_transform(z)
        i = np.arange(nx)
        return np.sum((self.condition ** (i / (nx - 1))) * (z ** 2), -1) + self.bias + self.boundaryHandling(x)

class F10(_Ellipsoidal):
    condition = 1e6
    def boundaryHandling(self, x):
        return 0.

    def __str__(self):
        return 'Ellipsoidal_high_cond'

class F116(GaussNoisyProblem, _Ellipsoidal):
    condition = 1e4
    gauss_beta = 1.
    def __str__(self):
        return 'Ellipsoidal_gauss'

class F117(UniformNoisyProblem, _Ellipsoidal):
    condition = 1e4
    uniform_alpha = 1.
    uniform_beta = 1.
    def __str__(self):
        return 'Ellipsoidal_uniform'

class F118(CauchyNoisyProblem, _Ellipsoidal):
    condition = 1e4
    cauchy_alpha = 1.
    cauchy_p = 0.2
    def __str__(self):
        return 'Ellipsoidal_cauchy'

class F11(BBOB_Numpy_Problem):
    """
    Discus
    """
    def __init__(self, dim, shift, rotate, bias, lb, ub):
        BBOB_Numpy_Problem.__init__(self, dim, shift, rotate, bias, lb, ub)

    def __str__(self):
        return 'Discus'

    def func(self, x):
        self.FES += x.shape[0]
        z = sr_func(x, self.shift, self.rotate)
        z = osc_transform(z)
        return np.power(10, 6) * (z[:, 0] ** 2) + np.sum(z[:, 1:] ** 2, -1) + self.bias

class F12(BBOB_Numpy_Problem):
    """
    Bent_Cigar
    """
    beta = 0.5

    def __init__(self, dim, shift, rotate, bias, lb, ub):
        BBOB_Numpy_Problem.__init__(self, dim, shift, rotate, bias, lb, ub)

    def __str__(self):
        return 'Bent_Cigar'

    def func(self, x):
        self.FES += x.shape[0]
        z = sr_func(x, self.shift, self.rotate)
        z = asy_transform(z, beta=self.beta)
        z = np.matmul(z, self.rotate.T)
        return z[:, 0] ** 2 + np.sum(np.power(10, 6) * (z[:, 1:] ** 2), -1) + self.bias

class F13(BBOB_Numpy_Problem):
    """
    Sharp_Ridge
    """
    def __init__(self, dim, shift, rotate, bias, lb, ub):
        scales = (10 ** 0.5) ** np.linspace(0, 1, dim)
        rotate = np.matmul(np.matmul(rotate_gen(dim), np.diag(scales)), rotate)
        BBOB_Numpy_Problem.__init__(self, dim, shift, rotate, bias, lb, ub)

    def __str__(self):
        return 'Sharp_Ridge'

    def func(self, x):
        self.FES += x.shape[0]
        z = sr_func(x, self.shift, self.rotate)
        return z[:, 0] ** 2. + 100. * np.sqrt(np.sum(z[:, 1:] ** 2., axis=-1)) + self.bias

class _Dif_powers(BBOB_Numpy_Problem):
    """
    Abstract Different_Powers
    """
    def __init__(self, dim, shift, rotate, bias, lb, ub):
        BBOB_Numpy_Problem.__init__(self, dim, shift, rotate, bias, lb, ub)

    def func(self, x):
        self.FES += x.shape[0]
        z = sr_func(x, self.shift, self.rotate)
        i = np.arange(self.dim)
        return np.power(np.sum(np.power(np.fabs(z), 2 + 4 * i / max(1, self.dim - 1)), -1), 0.5) + self.bias + self.boundaryHandling(x)

class F14(_Dif_powers):
    def boundaryHandling(self, x):
        return 0.

    def __str__(self):
        return 'Different_Powers'

class F119(GaussNoisyProblem, _Dif_powers):
    gauss_beta = 1.
    def __str__(self):
        return 'Different_Powers_gauss'

class F120(UniformNoisyProblem, _Dif_powers):
    uniform_alpha = 1.
    uniform_beta = 1.
    def __str__(self):
        return 'Different_Powers_uniform'

class F121(CauchyNoisyProblem, _Dif_powers):
    cauchy_alpha = 1.
    cauchy_p = 0.2
    def __str__(self):
        return 'Different_Powers_cauchy'

class F15(BBOB_Numpy_Problem):
    """
    Rastrigin_F15
    """
    def __init__(self, dim, shift, rotate, bias, lb, ub):
        scales = (10. ** 0.5) ** np.linspace(0, 1, dim)
        self.linearTF = np.matmul(np.matmul(rotate, np.diag(scales)), rotate_gen(dim))
        BBOB_Numpy_Problem.__init__(self, dim, shift, rotate, bias, lb, ub)

    def __str__(self):
        return 'Rastrigin_F15'

    def func(self, x):
        self.FES += x.shape[0]
        z = sr_func(x, self.shift, self.rotate)
        z = asy_transform(osc_transform(z), beta=0.2)
        z = np.matmul(z, self.linearTF.T)
        return 10. * (self.dim - np.sum(np.cos(2. * np.pi * z), axis=-1)) + np.sum(z ** 2, axis=-1) + self.bias

class F16(BBOB_Numpy_Problem):
    """
    Weierstrass
    """
    def __init__(self, dim, shift, rotate, bias, lb, ub):
        scales = (0.01 ** 0.5) ** np.linspace(0, 1, dim)
        self.linearTF = np.matmul(np.matmul(rotate, np.diag(scales)), rotate_gen(dim))
        self.aK = 0.5 ** np.arange(12)
        self.bK = 3.0 ** np.arange(12)
        self.f0 = np.sum(self.aK * np.cos(np.pi * self.bK))
        BBOB_Numpy_Problem.__init__(self, dim, shift, rotate, bias, lb, ub)

    def __str__(self):
        return 'Weierstrass'

    def func(self, x):
        self.FES += x.shape[0]
        z = sr_func(x, self.shift, self.rotate)
        z = np.matmul(osc_transform(z), self.linearTF.T)
        return 10 * np.power(np.mean(np.sum(self.aK * np.cos(np.matmul(2 * np.pi * (z[:, :, None] + 0.5), self.bK[None, :])), axis=-1), axis=-1) - self.f0, 3) + \
               10 / self.dim * pen_func(x, self.ub) + self.bias

class _Scaffer(BBOB_Numpy_Problem):
    """
    Abstract Scaffers
    """
    condition = None  # need to be defined in subclass

    def __init__(self, dim, shift, rotate, bias, lb, ub):
        scales = (self.condition ** 0.5) ** np.linspace(0, 1, dim)
        self.linearTF = np.matmul(np.diag(scales), rotate_gen(dim))
        BBOB_Numpy_Problem.__init__(self, dim, shift, rotate, bias, lb, ub)

    def func(self, x):
        self.FES += x.shape[0]
        z = sr_func(x, self.shift, self.rotate)
        z = np.matmul(asy_transform(z, beta=0.5), self.linearTF.T)
        s = np.sqrt(z[:, :-1] ** 2 + z[:, 1:] ** 2)
        return np.power(1 / (self.dim - 1) * np.sum(np.sqrt(s) * (np.power(np.sin(50 * np.power(s, 0.2)), 2) + 1), axis=-1), 2) + \
               self.boundaryHandling(x) + self.bias

class F17(_Scaffer):
    condition = 10.
    def boundaryHandling(self, x):
        return 10 * pen_func(x, self.ub)

    def __str__(self):
        return 'Schaffers'

class F18(_Scaffer):
    condition = 1000.
    def boundaryHandling(self, x):
        return 10 * pen_func(x, self.ub)

    def __str__(self):
        return 'Schaffers_high_cond'

class F122(GaussNoisyProblem, _Scaffer):
    condition = 10.
    gauss_beta = 1.
    def __str__(self):
        return 'Schaffers_gauss'

class F123(UniformNoisyProblem, _Scaffer):
    condition = 10.
    uniform_alpha = 1.
    uniform_beta = 1.
    def __str__(self):
        return 'Schaffers_uniform'

class F124(CauchyNoisyProblem, _Scaffer):
    condition = 10.
    cauchy_alpha = 1.
    cauchy_p = 0.2
    def __str__(self):
        return 'Schaffers_cauchy'

class _Composite_Grie_rosen(BBOB_Numpy_Problem):
    """
    Abstract Composite_Grie_rosen
    """
    factor = None

    def __init__(self, dim, shift, rotate, bias, lb, ub):
        scale = max(1., dim ** 0.5 / 8.)
        self.linearTF = scale * rotate
        shift = np.matmul(0.5 * np.ones(dim) / (scale ** 2.), self.linearTF)
        BBOB_Numpy_Problem.__init__(self, dim, shift, rotate, bias, lb, ub)

    def func(self, x):
        self.FES += x.shape[0]
        z = np.matmul(x, self.linearTF.T) + 0.5
        s = 100. * (z[:, :-1] ** 2 - z[:, 1:]) ** 2 + (1. - z[:, :-1]) ** 2
        return self.factor + self.factor * np.sum(s / 4000. - np.cos(s), axis=-1) / (self.dim - 1.) + self.bias + self.boundaryHandling(x)

class F19(_Composite_Grie_rosen):
    factor = 10.
    def boundaryHandling(self, x):
        return 0.

    def __str__(self):
        return 'Composite_Grie_rosen'

class F125(GaussNoisyProblem, _Composite_Grie_rosen):
    factor = 1.
    gauss_beta = 1.
    def __str__(self):
        return 'Composite_Grie_rosen_gauss'

class F126(UniformNoisyProblem, _Composite_Grie_rosen):
    factor = 1.
    uniform_alpha = 1.
    uniform_beta = 1.
    def __str__(self):
        return 'Composite_Grie_rosen_uniform'

class F127(CauchyNoisyProblem, _Composite_Grie_rosen):
    factor = 1.
    cauchy_alpha = 1.
    cauchy_p = 0.2
    def __str__(self):
        return 'Composite_Grie_rosen_cauchy'

class F20(BBOB_Numpy_Problem):
    """
    Schwefel
    """
    def __init__(self, dim, shift, rotate, bias, lb, ub):
        shift = 0.5 * 4.2096874633 * np.random.choice([-1., 1.], size=dim)
        BBOB_Numpy_Problem.__init__(self, dim, shift, rotate, bias, lb, ub)

    def __str__(self):
        return 'Schwefel'

    def func(self, x):
        self.FES += x.shape[0]
        tmp = 2 * np.abs(self.shift)
        scales = (10 ** 0.5) ** np.linspace(0, 1, self.dim)
        z = 2 * np.sign(self.shift) * x
        z[:, 1:] += 0.25 * (z[:, :-1] - tmp[:-1])
        z = 100. * (scales * (z - tmp) + tmp)
        b = 4.189828872724339
        return b - 0.01 * np.mean(z * np.sin(np.sqrt(np.abs(z))), axis=-1) + 100 * pen_func(z / 100, self.ub) + self.bias

class _Gallagher(BBOB_Numpy_Problem):
    """
    Abstract Gallagher
    """
    n_peaks = None

    def __init__(self, dim, shift, rotate, bias, lb, ub):
        # problem param config
        if self.n_peaks == 101:   # F21
            opt_shrink = 1.       # shrink of global & local optima
            global_opt_alpha = 1e3
        elif self.n_peaks == 21:  # F22
            opt_shrink = 0.98     # shrink of global & local optima
            global_opt_alpha = 1e6
        else:
            raise ValueError(f'{self.n_peaks} peaks Gallagher is not supported yet.')

        # generate global & local optima y[i]
        self.y = opt_shrink * (np.random.rand(self.n_peaks, dim) * (ub - lb) + lb)  # [n_peaks, dim]
        self.y[0] = shift * opt_shrink  # the global optimum
        shift = self.y[0]

        # generate the matrix C[i]
        sqrt_alpha = 1000 ** np.random.permutation(np.linspace(0, 1, self.n_peaks - 1))
        sqrt_alpha = np.insert(sqrt_alpha, obj=0, values=np.sqrt(global_opt_alpha))
        self.C = [np.random.permutation(sqrt_alpha[i] ** np.linspace(-0.5, 0.5, dim)) for i in range(self.n_peaks)]
        self.C = np.vstack(self.C)  # [n_peaks, dim]

        # generate the weight w[i]
        self.w = np.insert(np.linspace(1.1, 9.1, self.n_peaks - 1), 0, 10.)  # [n_peaks]

        BBOB_Numpy_Problem.__init__(self, dim, shift, rotate, bias, lb, ub)

    def func(self, x):
        self.FES += x.shape[0]
        z = np.matmul(np.expand_dims(x, axis=1).repeat(self.n_peaks, axis=1) - self.y, self.rotate.T)  # [NP, n_peaks, dim]
        z = np.max(self.w * np.exp((-0.5 / self.dim) * np.sum(self.C * (z ** 2), axis=-1)), axis=-1)  # [NP]
        return osc_transform(10 - z) ** 2 + self.bias + self.boundaryHandling(x)

class F21(_Gallagher):
    n_peaks = 101
    def boundaryHandling(self, x):
        return pen_func(x, self.ub)

    def __str__(self):
        return 'Gallagher_101Peaks'

class F22(_Gallagher):
    n_peaks = 21
    def boundaryHandling(self, x):
        return pen_func(x, self.ub)

    def __str__(self):
        return 'Gallagher_21Peaks'

class F128(GaussNoisyProblem, _Gallagher):
    n_peaks = 101
    gauss_beta = 1.
    def __str__(self):
        return 'Gallagher_101Peaks_gauss'


class F129(UniformNoisyProblem, _Gallagher):
    n_peaks = 101
    uniform_alpha = 1.
    uniform_beta = 1.
    def __str__(self):
        return 'Gallagher_101Peaks_uniform'


class F130(CauchyNoisyProblem, _Gallagher):
    n_peaks = 101
    cauchy_alpha = 1.
    cauchy_p = 0.2
    def __str__(self):
        return 'Gallagher_101Peaks_cauchy'


class F23(BBOB_Numpy_Problem):
    """
    Katsuura
    """
    def __init__(self, dim, shift, rotate, bias, lb, ub):
        scales = (100. ** 0.5) ** np.linspace(0, 1, dim)
        rotate = np.matmul(np.matmul(rotate_gen(dim), np.diag(scales)), rotate)
        BBOB_Numpy_Problem.__init__(self, dim, shift, rotate, bias, lb, ub)

    def __str__(self):
        return 'Katsuura'

    def func(self, x):
        self.FES += x.shape[0]
        z = sr_func(x, self.shift, self.rotate)
        tmp3 = np.power(self.dim, 1.2)
        tmp1 = np.repeat(np.power(np.ones((1, 32)) * 2, np.arange(1, 33)), x.shape[0], 0)
        res = np.ones(x.shape[0])
        for i in range(self.dim):
            tmp2 = tmp1 * np.repeat(z[:, i, None], 32, 1)
            temp = np.sum(np.fabs(tmp2 - np.floor(tmp2 + 0.5)) / tmp1, -1)
            res *= np.power(1 + (i + 1) * temp, 10 / tmp3)
        tmp = 10 / self.dim / self.dim
        return res * tmp - tmp + pen_func(x, self.ub) + self.bias


class F24(BBOB_Numpy_Problem):
    """
    Lunacek_bi_Rastrigin
    """
    def __init__(self, dim, shift, rotate, bias, lb, ub):
        self.mu0 = 2.5 / 5 * ub
        shift = np.random.choice([-1., 1.], size=dim) * self.mu0 / 2
        scales = (100 ** 0.5) ** np.linspace(0, 1, dim)
        rotate = np.matmul(np.matmul(rotate_gen(dim), np.diag(scales)), rotate)
        super().__init__(dim, shift, rotate, bias, lb, ub)

    def __str__(self):
        return 'Lunacek_bi_Rastrigin'

    def func(self, x):
        self.FES += x.shape[0]
        x_hat = 2. * np.sign(self.shift) * x
        z = np.matmul(x_hat - self.mu0, self.rotate.T)
        s = 1. - 1. / (2. * np.sqrt(self.dim + 20.) - 8.2)
        mu1 = -np.sqrt((self.mu0 ** 2 - 1) / s)
        return np.minimum(np.sum((x_hat - self.mu0) ** 2., axis=-1), self.dim + s * np.sum((x_hat - mu1) ** 2., axis=-1)) + \
               10. * (self.dim - np.sum(np.cos(2. * np.pi * z), axis=-1)) + 1e4 * pen_func(x, self.ub) + self.bias

