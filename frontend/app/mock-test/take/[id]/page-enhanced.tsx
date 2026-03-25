'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { 
  Clock, Send, ChevronLeft, ChevronRight, AlertCircle, 
  CheckCircle, Circle, Play, Code, FileCode, Eye, EyeOff
} from 'lucide-react';

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

interface TestCase {
  input: string;
  expected_output: string;
}

interface CodingQuestion {
  question_id: number;
  question_text: string;
  difficulty: string;
  topic: string;
  test_cases: TestCase[];
  starter_code?: string;
}

interface MockTest {
  test_id: number;
  test_name: string;
  generated_at: string;
  mcq_questions: MCQQuestion[];
  coding_questions: CodingQuestion[];
}

interface Violation {
  type: string;
  timestamp: string;
}

export default function EnhancedTakeTestPage() {
  const params = useParams();
  const router = useRouter();
  const testId = params.id as string;

  // Test data
  const [test, setTest] = useState<MockTest | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  
  // Timer - 2 hours = 7200 seconds
  const [timeLeft, setTimeLeft] = useState(7200);
  const [timerExpired, setTimerExpired] = useState(false);

  // Answer state
  const [mcqAnswers, setMcqAnswers] = useState<Record<number, string>>({});
  const [codingAnswers, setCodingAnswers] = useState<Record<number, string>>({});

  // Navigation
  const [currentSection, setCurrentSection] = useState<'mcq' | 'coding'>('mcq');
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

  // Fullscreen & Anti-cheat
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showConfirmModal, setShowConfirmModal] = useState(true);
  const [violations, setViolations] = useState<Violation[]>([]);
  const containerRef = useRef<HTMLDivElement>(null);

  // Coding question states
  const [codingTestResults, setCodingTestResults] = useState<Record<number, any>>({});
  const [runningTest, setRunningTest] = useState<number | null>(null);

  // Enter fullscreen mode
  const enterFullscreen = useCallback(() => {
    if (containerRef.current) {
      containerRef.current.requestFullscreen?.().then(() => {
        setIsFullscreen(true);
        setShowConfirmModal(false);
      }).catch((err) => {
        console.error('Fullscreen error:', err);
        alert('Could not enter fullscreen mode');
      });
    }
  }, []);

  // Track violations
  const logViolation = useCallback((type: string) => {
    const violation: Violation = {
      type,
      timestamp: new Date().toISOString()
    };
    setViolations(prev => [...prev, violation]);
    
    // Warn user
    if (violations.length + 1 >= 3) {
      alert(`WARNING: ${violations.length + 1} violations detected. The test may be auto-submitted.`);
    }
  }, [violations]);

  // Handle fullscreen change
  useEffect(() => {
    const handleFullscreenChange = () => {
      if (!document.fullscreenElement && isFullscreen) {
        logViolation('fullscreen_exit');
        setIsFullscreen(false);
      }
    };

    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => document.removeEventListener('fullscreenchange', handleFullscreenChange);
  }, [isFullscreen, logViolation]);

  // Handle tab visibility change
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.hidden && isFullscreen) {
        logViolation('tab_switch');
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, [isFullscreen, logViolation]);

  // Handle window blur
  useEffect(() => {
    const handleBlur = () => {
      if (isFullscreen) {
        logViolation('window_blur');
      }
    };

    window.addEventListener('blur', handleBlur);
    return () => window.removeEventListener('blur', handleBlur);
  }, [isFullscreen, logViolation]);

  // Disable copy/paste/right-click
  useEffect(() => {
    if (!isFullscreen) return;

    const preventCopy = (e: ClipboardEvent) => e.preventDefault();
    const preventPaste = (e: ClipboardEvent) => e.preventDefault();
    const preventContextMenu = (e: MouseEvent) => e.preventDefault();

    document.addEventListener('copy', preventCopy);
    document.addEventListener('paste', preventPaste);
    document.addEventListener('contextmenu', preventContextMenu);

    return () => {
      document.removeEventListener('copy', preventCopy);
      document.removeEventListener('paste', preventPaste);
      document.removeEventListener('contextmenu', preventContextMenu);
    };
  }, [isFullscreen]);

  // Timer countdown
  useEffect(() => {
    if (!isFullscreen || timerExpired) return;

    const interval = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          setTimerExpired(true);
          handleSubmit();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [isFullscreen, timerExpired]);

  // Format time
  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

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
          
          const mcqInit: Record<number, string> = {};
          data.mcq_questions.forEach((q: MCQQuestion) => {
            mcqInit[q.question_id] = '';
          });
          setMcqAnswers(mcqInit);

          const codingInit: Record<number, string> = {};
          data.coding_questions.forEach((q: CodingQuestion) => {
            codingInit[q.question_id] = q.starter_code || '';
          });
          setCodingAnswers(codingInit);
        } else {
          alert('Failed to load test');
          router.push('/mock-test');
        }
      } catch (error) {
        console.error('Error:', error);
        alert('Failed to load test');
        router.push('/mock-test');
      } finally {
        setLoading(false);
      }
    };

    loadTest();
  }, [testId, router]);

  // Handle MCQ answer
  const handleMCQAnswer = (questionId: number, answer: string) => {
    setMcqAnswers(prev => ({ ...prev, [questionId]: answer }));
  };

  // Handle coding answer
  const handleCodingAnswer = (questionId: number, code: string) => {
    setCodingAnswers(prev => ({ ...prev, [questionId]: code }));
  };

  // Run sample test cases (Hackerrank-style)
  const runSampleTests = async (questionId: number) => {
    setRunningTest(questionId);
    const question = test?.coding_questions.find(q => q.question_id === questionId);
    if (!question) return;

    // Simulate running first 2 test cases
    const sampleCases = question.test_cases.slice(0, 2);
    const results = {
      passed: Math.floor(Math.random() * 3), // 0, 1, or 2
      total: 2,
      cases: sampleCases.map((tc, i) => ({
        input: tc.input,
        expected: tc.expected_output,
        actual: i === 0 ? tc.expected_output : 'Different output',
        passed: i === 0
      }))
    };

    setCodingTestResults(prev => ({ ...prev, [questionId]: results }));
    setRunningTest(null);
  };

  // Submit test
  const handleSubmit = async () => {
    if (submitting) return;
    
    setSubmitting(true);
    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(`http://localhost:8000/api/mock-tests/${testId}/submit`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          mcq_answers: mcqAnswers,
          coding_answers: codingAnswers,
          time_taken_minutes: Math.floor((7200 - timeLeft) / 60),
          violations_count: violations.length,
          violations_log: violations
        })
      });

      if (response.ok) {
        const result = await response.json();
        router.push(`/mock-test/results/${testId}`);
      } else {
        alert('Failed to submit test');
      }
    } catch (error) {
      console.error('Submit error:', error);
      alert('Failed to submit test');
    } finally {
      setSubmitting(false);
    }
  };

  const currentQuestions = currentSection === 'mcq' ? test?.mcq_questions || [] : test?.coding_questions || [];
  const currentQuestion = currentQuestions[currentQuestionIndex];

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading test...</div>;
  }

  if (!test) {
    return <div className="flex items-center justify-center min-h-screen">Test not found</div>;
  }

  // Confirmation modal
  if (showConfirmModal) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <Card className="p-8 max-w-md">
          <h2 className="text-2xl font-bold mb-4">Ready to Start?</h2>
          <Alert className="mb-4">
            <AlertCircle className="h-4 w-4" />
            <div className="ml-2">
              <p className="font-semibold">Anti-Cheat Rules:</p>
              <ul className="list-disc ml-5 mt-2 space-y-1 text-sm">
                <li>Fullscreen mode is mandatory</li>
                <li>Tab switching is tracked</li>
                <li>Copy/paste is disabled</li>
                <li>Right-click is disabled</li>
                <li>Test auto-submits after 2 hours</li>
                <li>3+ violations may trigger auto-submit</li>
              </ul>
            </div>
          </Alert>
          <Button onClick={enterFullscreen} className="w-full" size="lg">
            Start Test (Enter Fullscreen)
          </Button>
        </Card>
      </div>
    );
  }

  return (
    <div ref={containerRef} className="min-h-screen bg-gray-50 flex">
      {/* LEFT SIDEBAR - Question Navigation */}
      <div className="w-64 bg-white border-r flex flex-col">
        <div className="p-4 border-b">
          <h3 className="font-bold text-lg">{test.test_name}</h3>
          <div className="flex items-center gap-2 mt-2 text-sm">
            <Clock className="h-4 w-4" />
            <span className={timeLeft < 600 ? 'text-red-600 font-bold' : ''}>{formatTime(timeLeft)}</span>
          </div>
          {violations.length > 0 && (
            <Badge variant="destructive" className="mt-2">
              {violations.length} Violation{violations.length > 1 ? 's' : ''}
            </Badge>
          )}
        </div>

        {/* Section Tabs */}
        <div className="flex border-b">
          <button
            onClick={() => { setCurrentSection('mcq'); setCurrentQuestionIndex(0); }}
            className={`flex-1 py-3 font-semibold ${currentSection === 'mcq' ? 'bg-blue-50 text-blue-700 border-b-2 border-blue-700' : 'text-gray-600'}`}
          >
            MCQ ({test.mcq_questions.length})
          </button>
          <button
            onClick={() => { setCurrentSection('coding'); setCurrentQuestionIndex(0); }}
            className={`flex-1 py-3 font-semibold ${currentSection === 'coding' ? 'bg-blue-50 text-blue-700 border-b-2 border-blue-700' : 'text-gray-600'}`}
          >
            Coding ({test.coding_questions.length})
          </button>
        </div>

        {/* Question List */}
        <div className="flex-1 overflow-y-auto p-2">
          {currentSection === 'mcq' && test.mcq_questions.map((q, idx) => {
            const isAnswered = mcqAnswers[q.question_id] !== '';
            const isCurrent = idx === currentQuestionIndex;
            return (
              <button
                key={q.question_id}
                onClick={() => setCurrentQuestionIndex(idx)}
                className={`w-full p-3 mb-2 rounded-lg flex items-center justify-between ${
                  isCurrent ? 'bg-blue-100 border-2 border-blue-500' : 
                  isAnswered ? 'bg-green-50 border border-green-300' : 
                  'bg-gray-50 border border-gray-200'
                }`}
              >
                <span className="font-semibold">Q{idx + 1}</span>
                {isAnswered ? <CheckCircle className="h-5 w-5 text-green-600" /> : <Circle className="h-5 w-5 text-gray-400" />}
              </button>
            );
          })}

          {currentSection === 'coding' && test.coding_questions.map((q, idx) => {
            const hasCode = codingAnswers[q.question_id] && codingAnswers[q.question_id].trim().length > 10;
            const isCurrent = idx === currentQuestionIndex;
            return (
              <button
                key={q.question_id}
                onClick={() => setCurrentQuestionIndex(idx)}
                className={`w-full p-3 mb-2 rounded-lg flex items-center justify-between ${
                  isCurrent ? 'bg-blue-100 border-2 border-blue-500' : 
                  hasCode ? 'bg-green-50 border border-green-300' : 
                  'bg-gray-50 border border-gray-200'
                }`}
              >
                <span className="font-semibold">C{idx + 1}</span>
                {hasCode ? <CheckCircle className="h-5 w-5 text-green-600" /> : <Code className="h-5 w-5 text-gray-400" />}
              </button>
            );
          })}
        </div>

        {/* Submit Button */}
        <div className="p-4 border-t">
          <Button 
            onClick={handleSubmit} 
            disabled={submitting}
            className="w-full"
            variant="default"
          >
            <Send className="mr-2 h-4 w-4" />
            Submit Test
          </Button>
        </div>
      </div>

      {/* MAIN CONTENT AREA */}
      <div className="flex-1 overflow-y-auto p-6">
        {currentSection === 'mcq' && currentQuestion && 'options' in currentQuestion && (
          <Card className="p-6">
            <div className="flex items-center justify-between mb-4">
              <Badge>{(currentQuestion as MCQQuestion).difficulty}</Badge>
              <span className="text-sm text-gray-500">Topic: {(currentQuestion as MCQQuestion).topic}</span>
            </div>

            <h2 className="text-xl font-bold mb-6">Question {currentQuestionIndex + 1}</h2>
            <p className="text-lg mb-6">{currentQuestion.question_text}</p>

            <div className="space-y-3">
              {(currentQuestion as MCQQuestion).options.map((option) => (
                <label
                  key={option.option_letter}
                  className={`block p-4 rounded-lg border-2 cursor-pointer transition-all ${
                    mcqAnswers[(currentQuestion as MCQQuestion).question_id] === option.option_letter
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-start">
                    <input
                      type="radio"
                      name={`question-${(currentQuestion as MCQQuestion).question_id}`}
                      value={option.option_letter}
                      checked={mcqAnswers[(currentQuestion as MCQQuestion).question_id] === option.option_letter}
                      onChange={(e) => handleMCQAnswer((currentQuestion as MCQQuestion).question_id, e.target.value)}
                      className="mt-1 mr-3"
                    />
                    <div>
                      <span className="font-semibold">{option.option_letter}.</span> {option.option_text}
                    </div>
                  </div>
                </label>
              ))}
            </div>

            <div className="flex justify-between mt-6">
              <Button
                onClick={() => setCurrentQuestionIndex(Math.max(0, currentQuestionIndex - 1))}
                disabled={currentQuestionIndex === 0}
                variant="outline"
              >
                <ChevronLeft className="mr-2 h-4 w-4" /> Previous
              </Button>
              <Button
                onClick={() => setCurrentQuestionIndex(Math.min(test.mcq_questions.length - 1, currentQuestionIndex + 1))}
                disabled={currentQuestionIndex === test.mcq_questions.length - 1}
              >
                Next <ChevronRight className="ml-2 h-4 w-4" />
              </Button>
            </div>
          </Card>
        )}

        {currentSection === 'coding' && currentQuestion && 'test_cases' in currentQuestion && (
          <Card className="p-6">
            <div className="flex items-center justify-between mb-4">
              <Badge>{(currentQuestion as CodingQuestion).difficulty}</Badge>
              <span className="text-sm text-gray-500">Topic: {(currentQuestion as CodingQuestion).topic}</span>
            </div>

            <h2 className="text-xl font-bold mb-4">Coding Problem {currentQuestionIndex + 1}</h2>
            <div className="prose mb-6">
              <p>{currentQuestion.question_text}</p>
            </div>

            {/* Sample Test Cases */}
            <div className="mb-4 p-4 bg-gray-50 rounded-lg">
              <h3 className="font-semibold mb-2">Sample Test Cases:</h3>
              {(currentQuestion as CodingQuestion).test_cases.slice(0, 2).map((tc, i) => (
                <div key={i} className="mb-2 text-sm">
                  <div><strong>Input:</strong> <code className="bg-gray-200 px-2 py-1 rounded">{tc.input}</code></div>
                  <div><strong>Expected Output:</strong> <code className="bg-gray-200 px-2 py-1 rounded">{tc.expected_output}</code></div>
                </div>
              ))}
            </div>

            {/* Code Editor */}
            <div className="mb-4">
              <div className="flex items-center justify-between mb-2">
                <label className="font-semibold">Your Code:</label>
                <Badge variant="outline">Python</Badge>
              </div>
              <textarea
                value={codingAnswers[(currentQuestion as CodingQuestion).question_id] || ''}
                onChange={(e) => handleCodingAnswer((currentQuestion as CodingQuestion).question_id, e.target.value)}
                className="w-full h-64 p-4 font-mono text-sm bg-gray-900 text-green-400 rounded-lg"
                placeholder="# Write your code here..."
              />
            </div>

            {/* Run & Submit Buttons */}
            <div className="flex gap-3 mb-4">
              <Button
                onClick={() => runSampleTests((currentQuestion as CodingQuestion).question_id)}
                disabled={runningTest === (currentQuestion as CodingQuestion).question_id}
                variant="outline"
              >
                <Play className="mr-2 h-4 w-4" />
                {runningTest === (currentQuestion as CodingQuestion).question_id ? 'Running...' : 'Run Sample Tests'}
              </Button>
              <Button variant="default">
                <Send className="mr-2 h-4 w-4" />
                Submit (All Test Cases)
              </Button>
            </div>

            {/* Test Results */}
            {codingTestResults[(currentQuestion as CodingQuestion).question_id] && (
              <div className="p-4 bg-blue-50 rounded-lg">
                <h4 className="font-semibold mb-2">Sample Test Results:</h4>
                <p className="mb-2">
                  Passed: {codingTestResults[(currentQuestion as CodingQuestion).question_id].passed} / {codingTestResults[(currentQuestion as CodingQuestion).question_id].total}
                </p>
                {codingTestResults[(currentQuestion as CodingQuestion).question_id].cases.map((tc: any, i: number) => (
                  <div key={i} className={`mb-2 p-2 rounded ${tc.passed ? 'bg-green-100' : 'bg-red-100'}`}>
                    <p className="text-sm"><strong>Test {i + 1}:</strong> {tc.passed ? '✓ Passed' : '✗ Failed'}</p>
                    <p className="text-xs">Expected: {tc.expected} | Got: {tc.actual}</p>
                  </div>
                ))}
              </div>
            )}

            <div className="flex justify-between mt-6">
              <Button
                onClick={() => setCurrentQuestionIndex(Math.max(0, currentQuestionIndex - 1))}
                disabled={currentQuestionIndex === 0}
                variant="outline"
              >
                <ChevronLeft className="mr-2 h-4 w-4" /> Previous
              </Button>
              <Button
                onClick={() => setCurrentQuestionIndex(Math.min(test.coding_questions.length - 1, currentQuestionIndex + 1))}
                disabled={currentQuestionIndex === test.coding_questions.length - 1}
              >
                Next <ChevronRight className="ml-2 h-4 w-4" />
              </Button>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
