"""
Patch script to add comprehensive test case generation to mock_tests.py
Run this once to enable 50-100 test cases per coding question
"""

import re
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def patch_mock_tests():
    file_path = 'app/routers/mock_tests.py'
    
    print("Reading mock_tests.py...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already patched
    if 'enhance_test_cases' in content:
        print("[OK] File already patched!")
        return
    
    print("Applying patch...")
    
    # Step 1: Add import
    import_pattern = r'from app\.services\.phase6_ai_service import phase6_ai_service'
    import_replacement = 'from app.services.phase6_ai_service import phase6_ai_service\nfrom app.utils.test_case_generator import enhance_test_cases'
    
    content = re.sub(import_pattern, import_replacement, content)
    
    # Step 2: Enhance test case generation
    old_code = """        # Combine for storage
        all_test_cases = visible_tests + hidden_tests
        visible_count = len(visible_tests)
        
        # Ensure minimum test cases
        if not all_test_cases:
            all_test_cases = [
                {"input": "test_input", "output": "expected_output"},
                {"input": "test_input2", "output": "expected_output2"}
            ]
            visible_count = 2
        
        # Store visible_count in the first test case metadata
        if all_test_cases and len(all_test_cases) > 0:
            all_test_cases[0]['_visible_count'] = visible_count"""
    
    new_code = """        # Combine base test cases
        base_test_cases = visible_tests + hidden_tests
        visible_count = len(visible_tests)
        
        # ENHANCE: Generate 50-100 comprehensive test cases
        if base_test_cases and len(base_test_cases) >= 2:
            # Generate comprehensive test cases based on difficulty
            difficulty = coding_data.get('difficulty', 'medium')
            target_count = 100 if difficulty == 'hard' else 75 if difficulty == 'medium' else 50
            
            try:
                all_test_cases = enhance_test_cases(base_test_cases, target_count=target_count)
                print(f"  -> Enhanced coding question: {len(all_test_cases)} total test cases (difficulty: {difficulty})")
            except Exception as e:
                print(f"  [WARNING] Test case generation failed: {e}, using base cases")
                all_test_cases = base_test_cases
        else:
            # Fallback if no base cases
            all_test_cases = [
                {"input": "test_input", "output": "expected_output"},
                {"input": "test_input2", "output": "expected_output2"}
            ]
            visible_count = 2
        
        # Store visible_count in the first test case metadata
        if all_test_cases and len(all_test_cases) > 0:
            all_test_cases[0]['_visible_count'] = visible_count"""
    
    content = content.replace(old_code, new_code)
    
    # Write back
    print("Writing patched file...")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("[SUCCESS] Patch applied successfully!")
    print("Mock tests will now generate 50-100 test cases per coding question")

if __name__ == '__main__':
    try:
        patch_mock_tests()
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
