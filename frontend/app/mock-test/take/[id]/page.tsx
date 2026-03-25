'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { useParams, useRouter } from 'next/navigation';
import dynamic from 'next/dynamic';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { 
  Clock, Send, ChevronLeft, ChevronRight, AlertCircle, 
  CheckCircle, Circle, Play, Code, FileCode, Eye, EyeOff,
  Maximize, ShieldAlert, XCircle
} from 'lucide-react';

// Dynamically import Monaco Editor (client-side only)
const MonacoEditor = dynamic(() => import('@monaco-editor/react'), { ssr: false });

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
  correct_answer?: string;
  points: number;
}

interface TestCase {
  input: string;
  expected_output: string;
  output?: string;
}

interface CodingQuestion {
  question_id: number;
  question_text: string;
  difficulty: string;
  topic: string;
  visible_test_cases: TestCase[];
  test_cases: TestCase[];
  starter_code?: string;
  language: string;
  points: number;
}

interface MockTest {
  test_id: number;
  test_name: string;
  test_date: string;
  mcq_count: number;
  coding_count: number;
  time_limit_minutes: number;
  topics_used: string[];
  mcq_questions: MCQQuestion[];
  coding_questions: CodingQuestion[];
  status: string;
}

interface Violation {
  type: string;
  timestamp: string;
}

interface TestCaseResult {
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
  test_results: TestCaseResult[];
  total_runtime_ms: number;
  memory_mb: number;
  message?: string;
}

