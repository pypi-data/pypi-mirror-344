import pytest
import numpy as np
from pyamtb.tight_binding_model import (
    calculate_distance,
    hopping_strength,
    get_coupling_strength,
    calculate_all_couplings,
    create_pythtb_model,
    calculate_band_structure,
    adjust_degenerate_bands,
    check_flat_bands
)
from pyamtb.parameters import Parameters
from pyamtb.read_datas import read_poscar


def test_hopping_strength():
    """Test hopping strength calculation"""
    params = Parameters()
    params.t0 = 1.0
    params.t0_distance = 2.0
    params.lambda_ = 1.0
    
    # Test case 1: At reference distance
    distance = 2.0
    strength = hopping_strength(distance)
    assert np.isclose(strength, 1.0)  # Should be equal to t0
    
    # Test case 2: At different distance
    distance = 3.0
    strength = hopping_strength(distance)
    expected = 1.0 * np.exp(-1.0 * (3.0 - 2.0) / 2.0)
    assert np.isclose(strength, expected)

def test_get_coupling_strength():
    """Test coupling strength calculation between two atoms"""
    params = Parameters("tbparas.toml")
    poscar_data = {
        "coordinates": np.array([[0.0, 0.0, 0.0], [0.5, 0.5, 0.5]]),
        "atom_symbols": ["Mn", "Mn"],
        "lattice": np.eye(3)
    }
    
    coupling_values, R_vectors, distance_values = get_coupling_strength(0, 1, poscar_data)
    
    assert isinstance(coupling_values, list)
    assert isinstance(R_vectors, list)
    assert isinstance(distance_values, list)
    assert len(coupling_values) == len(R_vectors) == len(distance_values)

def test_calculate_all_couplings():
    """Test calculation of all couplings"""
    params = Parameters("tbparas.toml")
    poscar_data = {
        "coordinates": np.array([[0.0, 0.0, 0.0], [0.5, 0.5, 0.5], [0.0, 0.5, 0.5]]),
        "atom_symbols": ["Mn", "Mn", "N"],
        "lattice": np.eye(3)
    }
    
    couplings = calculate_all_couplings(poscar_data, ["Mn", "N"])
    
    assert isinstance(couplings, list)
    for coupling in couplings:
        assert "atom1_index" in coupling
        assert "atom2_index" in coupling
        assert "elements" in coupling
        assert "coupling_values" in coupling
        assert "R_vectors" in coupling
        assert "distance_values" in coupling

def test_create_pythtb_model():
    """Test creation of pythtb model"""
    params = Parameters("tbparas.toml")
    try:
        model = create_pythtb_model(params)
        assert model is not None
        assert hasattr(model, '_norb')  # Check if model has number of orbitals
    except ImportError:
        pytest.skip("pythtb package not installed")

def test_calculate_band_structure():
    """Test band structure calculation"""
    params = Parameters("tbparas.toml")
    try:
        model = create_pythtb_model(params)
        calculate_band_structure(model, params)
        # If we get here without error, the test passes
        assert True
    except ImportError:
        pytest.skip("pythtb package not installed")
    except Exception as e:
        pytest.fail(f"Band structure calculation failed: {str(e)}")

def test_adjust_degenerate_bands():
    """Test adjustment of degenerate bands"""
    params = Parameters("tbparas.toml")
    try:
        # Create test data
        evals = np.array([[1.0, 1.0], [1.0, 1.0]])  # Two degenerate bands
        evecs = np.array([[[[1, 0], [0, 1]], [[1, 0], [0, 1]]],
                         [[[0, 1], [1, 0]], [[0, 1], [1, 0]]]])
        model = create_pythtb_model(params)
        
        new_evals, new_evecs = adjust_degenerate_bands(evals, evecs, model)
        
        assert np.array_equal(evals, new_evals)  # Eigenvalues should not change
        assert new_evecs.shape == evecs.shape  # Shape should remain the same
    except ImportError:
        pytest.skip("pythtb package not installed")

def test_check_flat_bands():
    """Test flat band detection"""
    # Create test data with a flat band
    evals = np.array([
        [1.0, 1.0, 1.0, 1.0],  # Flat band
        [0.0, 0.1, 0.2, 0.3]   # Non-flat band
    ])
    
    flat_bands = check_flat_bands(evals)
    
    assert isinstance(flat_bands, list)
    assert len(flat_bands) > 0
    for band in flat_bands:
        assert "band_index" in band
        assert "avg_energy" in band
        assert "std_energy" in band
        assert "k_range" in band 