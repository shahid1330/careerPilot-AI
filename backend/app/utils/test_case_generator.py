"""
Comprehensive Test Case Generator for Coding Questions
Generates 50-100 test cases including edge cases, boundary cases, and stress tests
"""

import random
import string
from typing import List, Dict, Any


class TestCaseGenerator:
    """Generates comprehensive test cases for coding problems"""
    
    @staticmethod
    def generate_comprehensive_test_cases(
        base_test_cases: List[Dict[str, str]],
        problem_type: str = "general",
        target_count: int = 50
    ) -> List[Dict[str, str]]:
        """
        Generate comprehensive test cases from base examples.
        
        Args:
            base_test_cases: 3-5 sample test cases from AI
            problem_type: Type of problem (array, string, math, tree, graph, etc.)
            target_count: Target number of test cases to generate (default 50)
            
        Returns:
            List of test cases with input/output
        """
        
        if not base_test_cases or len(base_test_cases) < 1:
            return base_test_cases
        
        # Start with base test cases (visible)
        all_test_cases = base_test_cases.copy()
        
        # Analyze base cases to understand the pattern
        analyzer = TestCaseAnalyzer(base_test_cases)
        pattern = analyzer.detect_pattern()
        
        # Generate different categories of test cases
        generated = []
        
        # Category 1: Edge Cases (10-15 cases)
        edge_cases = TestCaseGenerator._generate_edge_cases(pattern, 12)
        generated.extend(edge_cases)
        
        # Category 2: Boundary Cases (10-15 cases)
        boundary_cases = TestCaseGenerator._generate_boundary_cases(pattern, 12)
        generated.extend(boundary_cases)
        
        # Category 3: Normal Cases with variations (15-20 cases)
        normal_cases = TestCaseGenerator._generate_normal_variations(base_test_cases, pattern, 15)
        generated.extend(normal_cases)
        
        # Category 4: Large Input Cases (5-10 cases)
        large_cases = TestCaseGenerator._generate_large_inputs(pattern, 8)
        generated.extend(large_cases)
        
        # Category 5: Random Valid Cases (remaining to reach target)
        remaining = max(0, target_count - len(all_test_cases) - len(generated))
        random_cases = TestCaseGenerator._generate_random_cases(pattern, remaining)
        generated.extend(random_cases)
        
        # Combine all
        all_test_cases.extend(generated)
        
        # Shuffle hidden test cases (keep first 3 as visible)
        visible = all_test_cases[:3]
        hidden = all_test_cases[3:]
        random.shuffle(hidden)
        
        final_cases = visible + hidden[:target_count - 3]
        
        print(f"✓ Generated {len(final_cases)} total test cases ({len(visible)} visible, {len(final_cases) - len(visible)} hidden)")
        
        return final_cases
    
    @staticmethod
    def _generate_edge_cases(pattern: Dict[str, Any], count: int) -> List[Dict[str, str]]:
        """Generate edge cases based on problem pattern"""
        edge_cases = []
        
        input_type = pattern.get('input_type', 'mixed')
        
        # Common edge cases
        if input_type in ['array', 'list']:
            # Empty array
            edge_cases.append({'input': '[]', 'output': TestCaseGenerator._compute_output('[]', pattern)})
            # Single element
            edge_cases.append({'input': '[1]', 'output': TestCaseGenerator._compute_output('[1]', pattern)})
            # Two elements
            edge_cases.append({'input': '[1, 2]', 'output': TestCaseGenerator._compute_output('[1, 2]', pattern)})
            # All same elements
            edge_cases.append({'input': '[5, 5, 5, 5]', 'output': TestCaseGenerator._compute_output('[5, 5, 5, 5]', pattern)})
            # Negative numbers
            edge_cases.append({'input': '[-1, -5, -10]', 'output': TestCaseGenerator._compute_output('[-1, -5, -10]', pattern)})
            
        elif input_type == 'string':
            # Empty string
            edge_cases.append({'input': '""', 'output': TestCaseGenerator._compute_output('""', pattern)})
            # Single character
            edge_cases.append({'input': '"a"', 'output': TestCaseGenerator._compute_output('"a"', pattern)})
            # All same character
            edge_cases.append({'input': '"aaaa"', 'output': TestCaseGenerator._compute_output('"aaaa"', pattern)})
            # Special characters
            edge_cases.append({'input': '"@#$%"', 'output': TestCaseGenerator._compute_output('"@#$%"', pattern)})
            
        elif input_type == 'number':
            # Zero
            edge_cases.append({'input': '0', 'output': TestCaseGenerator._compute_output('0', pattern)})
            # Negative
            edge_cases.append({'input': '-100', 'output': TestCaseGenerator._compute_output('-100', pattern)})
            # Large number
            edge_cases.append({'input': '1000000', 'output': TestCaseGenerator._compute_output('1000000', pattern)})
        
        # Fill remaining with variations
        while len(edge_cases) < count:
            edge_cases.append(TestCaseGenerator._generate_random_edge_case(pattern))
        
        return edge_cases[:count]
    
    @staticmethod
    def _generate_boundary_cases(pattern: Dict[str, Any], count: int) -> List[Dict[str, str]]:
        """Generate boundary test cases"""
        boundary_cases = []
        
        input_type = pattern.get('input_type', 'mixed')
        
        if input_type in ['array', 'list']:
            # Minimum size
            boundary_cases.append({'input': '[1]', 'output': TestCaseGenerator._compute_output('[1]', pattern)})
            # Maximum reasonable size
            large_arr = str(list(range(100)))
            boundary_cases.append({'input': large_arr, 'output': TestCaseGenerator._compute_output(large_arr, pattern)})
            # All zeros
            boundary_cases.append({'input': '[0, 0, 0, 0]', 'output': TestCaseGenerator._compute_output('[0, 0, 0, 0]', pattern)})
            
        elif input_type == 'string':
            # Single char
            boundary_cases.append({'input': '"x"', 'output': TestCaseGenerator._compute_output('"x"', pattern)})
            # Long string
            long_str = '"' + 'a' * 100 + '"'
            boundary_cases.append({'input': long_str, 'output': TestCaseGenerator._compute_output(long_str, pattern)})
        
        elif input_type == 'number':
            # Min value
            boundary_cases.append({'input': '-2147483648', 'output': TestCaseGenerator._compute_output('-2147483648', pattern)})
            # Max value
            boundary_cases.append({'input': '2147483647', 'output': TestCaseGenerator._compute_output('2147483647', pattern)})
        
        # Fill remaining
        while len(boundary_cases) < count:
            boundary_cases.append(TestCaseGenerator._generate_random_boundary_case(pattern))
        
        return boundary_cases[:count]
    
    @staticmethod
    def _generate_normal_variations(base_cases: List[Dict[str, str]], pattern: Dict[str, Any], count: int) -> List[Dict[str, str]]:
        """Generate normal test cases with variations"""
        variations = []
        
        for _ in range(count):
            # Pick a random base case and modify it slightly
            base = random.choice(base_cases)
            varied = TestCaseGenerator._vary_test_case(base, pattern)
            variations.append(varied)
        
        return variations
    
    @staticmethod
    def _generate_large_inputs(pattern: Dict[str, Any], count: int) -> List[Dict[str, str]]:
        """Generate large input test cases for stress testing"""
        large_cases = []
        
        input_type = pattern.get('input_type', 'mixed')
        
        for size in [100, 500, 1000, 5000, 10000]:
            if len(large_cases) >= count:
                break
                
            if input_type in ['array', 'list']:
                large_input = str([random.randint(-1000, 1000) for _ in range(min(size, 1000))])
                large_cases.append({
                    'input': large_input,
                    'output': TestCaseGenerator._compute_output(large_input, pattern)
                })
            elif input_type == 'string':
                large_input = '"' + ''.join(random.choices(string.ascii_letters, k=min(size, 1000))) + '"'
                large_cases.append({
                    'input': large_input,
                    'output': TestCaseGenerator._compute_output(large_input, pattern)
                })
            elif input_type == 'number':
                large_input = str(random.randint(1000, 100000))
                large_cases.append({
                    'input': large_input,
                    'output': TestCaseGenerator._compute_output(large_input, pattern)
                })
        
        return large_cases[:count]
    
    @staticmethod
    def _generate_random_cases(pattern: Dict[str, Any], count: int) -> List[Dict[str, str]]:
        """Generate random valid test cases"""
        random_cases = []
        
        for _ in range(count):
            random_cases.append(TestCaseGenerator._generate_random_test_case(pattern))
        
        return random_cases
    
    @staticmethod
    def _compute_output(input_str: str, pattern: Dict[str, Any]) -> str:
        """
        Compute expected output for a given input.
        This is a simplified version - in production, you'd run the solution code.
        For now, we use pattern matching and heuristics.
        """
        # Simplified output generation
        # In production: execute reference solution here
        
        problem_category = pattern.get('category', 'unknown')
        
        # For demo: generate reasonable outputs based on category
        if 'sum' in problem_category.lower() or 'add' in problem_category.lower():
            try:
                arr = eval(input_str)
                return str(sum(arr))
            except:
                return "0"
        
        elif 'length' in problem_category.lower() or 'count' in problem_category.lower():
            try:
                obj = eval(input_str)
                return str(len(obj))
            except:
                return "0"
        
        elif 'reverse' in problem_category.lower():
            try:
                obj = eval(input_str)
                if isinstance(obj, list):
                    return str(obj[::-1])
                elif isinstance(obj, str):
                    return f'"{obj[::-1]}"'
            except:
                return input_str
        
        elif 'max' in problem_category.lower() or 'maximum' in problem_category.lower():
            try:
                arr = eval(input_str)
                return str(max(arr))
            except:
                return "0"
        
        elif 'min' in problem_category.lower() or 'minimum' in problem_category.lower():
            try:
                arr = eval(input_str)
                return str(min(arr))
            except:
                return "0"
        
        # Default: mirror input or use pattern-based output
        sample_output = pattern.get('sample_output', input_str)
        return sample_output
    
    @staticmethod
    def _vary_test_case(base_case: Dict[str, str], pattern: Dict[str, Any]) -> Dict[str, str]:
        """Create a variation of an existing test case"""
        try:
            input_obj = eval(base_case['input'])
            
            if isinstance(input_obj, list):
                # Modify array: change size, values, or order
                variation = input_obj.copy()
                random.shuffle(variation)
                if random.random() > 0.5:
                    variation.append(random.randint(-100, 100))
                varied_input = str(variation)
            elif isinstance(input_obj, str):
                # Modify string: change characters or length
                varied = input_obj + random.choice(string.ascii_letters)
                varied_input = f'"{varied}"'
            elif isinstance(input_obj, int):
                # Modify number: scale or shift
                varied_input = str(input_obj + random.randint(-10, 10))
            else:
                varied_input = base_case['input']
            
            return {
                'input': varied_input,
                'output': TestCaseGenerator._compute_output(varied_input, pattern)
            }
        except:
            return base_case
    
    @staticmethod
    def _generate_random_test_case(pattern: Dict[str, Any]) -> Dict[str, str]:
        """Generate a completely random test case"""
        input_type = pattern.get('input_type', 'array')
        
        if input_type in ['array', 'list']:
            size = random.randint(1, 50)
            random_arr = [random.randint(-100, 100) for _ in range(size)]
            input_str = str(random_arr)
        elif input_type == 'string':
            length = random.randint(1, 50)
            random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            input_str = f'"{random_str}"'
        elif input_type == 'number':
            input_str = str(random.randint(-1000, 1000))
        else:
            input_str = str(random.randint(1, 100))
        
        return {
            'input': input_str,
            'output': TestCaseGenerator._compute_output(input_str, pattern)
        }
    
    @staticmethod
    def _generate_random_edge_case(pattern: Dict[str, Any]) -> Dict[str, str]:
        """Generate a random edge case"""
        edge_inputs = ['[]', '[0]', '""', '"a"', '0', '-1', '1']
        input_str = random.choice(edge_inputs)
        return {
            'input': input_str,
            'output': TestCaseGenerator._compute_output(input_str, pattern)
        }
    
    @staticmethod
    def _generate_random_boundary_case(pattern: Dict[str, Any]) -> Dict[str, str]:
        """Generate a random boundary case"""
        boundary_values = [
            '[' + ', '.join([str(i) for i in range(100)]) + ']',
            '10000',
            '-10000',
            '"' + 'x' * 100 + '"'
        ]
        input_str = random.choice(boundary_values)
        return {
            'input': input_str,
            'output': TestCaseGenerator._compute_output(input_str, pattern)
        }


