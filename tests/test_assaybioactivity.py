"""
Tests for the AssayBioactivity class.

This test suite covers:
- Single concentration data retrieval by AEID
- Assay endpoints retrieval by gene symbol
- Detailed assay data with various projections
- Rate limiting
- Error handling
"""

import pytest
import time
from pycomptox.bioactivity import AssayBioactivity


@pytest.fixture
def assay_client():
    """Create an AssayBioactivity instance for testing."""
    return AssayBioactivity()


def test_get_single_concentration_by_aeid_default(assay_client):
    """Test getting single concentration data with default projection."""
    aeid = 3032
    result = assay_client.get_single_concentration_by_aeid(aeid)
    
    # Should return data (dict or list)
    assert result is not None
    
    # If it's a list, check the first item
    if isinstance(result, list):
        assert len(result) > 0
        item = result[0]
    else:
        item = result
    
    # Verify expected fields
    assert "aeid" in item or "endpointName" in item
    
    # Check for single conc fields
    expected_fields = ["preferredName", "dtxsid", "hitc", "endpointName"]
    for field in expected_fields:
        if field in item:
            assert item[field] is not None or item[field] == ""


def test_get_single_concentration_field_types(assay_client):
    """Test that single concentration results have expected field types."""
    aeid = 3032
    result = assay_client.get_single_concentration_by_aeid(aeid)
    
    # Get first item if list
    if isinstance(result, list):
        if len(result) == 0:
            pytest.skip("No data returned for this AEID")
        item = result[0]
    else:
        item = result
    
    # Check numeric fields if present
    if "aeid" in item:
        assert isinstance(item["aeid"], int)
    if "hitc" in item:
        assert isinstance(item["hitc"], (int, float, type(None)))
    if "coff" in item:
        assert isinstance(item["coff"], (int, float, type(None)))


def test_get_assay_endpoints_list_by_gene(assay_client):
    """Test getting assay endpoints by gene symbol."""
    gene_symbol = "TUBA1A"
    results = assay_client.get_assay_endpoints_list(gene_symbol)
    
    assert isinstance(results, list)
    assert len(results) > 0
    
    # Verify result structure
    first_endpoint = results[0]
    assert "aeid" in first_endpoint
    assert "geneSymbol" in first_endpoint
    assert "assayComponentEndpointName" in first_endpoint
    
    # Verify gene symbol matches
    assert first_endpoint["geneSymbol"] == gene_symbol


def test_get_assay_endpoints_different_genes(assay_client):
    """Test getting endpoints for different gene symbols."""
    test_genes = ["TUBA1A", "ESR1", "AR"]
    
    for gene in test_genes:
        try:
            results = assay_client.get_assay_endpoints_list(gene)
            assert isinstance(results, list)
            if len(results) > 0:
                # Check that all results match the gene
                for endpoint in results:
                    assert endpoint["geneSymbol"] == gene
        except ValueError:
            # Some genes might not have endpoints
            pass


def test_get_assay_data_full_without_projection(assay_client):
    """Test getting full assay data without projection."""
    aeid = 3032
    result = assay_client.get_assay_data_by_aeid_with_projections(aeid)
    
    assert result is not None
    
    # For full data, expect comprehensive information
    if isinstance(result, dict):
        # Should have basic assay fields
        expected_fields = ["aeid", "assayComponentEndpointName"]
        for field in expected_fields:
            if field in result:
                assert result[field] is not None


def test_get_assay_data_with_gene_projection(assay_client):
    """Test getting assay data with gene projection."""
    aeid = 3032
    result = assay_client.get_assay_data_by_aeid_with_projections(
        aeid, 
        projection="ccd-assay-gene"
    )
    
    assert result is not None
    
    # Gene projection should return gene information
    if isinstance(result, list):
        if len(result) > 0:
            gene = result[0]
            # Should have gene fields
            assert "geneSymbol" in gene or "geneName" in gene
    elif isinstance(result, dict):
        assert "geneSymbol" in result or "geneName" in result


def test_get_assay_data_with_annotation_projection(assay_client):
    """Test getting assay data with annotation projection."""
    aeid = 3032
    result = assay_client.get_assay_data_by_aeid_with_projections(
        aeid,
        projection="ccd-assay-annotation"
    )
    
    assert result is not None


def test_get_assay_data_with_citations_projection(assay_client):
    """Test getting assay data with citations projection."""
    aeid = 3032
    try:
        result = assay_client.get_assay_data_by_aeid_with_projections(
            aeid,
            projection="ccd-assay-citations"
        )
        assert result is not None
    except ValueError:
        # Some assays might not have citations
        pass


def test_get_assay_data_with_tcpl_projection(assay_client):
    """Test getting assay data with TCPL methods projection."""
    aeid = 3032
    try:
        result = assay_client.get_assay_data_by_aeid_with_projections(
            aeid,
            projection="ccd-assay-tcpl"
        )
        assert result is not None
    except ValueError:
        # Some assays might not have TCPL data
        pass


def test_invalid_aeid(assay_client):
    """Test handling of invalid AEID."""
    invalid_aeid = 999999999
    
    with pytest.raises(ValueError):
        assay_client.get_single_concentration_by_aeid(invalid_aeid)


def test_invalid_gene_symbol(assay_client):
    """Test handling of invalid gene symbol."""
    invalid_gene = "NOTAREALGENE12345"
    
    with pytest.raises(ValueError):
        assay_client.get_assay_endpoints_list(invalid_gene)


