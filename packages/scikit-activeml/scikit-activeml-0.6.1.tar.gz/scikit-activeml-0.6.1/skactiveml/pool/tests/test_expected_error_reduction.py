import unittest
from copy import deepcopy

import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

from skactiveml.base import SkactivemlClassifier
from skactiveml.classifier import ParzenWindowClassifier, SklearnClassifier
from skactiveml.pool import MonteCarloEER, ValueOfInformationEER
from skactiveml.pool._expected_error_reduction import ExpectedErrorReduction
from skactiveml.tests.template_query_strategy import (
    TemplateSingleAnnotatorPoolQueryStrategy,
    _cmp_object_dict,
)
from skactiveml.utils import MISSING_LABEL, is_labeled


class TemplateTestExpectedErrorReduction(
    TemplateSingleAnnotatorPoolQueryStrategy
):
    def setUp(self, qs_class):
        self.Strategy = qs_class
        self.X = np.array([[1, 2], [5, 8], [8, 4], [5, 4]])
        self.X_cand = np.array([[8, 4], [5, 4], [1, 2]])
        self.candidates = np.array([2, 1, 0], dtype=int)
        self.X_eval = np.array([[2, 1], [3, 7]])
        self.y = [0, 1, 2, 1]
        self.classes = [0, 1, 2]
        self.cost_matrix = 1 - np.eye(3)
        self.clf = ParzenWindowClassifier(classes=self.classes)
        self.clf_partial = SklearnClassifier(
            GaussianNB(), classes=self.classes
        ).fit(self.X, self.y)
        self.kwargs = dict(
            X=self.X, y=self.y, candidates=self.candidates, clf=self.clf
        )

        class DummyClf(SkactivemlClassifier):
            def __init__(self, classes=None):
                super().__init__(classes=classes)

            def fit(self, X, y, sample_weight=None):
                X, y, sample_weight = self._validate_data(
                    X=X, y=y, sample_weight=sample_weight
                )
                return self

            def predict_proba(self, X):
                return np.full(
                    shape=(len(X), len(self.classes_)), fill_value=0.5
                )

        self.DummyClf = DummyClf

        query_default_params_clf = {
            "X": np.linspace(0, 1, 20).reshape(10, 2),
            "y": np.hstack([[0, 1], np.full(8, MISSING_LABEL)]),
            "clf": ParzenWindowClassifier(
                random_state=0, classes=self.classes
            ),
        }
        super().setUp(
            qs_class=qs_class,
            init_default_params={},
            query_default_params_clf=query_default_params_clf,
        )

    def test_query_param_clf(self):
        add_test_cases = [
            (SVC(), TypeError),
            (SklearnClassifier(SVC()), AttributeError),
            (SklearnClassifier(SVC(probability=True)), None),
        ]
        super().test_query_param_clf(test_cases=add_test_cases)

    def test_init_param_cost_matrix(self, test_cases=None):
        test_cases = [] if test_cases is None else test_cases
        test_cases += [
            (np.ones((2, 3)), ValueError),
            ("string", ValueError),
            (np.ones((2, 2)), ValueError),
        ]
        self._test_param("init", "cost_matrix", test_cases)

    def test_query_param_fit_clf(self, test_cases=None):
        # custom test cases are not necessary
        test_cases = [] if test_cases is None else test_cases
        test_cases += [(np.nan, TypeError), ("state", TypeError)]
        self._test_param("query", "fit_clf", test_cases)

        # check if clf remains the same for both options
        for fit_clf in [True]:
            with self.subTest(msg="Clf consistency", fit_clf=fit_clf):
                clf = deepcopy(self.query_default_params_clf["clf"])
                if not fit_clf:
                    clf.fit(
                        self.query_default_params_clf["X"],
                        self.query_default_params_clf["y"],
                    )
                query_params = deepcopy(self.query_default_params_clf)
                query_params["clf"] = deepcopy(clf)
                query_params["fit_clf"] = fit_clf

                qs = self.qs_class(**self.init_default_params)
                qs.query(**query_params)
                self.assertTrue(
                    _cmp_object_dict(
                        query_params["clf"].__dict__, clf.__dict__
                    ),
                    msg=f"Classifier changed after calling query for "
                    f"`fit_clf={fit_clf}`.",
                )

    def test_init_param_subtract_current(self):
        test_cases = [(2, TypeError), ("string", TypeError)]
        self._test_param("init", "subtract_current", test_cases)

    def test_query_param_ignore_partial_fit(self):
        test_cases = [(2, TypeError), ("string", TypeError)]
        self._test_param("query", "ignore_partial_fit", test_cases)

    def test_query(self):
        """
        qs = self.Strategy()
        # return_utilities
        L = list(qs.query(**self.kwargs, return_utilities=True))
        self.assertTrue(len(L) == 2)
        L = list(qs.query(**self.kwargs, return_utilities=False))
        self.assertTrue(len(L) == 1)

        # batch_size
        bs = 3
        best_idx = qs.query(**self.kwargs, batch_size=bs)
        self.assertEqual(bs, len(best_idx))
        """
        pass


