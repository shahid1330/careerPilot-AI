'use client';

import { useState, useEffect, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import dynamic from 'next/dynamic';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Clock, Send, Play, CheckCircle, XCircle, AlertCircle, Maximize } from 'lucide-react';

const MonacoEditor = dynamic(() => import('@monaco-editor/react'), { ssr: false });

interface TestCase {
  input: string;
  output: string;
  explanation?: string;
}

interface MCQOption {
  option_letter: string;
  option_text: string;
}

interface MCQQuestion {
  question_id: number;
  question_text: string;
  options: MCQOption[];
  difficulty: string;
  topic: string;
}

interface CodingQuestion {
  question_id: number;
  question_text: string;
  difficulty: string;
  topic: string;
  language: string;
  starter_code: string;
  visible_test_cases: TestCase[];
}

interface MockTest {
  test_id: number;
  test_name: string;
  mcq_questions: MCQQuestion[];
  coding_questions: CodingQuestion[];
}

interface TestResult {
  input: string;
  expected_output: string;
  actual_output: string;
  passed: boolean;
  runtime_ms: number;
  error?: string;
}

interface ExecutionResult {
  status: string;
  passed_count: number;
  total_count: number;
  test_results: TestResult[];
  total_runtime_ms: number;
  memory_mb: number;
}

