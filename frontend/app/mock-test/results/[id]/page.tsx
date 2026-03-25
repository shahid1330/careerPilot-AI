'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { 
  CheckCircle2, 
  XCircle, 
  Clock, 
  Target, 
  TrendingUp,
  AlertCircle,
  ArrowLeft,
  Code
} from 'lucide-react';

interface MCQResult {
  question_id: number;
  question_text: string;
  selected_option: number;
  correct_option: number;
  is_correct: boolean;
  difficulty: string;
  options: string[];
}

interface CodingResult {
  question_id: number;
  question_text: string;
  submitted_code: string;
  feedback: string;
  difficulty: string;
}

interface TestResults {
  test_id: number;
  test_name: string;
  submitted_at: string;
  mcq_score: number;
  coding_score: number;
  overall_score: number;
  mcq_results: MCQResult[];
  coding_results: CodingResult[];
  time_taken_minutes: number;
}

export default function TestResultsPage() {
  const params = useParams();
  const router = useRouter();
  const testId = params.id as string;

  const [results, setResults] = useState<TestResults | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'mcq' | 'coding'>('overview');

  useEffect(() => {
    const loadResults = async () => {
      try {
        const token = localStorage.getItem('auth_token');
        if (!token) {
          router.push('/login');
          return;
        }

        // Fetch results from the test history endpoint
        const response = await fetch('http://localhost:8000/api/mock-tests/history', {
          headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
          const data = await response.json();
          const test = data.tests.find((t: any) => t.test_id === parseInt(testId));
          
          if (test && test.submitted_at) {
            setResults(test);
          } else {
            alert('Results not found or test not submitted');
            router.push('/mock-test');
          }
        } else {
          alert('Failed to load results');
          router.push('/mock-test');
        }
      } catch (error) {
        console.error('Error loading results:', error);
        alert('Failed to load results');
        router.push('/mock-test');
      } finally {
        setLoading(false);
      }
    };

    loadResults();
  }, [testId, router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading results...</p>
        </div>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <span>Results not found</span>
        </Alert>
      </div>
    );
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBadgeVariant = (score: number): 'default' | 'secondary' | 'destructive' => {
    if (score >= 80) return 'default';
    if (score >= 60) return 'secondary';
    return 'destructive';
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      {/* Header */}
      <div className="mb-6">
        <Button
          onClick={() => router.push('/mock-test')}
          variant="ghost"
          className="mb-4"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Mock Tests
        </Button>
        
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{results.test_name}</h1>
            <p className="text-sm text-gray-600 mt-1">
              Submitted on {new Date(results.submitted_at).toLocaleString()}
            </p>
          </div>
          <Badge variant={getScoreBadgeVariant(results.overall_score)} className="text-lg px-4 py-2">
            {results.overall_score}% Overall
          </Badge>
        </div>
      </div>

      {/* Score Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <Card className="p-6 bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-blue-700 font-medium">Overall Score</p>
              <p className={`text-3xl font-bold ${getScoreColor(results.overall_score)}`}>
                {results.overall_score}%
              </p>
            </div>
            <Target className="h-10 w-10 text-blue-600 opacity-50" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-to-br from-green-50 to-green-100 border-green-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-green-700 font-medium">MCQ Score</p>
              <p className={`text-3xl font-bold ${getScoreColor(results.mcq_score)}`}>
                {results.mcq_score}%
              </p>
            </div>
            <CheckCircle2 className="h-10 w-10 text-green-600 opacity-50" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-purple-700 font-medium">Coding Score</p>
              <p className={`text-3xl font-bold ${getScoreColor(results.coding_score)}`}>
                {results.coding_score}%
              </p>
            </div>
            <Code className="h-10 w-10 text-purple-600 opacity-50" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-to-br from-orange-50 to-orange-100 border-orange-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-orange-700 font-medium">Time Taken</p>
              <p className="text-3xl font-bold text-orange-900">
                {results.time_taken_minutes}m
              </p>
            </div>
            <Clock className="h-10 w-10 text-orange-600 opacity-50" />
          </div>
        </Card>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <div className="flex gap-4">
          <button
            onClick={() => setActiveTab('overview')}
            className={`px-4 py-2 border-b-2 font-medium transition-colors ${
              activeTab === 'overview'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => setActiveTab('mcq')}
            className={`px-4 py-2 border-b-2 font-medium transition-colors ${
              activeTab === 'mcq'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            MCQ Details ({results.mcq_results.length})
          </button>
          <button
            onClick={() => setActiveTab('coding')}
            className={`px-4 py-2 border-b-2 font-medium transition-colors ${
              activeTab === 'coding'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            Coding Details ({results.coding_results.length})
          </button>
        </div>
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <Card className="p-6">
            <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-blue-600" />
              Performance Summary
            </h3>
            
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="font-medium">MCQ Performance</span>
                  <span className="text-gray-600">
                    {results.mcq_results.filter(r => r.is_correct).length} / {results.mcq_results.length} correct
                  </span>
                </div>
                <Progress value={results.mcq_score} className="h-3" />
              </div>

              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="font-medium">Coding Performance</span>
                  <span className="text-gray-600">{results.coding_score}%</span>
                </div>
                <Progress value={results.coding_score} className="h-3" />
              </div>
            </div>

            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-blue-900">
                <strong>Recommendation:</strong>{' '}
                {results.overall_score >= 80
                  ? 'Excellent performance! Keep up the great work.'
                  : results.overall_score >= 60
                  ? 'Good effort! Review the questions you got wrong and practice more.'
                  : 'You need more practice. Review the concepts and try again.'}
              </p>
            </div>
          </Card>
        </div>
      )}

      {activeTab === 'mcq' && (
        <div className="space-y-4">
          {results.mcq_results.map((result, index) => (
            <Card key={result.question_id} className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <span className="font-semibold text-gray-700">Q{index + 1}</span>
                  <Badge variant={result.difficulty === 'hard' ? 'destructive' : result.difficulty === 'medium' ? 'default' : 'secondary'}>
                    {result.difficulty}
                  </Badge>
                  {result.is_correct ? (
                    <CheckCircle2 className="h-5 w-5 text-green-600" />
                  ) : (
                    <XCircle className="h-5 w-5 text-red-600" />
                  )}
                </div>
              </div>

              <p className="text-gray-900 font-medium mb-4">{result.question_text}</p>

              <div className="space-y-2">
                {result.options.map((option, idx) => (
                  <div
                    key={idx}
                    className={`p-3 rounded-lg border-2 ${
                      idx === result.correct_option
                        ? 'border-green-500 bg-green-50'
                        : idx === result.selected_option
                        ? 'border-red-500 bg-red-50'
                        : 'border-gray-200 bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span>{option}</span>
                      {idx === result.correct_option && (
                        <Badge variant="default" className="bg-green-600">Correct</Badge>
                      )}
                      {idx === result.selected_option && idx !== result.correct_option && (
                        <Badge variant="destructive">Your Answer</Badge>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          ))}
        </div>
      )}

      {activeTab === 'coding' && (
        <div className="space-y-4">
          {results.coding_results.map((result, index) => (
            <Card key={result.question_id} className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <span className="font-semibold text-gray-700">Coding Q{index + 1}</span>
                  <Badge variant={result.difficulty === 'hard' ? 'destructive' : result.difficulty === 'medium' ? 'default' : 'secondary'}>
                    {result.difficulty}
                  </Badge>
                </div>
              </div>

              <p className="text-gray-900 font-medium mb-4">{result.question_text}</p>

              <div className="mb-4">
                <h4 className="text-sm font-semibold text-gray-700 mb-2">Your Solution:</h4>
                <pre className="p-4 bg-gray-900 text-gray-100 rounded-lg overflow-x-auto text-sm font-mono">
                  {result.submitted_code || '// No code submitted'}
                </pre>
              </div>

              <div className="p-4 bg-blue-50 rounded-lg">
                <h4 className="text-sm font-semibold text-blue-900 mb-2">AI Feedback:</h4>
                <p className="text-sm text-blue-800 whitespace-pre-wrap">{result.feedback}</p>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