class TestExpectedErrorReduction(unittest.TestCase):
    def test__estimate_error_for_candidate(self):
        qs = ExpectedErrorReduction(enforce_mapping=False)
        self.assertRaises(
            NotImplementedError,
            qs._estimate_error_for_candidate,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        )

    def test__concatenate_samples(self):
        X = np.array([[1], [2], [3], [4]])
        y = np.array([0, 1, MISSING_LABEL, MISSING_LABEL])
        uld_idx = np.array([2, 3])
        sample_weight = np.array([0.1, 0.2, 0.3, 0.4])
        sample_weight_cand = np.array([0.1, 0.2])
        X_eval = np.array([[5], [6], [7], [8]])
        sample_weight_eval = np.array([0.5, 0.6, 0.7, 0.8])

        qs = ExpectedErrorReduction(enforce_mapping=False)
        qs.missing_label_ = MISSING_LABEL

        cand = None
        (
            X_full,
            y_full,
            w_full,
            w_eval,
            idx_train,
            idx_cand,
            idx_eval,
        ) = qs._concatenate_samples(
            X, y, sample_weight, cand, None, X_eval, sample_weight_eval
        )

        np.testing.assert_equal(len(X_full), len(y_full))
        np.testing.assert_equal(len(X_full), len(w_full))
        np.testing.assert_equal(len(X_full), len(w_eval))

        np.testing.assert_array_equal(X, X_full[idx_train])
        np.testing.assert_array_equal(y, y_full[idx_train])
        np.testing.assert_array_equal(sample_weight, w_full[idx_train])

        np.testing.assert_array_equal(X_eval, X_full[idx_eval])
        np.testing.assert_array_equal(sample_weight_eval, w_full[idx_eval])
        np.testing.assert_array_equal(sample_weight_eval, w_eval[idx_eval])

        np.testing.assert_array_equal(X[uld_idx], X_full[idx_cand])
        np.testing.assert_array_equal(y[uld_idx], y_full[idx_cand])
        np.testing.assert_array_equal(sample_weight[uld_idx], w_full[idx_cand])

        cand = np.array([2])
        (
            X_full,
            y_full,
            w_full,
            w_eval,
            idx_train,
            idx_cand,
            idx_eval,
        ) = qs._concatenate_samples(X, y, None, cand, None, None, None)

        np.testing.assert_array_equal(X, X_full[idx_train])
        np.testing.assert_array_equal(y, y_full[idx_train])

        cand = np.array([2])
        (
            X_full,
            y_full,
            w_full,
            w_eval,
            idx_train,
            idx_cand,
            idx_eval,
        ) = qs._concatenate_samples(
            X, y, sample_weight, cand, None, X_eval, sample_weight_eval
        )

        np.testing.assert_equal(len(X_full), len(y_full))
        np.testing.assert_equal(len(X_full), len(w_full))
        np.testing.assert_equal(len(X_full), len(w_eval))

        np.testing.assert_array_equal(X, X_full[idx_train])
        np.testing.assert_array_equal(y, y_full[idx_train])
        np.testing.assert_array_equal(sample_weight, w_full[idx_train])

        np.testing.assert_array_equal(X_eval, X_full[idx_eval])
        np.testing.assert_array_equal(sample_weight_eval, w_full[idx_eval])
        np.testing.assert_array_equal(sample_weight_eval, w_eval[idx_eval])

        np.testing.assert_array_equal(X[cand], X_full[idx_cand])
        np.testing.assert_array_equal(y[cand], y_full[idx_cand])
        np.testing.assert_array_equal(sample_weight[cand], w_full[idx_cand])

        cand = np.array([[0], [9]])
        (
            X_full,
            y_full,
            w_full,
            w_eval,
            idx_train,
            idx_cand,
            idx_eval,
        ) = qs._concatenate_samples(
            X,
            y,
            sample_weight,
            cand,
            sample_weight_cand,
            X_eval,
            sample_weight_eval,
        )

        np.testing.assert_equal(len(X_full), len(y_full))
        np.testing.assert_equal(len(X_full), len(w_full))
        np.testing.assert_equal(len(X_full), len(w_eval))

        np.testing.assert_array_equal(X, X_full[idx_train])
        np.testing.assert_array_equal(y, y_full[idx_train])
        np.testing.assert_array_equal(sample_weight, w_full[idx_train])

        np.testing.assert_array_equal(X_eval, X_full[idx_eval])
        np.testing.assert_array_equal(sample_weight_eval, w_full[idx_eval])
        np.testing.assert_array_equal(sample_weight_eval, w_eval[idx_eval])

        np.testing.assert_array_equal(cand, X_full[idx_cand])
        np.testing.assert_array_equal(
            np.full((len(cand)), np.nan), y_full[idx_cand]
        )
        np.testing.assert_array_equal(sample_weight_cand, w_full[idx_cand])

        (
            X_full,
            y_full,
            w_full,
            w_eval,
            idx_train,
            idx_cand,
            idx_eval,
        ) = qs._concatenate_samples(
            X, y, None, cand, sample_weight_cand, X_eval, sample_weight_eval
        )
        np.testing.assert_array_equal(
            np.ones(len(idx_train)), w_full[idx_train]
        )

        (
            X_full,
            y_full,
            w_full,
            w_eval,
            idx_train,
            idx_cand,
            idx_eval,
        ) = qs._concatenate_samples(
            X, y, sample_weight, cand, None, X_eval, sample_weight_eval
        )
        np.testing.assert_array_equal(np.ones(len(idx_cand)), w_full[idx_cand])

        (
            X_full,
            y_full,
            w_full,
            w_eval,
            idx_train,
            idx_cand,
            idx_eval,
        ) = qs._concatenate_samples(
            X, y, sample_weight, cand, sample_weight_cand, None, sample_weight
        )
        np.testing.assert_array_equal(sample_weight, w_full[idx_eval])

        self.assertRaises(
            ValueError,
            qs._concatenate_samples,
            X,
            y,
            np.ones(len(X) + 1),
            cand,
            None,
            X_eval,
            None,
        )
        self.assertRaises(
            ValueError,
            qs._concatenate_samples,
            X,
            y,
            None,
            cand,
            np.ones(len(cand) + 1),
            X_eval,
            None,
        )
        self.assertRaises(
            ValueError,
            qs._concatenate_samples,
            X,
            y,
            None,
            cand,
            None,
            X_eval,
            np.ones(len(X_eval) + 10),
        )
        self.assertRaises(
            ValueError,
            qs._concatenate_samples,
            X,
            y,
            None,
            cand,
            None,
            None,
            np.ones(len(X_eval) + 10),
        )

    def test__risk_estimation(self):
        def risk_estimation_slow(
            prob_true, prob_pred, cost_matrix, sample_weight
        ):
            n_samples = len(prob_true)
            n_classes = len(cost_matrix)
            result = 0
            if prob_true.ndim == 1 and prob_pred.ndim == 1:
                for i in range(n_samples):
                    result += (
                        sample_weight[i]
                        * cost_matrix[prob_true[i], prob_pred[i]]
                    )
            elif prob_true.ndim == 1 and prob_pred.ndim == 2:
                for i in range(n_samples):
                    for j in range(n_classes):
                        result += (
                            sample_weight[i]
                            * prob_pred[i, j]
                            * cost_matrix[prob_true[i], j]
                        )
            elif prob_true.ndim == 2 and prob_pred.ndim == 1:
                for i in range(n_samples):
                    for j in range(n_classes):
                        result += (
                            sample_weight[i]
                            * prob_true[i, j]
                            * cost_matrix[j, prob_pred[i]]
                        )
            else:
                for i in range(n_samples):
                    for j in range(n_classes):
                        for k in range(n_classes):
                            result += (
                                sample_weight[i]
                                * prob_true[i, j]
                                * prob_pred[i, k]
                                * cost_matrix[j, k]
                            )

            return result

        qs = ExpectedErrorReduction(enforce_mapping=False)
        n_samples = 20
        n_classes = 4

        pred_true = np.random.randint(0, n_classes, n_samples)
        prob_true = np.random.rand(n_samples, n_classes)
        prob_true /= prob_true.sum(0, keepdims=True)

        pred_pred = np.random.randint(0, n_classes, n_samples)
        prob_pred = np.random.rand(n_samples, n_classes)
        prob_pred /= prob_true.sum(0, keepdims=True)

        sw = np.random.rand(n_samples)
        cm = np.random.randint(0, 20, (n_classes, n_classes))

        params = [
            [pred_true, pred_pred, cm, sw],
            [pred_true, prob_pred, cm, sw],
            [prob_true, pred_pred, cm, sw],
            [prob_true, prob_pred, cm, sw],
        ]

        for args in params:
            with self.subTest(msg=args):
                a = risk_estimation_slow(*args)
                b = qs._risk_estimation(*args)
                np.testing.assert_allclose(a, b)

    def test__logloss_estimation(self):
        n_samples = 20
        n_classes = 4

        prob_true = np.random.rand(n_samples, n_classes)
        prob_pred = np.random.rand(n_samples, n_classes)

        a = -np.sum(prob_true * np.log(prob_pred + np.finfo(float).eps))
        qs = ExpectedErrorReduction(enforce_mapping=False)
        b = qs._logloss_estimation(prob_true, prob_pred)
        np.testing.assert_allclose(a, b)