export default function TakeTestPageNew() {
  const params = useParams();
  const router = useRouter();
  const testId = params.id as string;

  const [test, setTest] = useState<MockTest | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showFullscreenPrompt, setShowFullscreenPrompt] = useState(true);
  
  // Timer state - 2 hours
  const [timeLeft, setTimeLeft] = useState(7200);

  // Answer state
  const [mcqAnswers, setMcqAnswers] = useState<Record<number, number>>({});
  const [codingAnswers, setCodingAnswers] = useState<Record<number, string>>({});
  const [codingResults, setCodingResults] = useState<Record<number, ExecutionResult>>({});
  const [executing, setExecuting] = useState(false);

  // Navigation
  const [currentSection, setCurrentSection] = useState<'mcq' | 'coding'>('mcq');
  const [currentIndex, setCurrentIndex] = useState(0);

  // Load test
  useEffect(() => {
    const loadTest = async () => {
      try {
        const token = localStorage.getItem('auth_token');
        if (!token) {
          router.push('/login');
          return;
        }

        const response = await fetch(`http://localhost:8000/api/mock-tests/${testId}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
          const data = await response.json();
          setTest(data);
          
          const mcqInit: Record<number, number> = {};
          data.mcq_questions.forEach((q: MCQQuestion) => {
            mcqInit[q.question_id] = -1;
          });
          setMcqAnswers(mcqInit);

          const codingInit: Record<number, string> = {};
          data.coding_questions.forEach((q: CodingQuestion) => {
            codingInit[q.question_id] = q.starter_code || '';
          });
          setCodingAnswers(codingInit);
        }
      } catch (error) {
        console.error('Error:', error);
      } finally {
        setLoading(false);
      }
    };

    loadTest();
  }, [testId, router]);

  // Timer
  useEffect(() => {
    if (!test || !isFullscreen) return;
    const interval = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          clearInterval(interval);
          handleSubmitTest();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [test, isFullscreen]);

  const enterFullscreen = () => {
    document.documentElement.requestFullscreen();
    setIsFullscreen(true);
    setShowFullscreenPrompt(false);
  };

  const formatTime = (seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  const handleRunCode = async (questionId: number) => {
    setExecuting(true);
    try {
      const token = localStorage.getItem('auth_token');
      const code = codingAnswers[questionId];
      const language = test?.coding_questions.find(q => q.question_id === questionId)?.language || 'python';

      const response = await fetch('http://localhost:8000/api/execute/run-code', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          question_id: questionId,
          code,
          language,
          mode: 'run'
        })
      });

      if (response.ok) {
        const result = await response.json();
        setCodingResults(prev => ({ ...prev, [questionId]: result }));
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setExecuting(false);
    }
  };

  const handleSubmitCode = async (questionId: number) => {
    setExecuting(true);
    try {
      const token = localStorage.getItem('auth_token');
      const code = codingAnswers[questionId];
      const language = test?.coding_questions.find(q => q.question_id === questionId)?.language || 'python';

      const response = await fetch('http://localhost:8000/api/execute/run-code', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          question_id: questionId,
          code,
          language,
          mode: 'submit'
        })
      });

      if (response.ok) {
        const result = await response.json();
        setCodingResults(prev => ({ ...prev, [questionId]: result }));
        
        if (result.status === 'Accepted') {
          alert('🎉 All test cases passed! Moving to next question...');
          goToNextQuestion();
        }
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setExecuting(false);
    }
  };

  const goToNextQuestion = () => {
    if (currentSection === 'mcq' && test) {
      if (currentIndex < test.mcq_questions.length - 1) {
        setCurrentIndex(prev => prev + 1);
      } else {
        setCurrentSection('coding');
        setCurrentIndex(0);
      }
    } else if (currentSection === 'coding' && test) {
      if (currentIndex < test.coding_questions.length - 1) {
        setCurrentIndex(prev => prev + 1);
      }
    }
  };

  const handleSubmitTest = async () => {
    // Final submission logic
    alert('Test submitted!');
    router.push('/performance');
  };

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>;
  }

  if (showFullscreenPrompt) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-900">
        <Card className="p-8 max-w-md">
          <Maximize className="h-16 w-16 text-blue-600 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-center mb-4">Entering Fullscreen Mode</h2>
          <p className="text-gray-600 text-center mb-6">
            This test will run in fullscreen mode. Exiting fullscreen or switching tabs may result in violations.
          </p>
          <Button onClick={enterFullscreen} className="w-full bg-blue-600 hover:bg-blue-700">
            Start Test in Fullscreen
          </Button>
        </Card>
      </div>
    );
  }

  if (!test) return null;

  const currentQuestion = currentSection === 'mcq' 
    ? test.mcq_questions[currentIndex]
    : test.coding_questions[currentIndex];

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Left Sidebar */}
      <div className="w-64 bg-white border-r border-gray-200 overflow-y-auto">
        <div className="p-4 border-b">
          <h3 className="font-bold text-lg">{test.test_name}</h3>
          <div className="flex items-center gap-2 mt-2 text-blue-600">
            <Clock className="h-4 w-4" />
            <span className="font-mono">{formatTime(timeLeft)}</span>
          </div>
        </div>

        {/* MCQ Section */}
        <div className="p-4">
          <h4 className="font-semibold text-sm text-gray-600 mb-2">MCQ Questions</h4>
          <div className="space-y-1">
            {test.mcq_questions.map((q, idx) => {
              const isAnswered = mcqAnswers[q.question_id] !== -1;
              const isActive = currentSection === 'mcq' && currentIndex === idx;
              return (
                <button
                  key={q.question_id}
                  onClick={() => {
                    setCurrentSection('mcq');
                    setCurrentIndex(idx);
                  }}
                  className={`w-full flex items-center justify-between p-2 rounded ${
                    isActive ? 'bg-blue-100 border-2 border-blue-500' : 'bg-gray-50 hover:bg-gray-100'
                  }`}
                >
                  <span className="text-sm">Question {idx + 1}</span>
                  {isAnswered && <CheckCircle className="h-4 w-4 text-green-600" />}
                </button>
              );
            })}
          </div>
        </div>

        {/* Coding Section */}
        <div className="p-4 border-t">
          <h4 className="font-semibold text-sm text-gray-600 mb-2">Coding Questions</h4>
          <div className="space-y-1">
            {test.coding_questions.map((q, idx) => {
              const result = codingResults[q.question_id];
              const isAccepted = result?.status === 'Accepted';
              const isActive = currentSection === 'coding' && currentIndex === idx;
              return (
                <button
                  key={q.question_id}
                  onClick={() => {
                    setCurrentSection('coding');
                    setCurrentIndex(idx);
                  }}
                  className={`w-full flex items-center justify-between p-2 rounded ${
                    isActive ? 'bg-blue-100 border-2 border-blue-500' : 'bg-gray-50 hover:bg-gray-100'
                  }`}
                >
                  <span className="text-sm">Coding {idx + 1}</span>
                  {isAccepted && <CheckCircle className="h-4 w-4 text-green-600" />}
                </button>
              );
            })}
          </div>
        </div>

        <div className="p-4 border-t">
          <Button onClick={handleSubmitTest} className="w-full bg-green-600 hover:bg-green-700">
            <Send className="h-4 w-4 mr-2" />
            Submit Test
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto p-6">
        <Card className="p-6">
          <div className="flex items-center justify-between mb-4">
            <Badge variant={currentQuestion.difficulty === 'hard' ? 'destructive' : 'default'}>
              {currentQuestion.difficulty.toUpperCase()}
            </Badge>
            <Badge variant="outline">{currentQuestion.topic}</Badge>
          </div>

          {currentSection === 'mcq' ? (
            <div>
              <h3 className="text-lg font-semibold mb-4">{(currentQuestion as MCQQuestion).question_text}</h3>
              <div className="space-y-3">
                {(currentQuestion as MCQQuestion).options.map((option, idx) => (
                  <label
                    key={idx}
                    className={`block p-4 border-2 rounded cursor-pointer ${
                      mcqAnswers[(currentQuestion as MCQQuestion).question_id] === idx
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-blue-300'
                    }`}
                  >
                    <input
                      type="radio"
                      name={`mcq-${currentQuestion.question_id}`}
                      checked={mcqAnswers[(currentQuestion as MCQQuestion).question_id] === idx}
                      onChange={() => setMcqAnswers(prev => ({
                        ...prev,
                        [(currentQuestion as MCQQuestion).question_id]: idx
                      }))}
                      className="mr-3"
                    />
                    <span className="font-semibold mr-2">{option.option_letter}.</span>
                    {option.option_text}
                  </label>
                ))}
              </div>
              <div className="mt-6 flex justify-end">
                <Button onClick={goToNextQuestion} className="bg-blue-600">
                  Next Question
                </Button>
              </div>
            </div>
          ) : (
            <div>
              <div className="prose max-w-none mb-4">
                <pre className="whitespace-pre-wrap text-sm bg-gray-50 p-4 rounded">
                  {(currentQuestion as CodingQuestion).question_text}
                </pre>
              </div>

              {/* Visible Test Cases */}
              <div className="mb-4">
                <h4 className="font-semibold mb-2">Sample Test Cases:</h4>
                <div className="space-y-2">
                  {(currentQuestion as CodingQuestion).visible_test_cases?.map((tc, idx) => (
                    <div key={idx} className="bg-gray-50 p-3 rounded text-sm">
                      <div><strong>Input:</strong> {tc.input}</div>
                      <div><strong>Output:</strong> {tc.output}</div>
                      {tc.explanation && <div className="text-gray-600 italic">{tc.explanation}</div>}
                    </div>
                  ))}
                </div>
              </div>

              {/* Monaco Editor */}
              <div className="border rounded overflow-hidden mb-4">
                <MonacoEditor
                  height="400px"
                  language={(currentQuestion as CodingQuestion).language || 'python'}
                  theme="vs-dark"
                  value={codingAnswers[(currentQuestion as CodingQuestion).question_id] || ''}
                  onChange={(value) => setCodingAnswers(prev => ({
                    ...prev,
                    [(currentQuestion as CodingQuestion).question_id]: value || ''
                  }))}
                  options={{
                    minimap: { enabled: false },
                    fontSize: 14,
                    lineNumbers: 'on',
                    scrollBeyondLastLine: false
                  }}
                />
              </div>

              {/* Run/Submit Buttons */}
              <div className="flex gap-3 mb-4">
                <Button
                  onClick={() => handleRunCode((currentQuestion as CodingQuestion).question_id)}
                  disabled={executing}
                  variant="outline"
                >
                  <Play className="h-4 w-4 mr-2" />
                  Run Code
                </Button>
                <Button
                  onClick={() => handleSubmitCode((currentQuestion as CodingQuestion).question_id)}
                  disabled={executing}
                  className="bg-green-600 hover:bg-green-700"
                >
                  <Send className="h-4 w-4 mr-2" />
                  Submit
                </Button>
              </div>

              {/* Results */}
              {codingResults[(currentQuestion as CodingQuestion).question_id] && (
                <Card className="p-4 bg-gray-50">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-semibold">Results:</h4>
                    <Badge variant={codingResults[(currentQuestion as CodingQuestion).question_id].status === 'Accepted' ? 'default' : 'destructive'}>
                      {codingResults[(currentQuestion as CodingQuestion).question_id].status}
                    </Badge>
                  </div>
                  <div className="text-sm space-y-1 mb-3">
                    <div>Passed: {codingResults[(currentQuestion as CodingQuestion).question_id].passed_count} / {codingResults[(currentQuestion as CodingQuestion).question_id].total_count}</div>
                    <div>Runtime: {codingResults[(currentQuestion as CodingQuestion).question_id].total_runtime_ms.toFixed(2)} ms</div>
                    <div>Memory: {codingResults[(currentQuestion as CodingQuestion).question_id].memory_mb.toFixed(2)} MB</div>
                  </div>
                  <div className="space-y-2">
                    {codingResults[(currentQuestion as CodingQuestion).question_id].test_results.map((tr, idx) => (
                      <div key={idx} className={`p-2 rounded ${tr.passed ? 'bg-green-100' : 'bg-red-100'}`}>
                        <div className="flex items-center gap-2">
                          {tr.passed ? <CheckCircle className="h-4 w-4 text-green-600" /> : <XCircle className="h-4 w-4 text-red-600" />}
                          <span className="font-semibold">Test Case {idx + 1}</span>
                        </div>
                        {!tr.passed && tr.input !== 'Hidden' && (
                          <div className="text-sm mt-1 ml-6">
                            <div>Input: {tr.input}</div>
                            <div>Expected: {tr.expected_output}</div>
                            <div>Got: {tr.actual_output}</div>
                            {tr.error && <div className="text-red-600">Error: {tr.error}</div>}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </Card>
              )}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