export default function EnhancedTakeTestPage() {
  const params = useParams();
  const router = useRouter();
  const testId = params.id as string;
  const containerRef = useRef<HTMLDivElement>(null);

  // Test data
  const [test, setTest] = useState<MockTest | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  
  // Timer
  const [timeLeft, setTimeLeft] = useState(7200); // 2 hours
  const [timerExpired, setTimerExpired] = useState(false);

  // Answer state
  const [mcqAnswers, setMcqAnswers] = useState<Record<number, string>>({});
  const [codingAnswers, setCodingAnswers] = useState<Record<number, string>>({});
  const [codingSubmitted, setCodingSubmitted] = useState<Record<number, boolean>>({});

  // Navigation
  const [currentSection, setCurrentSection] = useState<'mcq' | 'coding'>('mcq');
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

  // Fullscreen & Anti-cheat
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showConfirmModal, setShowConfirmModal] = useState(true);
  const [violations, setViolations] = useState<Violation[]>([]);
  const [testStarted, setTestStarted] = useState(false);

  // Coding execution
  const [executionResults, setExecutionResults] = useState<Record<number, ExecutionResult>>({});
  const [executing, setExecuting] = useState<number | null>(null);
  const [submittingCode, setSubmittingCode] = useState<number | null>(null);

  // Load test data
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
          
          // Initialize MCQ answers
          const mcqInit: Record<number, string> = {};
          data.mcq_questions.forEach((q: MCQQuestion) => {
            mcqInit[q.question_id] = '';
          });
          setMcqAnswers(mcqInit);

          // Initialize coding answers
          const codingInit: Record<number, string> = {};
          const submittedInit: Record<number, boolean> = {};
          data.coding_questions.forEach((q: CodingQuestion) => {
            codingInit[q.question_id] = q.starter_code || `# Write your ${q.language} code here\n`;
            submittedInit[q.question_id] = false;
          });
          setCodingAnswers(codingInit);
          setCodingSubmitted(submittedInit);
        } else {
          alert('Failed to load test');
          router.push('/mock-test');
        }
      } catch (error) {
        console.error('Error loading test:', error);
        alert('Failed to load test');
        router.push('/mock-test');
      } finally {
        setLoading(false);
      }
    };

    loadTest();
  }, [testId, router]);

  // Enter fullscreen mode
  const enterFullscreen = useCallback(() => {
    const container = containerRef.current || document.documentElement;
    
    const enterFS = container.requestFullscreen || 
                    (container as any).webkitRequestFullscreen || 
                    (container as any).mozRequestFullScreen || 
                    (container as any).msRequestFullscreen;
    
    if (enterFS) {
      enterFS.call(container).then(() => {
        setIsFullscreen(true);
        setShowConfirmModal(false);
        setTestStarted(true);
      }).catch((err: Error) => {
        console.error('Fullscreen error:', err);
        // Still allow test to start even if fullscreen fails
        setShowConfirmModal(false);
        setTestStarted(true);
      });
    } else {
      // Browser doesn't support fullscreen, continue anyway
      setShowConfirmModal(false);
      setTestStarted(true);
    }
  }, []);

  // Track violations
  const logViolation = useCallback((type: string) => {
    const violation: Violation = {
      type,
      timestamp: new Date().toISOString()
    };
    setViolations(prev => {
      const newViolations = [...prev, violation];
      
      // Warn user at 3, 5, and 7 violations
      if (newViolations.length === 3 || newViolations.length === 5) {
        alert(`⚠️ WARNING: ${newViolations.length} violations detected!\n\nViolations:\n${newViolations.map(v => `• ${v.type}`).join('\n')}\n\nContinued violations may result in test disqualification.`);
      } else if (newViolations.length >= 7) {
        alert('🚫 Too many violations detected. Your test will be auto-submitted.');
        handleAutoSubmit();
      }
      
      return newViolations;
    });
  }, []);

  // Handle fullscreen change
  useEffect(() => {
    const handleFullscreenChange = () => {
      const isCurrentlyFullscreen = !!(document.fullscreenElement || 
                                       (document as any).webkitFullscreenElement || 
                                       (document as any).mozFullScreenElement);
      
      if (!isCurrentlyFullscreen && isFullscreen && testStarted) {
        logViolation('fullscreen_exit');
        setIsFullscreen(false);
        
        // Try to re-enter fullscreen
        setTimeout(() => {
          if (testStarted && !timerExpired) {
            alert('⚠️ Please remain in fullscreen mode during the test.');
          }
        }, 500);
      }
    };

    document.addEventListener('fullscreenchange', handleFullscreenChange);
    document.addEventListener('webkitfullscreenchange', handleFullscreenChange);
    document.addEventListener('mozfullscreenchange', handleFullscreenChange);
    
    return () => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
      document.removeEventListener('webkitfullscreenchange', handleFullscreenChange);
      document.removeEventListener('mozfullscreenchange', handleFullscreenChange);
    };
  }, [isFullscreen, testStarted, timerExpired, logViolation]);

  // Handle tab visibility change
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.hidden && testStarted && !timerExpired) {
        logViolation('tab_switch');
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, [testStarted, timerExpired, logViolation]);

  // Handle window blur
  useEffect(() => {
    const handleBlur = () => {
      if (testStarted && !timerExpired) {
        logViolation('window_blur');
      }
    };

    window.addEventListener('blur', handleBlur);
    return () => window.removeEventListener('blur', handleBlur);
  }, [testStarted, timerExpired, logViolation]);

  // Prevent context menu (right-click)
  useEffect(() => {
    const handleContextMenu = (e: MouseEvent) => {
      if (testStarted) {
        e.preventDefault();
        logViolation('right_click_attempt');
      }
    };

    document.addEventListener('contextmenu', handleContextMenu);
    return () => document.removeEventListener('contextmenu', handleContextMenu);
  }, [testStarted, logViolation]);

  // Prevent copy/paste (with some exceptions for code editor)
  useEffect(() => {
    const handleCopy = (e: ClipboardEvent) => {
      const target = e.target as HTMLElement;
      // Allow copy in Monaco editor
      if (!target.closest('.monaco-editor') && testStarted) {
        e.preventDefault();
        logViolation('copy_attempt');
      }
    };

    const handlePaste = (e: ClipboardEvent) => {
      const target = e.target as HTMLElement;
      // Allow paste in Monaco editor
      if (!target.closest('.monaco-editor') && testStarted) {
        e.preventDefault();
        logViolation('paste_attempt');
      }
    };

    document.addEventListener('copy', handleCopy);
    document.addEventListener('paste', handlePaste);
    
    return () => {
      document.removeEventListener('copy', handleCopy);
      document.removeEventListener('paste', handlePaste);
    };
  }, [testStarted, logViolation]);

  // Timer countdown
  useEffect(() => {
    if (!testStarted || loading || !test || timerExpired) return;

    const interval = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          setTimerExpired(true);
          clearInterval(interval);
          handleAutoSubmit();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [testStarted, loading, test, timerExpired]);

  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleAutoSubmit = useCallback(async () => {
    await submitTest(true);
  }, [testId, mcqAnswers, codingAnswers]);

  const submitTest = async (isAutoSubmit = false) => {
    if (submitting) return;

    const confirmed = isAutoSubmit || window.confirm(
      '⚠️ Are you sure you want to submit?\n\nYou cannot change your answers after submission.\n\nMake sure you have:\n✓ Answered all MCQ questions\n✓ Submitted all coding solutions'
    );

    if (!confirmed && !isAutoSubmit) return;

    setSubmitting(true);

    try {
      const token = localStorage.getItem('auth_token');
      const userRoleId = localStorage.getItem('currentUserRoleId');
      
      if (!token) {
        router.push('/login');
        return;
      }

      // Prepare MCQ submissions
      const mcqSubmissions = Object.entries(mcqAnswers)
        .filter(([_, answer]) => answer !== '')
        .map(([questionId, selectedAnswer]) => ({
          question_id: parseInt(questionId),
          selected_answer: selectedAnswer
        }));

      // Prepare coding submissions
      const codingSubmissions = Object.entries(codingAnswers)
        .map(([questionId, code]) => ({
          question_id: parseInt(questionId),
          code: code,
          language: test?.coding_questions.find(q => q.question_id === parseInt(questionId))?.language || 'python'
        }));

      const timeTaken = Math.floor((7200 - timeLeft) / 60); // Convert to minutes

      const response = await fetch(`http://localhost:8000/api/mock-tests/${testId}/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          user_role_id: parseInt(userRoleId || '0'),
          mcq_answers: mcqSubmissions,
          coding_submissions: codingSubmissions,
          time_taken_minutes: timeTaken,
          violations_count: violations.length,
          violations_log: violations
        })
      });

      if (response.ok) {
        // Exit fullscreen before navigating
        if (document.exitFullscreen) {
          await document.exitFullscreen().catch(() => {});
        }
        router.push(`/mock-test/results/${testId}`);
      } else {
        const errorData = await response.json();
        alert(errorData.detail || 'Failed to submit test');
        setSubmitting(false);
      }
    } catch (error) {
      console.error('Error submitting test:', error);
      alert('Failed to submit test. Please try again.');
      setSubmitting(false);
    }
  };

  // MCQ handlers
  const handleMCQAnswer = (questionId: number, optionLetter: string) => {
    setMcqAnswers(prev => ({
      ...prev,
      [questionId]: optionLetter
    }));
  };

  // Coding handlers
  const handleCodingAnswer = (questionId: number, code: string) => {
    setCodingAnswers(prev => ({
      ...prev,
      [questionId]: code
    }));
  };

  // Run code (visible test cases only)
  const runCode = async (questionId: number) => {
    const code = codingAnswers[questionId];
    if (!code || !code.trim()) {
      alert('Please write some code first!');
      return;
    }

    setExecuting(questionId);
    
    try {
      const token = localStorage.getItem('auth_token');
      const question = test?.coding_questions.find(q => q.question_id === questionId);
      
      if (!question) return;

      const response = await fetch('http://localhost:8000/api/execute/run-code', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          question_id: questionId,
          code: code,
          language: question.language,
          visible_only: true // Only run visible test cases
        })
      });

      if (response.ok) {
        const result = await response.json();
        setExecutionResults(prev => ({
          ...prev,
          [questionId]: result
        }));
      } else {
        const error = await response.json();
        alert(`Execution failed: ${error.detail || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Execution error:', error);
      alert('Failed to execute code. Please try again.');
    } finally {
      setExecuting(null);
    }
  };

  // Submit code solution (all test cases)
  const submitCodeSolution = async (questionId: number) => {
    const code = codingAnswers[questionId];
    if (!code || !code.trim()) {
      alert('Please write some code first!');
      return;
    }

    const confirmed = window.confirm(
      '⚠️ Submit this solution?\n\nThis will run ALL test cases (including hidden ones).\nYou can only submit once per question.'
    );

    if (!confirmed) return;

    setSubmittingCode(questionId);
    
    try {
      const token = localStorage.getItem('auth_token');
      const question = test?.coding_questions.find(q => q.question_id === questionId);
      
      if (!question) return;

      const response = await fetch('http://localhost:8000/api/execute/submit-code', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          question_id: questionId,
          code: code,
          language: question.language,
          visible_only: false // Run ALL test cases
        })
      });

      if (response.ok) {
        const result = await response.json();
        setExecutionResults(prev => ({
          ...prev,
          [questionId]: result
        }));
        setCodingSubmitted(prev => ({
          ...prev,
          [questionId]: true
        }));
        
        alert(`✅ Solution submitted!\n\n${result.passed_count}/${result.total_count} test cases passed\n\nStatus: ${result.status}`);
      } else {
        const error = await response.json();
        alert(`Submission failed: ${error.detail || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Submission error:', error);
      alert('Failed to submit solution. Please try again.');
    } finally {
      setSubmittingCode(null);
    }
  };

  // Navigation
  const goToQuestion = (section: 'mcq' | 'coding', index: number) => {
    setCurrentSection(section);
    setCurrentQuestionIndex(index);
  };

  const goToNextQuestion = () => {
    if (currentSection === 'mcq' && test) {
      if (currentQuestionIndex < test.mcq_questions.length - 1) {
        setCurrentQuestionIndex(prev => prev + 1);
      } else {
        setCurrentSection('coding');
        setCurrentQuestionIndex(0);
      }
    } else if (currentSection === 'coding' && test) {
      if (currentQuestionIndex < test.coding_questions.length - 1) {
        setCurrentQuestionIndex(prev => prev + 1);
      }
    }
  };

  const goToPreviousQuestion = () => {
    if (currentSection === 'coding' && currentQuestionIndex === 0) {
      setCurrentSection('mcq');
      setCurrentQuestionIndex(test?.mcq_questions.length ? test.mcq_questions.length - 1 : 0);
    } else if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  const getProgress = () => {
    if (!test) return 0;
    const answeredMCQ = Object.values(mcqAnswers).filter(a => a !== '').length;
    const submittedCoding = Object.values(codingSubmitted).filter(s => s).length;
    const totalQuestions = test.mcq_questions.length + test.coding_questions.length;
    return Math.round(((answeredMCQ + submittedCoding) / totalQuestions) * 100);
  };

  // Confirmation Modal
  if (showConfirmModal && !testStarted) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <Card className="max-w-2xl w-full p-8 bg-white">
          <div className="text-center mb-6">
            <Maximize className="mx-auto h-16 w-16 text-blue-600 mb-4" />
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Ready to Start?</h2>
            <p className="text-gray-600">Please read the rules carefully before proceeding</p>
          </div>

          <div className="bg-yellow-50 border-2 border-yellow-200 rounded-lg p-6 mb-6">
            <div className="flex items-start gap-3 mb-4">
              <ShieldAlert className="h-6 w-6 text-yellow-600 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-bold text-yellow-900 mb-2">Anti-Cheat System Active</h3>
                <ul className="text-sm text-yellow-800 space-y-2">
                  <li>✓ Fullscreen mode will be enforced (if supported by your browser)</li>
                  <li>✓ Tab switching will be tracked as violations</li>
                  <li>✓ Copy/paste in questions is disabled</li>
                  <li>✓ Right-click is disabled</li>
                  <li>✓ Window blur will be monitored</li>
                  <li className="font-bold text-red-600">⚠️ 7+ violations = automatic test submission</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-6 mb-6">
            <h3 className="font-bold text-blue-900 mb-3">Test Rules:</h3>
            <ul className="text-sm text-blue-800 space-y-2">
              <li>⏱️ Time limit: 2 hours</li>
              <li>📝 MCQ Section: Select one answer per question</li>
              <li>💻 Coding Section: Write and test your code, then submit</li>
              <li>▶️ Run Code: Tests visible sample cases only</li>
              <li>✅ Submit Solution: Tests ALL cases (including hidden)</li>
              <li>🚫 You can only submit each coding solution once</li>
            </ul>
          </div>

          <div className="flex gap-4">
            <Button
              onClick={() => router.push('/mock-test')}
              variant="outline"
              className="flex-1"
            >
              Cancel
            </Button>
            <Button
              onClick={enterFullscreen}
              className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
            >
              I Understand - Start Test
            </Button>
          </div>
        </Card>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Loading test...</p>
        </div>
      </div>
    );
  }

  if (!test) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Alert className="bg-red-50 border-red-200">
          <AlertCircle className="h-5 w-5 text-red-600" />
          <span className="text-red-800 ml-2">Test not found</span>
        </Alert>
      </div>
    );
  }

  const currentQuestion = currentSection === 'mcq'
    ? test.mcq_questions[currentQuestionIndex]
    : test.coding_questions[currentQuestionIndex];

  const isLastQuestion = currentSection === 'coding' && currentQuestionIndex === test.coding_questions.length - 1;

  return (
    <div ref={containerRef} className="min-h-screen bg-gray-50">
      <div className="flex h-screen">
        {/* LEFT SIDEBAR - Question Navigation */}
        <div className="w-64 bg-white border-r border-gray-200 overflow-y-auto">
          <div className="p-4 border-b bg-gradient-to-r from-blue-600 to-purple-600">
            <h2 className="text-white font-bold text-lg">Questions</h2>
          </div>

          {/* MCQ Questions */}
          <div className="p-4">
            <div className="text-xs font-semibold text-gray-500 uppercase mb-3">
              Section 1: MCQ ({test.mcq_questions.length})
            </div>
            <div className="grid grid-cols-5 gap-2">
              {test.mcq_questions.map((q, idx) => {
                const isAnswered = mcqAnswers[q.question_id] !== '';
                const isCurrent = currentSection === 'mcq' && currentQuestionIndex === idx;
                
                return (
                  <button
                    key={q.question_id}
                    onClick={() => goToQuestion('mcq', idx)}
                    className={`
                      aspect-square rounded-lg font-semibold text-sm transition-all
                      ${isCurrent 
                        ? 'bg-blue-600 text-white ring-2 ring-blue-400' 
                        : isAnswered 
                          ? 'bg-green-500 text-white hover:bg-green-600' 
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }
                    `}
                  >
                    <div className="flex flex-col items-center justify-center h-full">
                      <span>{idx + 1}</span>
                      {isAnswered && !isCurrent && (
                        <CheckCircle className="h-3 w-3 mt-1" />
                      )}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Coding Questions */}
          <div className="p-4 border-t">
            <div className="text-xs font-semibold text-gray-500 uppercase mb-3">
              Section 2: Coding ({test.coding_questions.length})
            </div>
            <div className="space-y-2">
              {test.coding_questions.map((q, idx) => {
                const isSubmitted = codingSubmitted[q.question_id];
                const isCurrent = currentSection === 'coding' && currentQuestionIndex === idx;
                
                return (
                  <button
                    key={q.question_id}
                    onClick={() => goToQuestion('coding', idx)}
                    className={`
                      w-full p-3 rounded-lg font-semibold text-sm transition-all text-left
                      ${isCurrent 
                        ? 'bg-purple-600 text-white ring-2 ring-purple-400' 
                        : isSubmitted 
                          ? 'bg-green-500 text-white hover:bg-green-600' 
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }
                    `}
                  >
                    <div className="flex items-center justify-between">
                      <span className="flex items-center gap-2">
                        <Code className="h-4 w-4" />
                        Problem {idx + 1}
                      </span>
                      {isSubmitted && !isCurrent && (
                        <CheckCircle className="h-4 w-4" />
                      )}
                    </div>
                    <div className="text-xs mt-1 opacity-90">{q.topic}</div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Progress Summary */}
          <div className="p-4 border-t bg-gray-50">
            <div className="text-xs font-semibold text-gray-500 mb-2">Progress</div>
            <Progress value={getProgress()} className="h-2 mb-2" />
            <div className="text-xs text-gray-600">{getProgress()}% Complete</div>
            
            {violations.length > 0 && (
              <div className="mt-4 p-2 bg-red-50 border border-red-200 rounded">
                <div className="text-xs font-semibold text-red-700 flex items-center gap-1">
                  <ShieldAlert className="h-3 w-3" />
                  {violations.length} Violation{violations.length !== 1 ? 's' : ''}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* MAIN CONTENT AREA */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* HEADER */}
          <div className="bg-white border-b border-gray-200 px-6 py-4">
            <div className="flex justify-between items-center">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">{test.test_name}</h1>
                <p className="text-sm text-gray-600 mt-1">
                  {currentSection === 'mcq' ? 'Section 1: Multiple Choice Questions' : 'Section 2: Coding Problems'}
                </p>
              </div>
              <div className="text-right">
                <div className={`flex items-center gap-2 ${timeLeft < 600 ? 'text-red-600' : 'text-blue-600'}`}>
                  <Clock className="h-6 w-6" />
                  <span className="text-3xl font-mono font-bold">{formatTime(timeLeft)}</span>
                </div>
                {timeLeft < 600 && (
                  <p className="text-xs text-red-600 mt-1 font-semibold animate-pulse">
                    ⚠️ Less than 10 minutes left!
                  </p>
                )}
              </div>
            </div>
          </div>

          {/* QUESTION AREA */}
          <div className="flex-1 overflow-y-auto p-6">
            <Card className="max-w-5xl mx-auto p-8">
              {/* Question Header */}
              <div className="flex justify-between items-start mb-6">
                <div className="flex gap-3">
                  <Badge 
                    variant={
                      currentQuestion.difficulty === 'hard' ? 'destructive' : 
                      currentQuestion.difficulty === 'medium' ? 'default' : 
                      'secondary'
                    }
                    className="text-sm"
                  >
                    {currentQuestion.difficulty.toUpperCase()}
                  </Badge>
                  <Badge variant="outline" className="text-sm">
                    {currentQuestion.topic}
                  </Badge>
                </div>
                <Badge className="bg-gray-700 text-sm">
                  {currentSection === 'mcq' ? `MCQ ${currentQuestionIndex + 1}/${test.mcq_questions.length}` : `Coding ${currentQuestionIndex + 1}/${test.coding_questions.length}`}
                </Badge>
              </div>

              {/* Question Text */}
              <div className="mb-8">
                <h3 className="text-xl font-semibold text-gray-900 mb-4 leading-relaxed whitespace-pre-wrap">
                  {currentQuestion.question_text}
                </h3>
              </div>

              {/* MCQ OPTIONS */}
              {currentSection === 'mcq' && (
                <div className="space-y-3">
                  {(currentQuestion as MCQQuestion).options.map((option, index) => {
                    const isSelected = mcqAnswers[(currentQuestion as MCQQuestion).question_id] === option.option_letter;
                    
                    return (
                      <label
                        key={index}
                        className={`
                          block p-5 border-2 rounded-xl cursor-pointer transition-all
                          ${isSelected
                            ? 'border-blue-500 bg-blue-50 shadow-md'
                            : 'border-gray-200 hover:border-blue-300 hover:bg-gray-50'
                          }
                        `}
                      >
                        <div className="flex items-start gap-4">
                          <input
                            type="radio"
                            name={`question-${currentQuestion.question_id}`}
                            checked={isSelected}
                            onChange={() => handleMCQAnswer((currentQuestion as MCQQuestion).question_id, option.option_letter)}
                            className="mt-1 h-5 w-5"
                          />
                          <div className="flex-1">
                            <span className="font-bold text-blue-600 text-lg mr-3">{option.option_letter}.</span>
                            <span className="text-gray-800 text-lg">{option.option_text}</span>
                          </div>
                        </div>
                      </label>
                    );
                  })}
                </div>
              )}

              {/* CODING SECTION */}
              {currentSection === 'coding' && (
                <div>
                  {/* Language Badge */}
                  <div className="mb-4 flex justify-between items-center">
                    <Badge className="bg-gray-700 text-sm px-4 py-2">
                      <Code className="h-4 w-4 mr-2" />
                      {(currentQuestion as CodingQuestion).language.toUpperCase()}
                    </Badge>
                    
                    {codingSubmitted[(currentQuestion as CodingQuestion).question_id] && (
                      <Badge className="bg-green-600 text-sm px-4 py-2">
                        <CheckCircle className="h-4 w-4 mr-2" />
                        Solution Submitted
                      </Badge>
                    )}
                  </div>

                  {/* Code Editor */}
                  <div className="border-2 border-gray-300 rounded-lg overflow-hidden mb-4">
                    <div className="bg-gray-800 px-4 py-2 flex justify-between items-center">
                      <span className="text-white text-sm font-mono">
                        {(currentQuestion as CodingQuestion).language}.{(currentQuestion as CodingQuestion).language === 'python' ? 'py' : (currentQuestion as CodingQuestion).language === 'java' ? 'java' : 'js'}
                      </span>
                      <div className="flex gap-2">
                        <Button
                          onClick={() => runCode((currentQuestion as CodingQuestion).question_id)}
                          disabled={executing === (currentQuestion as CodingQuestion).question_id}
                          size="sm"
                          className="bg-green-600 hover:bg-green-700"
                        >
                          {executing === (currentQuestion as CodingQuestion).question_id ? (
                            <>
                              <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-white mr-2"></div>
                              Running...
                            </>
                          ) : (
                            <>
                              <Play className="h-3 w-3 mr-2" />
                              Run Code
                            </>
                          )}
                        </Button>
                        
                        <Button
                          onClick={() => submitCodeSolution((currentQuestion as CodingQuestion).question_id)}
                          disabled={
                            codingSubmitted[(currentQuestion as CodingQuestion).question_id] ||
                            submittingCode === (currentQuestion as CodingQuestion).question_id
                          }
                          size="sm"
                          className="bg-blue-600 hover:bg-blue-700"
                        >
                          {submittingCode === (currentQuestion as CodingQuestion).question_id ? (
                            <>
                              <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-white mr-2"></div>
                              Submitting...
                            </>
                          ) : codingSubmitted[(currentQuestion as CodingQuestion).question_id] ? (
                            <>
                              <CheckCircle className="h-3 w-3 mr-2" />
                              Submitted
                            </>
                          ) : (
                            <>
                              <Send className="h-3 w-3 mr-2" />
                              Submit Solution
                            </>
                          )}
                        </Button>
                      </div>
                    </div>
                    
                    <MonacoEditor
                      height="450px"
                      language={(currentQuestion as CodingQuestion).language}
                      value={codingAnswers[(currentQuestion as CodingQuestion).question_id] || ''}
                      onChange={(value) => handleCodingAnswer((currentQuestion as CodingQuestion).question_id, value || '')}
                      theme="vs-dark"
                      options={{
                        minimap: { enabled: false },
                        fontSize: 15,
                        lineNumbers: 'on',
                        scrollBeyondLastLine: false,
                        automaticLayout: true,
                        tabSize: 4,
                        wordWrap: 'on',
                        readOnly: codingSubmitted[(currentQuestion as CodingQuestion).question_id]
                      }}
                    />
                  </div>

                  {/* Execution Results */}
                  {executionResults[(currentQuestion as CodingQuestion).question_id] && (
                    <Card className={`p-5 mb-4 ${
                      executionResults[(currentQuestion as CodingQuestion).question_id].status === 'Accepted'
                        ? 'bg-green-50 border-green-300'
                        : 'bg-red-50 border-red-300'
                    }`}>
                      <div className="flex items-center gap-4 mb-4">
                        {executionResults[(currentQuestion as CodingQuestion).question_id].status === 'Accepted' ? (
                          <CheckCircle className="h-8 w-8 text-green-600" />
                        ) : (
                          <XCircle className="h-8 w-8 text-red-600" />
                        )}
                        <div className="flex-1">
                          <h4 className={`font-bold text-xl ${
                            executionResults[(currentQuestion as CodingQuestion).question_id].status === 'Accepted'
                              ? 'text-green-700'
                              : 'text-red-700'
                          }`}>
                            {executionResults[(currentQuestion as CodingQuestion).question_id].status}
                          </h4>
                          <p className="text-sm text-gray-700 mt-1">
                            {executionResults[(currentQuestion as CodingQuestion).question_id].passed_count} / {executionResults[(currentQuestion as CodingQuestion).question_id].total_count} test cases passed
                          </p>
                        </div>
                        <div className="text-right space-y-1">
                          <div>
                            <p className="text-xs text-gray-600">Runtime</p>
                            <p className="font-mono font-bold text-lg">{executionResults[(currentQuestion as CodingQuestion).question_id].total_runtime_ms.toFixed(2)} ms</p>
                          </div>
                          <div>
                            <p className="text-xs text-gray-600">Memory</p>
                            <p className="font-mono font-bold text-lg">{executionResults[(currentQuestion as CodingQuestion).question_id].memory_mb.toFixed(2)} MB</p>
                          </div>
                        </div>
                      </div>

                      {/* Test Case Details */}
                      <div className="space-y-3 mt-4">
                        {executionResults[(currentQuestion as CodingQuestion).question_id].test_results.slice(0, 5).map((testCase: TestCaseResult, idx: number) => (
                          <div
                            key={idx}
                            className={`p-4 rounded-lg border-2 ${
                              testCase.passed
                                ? 'bg-green-100 border-green-400'
                                : 'bg-red-100 border-red-400'
                            }`}
                          >
                            <div className="flex items-center justify-between mb-2">
                              <span className="font-semibold">Test Case {idx + 1}</span>
                              {testCase.passed ? (
                                <Badge className="bg-green-600">✓ Passed</Badge>
                              ) : (
                                <Badge variant="destructive">✗ Failed</Badge>
                              )}
                            </div>
                            {!testCase.passed && (
                              <div className="text-sm font-mono space-y-2 mt-3">
                                <div>
                                  <span className="text-gray-700 font-semibold">Input:</span>
                                  <pre className="bg-white p-3 rounded mt-1 border">{testCase.input}</pre>
                                </div>
                                <div>
                                  <span className="text-gray-700 font-semibold">Expected:</span>
                                  <pre className="bg-white p-3 rounded mt-1 border">{testCase.expected_output}</pre>
                                </div>
                                <div>
                                  <span className="text-gray-700 font-semibold">Your Output:</span>
                                  <pre className="bg-white p-3 rounded mt-1 border text-red-600">{testCase.actual_output}</pre>
                                </div>
                                {testCase.error && (
                                  <div>
                                    <span className="text-red-700 font-semibold">Error:</span>
                                    <pre className="bg-white p-3 rounded mt-1 border text-red-600">{testCase.error}</pre>
                                  </div>
                                )}
                              </div>
                            )}
                          </div>
                        ))}
                      </div>

                      {executionResults[(currentQuestion as CodingQuestion).question_id].message && (
                        <p className="text-sm text-gray-600 mt-4 italic">
                          {executionResults[(currentQuestion as CodingQuestion).question_id].message}
                        </p>
                      )}
                    </Card>
                  )}

                  {/* Sample Test Cases */}
                  <div className="mt-4">
                    <h4 className="font-semibold text-gray-900 mb-3">Sample Test Cases:</h4>
                    <div className="space-y-3">
                      {(currentQuestion as CodingQuestion).visible_test_cases?.map((tc, idx) => (
                        <div key={idx} className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                          <div className="font-semibold text-sm text-gray-700 mb-2">Example {idx + 1}</div>
                          <div className="font-mono text-sm space-y-2">
                            <div>
                              <span className="text-gray-600">Input:</span>
                              <pre className="bg-white p-2 rounded mt-1 border">{tc.input}</pre>
                            </div>
                            <div>
                              <span className="text-gray-600">Output:</span>
                              <pre className="bg-white p-2 rounded mt-1 border">{tc.expected_output}</pre>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <p className="text-xs text-gray-500 mt-4 italic">
                    💡 Tip: Click "Run Code" to test with visible cases. Click "Submit Solution" when ready to test with all hidden cases.
                  </p>
                </div>
              )}
            </Card>
          </div>

          {/* FOOTER NAVIGATION */}
          <div className="bg-white border-t border-gray-200 px-6 py-4">
            <div className="max-w-5xl mx-auto flex justify-between items-center">
              <Button
                onClick={goToPreviousQuestion}
                disabled={currentSection === 'mcq' && currentQuestionIndex === 0}
                variant="outline"
                size="lg"
              >
                <ChevronLeft className="h-5 w-5 mr-2" />
                Previous
              </Button>

              <div className="flex gap-3">
                {!isLastQuestion ? (
                  <Button onClick={goToNextQuestion} size="lg" className="bg-blue-600 hover:bg-blue-700">
                    Next
                    <ChevronRight className="h-5 w-5 ml-2" />
                  </Button>
                ) : (
                  <Button
                    onClick={() => submitTest(false)}
                    disabled={submitting}
                    size="lg"
                    className="bg-green-600 hover:bg-green-700"
                  >
                    {submitting ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                        Submitting Test...
                      </>
                    ) : (
                      <>
                        <Send className="h-5 w-5 mr-2" />
                        Submit Test
                      </>
                    )}
                  </Button>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Timer Expired Warning */}
      {timerExpired && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
          <Card className="p-8 max-w-md text-center">
            <Clock className="h-16 w-16 text-red-600 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Time's Up!</h2>
            <p className="text-gray-600 mb-4">
              Your test is being submitted automatically...
            </p>
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          </Card>
        </div>
      )}
    </div>
  );
}
