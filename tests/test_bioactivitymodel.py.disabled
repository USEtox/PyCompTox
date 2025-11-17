"""
Tests for BioactivityModel API client.

This test suite validates the functionality of the BioactivityModel class,
including model predictions retrieval and error handling.
"""

import pytest
import time
from pycomptox import BioactivityModel


@pytest.fixture
def model_client():
    """Create a BioactivityModel client instance for testing."""
    return BioactivityModel()


class TestGetToxcastModelByDtxsid:
    """Tests for get_toxcast_model_by_dtxsid method."""
    
    def test_get_models_for_bisphenol_a(self, model_client):
        """Test retrieving all models for bisphenol A (DTXSID7020182)."""
        models = model_client.get_toxcast_model_by_dtxsid("DTXSID7020182")
        
        assert isinstance(models, list)
        assert len(models) > 0
        
        # Check structure of first result
        first_model = models[0]
        assert "dtxsid" in first_model
        assert "model" in first_model
        assert first_model["dtxsid"] == "DTXSID7020182"
    
    def test_model_result_structure(self, model_client):
        """Test that model results contain expected fields."""
        models = model_client.get_toxcast_model_by_dtxsid("DTXSID7020182")
        
        assert len(models) > 0
        model = models[0]
        
        # Verify all expected fields are present
        expected_fields = [
            "id", "dtxsid", "model", "receptor",
            "agonist", "antagonist", "binding", "modelDesc"
        ]
        for field in expected_fields:
            assert field in model, f"Missing field: {field}"
    
    def test_cerapp_model_included(self, model_client):
        """Test that CERAPP model is included in results."""
        models = model_client.get_toxcast_model_by_dtxsid("DTXSID7020182")
        
        model_names = [m["model"] for m in models]
        assert "CERAPP" in model_names, "CERAPP model should be present"
    
    def test_invalid_dtxsid(self, model_client):
        """Test behavior with invalid DTXSID."""
        # API might return empty list or error for invalid DTXSID
        result = model_client.get_toxcast_model_by_dtxsid("DTXSID0000000")
        assert isinstance(result, list)


class TestGetToxcastModelByDtxsidAndModel:
    """Tests for get_toxcast_model_by_dtxsid_and_model method."""
    
    def test_get_cerapp_model(self, model_client):
        """Test retrieving CERAPP model specifically."""
        models = model_client.get_toxcast_model_by_dtxsid_and_model(
            "DTXSID7020182", "CERAPP"
        )
        
        assert isinstance(models, list)
        assert len(models) > 0
        
        # Verify all results are CERAPP models
        for model in models:
            assert model["model"] == "CERAPP"
            assert model["dtxsid"] == "DTXSID7020182"
    
    def test_cerapp_predictions_structure(self, model_client):
        """Test CERAPP predictions have expected structure."""
        models = model_client.get_toxcast_model_by_dtxsid_and_model(
            "DTXSID7020182", "CERAPP"
        )
        
        assert len(models) > 0
        model = models[0]
        
        # CERAPP should have agonist, antagonist, and binding predictions
        assert "agonist" in model
        assert "antagonist" in model
        assert "binding" in model
        assert "receptor" in model
    
    def test_compara_model(self, model_client):
        """Test retrieving CoMPARA (androgen receptor) model."""
        models = model_client.get_toxcast_model_by_dtxsid_and_model(
            "DTXSID7020182", "CoMPARA"
        )
        
        assert isinstance(models, list)
        # CoMPARA may or may not be available for all chemicals
        if len(models) > 0:
            assert models[0]["model"] == "CoMPARA"
    
    def test_filtered_results(self, model_client):
        """Test that filtered results contain only requested model."""
        # Get all models
        all_models = model_client.get_toxcast_model_by_dtxsid("DTXSID7020182")
        
        # Get filtered models
        cerapp_models = model_client.get_toxcast_model_by_dtxsid_and_model(
            "DTXSID7020182", "CERAPP"
        )
        
        # Filtered should be subset of all
        assert len(cerapp_models) <= len(all_models)
        
        # All filtered results should be CERAPP
        for model in cerapp_models:
            assert model["model"] == "CERAPP"


class TestClientFunctionality:
    """Tests for general client functionality."""
    
    def test_client_initialization(self):
        """Test client can be initialized with and without API key."""
        # Without API key (uses config)
        client1 = BioactivityModel()
        assert client1.base_url == "https://comptox.epa.gov/ctx-api/"
        
        # With API key
        client2 = BioactivityModel(api_key="test_key")
        assert client2.api_key == "test_key"
    
    def test_rate_limiting(self, model_client):
        """Test that rate limiting is applied between requests."""
        start_time = time.time()
        
        # Make multiple requests
        model_client.get_toxcast_model_by_dtxsid("DTXSID7020182")
        model_client.get_toxcast_model_by_dtxsid("DTXSID7020182")
        
        elapsed = time.time() - start_time
        
        # Should take at least min_request_interval between requests
        # (0.1 seconds = 100ms minimum between requests)
        assert elapsed >= 0.1
    
    def test_different_chemicals(self, model_client):
        """Test retrieving models for different chemicals."""
        # Test with two different chemicals
        models1 = model_client.get_toxcast_model_by_dtxsid("DTXSID7020182")  # BPA
        models2 = model_client.get_toxcast_model_by_dtxsid("DTXSID5020064")  # Another chemical
        
        assert isinstance(models1, list)
        assert isinstance(models2, list)
        
        # Both should have results
        if len(models1) > 0 and len(models2) > 0:
            assert models1[0]["dtxsid"] != models2[0]["dtxsid"]


class TestErrorHandling:
    """Tests for error handling."""
    
    def test_invalid_api_endpoint(self, model_client):
        """Test handling of API errors."""
        # This should work or return empty list, not crash
        result = model_client.get_toxcast_model_by_dtxsid("INVALID")
        assert isinstance(result, list)
    
    def test_empty_model_name(self, model_client):
        """Test behavior with empty model name."""
        # Should handle gracefully
        result = model_client.get_toxcast_model_by_dtxsid_and_model(
            "DTXSID7020182", ""
        )
        assert isinstance(result, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
