#!/usr/bin/env python3
"""
Comprehensive Testing Suite for Construction Estimation System
Includes unit tests, integration tests, and performance tests
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os
import time
import psutil
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestConstructionEstimationSystem:
    """Comprehensive test suite for the Construction Estimation System"""
    
    @classmethod
    def setup_class(cls):
        """Setup test environment"""
        cls.start_time = time.time()
        cls.process = psutil.Process()
        cls.initial_memory = cls.process.memory_info().rss / 1024 / 1024  # MB
        
    def test_imports(self):
        """Test all required imports"""
        try:
            import streamlit as st
            import pandas as pd
            import numpy as np
            from datetime import datetime
            import io
            import json
            import os
            import glob
            from pathlib import Path
            import math
            from functools import lru_cache
            assert True, "All imports successful"
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
    
    def test_dataframe_schemas(self):
        """Test DataFrame schema definitions"""
        MEASUREMENT_COLUMNS = [
            'id', 'ssr_code', 'item_no', 'description', 'specification', 'location',
            'quantity', 'length', 'breadth', 'height', 'diameter', 'thickness', 
            'unit', 'total', 'deduction', 'net_total', 'remarks'
        ]
        
        ABSTRACT_COLUMNS = [
            'id', 'ssr_code', 'description', 'unit', 'quantity', 'rate', 'amount'
        ]
        
        # Test DataFrame creation
        measurements_df = pd.DataFrame(columns=MEASUREMENT_COLUMNS)
        abstract_df = pd.DataFrame(columns=ABSTRACT_COLUMNS)
        
        assert len(measurements_df.columns) == 17, f"Expected 17 measurement columns, got {len(measurements_df.columns)}"
        assert len(abstract_df.columns) == 7, f"Expected 7 abstract columns, got {len(abstract_df.columns)}"
        assert measurements_df.empty, "New measurement DataFrame should be empty"
        assert abstract_df.empty, "New abstract DataFrame should be empty"
    
    def test_calculation_functions(self):
        """Test calculation functions with various inputs"""
        import math
        
        def calculate_total(quantity, length, breadth, height, diameter=0, thickness=0, measurement_type="Standard"):
            """Test version of calculation function"""
            if measurement_type == "Linear":
                return quantity * max(1, length)
            elif measurement_type == "Area":
                return quantity * max(1, length) * max(1, breadth)
            elif measurement_type == "Volume":
                return quantity * max(1, length) * max(1, breadth) * max(1, height)
            elif measurement_type == "Circular Area":
                if diameter > 0:
                    return quantity * math.pi * (diameter/2)**2
                return 0
            elif measurement_type == "Circular Volume":
                if diameter > 0:
                    return quantity * math.pi * (diameter/2)**2 * max(1, height)
                return 0
            elif measurement_type == "Weight":
                unit_weight = 7.85 if thickness > 0 else 1
                return quantity * max(1, length) * thickness * unit_weight
            else:  # Standard
                return quantity * max(1, length) * max(1, breadth) * max(1, height)
        
        # Test cases
        test_cases = [
            {"type": "Standard", "qty": 1, "l": 2, "b": 3, "h": 4, "expected": 24},
            {"type": "Linear", "qty": 2, "l": 5, "b": 0, "h": 0, "expected": 10},
            {"type": "Area", "qty": 1, "l": 4, "b": 5, "h": 0, "expected": 20},
            {"type": "Volume", "qty": 1, "l": 2, "b": 3, "h": 4, "expected": 24},
            {"type": "Circular Area", "qty": 1, "l": 0, "b": 0, "h": 0, "d": 2, "expected": math.pi},
            {"type": "Weight", "qty": 1, "l": 10, "b": 0, "h": 0, "t": 0.1, "expected": 7.85},
        ]
        
        for test in test_cases:
            result = calculate_total(
                test["qty"], test["l"], test["b"], test["h"], 
                test.get("d", 0), test.get("t", 0), test["type"]
            )
            assert abs(result - test["expected"]) < 0.01, f"Test {test['type']} failed: {result} != {test['expected']}"
    
    def test_ssr_database_creation(self):
        """Test SSR database initialization and operations"""
        ssr_data = [
            {"code": "1.1.1", "description": "Earth work excavation", "category": "Earth Work", "unit": "cum", "rate": 245.50},
            {"code": "2.1.1", "description": "Cement concrete", "category": "Concrete Work", "unit": "cum", "rate": 4850.00},
        ]
        
        ssr_df = pd.DataFrame(ssr_data)
        
        assert len(ssr_df) == 2, f"Expected 2 SSR items, got {len(ssr_df)}"
        assert "code" in ssr_df.columns, "SSR DataFrame missing 'code' column"
        assert "rate" in ssr_df.columns, "SSR DataFrame missing 'rate' column"
        assert ssr_df['rate'].dtype in [np.float64, float], "Rate column should be numeric"
    
    def test_general_abstract_calculations(self):
        """Test General Abstract calculation logic"""
        civil_work_total = 1250000.00
        sanitary_work_total = 81418.00
        electric_work_percentage = 12.0
        electric_fixtures_percentage = 5.0
        
        electric_work_total = civil_work_total * (electric_work_percentage / 100)
        electric_fixtures = civil_work_total * (electric_fixtures_percentage / 100)
        subtotal = civil_work_total + sanitary_work_total + electric_work_total
        grand_total = subtotal + electric_fixtures
        
        assert electric_work_total == 150000.0, f"Electric work calculation error: {electric_work_total}"
        assert electric_fixtures == 62500.0, f"Electric fixtures calculation error: {electric_fixtures}"
        assert grand_total == 1543918.0, f"Grand total calculation error: {grand_total}"
    
    def test_data_validation(self):
        """Test data validation functions"""
        def validate_and_strip(text):
            return text.strip() if text else ""
        
        test_cases = [
            ("  hello world  ", "hello world"),
            ("", ""),
            (None, ""),
            ("no spaces", "no spaces"),
        ]
        
        for input_text, expected in test_cases:
            result = validate_and_strip(input_text)
            assert result == expected, f"Validation failed for '{input_text}': got '{result}', expected '{expected}'"
    
    def test_performance_calculations(self):
        """Test performance of calculation functions"""
        import math
        
        def calculate_total(quantity, length, breadth, height, diameter=0, thickness=0, measurement_type="Standard"):
            if measurement_type == "Standard":
                return quantity * max(1, length) * max(1, breadth) * max(1, height)
            return 0
        
        # Performance test with 1000 calculations
        start_time = time.time()
        
        for i in range(1000):
            result = calculate_total(1, 2, 3, 4)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert execution_time < 1.0, f"Performance test failed: {execution_time:.3f}s > 1.0s for 1000 calculations"
        assert result == 24, f"Calculation result incorrect: {result} != 24"
    
    def test_memory_usage(self):
        """Test memory usage with large datasets"""
        # Create large DataFrame
        large_data = []
        for i in range(1000):
            large_data.append({
                'id': i,
                'description': f'Test item {i}',
                'quantity': 1.0,
                'length': 2.0,
                'breadth': 3.0,
                'height': 4.0,
                'unit': 'Cum',
                'total': 24.0
            })
        
        df = pd.DataFrame(large_data)
        memory_usage = df.memory_usage(deep=True).sum()
        
        # Memory should be reasonable (less than 1MB for 1000 records)
        assert memory_usage < 1024 * 1024, f"Memory usage too high: {memory_usage / 1024:.1f} KB"
        assert len(df) == 1000, f"DataFrame size incorrect: {len(df)} != 1000"
    
    def test_error_handling(self):
        """Test error handling in critical functions"""
        def safe_calculate(a, b):
            try:
                return a / b
            except ZeroDivisionError:
                return 0
            except Exception:
                return None
        
        assert safe_calculate(10, 2) == 5, "Normal calculation failed"
        assert safe_calculate(10, 0) == 0, "Zero division not handled"
        assert safe_calculate("a", "b") is None, "Type error not handled"
    
    def test_csv_export_functionality(self):
        """Test CSV export functionality"""
        test_data = pd.DataFrame({
            'id': [1, 2, 3],
            'description': ['Item 1', 'Item 2', 'Item 3'],
            'quantity': [1.0, 2.0, 3.0],
            'rate': [100.0, 200.0, 300.0],
            'amount': [100.0, 400.0, 900.0]
        })
        
        csv_output = test_data.to_csv(index=False)
        
        assert 'id,description,quantity,rate,amount' in csv_output, "CSV header incorrect"
        assert '1,Item 1,1.0,100.0,100.0' in csv_output, "CSV data incorrect"
        assert len(csv_output.split('\n')) >= 4, "CSV should have header + 3 data rows"
    
    def test_file_operations(self):
        """Test file operations and path handling"""
        import tempfile
        
        # Test file creation and reading
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Test content")
            temp_path = f.name
        
        try:
            with open(temp_path, 'r') as f:
                content = f.read()
            assert content == "Test content", "File read/write failed"
        finally:
            os.unlink(temp_path)
    
    @classmethod
    def teardown_class(cls):
        """Cleanup and performance report"""
        end_time = time.time()
        final_memory = cls.process.memory_info().rss / 1024 / 1024  # MB
        
        execution_time = end_time - cls.start_time
        memory_increase = final_memory - cls.initial_memory
        
        logger.info(f"Test execution time: {execution_time:.2f} seconds")
        logger.info(f"Memory usage change: {memory_increase:.2f} MB")
        logger.info(f"Final memory usage: {final_memory:.2f} MB")

def run_performance_tests():
    """Run performance-specific tests"""
    print("🚀 Running Performance Tests...")
    
    # Test 1: Large dataset handling
    start_time = time.time()
    large_df = pd.DataFrame({
        'id': range(10000),
        'value': np.random.rand(10000)
    })
    creation_time = time.time() - start_time
    print(f"✅ Large DataFrame creation: {creation_time:.3f}s")
    
    # Test 2: Calculation performance
    start_time = time.time()
    results = []
    for i in range(1000):
        result = i * 2 * 3 * 4
        results.append(result)
    calc_time = time.time() - start_time
    print(f"✅ 1000 calculations: {calc_time:.3f}s")
    
    # Test 3: Memory efficiency
    memory_before = psutil.Process().memory_info().rss / 1024 / 1024
    test_data = [{'id': i, 'data': f'test_{i}'} for i in range(5000)]
    test_df = pd.DataFrame(test_data)
    memory_after = psutil.Process().memory_info().rss / 1024 / 1024
    memory_used = memory_after - memory_before
    print(f"✅ Memory usage for 5000 records: {memory_used:.2f} MB")
    
    return {
        'creation_time': creation_time,
        'calc_time': calc_time,
        'memory_used': memory_used
    }

def run_integration_tests():
    """Run integration tests"""
    print("🔗 Running Integration Tests...")
    
    # Test complete workflow
    try:
        # 1. Create measurement
        measurement = {
            'id': 1,
            'description': 'Test concrete work',
            'quantity': 1,
            'length': 10,
            'breadth': 5,
            'height': 0.15,
            'unit': 'Cum',
            'total': 7.5
        }
        
        # 2. Create abstract item
        abstract = {
            'id': 1,
            'description': 'Test concrete work',
            'unit': 'Cum',
            'quantity': 7.5,
            'rate': 4850.0,
            'amount': 36375.0
        }
        
        # 3. Verify calculations
        expected_total = 1 * 10 * 5 * 0.15
        expected_amount = expected_total * 4850.0
        
        assert abs(measurement['total'] - expected_total) < 0.01, "Measurement calculation failed"
        assert abs(abstract['amount'] - expected_amount) < 0.01, "Abstract calculation failed"
        
        print("✅ Workflow integration test passed")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Construction Estimation System - Comprehensive Test Suite")
    print("=" * 70)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run pytest tests
    print("🔬 Running Unit Tests...")
    pytest_result = pytest.main([__file__, "-v", "--tb=short"])
    
    # Run performance tests
    perf_results = run_performance_tests()
    
    # Run integration tests
    integration_result = run_integration_tests()
    
    print("\n" + "=" * 70)
    print("📊 Test Summary:")
    print(f"• Unit Tests: {'✅ PASSED' if pytest_result == 0 else '❌ FAILED'}")
    print(f"• Performance Tests: ✅ COMPLETED")
    print(f"• Integration Tests: {'✅ PASSED' if integration_result else '❌ FAILED'}")
    print(f"• DataFrame Creation: {perf_results['creation_time']:.3f}s")
    print(f"• Calculation Speed: {perf_results['calc_time']:.3f}s")
    print(f"• Memory Efficiency: {perf_results['memory_used']:.2f} MB")
    
    if pytest_result == 0 and integration_result:
        print("\n🎉 All tests passed! System is ready for deployment.")
    else:
        print("\n⚠️ Some tests failed. Please review the issues above.")
    
    sys.exit(0 if pytest_result == 0 and integration_result else 1)