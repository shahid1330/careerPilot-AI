'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import {
  Brain, TrendingUp, Target, Zap, Award, Star,
  BarChart3, Activity, Briefcase, CheckCircle,
  AlertCircle, Calendar, Clock, Rocket
} from 'lucide-react';

interface CareerDNA {
  logical_ability: number;
  problem_solving: number;
  speed: number;
  consistency: number;
  learning_efficiency: number;
  overall_score: number;
}

interface SkillNode {
  skill_name: string;
  mastery_level: number;
  category: string;
}

interface CareerForecast {
  internship_readiness: number;
  placement_readiness: number;
  recommended_roles: string[];
  estimated_timeline: string;
}

interface CareerIntelligenceData {
  career_dna: CareerDNA;
  skill_graph: SkillNode[];
  forecast: CareerForecast;
  weekly_strategy: {
    focus_topics: string[];
    practice_hours: number;
    improvement_areas: string[];
  };
  insights: string[];
}

export default function CareerIntelligencePage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<CareerIntelligenceData | null>(null);

  useEffect(() => {
    loadCareerIntelligence();
  }, []);

  const loadCareerIntelligence = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      const userRoleId = localStorage.getItem('currentUserRoleId');
      
      if (!token || !userRoleId) {
        router.push('/login');
        return;
      }

      const response = await fetch(`http://localhost:8000/api/career-intelligence/profile?user_role_id=${userRoleId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const result = await response.json();
        setData(result);
      } else {
        console.error('Failed to load career intelligence');
      }
    } catch (error) {
      console.error('Error loading career intelligence:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Analyzing your career data...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50 p-6">
        <div className="text-center max-w-2xl">
          <Brain className="h-24 w-24 text-gray-400 mx-auto mb-6" />
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Build Your Career Profile</h2>
          <p className="text-gray-600 mb-8">
            Complete at least 3 mock tests to unlock AI-powered career intelligence and personalized recommendations.
          </p>
          <button
            onClick={() => router.push('/mock-test')}
            className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 font-semibold"
          >
            Take Mock Test
          </button>
        </div>
      </div>
    );
  }

  const { career_dna, skill_graph, forecast, weekly_strategy, insights } = data;

  const getDNAColor = (value: number) => {
    if (value >= 80) return 'text-green-600';
    if (value >= 60) return 'text-blue-600';
    if (value >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getDNALabel = (value: number) => {
    if (value >= 80) return 'Excellent';
    if (value >= 60) return 'Good';
    if (value >= 40) return 'Average';
    return 'Needs Improvement';
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
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
            Career Intelligence Dashboard
          </h1>
          <p className="text-gray-600 text-lg">AI-Powered Career Insights & Personalized Strategy</p>
        </motion.div>

        {/* Career DNA Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-2xl shadow-xl p-8 mb-8"
        >
          <div className="flex items-center gap-3 mb-6">
            <Brain className="h-8 w-8 text-purple-600" />
            <h2 className="text-3xl font-bold text-gray-900">Your Career DNA</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {[
              { label: 'Logical Ability', value: career_dna.logical_ability, icon: Brain },
              { label: 'Problem Solving', value: career_dna.problem_solving, icon: Target },
              { label: 'Speed', value: career_dna.speed, icon: Zap },
              { label: 'Consistency', value: career_dna.consistency, icon: Activity },
              { label: 'Learning Efficiency', value: career_dna.learning_efficiency, icon: TrendingUp }
            ].map((dimension, idx) => (
              <div key={idx} className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl p-6">
                <div className="flex items-center justify-between mb-3">
                  <dimension.icon className="h-6 w-6 text-blue-600" />
                  <span className={`font-bold text-2xl ${getDNAColor(dimension.value)}`}>
                    {dimension.value}%
                  </span>
                </div>
                <h3 className="font-semibold text-gray-800 mb-2">{dimension.label}</h3>
                <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all ${
                      dimension.value >= 80 ? 'bg-green-500' :
                      dimension.value >= 60 ? 'bg-blue-500' :
                      dimension.value >= 40 ? 'bg-yellow-500' :
                      'bg-red-500'
                    }`}
                    style={{ width: `${dimension.value}%` }}
                  ></div>
                </div>
                <p className="text-sm text-gray-600 mt-2">{getDNALabel(dimension.value)}</p>
              </div>
            ))}
          </div>

          <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl p-8 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-purple-100 mb-2">Overall Career Readiness Score</p>
                <h3 className="text-5xl font-bold">{career_dna.overall_score}%</h3>
              </div>
              <Award className="h-24 w-24 text-white opacity-20" />
            </div>
          </div>
        </motion.div>

        {/* Skill Graph Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-2xl shadow-xl p-8 mb-8"
        >
          <div className="flex items-center gap-3 mb-6">
            <BarChart3 className="h-8 w-8 text-blue-600" />
            <h2 className="text-3xl font-bold text-gray-900">Skill Mastery Map</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {skill_graph.map((skill, idx) => (
              <div key={idx} className="border-2 border-gray-200 rounded-lg p-4 hover:border-blue-400 transition-all">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-semibold text-gray-800">{skill.skill_name}</h4>
                  <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                    {skill.category}
                  </span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="flex-1">
                    <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"
                        style={{ width: `${skill.mastery_level}%` }}
                      ></div>
                    </div>
                  </div>
                  <span className="font-bold text-blue-600">{skill.mastery_level}%</span>
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Career Forecast Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-2xl shadow-xl p-8 mb-8"
        >
          <div className="flex items-center gap-3 mb-6">
            <Rocket className="h-8 w-8 text-green-600" />
            <h2 className="text-3xl font-bold text-gray-900">Career Forecast</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-6">
              <h3 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
                <Briefcase className="h-5 w-5 text-green-600" />
                Internship Readiness
              </h3>
              <div className="relative">
                <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-green-400 to-green-600 rounded-full"
                    style={{ width: `${forecast.internship_readiness}%` }}
                  ></div>
                </div>
                <span className="absolute right-0 top-5 font-bold text-green-700 text-xl">
                  {forecast.internship_readiness}%
                </span>
              </div>
              <p className="text-sm text-gray-600 mt-3">
                {forecast.internship_readiness >= 70 ? 'You are ready to apply!' :
                 forecast.internship_readiness >= 50 ? 'Keep practicing!' :
                 'Focus on building fundamentals'}
              </p>
            </div>

            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6">
              <h3 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
                <Target className="h-5 w-5 text-blue-600" />
                Placement Readiness
              </h3>
              <div className="relative">
                <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-blue-400 to-blue-600 rounded-full"
                    style={{ width: `${forecast.placement_readiness}%` }}
                  ></div>
                </div>
                <span className="absolute right-0 top-5 font-bold text-blue-700 text-xl">
                  {forecast.placement_readiness}%
                </span>
              </div>
              <p className="text-sm text-gray-600 mt-3">
                {forecast.placement_readiness >= 80 ? 'Placement ready!' :
                 forecast.placement_readiness >= 60 ? 'Almost there!' :
                 'More practice needed'}
              </p>
            </div>
          </div>

          <div className="bg-purple-50 rounded-xl p-6">
            <h3 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <Star className="h-5 w-5 text-purple-600" />
              Best-Fit Roles for You
            </h3>
            <div className="flex flex-wrap gap-3">
              {forecast.recommended_roles.map((role, idx) => (
                <span
                  key={idx}
                  className="px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-semibold"
                >
                  {role}
                </span>
              ))}
            </div>
            <p className="text-sm text-gray-600 mt-4 flex items-center gap-2">
              <Calendar className="h-4 w-4" />
              Estimated Timeline: <span className="font-semibold">{forecast.estimated_timeline}</span>
            </p>
          </div>
        </motion.div>

        {/* Weekly Strategy Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-2xl shadow-xl p-8 mb-8"
        >
          <div className="flex items-center gap-3 mb-6">
            <Zap className="h-8 w-8 text-yellow-600" />
            <h2 className="text-3xl font-bold text-gray-900">Your Weekly Learning Strategy</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-yellow-50 rounded-xl p-6">
              <h3 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
                <Target className="h-5 w-5 text-yellow-600" />
                Focus Topics
              </h3>
              <ul className="space-y-2">
                {weekly_strategy.focus_topics.map((topic, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <CheckCircle className="h-4 w-4 text-yellow-600 mt-1 flex-shrink-0" />
                    <span className="text-gray-700">{topic}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-blue-50 rounded-xl p-6">
              <h3 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
                <Clock className="h-5 w-5 text-blue-600" />
                Practice Hours
              </h3>
              <div className="text-center">
                <p className="text-6xl font-bold text-blue-600 mb-2">
                  {weekly_strategy.practice_hours}
                </p>
                <p className="text-gray-600">hours per week recommended</p>
              </div>
            </div>

            <div className="bg-red-50 rounded-xl p-6">
              <h3 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
                <AlertCircle className="h-5 w-5 text-red-600" />
                Improvement Areas
              </h3>
              <ul className="space-y-2">
                {weekly_strategy.improvement_areas.map((area, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <AlertCircle className="h-4 w-4 text-red-600 mt-1 flex-shrink-0" />
                    <span className="text-gray-700">{area}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </motion.div>

        {/* AI Insights Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl shadow-xl p-8 text-white"
        >
          <div className="flex items-center gap-3 mb-6">
            <Brain className="h-8 w-8" />
            <h2 className="text-3xl font-bold">AI Coach Insights</h2>
          </div>

          <div className="space-y-4">
            {insights.map((insight, idx) => (
              <div key={idx} className="bg-white bg-opacity-10 rounded-lg p-4 backdrop-blur">
                <p className="text-white">{insight}</p>
              </div>
            ))}
          </div>

          <div className="mt-6 pt-6 border-t border-white border-opacity-20">
            <p className="text-blue-100 text-sm">
              These insights are generated by AI based on your mock test performance, learning patterns, and skill development.
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
