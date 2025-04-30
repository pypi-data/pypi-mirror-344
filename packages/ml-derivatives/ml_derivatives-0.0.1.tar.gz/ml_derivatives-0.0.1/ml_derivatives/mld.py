import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeCV
from tqdm import tqdm
from itertools import product
import pickle
import os

PI = np.pi
NT_PER_PERIOD = 5
LOWEST_LOG_W = -3
LOWEST_LOG_alpha = -4
HIGHEST_LOG_alpha = 3
N_alphas = 25
EPS_COMPRESSION = 1e-5
NOISE_LEVELS = [0.01, 0.025, 0.05, 0.08, 0.1]
NOISE_MODES = ['a']
N_W_BAR = 50
DEG_MAX = 4
N_SAMPLES_FOR_LEARNING = 1000
TH_4_j = 0.01
TH_4_j_0 = 0.1
N_OMEGAS = 200
NT_MAX = 10001

# The basic sinusoidal and its derivatives

Bs = lambda w, t, d: np.power(w, d) * np.sin(w * t + d * PI / 2)
Bc = lambda w, t, d: np.power(w, d) * np.sin(w * t + (d + 1) * PI / 2)


def add_noise(V, level, mode='a'):
    # Add noise to a matrix V.
    # mode in {'r', 'a'} designates the additive or relative noise.
    # The data used in the package are based on learning of the 'a' mode.

    nn = np.random.randn(*V.shape) * level
    if mode.lower() == 'a':
        Vn = V + nn
    else:
        Vn = V * (1 + nn)
    return Vn


