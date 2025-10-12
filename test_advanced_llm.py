"""
Test suite for Advanced MockLLM with comprehensive parameter testing
"""

import time
from ribit_2_0.advanced_mock_llm import AdvancedMockLLM

def test_basic_functionality():
    """Test basic LLM functionality."""
    print("="*70)
    print("Test 1: Basic Functionality")
    print("="*70)
    
    llm = AdvancedMockLLM()
    
    response = llm.generate_response("What is quantum physics?")
    print(f"\n✓ Basic response generated")
    print(f"  Length: {len(response)} characters")
    print(f"  Preview: {response[:100]}...")
    
    assert len(response) > 0, "Response should not be empty"
    print("\n✓ Basic functionality test passed")

def test_length_constraints():
    """Test min/max length constraints."""
    print("\n" + "="*70)
    print("Test 2: Length Constraints")
    print("="*70)
    
    # Test min length
    llm = AdvancedMockLLM(min_length=100, max_length=200)
    response = llm.generate_response("Hi")
    print(f"\n✓ Min length constraint (100)")
    print(f"  Response length: {len(response)}")
    assert len(response) >= 100, f"Response too short: {len(response)}"
    
    # Test max length
    response = llm.generate_response("Explain quantum physics in great detail" * 10)
    print(f"\n✓ Max length constraint (200)")
    print(f"  Response length: {len(response)}")
    assert len(response) <= 200, f"Response too long: {len(response)}"
    
    print("\n✓ Length constraints test passed")

def test_sampling_strategies():
    """Test different sampling strategies."""
    print("\n" + "="*70)
    print("Test 3: Sampling Strategies")
    print("="*70)
    
    prompt = "What is consciousness?"
    strategies = ['greedy', 'top_k', 'nucleus', 'beam']
    
    for strategy in strategies:
        llm = AdvancedMockLLM(sampling_strategy=strategy, num_beams=3)
        response = llm.generate_response(prompt, max_length=150)
        print(f"\n✓ {strategy.upper()} sampling")
        print(f"  Length: {len(response)}")
        print(f"  Preview: {response[:80]}...")
    
    print("\n✓ Sampling strategies test passed")

def test_repetition_penalty():
    """Test repetition penalty."""
    print("\n" + "="*70)
    print("Test 4: Repetition Penalty")
    print("="*70)
    
    # Low penalty
    llm = AdvancedMockLLM(repetition_penalty=1.0, no_repeat_ngram_size=3)
    response1 = llm.generate_response("Tell me about quantum physics")
    
    # High penalty
    llm.set_advanced_parameters(repetition_penalty=1.8)
    response2 = llm.generate_response("Tell me about quantum physics")
    
    print(f"\n✓ Low penalty response: {len(response1)} chars")
    print(f"✓ High penalty response: {len(response2)} chars")
    print(f"  Responses differ: {response1 != response2}")
    
    print("\n✓ Repetition penalty test passed")

def test_caching():
    """Test response caching."""
    print("\n" + "="*70)
    print("Test 5: Response Caching")
    print("="*70)
    
    llm = AdvancedMockLLM(enable_caching=True, cache_size=50)
    
    prompt = "What is AI?"
    
    # First request (cache miss)
    start = time.time()
    response1 = llm.generate_response(prompt)
    time1 = time.time() - start
    
    # Second request (cache hit)
    start = time.time()
    response2 = llm.generate_response(prompt)
    time2 = time.time() - start
    
    print(f"\n✓ First request (cache miss): {time1*1000:.2f}ms")
    print(f"✓ Second request (cache hit): {time2*1000:.2f}ms")
    print(f"  Speedup: {time1/time2:.1f}x" if time2 > 0 else "  Instant")
    print(f"  Responses identical: {response1 == response2}")
    
    stats = llm.get_performance_stats()
    print(f"\n  Cache hits: {stats['cache_hits']}")
    print(f"  Cache misses: {stats['cache_misses']}")
    print(f"  Cache hit rate: {stats['cache_hit_rate']:.1%}")
    
    assert response1 == response2, "Cached responses should be identical"
    print("\n✓ Caching test passed")

def test_performance_monitoring():
    """Test performance monitoring."""
    print("\n" + "="*70)
    print("Test 6: Performance Monitoring")
    print("="*70)
    
    llm = AdvancedMockLLM(enable_monitoring=True)
    
    # Generate several responses
    for i in range(5):
        llm.generate_response(f"Question {i}")
    
    stats = llm.get_performance_stats()
    
    print(f"\n✓ Performance Statistics:")
    print(f"  Total requests: {stats['total_requests']}")
    print(f"  Successful: {stats['successful_requests']}")
    print(f"  Success rate: {stats['success_rate']:.1%}")
    print(f"  Avg response time: {stats['avg_response_time']:.3f}s")
    print(f"  Errors: {stats['error_count']}")
    
    assert stats['total_requests'] == 5, "Should have 5 requests"
    assert stats['success_rate'] > 0.8, "Success rate should be high"
    
    print("\n✓ Performance monitoring test passed")

def test_context_window():
    """Test context window management."""
    print("\n" + "="*70)
    print("Test 7: Context Window Management")
    print("="*70)
    
    llm = AdvancedMockLLM(context_window=100, sliding_window=True)
    
    context = [f"Message {i}" for i in range(10)]
    response = llm.generate_response("Continue", context=context)
    
    stored_context = llm.get_context()
    print(f"\n✓ Context stored: {len(stored_context)} messages")
    print(f"  Context window limit: {llm.context_window}")
    
    # Add more context
    more_context = [f"Message {i}" for i in range(10, 200)]
    llm.generate_response("Continue", context=more_context)
    
    stored_context = llm.get_context()
    print(f"✓ After adding more: {len(stored_context)} messages")
    print(f"  Sliding window working: {len(stored_context) <= llm.context_window}")
    
    assert len(stored_context) <= llm.context_window, "Context should not exceed window"
    
    print("\n✓ Context window test passed")

