from ontology_tools import hello


def test_hello():
    """Test that the hello function returns the expected greeting."""
    result = hello()
    assert result == "Hello from ontology-tools!"