class TestMonteCarloEER(TemplateTestExpectedErrorReduction, unittest.TestCase):
    def setUp(self):
        super().setUp(qs_class=MonteCarloEER)

    def test_init_param_method(self):
        test_cases = [(2, TypeError), ("string", ValueError)]
        self._test_param("init", "method", test_cases)
        test_cases = [("log_loss", ValueError)]
        replace_init_params = {"cost_matrix": 1 - np.eye(2)}
        self._test_param(
            "init",
            "method",
            test_cases,
            replace_init_params=replace_init_params,
        )

    def test_init_param_cost_matrix(self):
        super().test_init_param_cost_matrix([("log_loss", ValueError)])

    def test_query_param_sample_weight_candidates(self):
        X = self.query_default_params_clf["X"]
        X_cand = X[:4]
        test_cases = [
            (np.ones((len(X_cand) - 1)), ValueError),
            ("string", ValueError),
            (np.ones(len(X_cand)), None),
        ]
        replace_query_params = {"candidates": X_cand}
        self._test_param(
            "query",
            "sample_weight_candidates",
            test_cases,
            replace_query_params=replace_query_params,
        )
        replace_query_params["sample_weight"] = np.ones(len(X))
        self._test_param(
            "query",
            "sample_weight_candidates",
            test_cases,
            replace_query_params=replace_query_params,
        )
        # check if error is raised if candidates are None with sw_candidates
        self._test_param(
            "query",
            "sample_weight_candidates",
            [(np.ones(len(X_cand)), ValueError)],
        )

    def test_query_param_X_eval(self):
        test_cases = [
            (np.ones(5), TypeError),
            ("str", ValueError),
            ([], TypeError),
        ]
        self._test_param("init", "method", test_cases)

    def test_query_param_sample_weight_eval(self):
        X = self.query_default_params_clf["X"]
        X_cand = X[:3]
        X_eval = X[:4]
        test_cases = [
            (np.ones((len(X_eval) - 1)), ValueError),
            ("string", ValueError),
            (np.ones(len(X_eval)), None),
        ]
        replace_query_params = {"X_eval": X_eval}
        self._test_param(
            "query",
            "sample_weight_eval",
            test_cases,
            replace_query_params=replace_query_params,
        )
        replace_query_params["sample_weight"] = np.ones(len(X))
        self._test_param(
            "query",
            "sample_weight_eval",
            test_cases,
            replace_query_params=replace_query_params,
        )
        replace_query_params["candidates"] = X_cand
        replace_query_params["sample_weight_candidates"] = np.ones(len(X_cand))
        self._test_param(
            "query",
            "sample_weight_eval",
            test_cases,
            replace_query_params=replace_query_params,
        )

        # qs = self.Strategy()
        # for swe in [
        #     "string",
        #     self.candidates,
        #     None,
        #     np.empty((len(self.X_eval) - 1)),
        # ]:
        #     with self.assertRaises(
        #         ValueError, msg=f"sample_weight_eval={swe}"
        #     ):
        #         qs.query(
        #             **self.kwargs,
        #             X_eval=self.X_eval,
        #             sample_weight=np.ones(len(self.X)),
        #             sample_weight_candidates=np.ones(len(self.candidates)),
        #             sample_weight_eval=swe,
        #         )

    def test_query(self):
        super().test_query()
        classes = [0, 1]
        X = [[0], [0], [0], [0]]
        y = [0, MISSING_LABEL, MISSING_LABEL, 1]
        candidates = [1, 2]
        id_cost_matrix = 1 - np.eye(2)

        clf = self.DummyClf(classes=classes)
        # clf = ParzenWindowClassifier(classes=classes)

        params_list = [
            [
                "log_loss",
                None,
                False,
                candidates,
                None,
                np.full(
                    shape=(1, len(candidates)),
                    fill_value=0.5 * np.log(0.5) * len(classes) * len(X),
                ),
            ],
            [
                "log_loss",
                None,
                True,
                candidates,
                None,
                np.full(
                    shape=(1, len(candidates)),
                    fill_value=0,
                ),
            ],
            [
                "misclassification_loss",
                id_cost_matrix,
                False,
                candidates,
                None,
                np.full(shape=(1, len(candidates)), fill_value=-0.5 * len(X)),
            ],
            [
                "misclassification_loss",
                id_cost_matrix,
                False,
                X,
                None,
                np.full(shape=(1, len(X)), fill_value=-0.5 * len(X)),
            ],
            [
                "misclassification_loss",
                id_cost_matrix,
                False,
                candidates,
                X,
                np.full(shape=(1, len(candidates)), fill_value=-0.5 * len(X)),
            ],
            [
                "misclassification_loss",
                id_cost_matrix,
                True,
                candidates,
                X,
                np.full(shape=(1, len(candidates)), fill_value=0),
            ],
        ]

        for (
            method,
            cost_matrix,
            subtract_cur,
            cand,
            X_eval,
            expected_utils,
        ) in params_list:
            with self.subTest(
                msg=method, subtract_cur=subtract_cur, cand=cand, eval=X_eval
            ):
                qs = MonteCarloEER(
                    method=method,
                    cost_matrix=cost_matrix,
                    subtract_current=subtract_cur,
                )
                qs.query(
                    X,
                    y=np.full(shape=len(X), fill_value=np.nan),
                    clf=clf,
                    fit_clf=True,
                    ignore_partial_fit=True,
                    candidates=cand,
                    X_eval=X_eval,
                    return_utilities=True,
                )
                idx, utils = qs.query(
                    X,
                    y,
                    clf,
                    fit_clf=True,
                    ignore_partial_fit=True,
                    candidates=cand,
                    X_eval=X_eval,
                    return_utilities=True,
                )
                if np.array(cand).ndim == 1:
                    np.testing.assert_allclose(expected_utils, utils[:, cand])
                else:
                    np.testing.assert_allclose(expected_utils, utils)

        # TODO: ParzenWindowClassifier Test