class TestCaseAnalyzer:
    """Analyzes base test cases to understand patterns"""
    
    def __init__(self, test_cases: List[Dict[str, str]]):
        self.test_cases = test_cases
    
    def detect_pattern(self) -> Dict[str, Any]:
        """Detect pattern from base test cases"""
        if not self.test_cases:
            return {'input_type': 'mixed', 'category': 'general'}
        
        # Analyze first test case
        first_input = self.test_cases[0].get('input', '')
        first_output = self.test_cases[0].get('output', '')
        
        # Detect input type
        input_type = 'mixed'
        if first_input.startswith('['):
            input_type = 'array'
        elif first_input.startswith('"') or first_input.startswith("'"):
            input_type = 'string'
        elif first_input.strip().lstrip('-').isdigit():
            input_type = 'number'
        
        # Detect problem category from input/output relationship
        category = 'general'
        try:
            if input_type == 'array':
                input_arr = eval(first_input)
                output_val = eval(first_output) if first_output else None
                
                if output_val == sum(input_arr):
                    category = 'sum'
                elif output_val == len(input_arr):
                    category = 'length'
                elif output_val == max(input_arr):
                    category = 'maximum'
                elif str(output_val) == str(input_arr[::-1]):
                    category = 'reverse'
        except:
            pass
        
        return {
            'input_type': input_type,
            'category': category,
            'sample_output': first_output
        }


# Convenience function
def enhance_test_cases(base_cases: List[Dict[str, str]], target_count: int = 50) -> List[Dict[str, str]]:
    """
    Enhance base test cases to reach target count.
    
    Usage:
        base_cases = [
            {'input': '[1, 2, 3]', 'output': '6'},
            {'input': '[5, 10]', 'output': '15'},
            {'input': '[0, 0, 0]', 'output': '0'}
        ]
        
        enhanced = enhance_test_cases(base_cases, target_count=50)
        # Returns 50 test cases total
    """
    return TestCaseGenerator.generate_comprehensive_test_cases(base_cases, target_count=target_count)
