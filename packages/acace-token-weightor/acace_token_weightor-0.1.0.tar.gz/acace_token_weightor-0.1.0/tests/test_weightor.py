"""
Tests for the acace_token_weightor module.
"""

import unittest
from acace_token_weightor import TokenWeightor, assign_weights


class TestTokenWeightor(unittest.TestCase):
    """Test cases for the TokenWeightor class."""
    
    def setUp(self):
        """Set up test data."""
        self.tokens = ["The", "quick", "brown", "fox", "jumped", "over", "the", "lazy", "dog", "."]
        self.context = "The quick brown fox jumped over the lazy dog."
    
    def test_tfidf_weighting(self):
        """Test TF-IDF weighting strategy."""
        weightor = TokenWeightor(strategy="tfidf")
        weighted_tokens = weightor.assign_weights(self.tokens, self.context)
        
        # Basic validation
        self.assertEqual(len(weighted_tokens), len(self.tokens))
        
        # Check all tokens have weights between 0 and 1
        for item in weighted_tokens:
            self.assertIsInstance(item["token"], str)
            self.assertIsInstance(item["weight"], float)
            self.assertGreaterEqual(item["weight"], 0.0)
            self.assertLessEqual(item["weight"], 1.0)
        
        # Check stopwords have lower weights
        the_weight = next(item["weight"] for item in weighted_tokens if item["token"].lower() == "the")
        fox_weight = next(item["weight"] for item in weighted_tokens if item["token"].lower() == "fox")
        self.assertLess(the_weight, fox_weight)
    
    def test_pos_weighting_fallback(self):
        """Test POS weighting strategy without spaCy (fallback)."""
        weightor = TokenWeightor(strategy="pos", use_spacy=False)
        weighted_tokens = weightor.assign_weights(self.tokens, self.context)
        
        # Basic validation
        self.assertEqual(len(weighted_tokens), len(self.tokens))
        
        # Check all tokens have weights between 0 and 1
        for item in weighted_tokens:
            self.assertIsInstance(item["token"], str)
            self.assertIsInstance(item["weight"], float)
            self.assertGreaterEqual(item["weight"], 0.0)
            self.assertLessEqual(item["weight"], 1.0)
            
            # Check metadata
            self.assertIn("pos", item["metadata"])
            self.assertIn("estimated", item["metadata"])
            self.assertTrue(item["metadata"]["estimated"])
    
    def test_custom_weighting(self):
        """Test custom weighting strategy."""
        custom_weights = {
            "quick": 0.9,
            "fox": 0.8,
            "lazy": 0.7,
        }
        
        weightor = TokenWeightor(strategy="custom", custom_weights=custom_weights)
        weighted_tokens = weightor.assign_weights(self.tokens)
        
        # Basic validation
        self.assertEqual(len(weighted_tokens), len(self.tokens))
        
        # Check tokens with custom weights
        quick_item = next(item for item in weighted_tokens if item["token"] == "quick")
        fox_item = next(item for item in weighted_tokens if item["token"] == "fox")
        lazy_item = next(item for item in weighted_tokens if item["token"] == "lazy")
        
        self.assertAlmostEqual(quick_item["weight"], 0.9)
        self.assertAlmostEqual(fox_item["weight"], 0.8)
        self.assertAlmostEqual(lazy_item["weight"], 0.7)
        
        # Check tokens without custom weights have default weight (0.5 before normalization)
        dog_item = next(item for item in weighted_tokens if item["token"] == "dog")
        self.assertNotEqual(dog_item["weight"], 0.0)
    
    def test_hybrid_weighting(self):
        """Test hybrid weighting strategy."""
        weightor = TokenWeightor(
            strategy="hybrid",
            use_spacy=False,
            tfidf_factor=0.7,
            pos_factor=0.3
        )
        weighted_tokens = weightor.assign_weights(self.tokens, self.context)
        
        # Basic validation
        self.assertEqual(len(weighted_tokens), len(self.tokens))
        
        # Check metadata includes both strategies
        for item in weighted_tokens:
            self.assertIn("tfidf_weight", item["metadata"])
            self.assertIn("pos_weight", item["metadata"])
            self.assertIn("tfidf_factor", item["metadata"])
            self.assertIn("pos_factor", item["metadata"])
            
            # Check factors are correct
            self.assertEqual(item["metadata"]["tfidf_factor"], 0.7)
            self.assertEqual(item["metadata"]["pos_factor"], 0.3)
    
    def test_normalize_weights(self):
        """Test weight normalization."""
        # Create a weightor with custom range
        weightor = TokenWeightor(min_weight=0.2, max_weight=0.8)
        weighted_tokens = weightor.assign_weights(self.tokens, self.context)
        
        # Check weights are within the custom range
        for item in weighted_tokens:
            self.assertGreaterEqual(item["weight"], 0.2)
            self.assertLessEqual(item["weight"], 0.8)
    
    def test_empty_tokens(self):
        """Test handling of empty token list."""
        weightor = TokenWeightor()
        weighted_tokens = weightor.assign_weights([])
        self.assertEqual(weighted_tokens, [])
    
    def test_invalid_strategy(self):
        """Test handling of invalid weighting strategy."""
        with self.assertRaises(ValueError):
            TokenWeightor(strategy="invalid_strategy")


class TestAssignWeights(unittest.TestCase):
    """Test cases for the assign_weights function."""
    
    def test_function_interface(self):
        """Test the function interface with various options."""
        tokens = ["The", "quick", "brown", "fox"]
        
        # Default options
        weighted_tokens = assign_weights(tokens)
        self.assertEqual(len(weighted_tokens), len(tokens))
        
        # Custom options
        weighted_tokens = assign_weights(
            tokens,
            strategy="tfidf",
            min_weight=0.1,
            max_weight=0.9
        )
        
        # Check weights are within the custom range
        for item in weighted_tokens:
            self.assertGreaterEqual(item["weight"], 0.1)
            self.assertLessEqual(item["weight"], 0.9)


if __name__ == "__main__":
    unittest.main()