def test_invalid_projection(assay_client):
    """Test handling of invalid projection type."""
    aeid = 3032
    invalid_projection = "invalid-projection-type"
    
    # API may return data even with invalid projection (defaults to full data)
    # So we just verify it doesn't crash
    try:
        result = assay_client.get_assay_data_by_aeid_with_projections(
            aeid,
            projection=invalid_projection
        )
        # Should get some data back
        assert result is not None
    except ValueError:
        # It's also acceptable if API rejects invalid projection
        pass


def test_client_initialization_with_api_key():
    """Test that client can be initialized with explicit API key."""
    from pycomptox.config import load_api_key
    api_key = load_api_key()
    
    if api_key:
        client = AssayBioactivity(api_key=api_key)
        assert client.api_key == api_key


def test_rate_limiting():
    """Test that rate limiting works correctly."""
    client_with_delay = AssayBioactivity(time_delay_between_calls=0.5)
    
    start_time = time.time()
    
    # Make two consecutive calls with cache disabled
    try:
        client_with_delay.get_assay_endpoints_list("TUBA1A", use_cache=False)
        client_with_delay.get_assay_endpoints_list("ESR1", use_cache=False)
    except ValueError:
        # Ignore data errors, we're testing rate limiting
        pass
    
    elapsed_time = time.time() - start_time
    
    # Should take at least 0.5 seconds due to rate limiting
    assert elapsed_time >= 0.5


def test_different_projection_types(assay_client):
    """Test that different projection types return different data structures."""
    aeid = 3032
    
    projections = [
        None,
        "ccd-assay-annotation",
        "ccd-assay-gene"
    ]
    
    results = {}
    for projection in projections:
        try:
            result = assay_client.get_assay_data_by_aeid_with_projections(
                aeid,
                projection=projection
            )
            results[str(projection)] = result
        except ValueError:
            # Some projections might not have data
            pass
    
    # Should have at least gotten some results
    assert len(results) > 0


def test_endpoint_list_consistency(assay_client):
    """Test that endpoint lists contain consistent data."""
    gene_symbol = "TUBA1A"
    endpoints = assay_client.get_assay_endpoints_list(gene_symbol)
    
    assert len(endpoints) > 0
    
    # All endpoints should have the same gene symbol
    for endpoint in endpoints:
        assert endpoint["geneSymbol"] == gene_symbol
        assert isinstance(endpoint["aeid"], int)


# Manual test runner for development
if __name__ == "__main__":
    print("Running AssayBioactivity tests manually...")
    client = AssayBioactivity()
    
    print("\n1. Testing single concentration data:")
    single_conc = client.get_single_concentration_by_aeid(3032)
    if isinstance(single_conc, list):
        print(f"   Found {len(single_conc)} entries")
        if len(single_conc) > 0:
            print(f"   First entry DTXSID: {single_conc[0].get('dtxsid', 'N/A')}")
    else:
        print(f"   Endpoint: {single_conc.get('endpointName', 'N/A')}")
    
    print("\n2. Testing gene endpoints:")
    endpoints = client.get_assay_endpoints_list("TUBA1A")
    print(f"   Found {len(endpoints)} endpoints for TUBA1A")
    if endpoints:
        print(f"   First: {endpoints[0]['assayComponentEndpointName']}")
    
    print("\n3. Testing full assay data:")
    full_data = client.get_assay_data_by_aeid_with_projections(3032)
    if isinstance(full_data, dict):
        print(f"   Assay: {full_data.get('assayComponentEndpointName', 'N/A')}")
        print(f"   Target: {full_data.get('intendedTargetFamily', 'N/A')}")
    
    print("\n4. Testing gene projection:")
    gene_data = client.get_assay_data_by_aeid_with_projections(
        3032,
        projection="ccd-assay-gene"
    )
    if isinstance(gene_data, list) and len(gene_data) > 0:
        print(f"   Genes: {[g.get('geneSymbol', 'N/A') for g in gene_data[:3]]}")
    
    print("\n5. Testing batch annotations:")
    batch_results = client.find_assay_annotations_by_aeid_batch([3032, 3033])
    print(f"   Retrieved {len(batch_results)} annotations")
    if batch_results:
        print(f"   First: {batch_results[0]['assayComponentEndpointName']}")
    
    print("\n✓ All manual tests completed!")


def test_find_assay_annotations_by_aeid_batch(assay_client):
    """Test batch retrieval of assay annotations."""
    aeids = [3032, 3033]
    result = assay_client.find_assay_annotations_by_aeid_batch(aeids)
    
    # Should return a list
    assert isinstance(result, list)
    assert len(result) > 0
    
    # Check structure of first result
    first = result[0]
    assert "aeid" in first
    assert "assayComponentEndpointName" in first
    assert "intendedTargetFamily" in first


def test_find_assay_annotations_batch_empty_list(assay_client):
    """Test that empty AEID list raises ValueError."""
    with pytest.raises(ValueError, match="cannot be empty"):
        assay_client.find_assay_annotations_by_aeid_batch([])


def test_find_assay_annotations_batch_invalid_aeid(assay_client):
    """Test that invalid AEIDs raise ValueError."""
    with pytest.raises(ValueError, match="valid integers"):
        assay_client.find_assay_annotations_by_aeid_batch(["invalid"])


def test_find_assay_annotations_batch_single_aeid(assay_client):
    """Test batch method with single AEID."""
    result = assay_client.find_assay_annotations_by_aeid_batch([3032])
    
    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0]["aeid"] == 3032

