'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { TrendChart } from '@/components/ui/trend-chart';
import {
  TrendingUp,
  TrendingDown,
  Award,
  Target,
  Brain,
  Zap,
  BarChart3,
  AlertCircle
} from 'lucide-react';

interface PerformanceData {
  user_role_id: number;
  total_tests_taken: number;
  average_score: number;
  best_score: number;
  worst_score: number;
  score_trend: Array<{ date: string; score: number; test_name: string }>;
  accuracy_improvement: number;
  strong_areas: Array<{ topic: string; accuracy: number; questions_attempted: number; questions_correct: number }>;
  weak_areas: Array<{ topic: string; accuracy: number; questions_attempted: number; questions_correct: number }>;
  last_updated: string;
}

export default function PerformancePage() {
  const router = useRouter();
  const [performance, setPerformance] = useState<PerformanceData | null>(null);
  const [loading, setLoading] = useState(true);
  const [dailyQuote, setDailyQuote] = useState({ quote_text: '', author: '' });

  useEffect(() => {
    loadPerformanceData();
    loadDailyQuote();
  }, []);

  const loadPerformanceData = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        return;
      }

      // Get user_role_id from localStorage (set by roadmap page)
      let userRoleId: string | null = localStorage.getItem('currentUserRoleId');
      
      // If not set, try to load from saved roadmaps
      if (!userRoleId) {
        const savedRoadmaps = localStorage.getItem('user_roadmaps');
        if (savedRoadmaps) {
          try {
            const roadmaps = JSON.parse(savedRoadmaps);
            if (roadmaps && roadmaps.length > 0) {
              const latestRoadmap = roadmaps[roadmaps.length - 1];
              if (latestRoadmap.user_role_id) {
                const roleIdStr = latestRoadmap.user_role_id.toString();
                localStorage.setItem('currentUserRoleId', roleIdStr);
                userRoleId = roleIdStr;
              }
            }
          } catch (e) {
            console.error('Failed to parse saved roadmaps:', e);
          }
        }
      }

      if (!userRoleId) {
        console.error('No user role ID found');
        return;
      }

      const response = await fetch(`http://localhost:8000/api/performance/summary?user_role_id=${userRoleId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setPerformance(data);
      } else {
        console.error('Performance API error:', response.status);
      }
    } catch (error) {
      console.error('Error loading performance:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadDailyQuote = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/daily-quote');
      if (response.ok) {
        const data = await response.json();
        setDailyQuote(data);
      }
    } catch (error) {
      console.error('Error loading quote:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!performance) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <AlertCircle size={48} className="mx-auto mb-4 text-gray-400" />
          <p className="text-gray-600">No performance data available yet</p>
          <button
            onClick={() => router.push('/mock-test')}
            className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Take Your First Test
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Daily Quote */}
        {dailyQuote.quote_text && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-2xl p-6 mb-8 shadow-xl"
          >
            <p className="text-xl italic mb-2">&quot;{dailyQuote.quote_text}&quot;</p>
            <p className="text-right text-blue-100">— {dailyQuote.author}</p>
          </motion.div>
        )}

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
            Performance Analytics
          </h1>
          <p className="text-gray-600">Track your progress and identify areas for improvement</p>
        </motion.div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white rounded-xl shadow-lg p-6"
          >
            <div className="flex items-center justify-between mb-4">
              <Award className="text-blue-600" size={32} />
              <span className="text-3xl font-bold text-blue-600">{performance.total_tests_taken}</span>
            </div>
            <p className="text-gray-600 text-sm">Tests Completed</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
            className="bg-white rounded-xl shadow-lg p-6"
          >
            <div className="flex items-center justify-between mb-4">
              <Target className="text-green-600" size={32} />
              <span className="text-3xl font-bold text-green-600">{performance.average_score.toFixed(1)}%</span>
            </div>
            <p className="text-gray-600 text-sm">Average Score</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-xl shadow-lg p-6"
          >
            <div className="flex items-center justify-between mb-4">
              <TrendingUp className="text-purple-600" size={32} />
              <span className="text-3xl font-bold text-purple-600">{performance.best_score.toFixed(1)}%</span>
            </div>
            <p className="text-gray-600 text-sm">Best Score</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
            className="bg-white rounded-xl shadow-lg p-6"
          >
            <div className="flex items-center justify-between mb-4">
              {performance.accuracy_improvement >= 0 ? (
                <TrendingUp className="text-green-600" size={32} />
              ) : (
                <TrendingDown className="text-red-600" size={32} />
              )}
              <span className={`text-3xl font-bold ${performance.accuracy_improvement >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {performance.accuracy_improvement >= 0 ? '+' : ''}{performance.accuracy_improvement.toFixed(1)}%
              </span>
            </div>
            <p className="text-gray-600 text-sm">Improvement</p>
          </motion.div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Score Trend Graph */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-2xl shadow-xl p-6"
          >
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
              <BarChart3 className="text-blue-600" />
              Score Trend (Last 10 Tests)
            </h2>
            <div className="pl-8">
              <TrendChart data={performance.score_trend.slice(-10)} height={250} />
            </div>
            {performance.score_trend.length > 0 && (
              <div className="mt-6 pt-4 border-t">
                <div className="grid grid-cols-2 gap-4 text-center">
                  <div>
                    <p className="text-sm text-gray-500">Latest Score</p>
                    <p className="text-2xl font-bold text-blue-600">
                      {performance.score_trend[performance.score_trend.length - 1].score.toFixed(1)}%
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Tests Taken</p>
                    <p className="text-2xl font-bold text-purple-600">
                      {performance.score_trend.length}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </motion.div>


          {/* Strong & Weak Areas */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-2xl shadow-xl p-6"
          >
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
              <Brain className="text-green-600" />
              Strong Areas
            </h2>
            <div className="space-y-4">
              {performance.strong_areas.slice(0, 5).map((area, index) => (
                <div key={index} className="bg-green-50 rounded-lg p-4">
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-semibold text-gray-800">{area.topic}</span>
                    <span className="text-green-600 font-bold">{(area.accuracy * 100).toFixed(0)}%</span>
                  </div>
                  <div className="text-sm text-gray-600">
                    {area.questions_correct} / {area.questions_attempted} correct
                  </div>
                  <div className="mt-2 bg-white rounded-full h-2 overflow-hidden">
                    <div
                      className="bg-green-500 h-full rounded-full"
                      style={{ width: `${area.accuracy * 100}%` }}
                    ></div>
                  </div>
                </div>
              ))}
              {performance.strong_areas.length === 0 && (
                <p className="text-center text-gray-500 py-8">No data yet. Keep taking tests!</p>
              )}
            </div>
          </motion.div>
        </div>

        {/* Weak Areas - Needs Improvement */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl shadow-xl p-6"
        >
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
            <Zap className="text-orange-600" />
            Areas for Improvement
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {performance.weak_areas.slice(0, 6).map((area, index) => (
              <div key={index} className="bg-orange-50 rounded-lg p-4 border-l-4 border-orange-500">
                <div className="flex justify-between items-center mb-2">
                  <span className="font-semibold text-gray-800">{area.topic}</span>
                  <span className="text-orange-600 font-bold">{(area.accuracy * 100).toFixed(0)}%</span>
                </div>
                <div className="text-sm text-gray-600 mb-2">
                  {area.questions_correct} / {area.questions_attempted} correct
                </div>
                <div className="bg-white rounded-full h-2 overflow-hidden">
                  <div
                    className="bg-orange-500 h-full rounded-full"
                    style={{ width: `${area.accuracy * 100}%` }}
                  ></div>
                </div>
                <div className="mt-3 space-y-2">
                  <p className="text-xs text-gray-600 italic">
                    💡 Focus on practicing {area.topic} fundamentals and edge cases
                  </p>
                  <button 
                    onClick={() => router.push('/roadmap')}
                    className="w-full text-sm bg-orange-600 text-white py-2 rounded hover:bg-orange-700 transition-colors"
                  >
                    Practice Now
                  </button>
                </div>
              </div>
            ))}
            {performance.weak_areas.length === 0 && (
              <div className="col-span-full text-center text-gray-500 py-8">
                <p>Great job! No weak areas identified yet.</p>
              </div>
            )}
          </div>

          {/* AI-Powered Improvement Suggestions */}
          {performance.weak_areas.length > 0 && (
            <div className="mt-6 p-5 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl border-2 border-blue-200">
              <h3 className="font-bold text-lg mb-3 flex items-center gap-2">
                <Brain className="text-purple-600" />
                AI-Powered Recommendations
              </h3>
              <div className="space-y-3">
                {performance.weak_areas.slice(0, 3).map((area, idx) => (
                  <div key={idx} className="bg-white p-4 rounded-lg shadow-sm">
                    <p className="font-semibold text-gray-800 mb-2">📖 {area.topic}</p>
                    <p className="text-sm text-gray-600 mb-2">
                      Your accuracy is {(area.accuracy * 100).toFixed(0)}% - here&apos;s how to improve:
                    </p>
                    <ul className="text-sm text-gray-700 space-y-1 ml-4">
                      <li>• Review fundamental concepts and common patterns in {area.topic}</li>
                      <li>• Practice {Math.max(10, Math.ceil((1 - area.accuracy) * 20))} more problems focusing on edge cases</li>
                      <li>• Analyze mistakes from previous attempts to identify knowledge gaps</li>
                      <li>• Watch tutorials or read documentation specific to {area.topic}</li>
                    </ul>
                  </div>
                ))}
                <div className="bg-blue-600 text-white p-4 rounded-lg">
                  <p className="font-semibold mb-2">🎯 Your Improvement Plan</p>
                  <p className="text-sm">
                    Focus on {performance.weak_areas.length} topics. Dedicate 30 minutes daily to practice.
                    Expected improvement: +{Math.min(25, performance.weak_areas.length * 5)}% accuracy within 2 weeks.
                  </p>
                </div>
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}
