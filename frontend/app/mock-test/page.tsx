'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { 
  BookOpen, 
  Code, 
  Clock, 
  TrendingUp, 
  Award,
  Play,
  History
} from 'lucide-react';

interface TestHistory {
  test_id: number;
  test_name: string;
  test_date: string;
  total_score: number;
  mcq_score: number;
  coding_score: number;
  status: string;
  time_taken_minutes: number;
}

// Calculate test duration based on question counts
const getTestDuration = (mcqCount: number, codingCount: number): string => {
  // Rules:
  // 10 MCQ + 2 Coding = 2 hours
  // 15 MCQ + 2 Coding = 2.5 hours
  // 20 MCQ + 2 Coding = 2 hours 45 minutes
  // 15 MCQ + 3 Coding = 3 hours
  // 10 MCQ + 4 Coding = 3.5 hours
  // 20 MCQ + 4 Coding = 3.5 hours
  
  if (mcqCount === 10 && codingCount === 2) return '2 hours';
  if (mcqCount === 15 && codingCount === 2) return '2.5 hours';
  if (mcqCount === 20 && codingCount === 2) return '2 hrs 45 min';
  if (mcqCount === 15 && codingCount === 3) return '3 hours';
  if (mcqCount === 10 && codingCount === 4) return '3.5 hours';
  if (mcqCount === 20 && codingCount === 4) return '3.5 hours';
  
  // Default calculation for other combinations
  const minutes = mcqCount * 3 + codingCount * 30; // 3 min per MCQ, 30 min per coding
  const hours = minutes / 60;
  
  if (hours === Math.floor(hours)) {
    return `${hours} hour${hours !== 1 ? 's' : ''}`;
  } else {
    return `${hours.toFixed(1)} hours`;
  }
};

// Get test duration in seconds
const getTestDurationInSeconds = (mcqCount: number, codingCount: number): number => {
  // Convert hours to seconds
  if (mcqCount === 10 && codingCount === 2) return 2 * 3600; // 2 hours
  if (mcqCount === 15 && codingCount === 2) return 2.5 * 3600; // 2.5 hours
  if (mcqCount === 20 && codingCount === 2) return 165 * 60; // 2 hours 45 minutes = 165 minutes
  if (mcqCount === 15 && codingCount === 3) return 3 * 3600; // 3 hours
  if (mcqCount === 10 && codingCount === 4) return 3.5 * 3600; // 3.5 hours
  if (mcqCount === 20 && codingCount === 4) return 3.5 * 3600; // 3.5 hours
  
  // Default calculation
  const minutes = mcqCount * 3 + codingCount * 30;
  return minutes * 60;
};

