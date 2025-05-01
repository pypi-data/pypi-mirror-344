from __future__ import annotations

import os
import sys
import unittest

import numpy as np
import torch
from parameterized import parameterized

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from topolosses.losses import CLDiceLoss
from topolosses.losses import DiceLoss

# TODO test iter_, test weights
TEST_CASES = [
    [  # shape: (1, 1, 2, 2)
        {"include_background": True, "sigmoid": True, "smooth": 1e-6, "alpha": 0},
        {"input": torch.tensor([[[[1.0, -1.0], [-1.0, 1.0]]]]), "target": torch.tensor([[[[1.0, 0.0], [1.0, 1.0]]]])},
        0.307576,
    ],
    [  # shape: (1, 1, 2, 2) returning just the cl dice component
        {"include_background": True, "sigmoid": True, "smooth": 1e-6, "use_base_loss": False, "alpha": 1},
        {"input": torch.tensor([[[[1.0, -1.0], [-1.0, 1.0]]]]), "target": torch.tensor([[[[1.0, 0.0], [1.0, 1.0]]]])},
        0.5761159658,
    ],
    [  # shape: (2, 1, 2, 2) default base loss
        {"include_background": True, "sigmoid": True, "smooth": 1e-4},
        {
            "input": torch.tensor([[[[1.0, -1.0], [-1.0, 1.0]]], [[[1.0, -1.0], [-1.0, 1.0]]]]),
            "target": torch.tensor([[[[1.0, 1.0], [1.0, 1.0]]], [[[1.0, 0.0], [1.0, 0.0]]]]),
        },
        0.541648,
    ],
    [  # shape: (2, 1, 2, 2) default base loss
        {"include_background": True, "sigmoid": True, "batch": True},
        {
            "input": torch.tensor([[[[1.0, -1.0], [-1.0, 1.0]]], [[[1.0, -1.0], [-1.0, 1.0]]]]),
            "target": torch.tensor([[[[1.0, 1.0], [1.0, 1.0]]], [[[1.0, 0.0], [1.0, 0.0]]]]),
        },
        0.599998,
    ],
    [  # shape: (1, 3, 2, 2) default base loss (weighted dice),
        {"softmax": True},
        {
            "input": torch.tensor(
                [
                    [
                        [[1.0, -1.0], [-1.0, 1.0]],
                        [[0.5, 0.2], [-0.3, -0.7]],
                        [[-1.0, 1.0], [1.0, -1.0]],
                    ]
                ]
            ),
            "target": torch.tensor(
                [
                    [
                        [[1.0, 0.0], [1.0, 1.0]],
                        [[0.0, 1.0], [1.0, 0.0]],
                        [[1.0, 1.0], [0.0, 1.0]],
                    ]
                ]
            ),
        },
        0.858929,
    ],
    [  # shape: (2, 1, 2, 2), same as above but with defined base loss - sigmoid and smooth must be passed to base loss as well (alterantive )
        {
            "include_background": True,
            "sigmoid": True,
            "smooth": 1e-4,
            "base_loss": DiceLoss(sigmoid=True, smooth=1e-4),
        },
        {
            "input": torch.tensor([[[[1.0, -1.0], [-1.0, 1.0]]], [[[1.0, -1.0], [-1.0, 1.0]]]]),
            "target": torch.tensor([[[[1.0, 1.0], [1.0, 1.0]]], [[[1.0, 0.0], [1.0, 0.0]]]]),
        },
        0.541648,
    ],
    [  # shape: (1, 2, 6, 6,)
        {},
        {
            "input": torch.nn.functional.one_hot(
                1
                - torch.tensor(
                    [
                        [
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        ]
                    ]
                ).to(torch.int64),
                2,
            ).permute(0, 3, 1, 2),
            "target": torch.nn.functional.one_hot(
                1
                - torch.tensor(
                    [
                        [
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        ]
                    ]
                ).to(torch.int64),
                2,
            ).permute(0, 3, 1, 2),
        },
        0.308791,
    ],
]


class TestDiceCLDiceLoss(unittest.TestCase):
    @parameterized.expand(TEST_CASES)
    def test_result(self, input_param, input_data, expected_val):
        result = CLDiceLoss(**input_param).forward(**input_data)
        np.testing.assert_allclose(result.detach().cpu().numpy(), expected_val, rtol=1e-5)

    # @parameterized.expand(TEST_CASES)
    # def test_result_CLDice(self, input_param, input_data, expected_val):
    #     result = CLDiceLoss(**input_param).forward(**input_data)
    #     print(result.item())
    #     expected_val, dic = Multiclass_CLDice(**input_param).forward(**input_data)
    #     print(dic)
    #     print(expected_val[0].item())
    #     np.testing.assert_allclose(result.detach().cpu().numpy(), expected_val[0].item(), rtol=1e-5)

    def test_with_cuda(self):
        if torch.cuda.is_available():
            loss = CLDiceLoss(include_background=True, sigmoid=True, smooth=1e-4).cuda()
            input_data = {
                "input": torch.tensor([[[[1.0, -1.0], [-1.0, 1.0]]], [[[1.0, -1.0], [-1.0, 1.0]]]]).cuda(),
                "target": torch.tensor([[[[1.0, 1.0], [1.0, 1.0]]], [[[1.0, 0.0], [1.0, 0.0]]]]).cuda(),
            }
            result = loss.forward(**input_data)
            np.testing.assert_allclose(result.detach().cpu().numpy(), 0.541648, rtol=1e-4)

    def test_ill_shape(self):
        loss = CLDiceLoss()
        with self.assertRaisesRegex(ValueError, ""):
            loss.forward(torch.ones((1, 2, 3)), torch.ones((4, 5, 6)))

    def test_ill_opts(self):
        with self.assertRaisesRegex(ValueError, ""):
            CLDiceLoss(sigmoid=True, softmax=True)
        chn_input = torch.ones((1, 1, 3, 3))
        chn_target = torch.ones((1, 1, 3, 3))
        with self.assertRaisesRegex(ValueError, ""):
            loss = CLDiceLoss(softmax=True)
            loss.forward(chn_input, chn_target)
        chn_input = torch.ones((1, 1, 3))
        chn_target = torch.ones((1, 1, 3))
        with self.assertRaisesRegex(ValueError, ""):
            loss = CLDiceLoss()
            loss.forward(chn_input, chn_target)

    def test_input_warnings(self):
        chn_input = torch.ones((1, 1, 3, 3))
        chn_target = torch.ones((1, 1, 3, 3))
        with self.assertWarns(Warning):
            loss = CLDiceLoss(include_background=False)
            loss.forward(chn_input, chn_target)
        with self.assertWarns(Warning):
            loss = CLDiceLoss(use_base_loss=False, alpha=0.5)
        with self.assertWarns(Warning):
            loss = CLDiceLoss(use_base_loss=False, base_loss=DiceLoss())

    # from test_utils import test_script_save
    # def test_script(self):
    #     loss = DiceCLDiceLoss()
    #     test_input = torch.ones(2, 1, 8, 8)
    #     test_script_save(loss, test_input, test_input)


if __name__ == "__main__":
    unittest.main()