class Derivator:

    # The main class for higher order derivatives estimation
    # in the presence of noisy measurements.

    def __init__(self, window=50, w_bandwidth_est=2000, noise_level=0.05):

        # Definition of the attributes (all are preceded by self.*)
        # ------------------------------------------
        #   window: the width of the averaging window.
        #   w_max: the maximum pulsation for which reconstruction is relevant.
        #   n_omegas: the number of pulsation used in generating the learning time series
        #   nt_max: the maximum number of instance in a single processed time series.
        #   ws: the vector of n_omegas pulsations
        #   O: the index of pulsation in the 2*n_omegas+1 basis functions
        #   tl: the nt_max-dimensional time vector.
        #   w_bars: the vector of N_W_BAR pulsation used in the computation of models
        #   i_max: The maximum index in ws of a given w_bars.
        #   Ms: The dictionary (key=d) of the basis functions (2*n_omegas+1) columns
        #   n_Basis: The number of columns = 2*n_omegas+1
        #   keys_dj: list of indices (d,j)
        #   w_bandwidth_est: number of samples used to estimate the bandwidth
        #   fit_projector: prepare the projection matrices for the chosen w_bandwidth_est
        #   if fit_projector is called, one gets a dictionary of matrices  M_proj[j] such that:
        #           M_proj[j].dot(yn) is the best approximation of yn by elements of the basis
        #           representing pulsations in ws up to w_bars[j].

        self.current_dict_models = None
        self.M_proj = None
        self.window = window
        self.noise_level = noise_level
        self.w_max = 2 * PI / (NT_PER_PERIOD)
        self.n_omegas = N_OMEGAS
        self.nt_max = NT_MAX
        self.ws = np.logspace(LOWEST_LOG_W, 0, self.n_omegas) * self.w_max
        self.O = self.compute_O()
        self.tl = np.array([i for i in range(self.nt_max)])
        w_min = 10 ** LOWEST_LOG_W * self.w_max
        self.w_bars = (np.linspace(10 ** LOWEST_LOG_W, 1, N_W_BAR) ** 1.2) * self.w_max
        self.i_max = [
            min(np.sum(self.O <= w_bar), len(self.O) - 1)
            for w_bar in self.w_bars
        ]
        self.Ms = self.generate_Ms()
        self.n_Basis = self.Ms[0].shape[1]
        set_j = list(np.arange(0, N_W_BAR))
        set_d = [i for i in range(DEG_MAX + 1)]
        self.keys_dj = [k for k in product(set_d, set_j)]
        self.w_bandwidth_est = w_bandwidth_est
        self.fit_projector(w_bandwidth_est)

        self.load_appropriate_models(noise_level)

    def load_appropriate_models(self, noise_level):

        level = NOISE_LEVELS[np.argmin(abs(noise_level - np.array(NOISE_LEVELS)))]
        # Only valid in exploitation mode
        module_path = os.path.dirname(os.path.abspath(__file__))
        data_folder = os.path.join(module_path, 'data')
        try:
            file_path = os.path.join(data_folder, f'Ma_{level}_{self.window}.pkl')
            self.models = pickle.load(open(file_path, 'rb'))
        except:
            print('Impossible to load the data for the model')
            print('please check the distribution integrity!')

        return self

    def compute_O(self):
        # Computes the pulsations associated to the indices of the
        # columns of the matrices Ms[d]. used for pulsation cutting
        # when analyzing the bandwidth of a signal.
        O = np.concatenate([
            [0],
            np.hstack([np.array([self.ws[j], self.ws[j]]).T
                       for j in range(self.n_omegas)])
        ])
        return O

    def generate_M(self, d):

        # Generates a matrix representing the d-derivatives of the sin/cos columns
        # starting with ones in the first column. The columns using the increasing
        # pulsations contained in the vector of pulsation ws.
        # This is used in  generate Ms dictionary that is heavily used in what follows.

        Bsc = np.hstack([
            np.array([
                Bs(self.ws[j], self.tl, d), Bc(self.ws[j], self.tl, d)
            ]).T
            for j in range(self.n_omegas)
        ])
        Bones = np.array([1 for i in range(self.nt_max)]).reshape(-1, 1)
        if d == 0:
            M = np.hstack([Bones, Bsc])
        else:
            M = np.hstack([0 * Bones, Bsc])
        return M

    def generate_Ms(self):

        # Generates a dictionary matrices M[0],...,M[DEG_MAX] such that
        # M[0].dot(alpha) is a randomly generated signal with derivatives
        # given by M[d].dot(alpha)

        Ms = {d: self.generate_M(d) for d in range(DEG_MAX + 1)}
        return Ms

    def fit_projector(self, n):

        # This utility is only used when estimating the bandwidth of a time series
        # n is the length of the time series.
        # The resulting dictionary of matrices  M_proj[j] is such that:
        # M_proj[j].dot(yn) is the best approximation of yn by elements of the basis
        # representing pulsations in ws up to w_bars[j].
        # The reason for which this is not computed once for all is that the result depends
        # on the length of the window to be used (n) which is left to the user.

        M_inv = {j: np.linalg.pinv(self.Ms[0][:n, 0:self.i_max[j]]) for j in range(len(self.i_max))}
        M_proj = {j: self.Ms[0][0:n, 0:self.i_max[j]].dot(M_inv[j])
                  for j in range(len(self.i_max))}
        self.M_proj = M_proj
        return M_proj

    def which_j(self, yn, mute_warnings):

        # computes the bandwidth expressed as the cut-ff index j after which
        # the error does not improve. This decision is based on the threshold TH_4_j
        # with a special case handling when j=0 is already quite good, which involves
        # the threshold TH_4_j_0
        # returns j, e

        # Handle the length of the time series used as argument.
        if len(yn) > self.w_bandwidth_est:
            yn = yn[0:self.w_bandwidth_est]
        if len(yn) < self.w_bandwidth_est:
            if not mute_warnings:
                print('time series shorter than optimally needed, results might be inaccurate')
            self.fit_projector(len(yn))

        # Compute the residual of the projection for all candidate pulsation in w_bars
        e = np.array([abs(np.dot(self.M_proj[j], yn) - yn).mean()
                      for j in range(N_W_BAR)])

        # compute the threshold compared to the error when using j=0
        th = e[-1] + TH_4_j * (e[0] - e[-1])
        j = [j for j in range(len(e)) if e[j] <= th][0]

        # Handle the special case where j=0 is already too good.
        if e[0] / abs(yn).max() < TH_4_j_0:
            j = 0
        return j, e

    def generate_learning_data(self):

        # Generate the dictionary of time series and their derivatives
        # the keys are given by (d,j) where d is the derivation order
        # and j is the index in w_bars of the pulsation.
        # there will be a model for each pair (d,j).
        # The time series are normalized using the abs(Y[0,j]).max().

        coefficients = np.random.randn(len(self.O), N_SAMPLES_FOR_LEARNING)
        Y = {}
        for iw in tqdm(range(len(self.w_bars))):
            i_max = self.i_max[iw]
            for d in range(DEG_MAX + 1):
                Y[(d, iw)] = (self.Ms[d][:self.window, :i_max].dot(coefficients[0:i_max, :])).T
            den = abs(Y[(0, iw)]).max(axis=1)
            for d in range(DEG_MAX + 1):
                Y[(d, iw)] = np.diag(1 / den).dot(Y[(d, iw)])
        return Y

    def generate_a_time_series(self, nt, w_real, tau):

        # Generate a time series with its derivatives that contains nt time instants
        # and using pulsations lower than w_real with a sampling period of tau.
        # Note that nt cannot be greater than NT_MAX. If so only nt_max length
        # time series is generated.
        # The output is a list of time series such that Z[d] is the d-th derivative of Z[0]

        nt = min(nt, self.nt_max)
        coefficients = np.random.randn(self.n_Basis)
        imax = np.sum(self.O <= w_real * tau) - 1
        Z = [self.Ms[d][:nt, 0:imax].dot(coefficients[0:imax])
             for d in range(DEG_MAX + 1)]
        den = abs(Z[0]).max()
        t = np.array([i * tau for i in range(nt)])
        for d in range(DEG_MAX + 1):
            Z[d] /= (tau ** d) * den
        return t, Z

    def predict(self, y0n, model, dt):

        # Given a long time-series y0n, generates prediction based
        # on a given model (instance of the class Model) and assuming that
        # the data is sampled with a sampling period of dt.
        # Here the time series y0n is assumed to be normalized. This is why the model
        # is applied on it without any other normalization procedure.
        # Notice that the order of the derivation is included in the choice of the model
        # inside the dictionary of available models since this dictionary is indexed by
        # the pairs (d,j).

        df = pd.DataFrame(y0n, columns=['y0n'])
        X = pd.concat([df.shift(-i) for i in range(len(df))], axis=1).values[
            :-(self.window - 1), 0:self.window
            ]
        #------------------------------------------------------------
        u, s, v = model['u'], model['s'], model['v']
        M = np.dot(u, np.dot(np.diag(s), v)).T
        V = X.dot(M) / (dt ** model['d'])
        # ------------------------------------------------------------
        V = np.vstack([
            V,
            np.full((self.window - 1, self.window), np.nan)
        ])
        ypred = np.array([
            np.nanmean(np.array([V[i - sig, sig]
                                 for sig in range(min(V.shape[1], i + 1))]))
            for i in range(len(V))
        ])
        e_std = np.array([
            np.nanstd(np.array([V[i - sig, sig]
                                for sig in range(min(V.shape[1], i + 1))]))
            for i in range(len(V))
        ])
        return ypred, e_std

    def fit(self, noise_level, noise_mode, cv=2, plot=False):

        #-----------------------------------------------------
        # This utility is only used by the creator of the package to fit the
        # models that are inside the data directory.
        # NOTA: This is done for A SINGLE NOISE LEVEL and a single noise mode.
        # returns: a dictionary of model (instances of Model) indexed by (d,j)
        # -----------------------------------------------------

        Y = self.generate_learning_data()

        # create the alphas for the RidgeCV sklearn module

        alphas = np.logspace(LOWEST_LOG_alpha,
                             HIGHEST_LOG_alpha, N_alphas)

        def compress(A):

            # Perform Singular Value Decomposition (SVD) of a matrix A
            # cut the number of singular values according to EPS_COMPRESSION
            # create an instance of the Compressed class.
            # Output: the compressed model, the compression rate achieved.

            U, S, V = np.linalg.svd(A)
            # Keep only the top k singular values/components to compress

            # Initialize the binary search
            k_min, k_max, = 1, len(V)
            again = True
            while again:
                # compute the new candidate value of k
                k = int((k_min + k_max) / 2)
                Mc = np.dot(U[:, :k], np.dot(np.diag(S[:k]), V[:k, :]))
                # compare the maximum error to the 5% percentile of A
                e = abs(A - Mc).max() / (EPS_COMPRESSION + np.percentile(abs(A), 5))
                if e < EPS_COMPRESSION:
                    k_max = k
                else:
                    k_min = k
                again = k_max - k_min > 1
                nV = len(V)
                n = nV * nV
                nc = (2 * k + 1) * nV
                compression_rate = n / nc

            return U[:, :k], S[:k], V[:k, :], compression_rate

        def single_fit(d, j):

            # fit the model for a given derivation degree and a single
            # cut-off frequency, namely for a pair (d,j).
            # returns: compressed model, complete coefficients, compression rate.

            # Select the label
            y = Y[(d, j)]
            # Generate the noisy features
            noise = np.random.randn(*Y[(0, j)].shape) * noise_level
            if noise_mode.lower() == 'a':
                X = Y[(0, j)] + noise
            else:
                X = Y[(0, j)] * (1 + noise)

            # Fit the primary model via cross validation
            reg = RidgeCV(alphas=alphas, cv=cv, fit_intercept=False).fit(X, y)

            # Compress the matrix of coefficients
            u, s, v, compression_rate = compress(reg.coef_)
            model = {'u': u, 's': s, 'v': v, 'd': d, 'j': j}
            return model, reg.alpha_, compression_rate

        models = {}
        for k in tqdm(self.keys_dj):
            models[k], alpha, cr = single_fit(*k)

        return models

    def generate_models(self):

        # This utility is used by the author of the package to generate the models
        # for all possible noise_level and noise_mode
        # and save them in the specific pickle object.
        # for each noise level and each noise mode, the model is a dictionary of
        # model indexed by (d,j).

        for noise_mode in NOISE_MODES:
            for noise_level in NOISE_LEVELS:
                print(noise_mode, noise_level, self.window)
                models = self.fit(noise_level=noise_level,
                                  noise_mode=noise_mode
                                  )
                fileName = f'M{noise_mode}_{noise_level}_{self.window}.pkl'
                pickle.dump(models, open(fileName, 'wb'))

    def fit_predictor(self, y, mute_warnings=True):

        # This utility needs the attribute self.models to be instantiated
        # The call of pickle.load in the __init__ procedure of the
        # class Derivator should be successful.

        # Instantiate the self.current_dict_models: A dictionary of models indexed
        # by the derivation order d. by determining first the bandwidth index j and
        # then pick the corresponding self.models[(j,d)] for each d.

        # This is separated from the derivate facility because the same
        # bandwidth determination is valid for all the derivation order and hence
        # there is no need to repeat the operation for all of them.

        jc, e = self.which_j(y, mute_warnings)
        jc = min(jc, N_W_BAR - 1)
        self.current_dict_models = {d: self.models[(d, jc)] for d in range(DEG_MAX + 1)}

    def derivate(self, y, d, dt,
                            fit_before=False,
                            assess=False,
                            force_level=False,
                            mute_warnings=True):

        # predict the d-derivative of a time series y acquired with a sampling
        # period of dt
        # returns the estimated derivative and the standard deviation resulting
        # from the averaging process.

        if (self.current_dict_models == None) or (fit_before):
            self.fit_predictor(y, mute_warnings=mute_warnings)

        if (assess):
            yhat, e_std = self.predict(y, self.current_dict_models[d], dt)
            if d != 0:
                yhat0, e_std0 = self.predict(y, self.current_dict_models[0], dt)
            else:
                yhat0, e_std0 = 1.0 * yhat, 1.0 * e_std
            log = {
                'e_mean': np.mean(yhat0 - y),
                'e_std': np.std(yhat0 - y),
                'abs_e_mean': abs(yhat0 - y).mean(),
                'used_level': self.noise_level
            }
            if force_level:
                i_best = np.argmin(abs(log['e_std'] / abs(y).max() - np.array(NOISE_LEVELS)))
                true_level = level = NOISE_LEVELS[i_best]
                self.noise_level = true_level
                self.load_appropriate_models(true_level)
                self.fit_predictor(y, mute_warnings=mute_warnings)
                yhat, e_std = self.predict(y, self.current_dict_models[d], dt)
                log['used_level'] = self.noise_level
            return yhat, e_std, log
        else:
            yhat, e_std = self.predict(y, self.current_dict_models[d], dt)
            return yhat, e_std, None


if __name__ == "__main__":
    pass
