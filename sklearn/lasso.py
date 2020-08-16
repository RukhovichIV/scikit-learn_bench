# Copyright (C) 2020 Intel Corporation
#
# SPDX-License-Identifier: MIT

import argparse
from bench import (
    parse_args, measure_function_time, load_data, print_output, rmse_score
)
from sklearn.linear_model import Lasso

parser = argparse.ArgumentParser(description='scikit-learn lasso regression '
                                             'benchmark')
parser.add_argument('--no-fit-intercept', dest='fit_intercept', default=False,
                    action='store_false',
                    help="Don't fit intercept (assume data already centered)")
parser.add_argument('--alpha', dest='alpha', type=float, default=1.0,
                    help='Regularization parameter')
parser.add_argument('--maxiter', type=int, default=1000,
                    help='Maximum iterations for the iterative solver')
parser.add_argument('--tol', type=float, default=0.0,
                    help='Tolerance for solver.')
params = parse_args(parser)

# Load data
X_train, X_test, y_train, y_test = load_data(params)

# Create our regression object
regr = Lasso(fit_intercept=params.fit_intercept, alpha=params.alpha,
             tol=params.tol, max_iter=params.maxiter, copy_X=False)

columns = ('batch', 'arch', 'prefix', 'function', 'threads', 'dtype', 'size',
           'time')

# Time fit
fit_time, _ = measure_function_time(regr.fit, X_train, y_train, params=params)

# Time predict
predict_time, pred_train = measure_function_time(
    regr.predict, X_train, params=params)

train_rmse = rmse_score(pred_train, y_train)
pred_test = regr.predict(X_test)
test_rmse = rmse_score(pred_test, y_test)

print_output(library='sklearn', algorithm='lasso',
             stages=['training', 'prediction'], columns=columns,
             params=params, functions=['Lasso.fit', 'Lasso.predict'],
             times=[fit_time, predict_time], accuracy_type='rmse',
             accuracies=[train_rmse, test_rmse], data=[X_train, X_test],
             alg_instance=regr)