class TestValueOfInformationEER(
    TemplateTestExpectedErrorReduction, unittest.TestCase
):
    def setUp(self):
        super().setUp(qs_class=ValueOfInformationEER)

    def test_init_param_consider_unlabeled(self):
        test_cases = [(2, TypeError), ("string", TypeError)]
        self._test_param("query", "consider_unlabeled", test_cases)

    def test_init_param_consider_labeled(self):
        test_cases = [(2, TypeError), ("string", TypeError)]
        self._test_param("query", "consider_labeled", test_cases)

    def test_init_param_candidate_to_labeled(self):
        test_cases = [(2, TypeError), ("string", TypeError)]
        self._test_param("query", "candidate_to_labeled", test_cases)

    def test_init_param_normalize(self):
        test_cases = [(2, TypeError), ("string", TypeError)]
        self._test_param("query", "normalize", test_cases)

    def test_query(self):
        super().test_query()
        classes = [0, 1]
        X = [[0], [0], [0], [0]]
        y = [0, MISSING_LABEL, MISSING_LABEL, 1]
        y2 = [0, 0, MISSING_LABEL, 1]
        cand = [1, 2]
        cost_matrix = 1 - np.eye(2)
        # clf_partial = SklearnClassifier(
        #     GaussianNB(), classes=classes
        # ).fit(X, y)

        params_list = [
            ["kapoor-sub", True, True, True, True, False, [[0, 0]]],
            [
                "kapoor",
                True,
                True,
                True,
                False,
                False,
                np.full(shape=(1, len(cand)), fill_value=-0.5 * len(X)),
            ],
            [
                "Margeniantu",
                False,
                True,
                False,
                False,
                False,
                np.full(
                    shape=(1, len(cand)),
                    fill_value=-0.25
                    * (len(classes) - 1)
                    * len(classes)
                    * np.sum(is_labeled(y, missing_label=MISSING_LABEL)),
                ),
            ],
            [
                "Joshi-sub-unnorm",
                True,
                False,
                True,
                True,
                False,
                np.full(shape=(1, len(cand)), fill_value=0.5),
                # TODO Normalize each term individually
            ],
            [
                "Joshi-sub",
                True,
                False,
                True,
                True,
                True,
                np.full(shape=(1, len(cand)), fill_value=0),
                # TODO Normalize each term individually
            ],
            [
                "Joshi",
                True,
                False,
                True,
                False,
                False,
                np.full(
                    shape=(1, len(cand)),
                    fill_value=-0.25 * np.sum(cost_matrix),
                ),
            ],
        ]

        # Test with zero labels.
        for (
            msg,
            consider_unlabeled,
            consider_labeled,
            candidate_to_labeled,
            substract_current,
            normalize,
            expected_utils,
        ) in params_list:
            with self.subTest(msg=msg + ": Scenario (zero labels)"):
                qs = ValueOfInformationEER(
                    consider_unlabeled=consider_unlabeled,
                    consider_labeled=consider_labeled,
                    candidate_to_labeled=candidate_to_labeled,
                    subtract_current=substract_current,
                    normalize=normalize,
                    cost_matrix=cost_matrix,
                )
                clf = ParzenWindowClassifier(classes=classes)
                qs.query(
                    candidates=cand,
                    clf=clf,
                    X=X,
                    y=np.full(shape=len(X), fill_value=np.nan),
                )

        # Test Scenario.
        for (
            msg,
            consider_unlabeled,
            consider_labeled,
            candidate_to_labeled,
            substract_current,
            normalize,
            expected_utils,
        ) in params_list:
            with self.subTest(msg=msg + ": Scenario"):
                qs = ValueOfInformationEER(
                    consider_unlabeled=consider_unlabeled,
                    consider_labeled=consider_labeled,
                    candidate_to_labeled=candidate_to_labeled,
                    subtract_current=substract_current,
                    normalize=normalize,
                    cost_matrix=cost_matrix,
                )
                clf = self.DummyClf()
                qs.query(candidates=cand, clf=clf, X=X, y=y)

                idxs, utils = qs.query(
                    candidates=cand,
                    clf=self.DummyClf(),
                    X=X,
                    y=y,
                    return_utilities=True,
                )
                np.testing.assert_array_equal(expected_utils, utils[:, cand])

        # Test Scenario.
        for (
            msg,
            consider_unlabeled,
            consider_labeled,
            candidate_to_labeled,
            substract_current,
            normalize,
            expected_utils,
        ) in params_list:
            with self.subTest(msg=msg + ": Scenario (last label)"):
                qs = ValueOfInformationEER(
                    consider_unlabeled=consider_unlabeled,
                    consider_labeled=consider_labeled,
                    candidate_to_labeled=candidate_to_labeled,
                    subtract_current=substract_current,
                    normalize=normalize,
                    cost_matrix=cost_matrix,
                )
                clf = self.DummyClf()
                qs.query(candidates=cand, clf=clf, X=X, y=y2)

                idxs, utils = qs.query(
                    candidates=cand,
                    clf=self.DummyClf(),
                    X=X,
                    y=y,
                    return_utilities=True,
                )
                np.testing.assert_array_equal(expected_utils, utils[:, cand])
