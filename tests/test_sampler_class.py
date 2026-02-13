import bilby
import pytest
from kombine_bilby import Kombine


@pytest.fixture()
def SamplerClass():
    return Kombine


@pytest.fixture()
def create_sampler(SamplerClass, bilby_gaussian_likelihood_and_priors, tmp_path):
    likelihood, priors = bilby_gaussian_likelihood_and_priors

    def create_fn(**kwargs):
        return SamplerClass(
            likelihood,
            priors,
            outdir=tmp_path / "outdir",
            label="test",
            use_ratio=False,
            **kwargs,
        )

    return create_fn


@pytest.fixture
def sampler(create_sampler):
    return create_sampler()


def test_default_kwargs(sampler):
    expected = dict(
        nwalkers=500,
        args=[],
        pool=None,
        transd=False,
        lnpost0=None,
        blob0=None,
        iterations=500,
        storechain=True,
        processes=1,
        update_interval=None,
        kde=None,
        kde_size=None,
        spaces=None,
        freeze_transd=False,
        test_steps=16,
        critical_pval=0.05,
        max_steps=None,
        burnin_verbose=False,
    )
    assert sampler.kwargs == expected


@pytest.mark.parametrize(
    "equiv",
    bilby.core.sampler.base_sampler.MCMCSampler.nwalkers_equiv_kwargs,
)
def test_translate_kwargs(create_sampler, equiv):
    expected = dict(
        nwalkers=123,
        args=[],
        pool=None,
        transd=False,
        lnpost0=None,
        blob0=None,
        iterations=500,
        storechain=True,
        processes=1,
        update_interval=None,
        kde=None,
        kde_size=None,
        spaces=None,
        freeze_transd=False,
        test_steps=16,
        critical_pval=0.05,
        max_steps=None,
        burnin_verbose=False,
    )

    sampler = create_sampler(**{equiv: 123})
    assert sampler.kwargs == expected