export default function MockTestPage() {
  const router = useRouter();
  const [mcqCount, setMcqCount] = useState(15);
  const [codingCount, setCodingCount] = useState(3);
  const [generating, setGenerating] = useState(false);
  const [testHistory, setTestHistory] = useState<TestHistory[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Auto-load currentUserRoleId from saved roadmaps if not set
    let userRoleId = localStorage.getItem('currentUserRoleId');
    if (!userRoleId) {
      const savedRoadmaps = localStorage.getItem('user_roadmaps');
      if (savedRoadmaps) {
        try {
          const roadmaps = JSON.parse(savedRoadmaps);
          if (roadmaps && roadmaps.length > 0) {
            // Use the most recent roadmap (last in array)
            const latestRoadmap = roadmaps[roadmaps.length - 1];
            if (latestRoadmap.user_role_id) {
              localStorage.setItem('currentUserRoleId', latestRoadmap.user_role_id.toString());
            }
          }
        } catch (e) {
          console.error('Failed to parse saved roadmaps:', e);
        }
      }
    }
    loadTestHistory();
  }, []);

  const loadTestHistory = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        setLoading(false);
        return;
      }

      // Get user_role_id
      let userRoleId: string | null = localStorage.getItem('currentUserRoleId');
      if (!userRoleId) {
        const savedRoadmaps = localStorage.getItem('user_roadmaps');
        if (savedRoadmaps) {
          try {
            const roadmaps = JSON.parse(savedRoadmaps);
            if (roadmaps && Array.isArray(roadmaps) && roadmaps.length > 0) {
              const latestRoadmap = roadmaps[roadmaps.length - 1];
              if (latestRoadmap && latestRoadmap.user_role_id) {
                userRoleId = String(latestRoadmap.user_role_id);
                localStorage.setItem('currentUserRoleId', userRoleId);
              }
            }
          } catch (e) {
            console.error('Failed to parse saved roadmaps:', e);
          }
        }
      }

      if (!userRoleId) {
        // No roadmap yet, skip loading history
        setLoading(false);
        return;
      }

      const response = await fetch(`http://localhost:8000/api/mock-tests/history?user_role_id=${userRoleId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setTestHistory(data.tests || []);
      }
    } catch (error) {
      console.error('Error loading test history:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateTest = async () => {
    setGenerating(true);
    try {
      const token = localStorage.getItem('auth_token');
      let userRoleId: string | null = localStorage.getItem('currentUserRoleId');

      if (!token) {
        alert('Please login first');
        router.push('/login');
        return;
      }

      // Get user_role_id from saved roadmaps if not in localStorage
      if (!userRoleId) {
        const savedRoadmaps = localStorage.getItem('user_roadmaps');
        if (savedRoadmaps) {
          try {
            const roadmaps = JSON.parse(savedRoadmaps);
            if (roadmaps && Array.isArray(roadmaps) && roadmaps.length > 0) {
              const latestRoadmap = roadmaps[roadmaps.length - 1];
              if (latestRoadmap && latestRoadmap.user_role_id) {
                userRoleId = String(latestRoadmap.user_role_id);
                localStorage.setItem('currentUserRoleId', userRoleId);
              }
            }
          } catch (e) {
            console.error('Failed to parse saved roadmaps:', e);
          }
        }
      }

      if (!userRoleId) {
        alert('Please create a roadmap first');
        router.push('/roadmap');
        return;
      }

      // Get completed topics from completed daily plans
      const completedDaysData = localStorage.getItem('completed_daily_plans');
      let completedDayNumbers: number[] = [];
      
      if (completedDaysData) {
        try {
          const parsed = JSON.parse(completedDaysData);
          if (parsed && typeof parsed === 'object') {
            const roleCompletedDays = parsed[userRoleId] || [];
            completedDayNumbers = Array.isArray(roleCompletedDays) ? roleCompletedDays : [];
          }
        } catch (e) {
          console.error('Failed to parse completed days:', e);
        }
      }

      if (completedDayNumbers.length === 0) {
        alert('⚠️ No completed topics found!\n\nPlease:\n1. Go to Daily Plan page\n2. Complete (tick) at least 5 days\n3. Come back and generate test\n\nQuestions will ONLY come from your completed topics!');
        router.push('/daily-plan');
        return;
      }

      console.log('✅ Generating test with:', {
        userRoleId,
        completedDayNumbers,
        mcqCount,
        codingCount
      });

      // Calculate time limit in minutes based on question counts
      const timeLimitSeconds = getTestDurationInSeconds(mcqCount, codingCount);
      const timeLimitMinutes = timeLimitSeconds / 60;

      // Store test duration in localStorage for the test page
      localStorage.setItem('currentTestDuration', timeLimitSeconds.toString());

      const response = await fetch('http://localhost:8000/api/mock-tests/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          user_role_id: parseInt(userRoleId),
          mcq_count: mcqCount,
          coding_count: codingCount,
          test_name: `Mock Test - ${new Date().toLocaleDateString()}`,
          completed_day_numbers: completedDayNumbers,
          time_limit_minutes: timeLimitMinutes
        })
      });

      if (response.ok) {
        const data = await response.json();
        // Navigate to test taking page
        router.push(`/mock-test/take/${data.test_id}`);
      } else {
        const errorData = await response.json().catch(() => null);
        const errorMessage = errorData?.detail || 'Failed to generate test';
        
        alert(`Error: ${errorMessage}\n\nPlease make sure:\n1. Backend server is running on http://localhost:8000\n2. You have completed at least 5 days in Daily Plan\n3. You are logged in\n4. You have created a roadmap`);
        
        console.error('Server response:', response.status, errorData);
      }
    } catch (error: any) {
      console.error('Error generating test:', error);
      
      // Better error message
      let errorMessage = 'Network error: Failed to connect to backend';
      if (error.message) {
        errorMessage += `\n\nDetails: ${error.message}`;
      }
      
      alert(`${errorMessage}\n\nPlease check:\n1. Backend is running: http://localhost:8000\n2. Check browser console for details (F12)\n3. Try refreshing the page\n4. Make sure you're logged in`);
    } finally {
      setGenerating(false);
    }
  };

  const handleViewTest = (testId: number) => {
    router.push(`/mock-test/results/${testId}`);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
            Smart Mock Tests
          </h1>
          <p className="text-gray-600">
            Personalized tests based on topics you&apos;ve completed
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Test Generation Panel */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-2xl shadow-xl p-8"
          >
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
              <Play className="text-blue-600" />
              Generate New Test
            </h2>

            {/* MCQ Count */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-3">
                <BookOpen className="inline mr-2" size={18} />
                MCQ Questions
              </label>
              <div className="flex gap-4">
                {[10, 15, 20].map((count) => (
                  <button
                    key={count}
                    onClick={() => setMcqCount(count)}
                    className={`flex-1 py-3 rounded-lg font-semibold transition-all ${
                      mcqCount === count
                        ? 'bg-blue-600 text-white shadow-lg scale-105'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {count}
                  </button>
                ))}
              </div>
            </div>

            {/* Coding Count */}
            <div className="mb-8">
              <label className="block text-sm font-medium text-gray-700 mb-3">
                <Code className="inline mr-2" size={18} />
                Coding Questions
              </label>
              <div className="flex gap-4">
                {[2, 3, 4].map((count) => (
                  <button
                    key={count}
                    onClick={() => setCodingCount(count)}
                    className={`flex-1 py-3 rounded-lg font-semibold transition-all ${
                      codingCount === count
                        ? 'bg-purple-600 text-white shadow-lg scale-105'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {count}
                  </button>
                ))}
              </div>
            </div>

            {/* Test Info */}
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 mb-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-gray-600">Total Questions:</span>
                <span className="font-bold text-lg">{mcqCount + codingCount}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600 flex items-center gap-2">
                  <Clock size={16} />
                  Time Allocated:
                </span>
                <span className="font-bold text-lg text-green-600">{getTestDuration(mcqCount, codingCount)}</span>
              </div>
            </div>

            {/* Generate Button */}
            <button
              onClick={handleGenerateTest}
              disabled={generating}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 rounded-lg font-bold text-lg hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {generating ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  Generating Test...
                </span>
              ) : (
                'Generate Test & Start'
              )}
            </button>

            <p className="text-xs text-gray-500 mt-3 text-center">
              ✅ Questions generated ONLY from your completed topics
            </p>
          </motion.div>

          {/* Test History */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-2xl shadow-xl p-8"
          >
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
              <History className="text-purple-600" />
              Test History
            </h2>

            {loading ? (
              <div className="flex justify-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
              </div>
            ) : testHistory.length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                <Award size={48} className="mx-auto mb-4 opacity-50" />
                <p>No tests taken yet</p>
                <p className="text-sm">Generate your first test to get started!</p>
              </div>
            ) : (
              <div className="space-y-4 max-h-[500px] overflow-y-auto">
                {testHistory.map((test) => (
                  <div
                    key={test.test_id}
                    onClick={() => handleViewTest(test.test_id)}
                    className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 cursor-pointer hover:shadow-lg transition-all"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-semibold text-gray-800">{test.test_name}</h3>
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        test.status === 'completed' 
                          ? 'bg-green-100 text-green-700'
                          : 'bg-yellow-100 text-yellow-700'
                      }`}>
                        {test.status}
                      </span>
                    </div>
                    
                    <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
                      <span>{new Date(test.test_date).toLocaleDateString()}</span>
                      <span className="flex items-center gap-1">
                        <Clock size={14} />
                        {test.time_taken_minutes} min
                      </span>
                    </div>

                    {test.status === 'completed' && (
                      <div className="grid grid-cols-3 gap-2 mt-3">
                        <div className="bg-white rounded p-2 text-center">
                          <div className="text-xs text-gray-500">Total</div>
                          <div className="text-lg font-bold text-blue-600">{test.total_score.toFixed(1)}%</div>
                        </div>
                        <div className="bg-white rounded p-2 text-center">
                          <div className="text-xs text-gray-500">MCQ</div>
                          <div className="text-lg font-bold text-green-600">{test.mcq_score.toFixed(1)}%</div>
                        </div>
                        <div className="bg-white rounded p-2 text-center">
                          <div className="text-xs text-gray-500">Code</div>
                          <div className="text-lg font-bold text-purple-600">{test.coding_score.toFixed(1)}%</div>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </motion.div>
        </div>

        {/* Quick Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          <div className="bg-white rounded-xl shadow-lg p-6 text-center">
            <TrendingUp className="mx-auto mb-3 text-blue-600" size={32} />
            <div className="text-3xl font-bold text-blue-600">{testHistory.length}</div>
            <div className="text-gray-600 text-sm">Tests Taken</div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6 text-center">
            <Award className="mx-auto mb-3 text-green-600" size={32} />
            <div className="text-3xl font-bold text-green-600">
              {testHistory.length > 0
                ? (testHistory.reduce((sum, t) => sum + t.total_score, 0) / testHistory.length).toFixed(1)
                : '0.0'}%
            </div>
            <div className="text-gray-600 text-sm">Average Score</div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6 text-center">
            <BookOpen className="mx-auto mb-3 text-purple-600" size={32} />
            <div className="text-3xl font-bold text-purple-600">
              {testHistory.reduce((sum, t) => sum + (t.time_taken_minutes || 0), 0)}
            </div>
            <div className="text-gray-600 text-sm">Total Minutes</div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
