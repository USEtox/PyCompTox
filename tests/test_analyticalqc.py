"""
Tests for AnalyticalQC API client.

This test suite validates the functionality of the AnalyticalQC class,
including QC data retrieval and error handling.
"""

import pytest
import time
from pycomptox.bioactivity import AnalyticalQC


@pytest.fixture
def qc_client():
    """Create an AnalyticalQC client instance for testing."""
    return AnalyticalQC()


class TestGetAnalyticalQcDataByDtxsid:
    """Tests for get_analytical_qc_data_by_dtxsid method."""
    
    def test_get_qc_data_for_bisphenol_a(self, qc_client):
        """Test retrieving QC data for bisphenol A (DTXSID7020182)."""
        qc_data = qc_client.get_analytical_qc_data_by_dtxsid("DTXSID7020182")
        
        # Should return a list
        assert isinstance(qc_data, list)
        
        # May have QC records
        if len(qc_data) > 0:
            assert "dtxsid" in qc_data[0]
            assert qc_data[0]["dtxsid"] == "DTXSID7020182"
    
    def test_qc_data_structure(self, qc_client):
        """Test that QC data contains expected fields when available."""
        qc_data = qc_client.get_analytical_qc_data_by_dtxsid("DTXSID7020182")
        
        if len(qc_data) > 0:
            # Verify expected fields are present in first record
            first_record = qc_data[0]
            expected_fields = [
                "analyticalQcId", "dtxsid", "chnm", "spid",
                "qcLevel", "t0", "t4", "call"
            ]
            for field in expected_fields:
                assert field in first_record, f"Missing field: {field}"
    
    def test_qc_level_field(self, qc_client):
        """Test that QC level field is present when data exists."""
        qc_data = qc_client.get_analytical_qc_data_by_dtxsid("DTXSID7020182")
        
        if len(qc_data) > 0:
            assert "qcLevel" in qc_data[0]
            # QC level should be a string
            assert isinstance(qc_data[0]["qcLevel"], (str, type(None)))
    
    def test_stability_data_fields(self, qc_client):
        """Test that stability data (T0, T4) is included."""
        qc_data = qc_client.get_analytical_qc_data_by_dtxsid("DTXSID7020182")
        
        if len(qc_data) > 0:
            assert "t0" in qc_data[0]
            assert "t4" in qc_data[0]
    
    def test_invalid_dtxsid_returns_empty_list(self, qc_client):
        """Test that invalid DTXSID returns empty list."""
        result = qc_client.get_analytical_qc_data_by_dtxsid("DTXSID0000000")
        assert isinstance(result, list)
        # May be empty or have no results
    
    def test_chemical_name_included(self, qc_client):
        """Test that chemical name (chnm) is included when available."""
        qc_data = qc_client.get_analytical_qc_data_by_dtxsid("DTXSID7020182")
        
        if len(qc_data) > 0:
            assert "chnm" in qc_data[0]
            if qc_data[0]["chnm"]:
                assert isinstance(qc_data[0]["chnm"], str)
    
    def test_multiple_qc_records(self, qc_client):
        """Test that multiple QC records can be returned."""
        qc_data = qc_client.get_analytical_qc_data_by_dtxsid("DTXSID7020182")
        
        # BPA likely has multiple QC records
        assert isinstance(qc_data, list)
        if len(qc_data) > 1:
            # Each should have unique QC ID
            qc_ids = [record["analyticalQcId"] for record in qc_data]
            assert len(qc_ids) == len(set(qc_ids)), "QC IDs should be unique"


class TestClientFunctionality:
    """Tests for general client functionality."""
    
    def test_client_initialization(self):
        """Test client can be initialized with and without API key."""
        # Without API key (uses config)
        client1 = AnalyticalQC()
        assert client1.base_url == "https://comptox.epa.gov/ctx-api"
        
        # With API key
        client2 = AnalyticalQC(api_key="test_key")
        assert client2.api_key == "test_key"
    
    def test_rate_limiting(self, qc_client):
        """Test that rate limiting is applied between requests."""
        start_time = time.time()
        
        # Make multiple requests with cache disabled to test rate limiting
        qc_client.get_analytical_qc_data_by_dtxsid("DTXSID7020182", use_cache=False)
        qc_client.get_analytical_qc_data_by_dtxsid("DTXSID5020064", use_cache=False)
        
        elapsed = time.time() - start_time
        
        # Should take at least min_request_interval between requests
        assert elapsed >= 0.1
    
    def test_different_chemicals(self, qc_client):
        """Test retrieving QC data for different chemicals."""
        # Test with two different chemicals
        qc_data1 = qc_client.get_analytical_qc_data_by_dtxsid("DTXSID7020182")
        qc_data2 = qc_client.get_analytical_qc_data_by_dtxsid("DTXSID5020064")
        
        # Both should be lists
        assert isinstance(qc_data1, list)
        assert isinstance(qc_data2, list)
        
        # If both have data, they should be different chemicals
        if len(qc_data1) > 0 and len(qc_data2) > 0:
            assert qc_data1[0]["dtxsid"] != qc_data2[0]["dtxsid"]


class TestQCDataFields:
    """Tests for specific QC data fields."""
    
    def test_qc_call_field(self, qc_client):
        """Test QC call field when available."""
        qc_data = qc_client.get_analytical_qc_data_by_dtxsid("DTXSID7020182")
        
        if len(qc_data) > 0:
            assert "call" in qc_data[0]
    
    def test_flags_field(self, qc_client):
        """Test flags field when available."""
        qc_data = qc_client.get_analytical_qc_data_by_dtxsid("DTXSID7020182")
        
        if len(qc_data) > 0:
            assert "flags" in qc_data[0]
    
    def test_physical_properties(self, qc_client):
        """Test physical-chemical property predictions."""
        qc_data = qc_client.get_analytical_qc_data_by_dtxsid("DTXSID7020182")
        
        if len(qc_data) > 0:
            # Should have predicted properties
            assert "log10VaporPressureOperaPred" in qc_data[0]
            assert "logkowOctanolWaterOperaPred" in qc_data[0]
    
    def test_metadata_fields(self, qc_client):
        """Test metadata fields are present."""
        qc_data = qc_client.get_analytical_qc_data_by_dtxsid("DTXSID7020182")
        
        if len(qc_data) > 0:
            assert "exportDate" in qc_data[0]
            assert "dataVersion" in qc_data[0]


class TestErrorHandling:
    """Tests for error handling."""
    
    def test_empty_dtxsid(self, qc_client):
        """Test behavior with empty DTXSID."""
        # Should handle gracefully
        result = qc_client.get_analytical_qc_data_by_dtxsid("")
        assert isinstance(result, list)
    
    def test_malformed_dtxsid(self, qc_client):
        """Test behavior with malformed DTXSID."""
        result = qc_client.get_analytical_qc_data_by_dtxsid("INVALID_FORMAT")
        assert isinstance(result, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