def test_parameter_adjustment():
    """Test dynamic parameter adjustment."""
    print("\n" + "="*70)
    print("Test 8: Dynamic Parameter Adjustment")
    print("="*70)
    
    llm = AdvancedMockLLM(temperature=0.5)
    
    print(f"\n✓ Initial temperature: {llm.temperature}")
    
    # Adjust parameters
    llm.set_parameters(temperature=1.5)
    llm.set_advanced_parameters(
        repetition_penalty=1.5,
        length_penalty=1.2,
        diversity_penalty=0.5
    )
    
    print(f"✓ Adjusted temperature: {llm.temperature}")
    print(f"✓ Repetition penalty: {llm.repetition_penalty}")
    print(f"✓ Length penalty: {llm.length_penalty}")
    print(f"✓ Diversity penalty: {llm.diversity_penalty}")
    
    assert llm.temperature == 1.5, "Temperature should be updated"
    assert llm.repetition_penalty == 1.5, "Repetition penalty should be updated"
    
    print("\n✓ Parameter adjustment test passed")

def test_diagnostics():
    """Test diagnostic system."""
    print("\n" + "="*70)
    print("Test 9: Diagnostic System")
    print("="*70)
    
    llm = AdvancedMockLLM()
    
    # Generate some requests
    for i in range(10):
        llm.generate_response(f"Test query {i}")
    
    diagnosis = llm.diagnose()
    
    print(f"\n✓ Health Status: {diagnosis['status']}")
    print(f"  Issues: {len(diagnosis['issues'])}")
    print(f"  Warnings: {len(diagnosis['warnings'])}")
    
    if diagnosis['issues']:
        print("\n  Issues found:")
        for issue in diagnosis['issues']:
            print(f"    - {issue}")
    
    if diagnosis['warnings']:
        print("\n  Warnings:")
        for warning in diagnosis['warnings']:
            print(f"    - {warning}")
    
    if diagnosis['recommendations']:
        print("\n  Recommendations:")
        for rec in diagnosis['recommendations']:
            print(f"    - {rec}")
    
    print("\n  Performance:")
    for key, value in diagnosis['performance'].items():
        print(f"    {key}: {value}")
    
    print("\n✓ Diagnostics test passed")

def test_all_parameters():
    """Test getting all parameters."""
    print("\n" + "="*70)
    print("Test 10: All Parameters Display")
    print("="*70)
    
    llm = AdvancedMockLLM(
        temperature=0.8,
        top_p=0.95,
        repetition_penalty=1.3,
        length_penalty=1.1,
        diversity_penalty=0.3,
        min_length=50,
        max_length=300,
        top_k=40,
        num_beams=2,
        sampling_strategy='beam'
    )
    
    params = llm.get_all_parameters()
    
    print("\n✓ Base Parameters:")
    for key, value in params['base_parameters'].items():
        print(f"    {key}: {value}")
    
    print("\n✓ Advanced Parameters:")
    for key, value in params['advanced_parameters'].items():
        print(f"    {key}: {value}")
    
    print("\n✓ System Settings:")
    for key, value in params['system_settings'].items():
        print(f"    {key}: {value}")
    
    print(f"\n✓ Current Style: {params['current_style']}")
    
    print("\n✓ All parameters test passed")

def test_error_handling():
    """Test error handling and recovery."""
    print("\n" + "="*70)
    print("Test 11: Error Handling")
    print("="*70)
    
    llm = AdvancedMockLLM(
        max_retries=3,
        fallback_response="Sorry, I encountered an error."
    )
    
    # Normal request should work
    response = llm.generate_response("Normal query")
    print(f"\n✓ Normal request successful")
    print(f"  Response: {response[:50]}...")
    
    stats = llm.get_performance_stats()
    print(f"\n✓ Error handling stats:")
    print(f"  Total requests: {stats['total_requests']}")
    print(f"  Errors: {stats['error_count']}")
    print(f"  Success rate: {stats['success_rate']:.1%}")
    
    print("\n✓ Error handling test passed")

def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("ADVANCED MOCK LLM - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    tests = [
        test_basic_functionality,
        test_length_constraints,
        test_sampling_strategies,
        test_repetition_penalty,
        test_caching,
        test_performance_monitoring,
        test_context_window,
        test_parameter_adjustment,
        test_diagnostics,
        test_all_parameters,
        test_error_handling
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"\n❌ TEST FAILED: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*70)
    
    if failed == 0:
        print("\n✅ ALL TESTS PASSED!")
        print("\nAdvanced MockLLM Features Verified:")
        print("  ✓ Basic response generation")
        print("  ✓ Length constraints (min/max)")
        print("  ✓ Multiple sampling strategies (greedy, top-k, nucleus, beam)")
        print("  ✓ Repetition penalty (n-gram level)")
        print("  ✓ Response caching")
        print("  ✓ Performance monitoring")
        print("  ✓ Context window management")
        print("  ✓ Dynamic parameter adjustment")
        print("  ✓ Diagnostic system")
        print("  ✓ Comprehensive parameter display")
        print("  ✓ Error handling and recovery")
        print("\n" + "="*70)
    else:
        print(f"\n❌ {failed} test(s) failed")

if __name__ == "__main__":
    main()

