"""
Regression tests for the 16 client methods that could not work before 0.7.0.

Each of these raised ``AttributeError`` or returned HTTP 404 on every call, and
none had a test. They fall into three groups:

1. Eight called a ``self._make_request(...)`` that was never defined.
2. Five hand-rolled their request and built the URL as ``f"{base_url}{endpoint}"``
   with no separator, producing ``.../ctx-apibioactivity/...``.
3. Three used an endpoint path the API does not serve.

These are live-API tests, so ``conftest.py`` marks them ``integration``. The
offline counterpart is ``test_spec_conformance.py``, which catches group 3
without any network access.
"""

import pytest

from pycomptox import (
    BioactivityData,
    BioactivityModel,
    Chemical,
    DemographicExposure,
    ExposurePrediction,
    FunctionalUse,
    HTTKData,
    ListPresence,
    ProductData,
)

DTXSID = "DTXSID7020182"          # Bisphenol A
DTXSID_AED = "DTXSID5021209"      # has AED data
BATCH = [DTXSID]


def _assert_returned_data(result):
    """The method completed and produced a JSON-ish payload."""
    assert result is not None
    assert isinstance(result, (list, dict))


# --- group 1: methods that called the nonexistent _make_request ---------------

def test_search_ms_ready_by_mass_range():
    result = Chemical().search_ms_ready_by_mass_range(200.9, 200.95)
    _assert_returned_data(result)
    assert len(result) > 0


def test_search_ms_ready_by_formula():
    result = Chemical().search_ms_ready_by_formula("C16H24N2O5S")
    _assert_returned_data(result)
    assert len(result) > 0


@pytest.mark.parametrize(
    "client_cls,method",
    [
        (ListPresence, "get_list_presence_data_by_dtxsid_batch"),
        (ExposurePrediction, "get_general_seem_prediction_by_dtxsid_batch"),
        (DemographicExposure, "get_seem_prediction_by_dtxsid_batch"),
        (ProductData, "get_product_data_by_dtxsid_batch"),
        (HTTKData, "get_httk_data_by_dtxsid_batch"),
        (FunctionalUse, "get_functional_use_by_dtxsid_batch"),
    ],
)
def test_exposure_batch_methods(client_cls, method):
    """These six raised AttributeError on every call before 0.7.0."""
    result = getattr(client_cls(), method)(BATCH)
    _assert_returned_data(result)


# --- group 2: hand-rolled POSTs with a malformed URL --------------------------

@pytest.mark.parametrize(
    "method,arg",
    [
        ("get_bioactivity_data_by_dtxsid_batch", BATCH),
        ("get_aed_data_by_dtxsid_batch", [DTXSID_AED]),
        ("get_bioactivity_data_by_aeid_batch", [3032]),
        ("get_bioactivity_data_by_spid_batch", ["EPAPLT0232A03"]),
        ("get_bioactivity_data_by_m4id_batch", [1135145]),
    ],
)
def test_bioactivity_batch_methods(method, arg):
    """These five built '.../ctx-apibioactivity/...' and returned 404."""
    result = getattr(BioactivityData(), method)(arg)
    _assert_returned_data(result)


def test_bioactivity_batch_methods_go_through_the_base_client():
    """
    They previously bypassed the base client, so they had no timeout, no retry,
    and no rate limiting. Confirm caching now works through them, which is only
    possible via _make_cached_request.
    """
    client = BioactivityData(use_cache=True)
    first = client.get_aed_data_by_dtxsid_batch([DTXSID_AED])
    second = client.get_aed_data_by_dtxsid_batch([DTXSID_AED])
    assert first == second


# --- group 3: wrong endpoint paths -------------------------------------------

def test_search_by_exact_formula_uses_the_by_exact_formula_path():
    """Previously requested chemical/search/by-formula/ -> 404."""
    result = Chemical().search_by_exact_formula("C15H16O2")
    _assert_returned_data(result)
    assert len(result) > 0


def test_get_toxcast_model_by_dtxsid():
    """Previously requested bioactivity/models/by-dtxsid/ -> 404."""
    result = BioactivityModel().get_toxcast_model_by_dtxsid(DTXSID)
    _assert_returned_data(result)
    assert len(result) > 0


def test_get_toxcast_model_by_dtxsid_and_model():
    """Previously requested bioactivity/models/search (no trailing slash) -> 404."""
    result = BioactivityModel().get_toxcast_model_by_dtxsid_and_model(DTXSID, "CERAPP")
    _assert_returned_data(result)
    assert len(result) > 0


# --- the trailing slash that makes group 1 and 3 work ------------------------

def test_batch_post_endpoints_need_their_trailing_slash():
    """
    Documents the API behaviour the fix depends on: the batch POST endpoints
    answer on '.../search/by-dtxsid/' and 404 without the trailing slash. If
    this ever stops being true, _normalize_endpoint should be revisited.
    """
    from pycomptox.exceptions import NotFoundError

    client = HTTKData()
    with_slash = client._make_cached_request(
        "exposure/httk/search/by-dtxsid/", method="POST", json=BATCH
    )
    _assert_returned_data(with_slash)

    with pytest.raises(NotFoundError):
        client._make_cached_request(
            "exposure/httk/search/by-dtxsid", method="POST", json=BATCH
        )
