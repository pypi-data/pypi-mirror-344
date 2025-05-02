import pytest
import os
from dotenv import load_dotenv

from synthex import Synthex
from synthex.exceptions import ConfigurationError


@pytest.mark.unit
def test_synthex_instantiation_apikey_in_env_success():
    """
    This test ensures that the Synthex class can be successfully instantiated without raising
    an exception when the required API key is available in the environment and not explicitly
    passed as an argument upon instantiation. If instantiation fails, the test will fail.
    """
    
    # Check if the API_KEY environment variable is set, otherwise skip the test.
    api_key = os.getenv("API_KEY")
    if api_key is None:
        pytest.skip("API_KEY environment variable not set. Skipping test.")
        
    try:
        Synthex()
    except Exception:
        pytest.fail("Synthex instantiation failed with API key in environment variable.")


@pytest.mark.unit
def test_synthex_instantiation_apikey_in_argument_success():
    """
    This test ensures that the Synthex class can be successfully instantiated without raising
    an exception when the required API key is not present in the environment variables, but is 
    passed explicitly at instantiation. If instantiation fails, the test will fail.
    """
    
    # Remove .env file, so the API KEY does not get picked up by Synthex.
    os.remove(".env")
    # Remove the API_KEY environment variable if it exists.
    if "API_KEY" in os.environ:
        del os.environ["API_KEY"]
    # Reload the enviornment variables.
    load_dotenv()
    
    # Check that the API_KEY environment variable is not set, othwise skip the test.
    api_key = os.getenv("API_KEY")
    if api_key is not None:
        pytest.skip("API_KEY environment variable set. Skipping test.")
    
    try:
        Synthex(api_key="test_api_key")
    except Exception:
        pytest.fail("Synthex instantiation failed with API key passed as an argument.")


@pytest.mark.unit
def test_synthex_instantiation_apikey_absent_failure():
    """
    This test ensures that the Synthex class cannot be instantiated when the required API key 
    is not present in the environment variables and is not passed as an argument. If instantiation 
    succeeds, the test will fail.
    """
    
    # Remove .env file, so the API KEY does not get picked up by Synthex.
    os.remove(".env")
    # Remove the API_KEY environment variable if it exists.
    if "API_KEY" in os.environ:
        del os.environ["API_KEY"]
    # Reload the enviornment variables.
    load_dotenv()
    
    # Check that the API_KEY environment variable is not set, othwise skip the test.
    api_key = os.getenv("API_KEY")
    if api_key is not None:
        pytest.skip("API_KEY environment variable set. Skipping test.")
        
    with pytest.raises(ConfigurationError):
        # Attempt to instantiate Synthex without passing the API key argument.
        Synthex()
