from hover.utils.torch_helper import vector_dataloader, one_hot, label_smoothing
import numpy as np


def test_vector_dataloader(num_entries=100, dim_inp=128, dim_out=3):
    vec_inp = np.random.rand(num_entries, dim_inp)
    vec_out = np.random.rand(num_entries, dim_out)
    loader = vector_dataloader(vec_inp, vec_out, batch_size=min(num_entries, 16))
    # no further assertions; just checking that the vector_dataloader function does not crash
    assert loader


def test_one_hot():
    categorical_labels = [0, 1, 2, 1]
    one_hot_labels = one_hot(categorical_labels, 3)
    assert one_hot_labels.shape == (4, 3)


def test_label_smoothing(num_entries=100, num_classes=3, coeff=0.1):
    assert num_classes >= 2
    assert coeff >= 0.0

    categorical_labels = [0] * num_entries
    prob_labels = one_hot(categorical_labels, num_classes)

    assert np.allclose(label_smoothing(prob_labels, coefficient=0.0), prob_labels)
    smoothed = label_smoothing(prob_labels, coefficient=coeff)
    np.testing.assert_almost_equal(
        smoothed[0][0], 1.0 - coeff * (1.0 - 1.0 / num_classes)
    )
    np.testing.assert_almost_equal(smoothed[0][1], coeff / num_classes)
