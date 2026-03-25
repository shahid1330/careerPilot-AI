"""Code execution endpoint for running coding questions against test cases."""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import subprocess
import tempfile
import os
import time
import sys

from app.core.database import get_db
from app.models.mock_test_v2 import MockTestQuestion
from app.utils.jwt import get_current_user

router = APIRouter(prefix="/api/execute", tags=["Code Execution"])


class CodeExecutionRequest(BaseModel):
    """Request model for code execution."""
    question_id: int
    code: str
    language: str
    visible_only: Optional[bool] = True  # True = run visible only, False = run all


class TestCaseResult(BaseModel):
    """Result for a single test case."""
    input: str
    expected_output: str
    actual_output: str
    passed: bool
    runtime_ms: float
    error: Optional[str] = None


class CodeExecutionResponse(BaseModel):
    """Response model for code execution."""
    status: str  # "Accepted", "Wrong Answer", "Runtime Error", "Time Limit Exceeded", "Compilation Error"
    passed_count: int
    total_count: int
    test_results: List[TestCaseResult]
    total_runtime_ms: float
    memory_mb: float
    message: Optional[str] = None


def execute_python_code(code: str, test_input: str, timeout: int = 5) -> Dict[str, Any]:
    """Execute Python code with given input and return result."""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        start_time = time.time()
        process = subprocess.Popen(
            [sys.executable, temp_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input=test_input, timeout=timeout)
        runtime_ms = (time.time() - start_time) * 1000
        
        os.unlink(temp_file)
        
        if process.returncode != 0:
            return {
                'output': stdout.strip(),
                'error': stderr.strip(),
                'runtime_ms': runtime_ms,
                'success': False
            }
        
        return {
            'output': stdout.strip(),
            'error': None,
            'runtime_ms': runtime_ms,
            'success': True
        }
    
    except subprocess.TimeoutExpired:
        if os.path.exists(temp_file):
            os.unlink(temp_file)
        return {
            'output': '',
            'error': 'Time Limit Exceeded',
            'runtime_ms': timeout * 1000,
            'success': False
        }
    except Exception as e:
        if 'temp_file' in locals() and os.path.exists(temp_file):
            os.unlink(temp_file)
        return {
            'output': '',
            'error': str(e),
            'runtime_ms': 0,
            'success': False
        }


def execute_java_code(code: str, test_input: str, timeout: int = 5) -> Dict[str, Any]:
    """Execute Java code with given input and return result."""
    temp_dir = None
    try:
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        
        # Extract class name from code
        class_name = "Solution"
        for line in code.split('\n'):
            if 'public class' in line:
                class_name = line.split('public class')[1].split()[0].strip('{')
                break
        
        java_file = os.path.join(temp_dir, f"{class_name}.java")
        with open(java_file, 'w') as f:
            f.write(code)
        
        # Compile
        compile_process = subprocess.run(
            ['javac', java_file],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if compile_process.returncode != 0:
            import shutil
            shutil.rmtree(temp_dir)
            return {
                'output': '',
                'error': f'Compilation Error: {compile_process.stderr}',
                'runtime_ms': 0,
                'success': False
            }
        
        # Execute
        start_time = time.time()
        run_process = subprocess.Popen(
            ['java', '-cp', temp_dir, class_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = run_process.communicate(input=test_input, timeout=timeout)
        runtime_ms = (time.time() - start_time) * 1000
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
        
        if run_process.returncode != 0:
            return {
                'output': stdout.strip(),
                'error': stderr.strip(),
                'runtime_ms': runtime_ms,
                'success': False
            }
        
        return {
            'output': stdout.strip(),
            'error': None,
            'runtime_ms': runtime_ms,
            'success': True
        }
    
    except subprocess.TimeoutExpired:
        if temp_dir and os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)
        return {
            'output': '',
            'error': 'Time Limit Exceeded',
            'runtime_ms': timeout * 1000,
            'success': False
        }
    except Exception as e:
        if temp_dir and os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)
        return {
            'output': '',
            'error': str(e),
            'runtime_ms': 0,
            'success': False
        }


def execute_javascript_code(code: str, test_input: str, timeout: int = 5) -> Dict[str, Any]:
    """Execute JavaScript code with given input and return result."""
    temp_file = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            # Wrap code to handle stdin
            wrapped_code = f"""
const readline = require('readline');
const rl = readline.createInterface({{
    input: process.stdin,
    output: process.stdout
}});

let inputLines = [];
rl.on('line', (line) => {{
    inputLines.push(line);
}});

rl.on('close', () => {{
    {code}
}});
"""
            f.write(wrapped_code)
            temp_file = f.name
        
        start_time = time.time()
        process = subprocess.Popen(
            ['node', temp_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input=test_input, timeout=timeout)
        runtime_ms = (time.time() - start_time) * 1000
        
        os.unlink(temp_file)
        
        if process.returncode != 0:
            return {
                'output': stdout.strip(),
                'error': stderr.strip(),
                'runtime_ms': runtime_ms,
                'success': False
            }
        
        return {
            'output': stdout.strip(),
            'error': None,
            'runtime_ms': runtime_ms,
            'success': True
        }
    
    except subprocess.TimeoutExpired:
        if temp_file and os.path.exists(temp_file):
            os.unlink(temp_file)
        return {
            'output': '',
            'error': 'Time Limit Exceeded',
            'runtime_ms': timeout * 1000,
            'success': False
        }
    except Exception as e:
        if temp_file and os.path.exists(temp_file):
            os.unlink(temp_file)
        return {
            'output': '',
            'error': str(e),
            'runtime_ms': 0,
            'success': False
        }


@router.post("/run-code", response_model=CodeExecutionResponse)
async def run_code(
    request: CodeExecutionRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    🟢 RUN CODE - Execute code against VISIBLE test cases only.
    Used for "Run Code" button to quickly test with sample cases.
    """
    
    # Get question with test cases
    question = db.query(MockTestQuestion).filter(
        MockTestQuestion.id == request.question_id
    ).first()
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    if question.question_type != 'coding':
        raise HTTPException(status_code=400, detail="Not a coding question")
    
    # Get all test cases
    all_test_cases = question.test_cases or []
    
    # Determine visible count
    visible_count = 3  # Default
    if question.question_data and 'visible_count' in question.question_data:
        visible_count = question.question_data['visible_count']
    elif all_test_cases and '_visible_count' in all_test_cases[0]:
        visible_count = all_test_cases[0]['_visible_count']
    
    # Run only visible test cases when visible_only=True
    if request.visible_only:
        test_cases_to_run = all_test_cases[:visible_count]
        mode_message = f"Running {len(test_cases_to_run)} visible test cases..."
    else:
        test_cases_to_run = all_test_cases
        mode_message = f"Running ALL {len(test_cases_to_run)} test cases (including hidden)..."
    
    if not test_cases_to_run:
        raise HTTPException(status_code=400, detail="No test cases found for this question")
    
    print(f"\n{'='*60}")
    print(f"🔵 CODE EXECUTION REQUEST")
    print(f"Question ID: {request.question_id}")
    print(f"Language: {request.language}")
    print(f"Visible Only: {request.visible_only}")
    print(f"{mode_message}")
    print(f"{'='*60}\n")
    
    # Execute code against each test case
    test_results = []
    total_runtime = 0
    passed_count = 0
    status = "Accepted"
    error_message = None
    
    for idx, test_case in enumerate(test_cases_to_run):
        test_input = test_case.get('input', '')
        expected_output = test_case.get('output', test_case.get('expected_output', '')).strip()
        is_visible = idx < visible_count
        
        # Execute based on language
        if request.language.lower() == 'python':
            result = execute_python_code(request.code, test_input)
        elif request.language.lower() == 'java':
            result = execute_java_code(request.code, test_input)
        elif request.language.lower() in ['javascript', 'js']:
            result = execute_javascript_code(request.code, test_input)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported language: {request.language}")
        
        actual_output = result['output'].strip()
        runtime_ms = result['runtime_ms']
        total_runtime += runtime_ms
        
        passed = result['success'] and actual_output == expected_output
        
        if passed:
            passed_count += 1
        else:
            if not result['success']:
                if 'Time Limit Exceeded' in result.get('error', ''):
                    status = "Time Limit Exceeded"
                elif 'Compilation Error' in result.get('error', ''):
                    status = "Compilation Error"
                else:
                    status = "Runtime Error"
                error_message = result.get('error')
            else:
                status = "Wrong Answer"
        
        # Show details only for visible test cases, hide for hidden
        if is_visible or request.visible_only:
            test_results.append(TestCaseResult(
                input=test_input,
                expected_output=expected_output,
                actual_output=actual_output,
                passed=passed,
                runtime_ms=runtime_ms,
                error=result.get('error')
            ))
        else:
            # For hidden test cases, don't reveal input/output
            test_results.append(TestCaseResult(
                input="Hidden",
                expected_output="Hidden",
                actual_output="Hidden" if not passed else "Correct",
                passed=passed,
                runtime_ms=runtime_ms,
                error=result.get('error') if not passed else None
            ))
        
        # Stop on first failure for certain error types
        if not passed and status in ["Runtime Error", "Compilation Error", "Time Limit Exceeded"]:
            break
    
    # If all passed, status remains "Accepted"
    if passed_count == len(test_cases_to_run):
        status = "Accepted"
    
    # Estimate memory (simplified)
    memory_mb = 0.5 + (len(request.code) / 10000)
    
    print(f"✅ Execution complete: {status} - {passed_count}/{len(test_cases_to_run)} passed\n")
    
    return CodeExecutionResponse(
        status=status,
        passed_count=passed_count,
        total_count=len(test_cases_to_run),
        test_results=test_results,
        total_runtime_ms=total_runtime,
        memory_mb=memory_mb,
        message=error_message
    )


@router.post("/submit-code", response_model=CodeExecutionResponse)
async def submit_code(
    request: CodeExecutionRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    🔵 SUBMIT CODE - Execute code against ALL test cases (including hidden).
    Used for "Submit Solution" button to get final verdict.
    """
    # Force visible_only to False for submission
    request.visible_only = False
    
    # Call the same run_code logic
    return await run_code(request, current_user, db)
