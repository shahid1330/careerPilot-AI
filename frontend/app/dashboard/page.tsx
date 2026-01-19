'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { useAuth } from '@/context/AuthContext';
import { aiService, GenerateDailyPlanResponse } from '@/lib/ai-service';
import { 
  Target, Calendar, BookOpen, TrendingUp, ArrowRight, Sparkles, 
  CheckCircle2, Clock, Flame, Award, Activity, Zap 
} from 'lucide-react';
import Link from 'next/link';

export default function DashboardPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    totalRoadmaps: 0,
    totalDays: 0,
    completedDays: 0,
    completionPercentage: 0,
    todayTasks: 0,
    streak: 0
  });
  const [recentActivity, setRecentActivity] = useState<GenerateDailyPlanResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const dailyPlans = await aiService.getDailyPlans();
      
      const savedCompleted = localStorage.getItem('completed_daily_plans');
      let completedDays: Record<number, Set<number>> = {};
      
      if (savedCompleted) {
        try {
          const parsed = JSON.parse(savedCompleted);
          Object.keys(parsed).forEach(roleId => {
            completedDays[parseInt(roleId)] = new Set(parsed[roleId]);
          });
        } catch (e) {
          console.error('Failed to parse completed days:', e);
        }
      }

      const totalRoadmaps = dailyPlans.length;
      const totalDays = dailyPlans.reduce((sum, plan) => sum + plan.plans.length, 0);
      
      // Only count completed days for roles that still have daily plans
      const activeRoleIds = new Set(dailyPlans.map(plan => plan.user_role_id!));
      const completedCount = Object.entries(completedDays)
        .filter(([roleId]) => activeRoleIds.has(parseInt(roleId)))
        .reduce((sum, [, set]) => sum + set.size, 0);
      const completionPercentage = totalDays > 0 ? Math.round((completedCount / totalDays) * 100) : 0;

      // Calculate today's tasks (Day 1 from each roadmap not yet completed)
      let todayTasks = 0;
      dailyPlans.forEach(plan => {
        const roleCompleted = completedDays[plan.user_role_id!] || new Set();
        if (!roleCompleted.has(1)) {
          todayTasks++;
        }
      });

      // Calculate streak (consecutive days completed)
      const streak = calculateStreak(completedDays);

      setStats({
        totalRoadmaps,
        totalDays,
        completedDays: completedCount,
        completionPercentage,
        todayTasks,
        streak
      });

      setRecentActivity(dailyPlans.slice(0, 3));
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateStreak = (completedDays: Record<number, Set<number>>): number => {
    // Simple streak calculation - count unique days completed in last 7 days
    const allDays = Object.values(completedDays).reduce((acc, set) => acc + set.size, 0);
    return Math.min(allDays, 7); // Cap at 7 for now
  };

  const quickActions = [
    {
      title: 'Create Roadmap',
      description: 'Generate an AI-powered career roadmap',
      icon: Target,
      href: '/roadmap',
      gradient: 'from-blue-600 to-indigo-600',
    },
    {
      title: 'Daily Plan',
      description: 'View and manage your daily learning plan',
      icon: Calendar,
      href: '/daily-plan',
      gradient: 'from-purple-600 to-pink-600',
    },
    {
      title: 'Learn Topics',
      description: 'Get AI explanations for any topic',
      icon: BookOpen,
      href: '/learn',
      gradient: 'from-emerald-600 to-teal-600',
    },
  ];

  return (
    <div className="space-y-8 pb-20 lg:pb-8">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Card className="p-8 bg-gradient-to-br from-blue-600 to-indigo-600 border-0 text-white">
          <div className="flex items-start justify-between">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Sparkles className="h-5 w-5" />
                <span className="text-sm font-medium text-blue-100">Welcome back</span>
              </div>
              <h1 className="text-4xl font-bold mb-2">
                Hello, {user?.full_name}!
              </h1>
              <p className="text-lg text-blue-100">
                Ready to accelerate your career growth today?
              </p>
            </div>
            <div className="hidden md:block">
              <div className="h-20 w-20 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center">
                <TrendingUp className="h-10 w-10" />
              </div>
            </div>
          </div>
        </Card>
      </motion.div>

      {/* Stats Overview */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
          <Card className="p-6">
            <div className="flex items-center justify-between mb-2">
              <Target className="h-8 w-8 text-blue-600" />
              <Badge className="bg-blue-100 text-blue-700">Active</Badge>
            </div>
            <p className="text-3xl font-bold text-slate-900">{stats.totalRoadmaps}</p>
            <p className="text-sm text-slate-600">Roadmaps</p>
          </Card>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
          <Card className="p-6">
            <div className="flex items-center justify-between mb-2">
              <CheckCircle2 className="h-8 w-8 text-emerald-600" />
              <Badge className="bg-emerald-100 text-emerald-700">{stats.completionPercentage}%</Badge>
            </div>
            <p className="text-3xl font-bold text-slate-900">{stats.completedDays}</p>
            <p className="text-sm text-slate-600">Days Completed</p>
          </Card>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
          <Card className="p-6">
            <div className="flex items-center justify-between mb-2">
              <Flame className="h-8 w-8 text-orange-600" />
              <Badge className="bg-orange-100 text-orange-700">Streak</Badge>
            </div>
            <p className="text-3xl font-bold text-slate-900">{stats.streak}</p>
            <p className="text-sm text-slate-600">Day Streak</p>
          </Card>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}>
          <Card className="p-6">
            <div className="flex items-center justify-between mb-2">
              <Clock className="h-8 w-8 text-purple-600" />
              <Badge className="bg-purple-100 text-purple-700">Today</Badge>
            </div>
            <p className="text-3xl font-bold text-slate-900">{stats.todayTasks}</p>
            <p className="text-sm text-slate-600">Tasks Pending</p>
          </Card>
        </motion.div>
      </div>

      {/* Progress Overview */}
      {stats.totalDays > 0 && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 }}>
          <Card className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <Activity className="h-6 w-6 text-blue-600" />
                <h3 className="text-xl font-bold text-slate-900">Overall Progress</h3>
              </div>
              <Badge className="text-lg px-3 py-1 bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
                {stats.completionPercentage}%
              </Badge>
            </div>
            <Progress value={stats.completionPercentage} className="h-3 mb-2" />
            <p className="text-sm text-slate-600">
              {stats.completedDays} of {stats.totalDays} days completed across all roadmaps
            </p>
          </Card>
        </motion.div>
      )}

      {/* Quick Actions */}
      <div>
        <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-2">
          <Zap className="h-6 w-6 text-yellow-500" />
          Quick Actions
        </h2>
        <div className="grid md:grid-cols-3 gap-6">
          {quickActions.map((action, index) => {
            const Icon = action.icon;
            return (
              <motion.div
                key={action.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                whileHover={{ y: -5 }}
              >
                <Link href={action.href}>
                  <Card className="p-6 h-full hover:shadow-xl transition-all border-2 border-transparent hover:border-blue-200 cursor-pointer">
                    <div className={`h-14 w-14 rounded-2xl bg-gradient-to-br ${action.gradient} flex items-center justify-center text-white mb-4`}>
                      <Icon className="h-7 w-7" />
                    </div>
                    <h3 className="text-xl font-bold text-slate-900 mb-2">{action.title}</h3>
                    <p className="text-slate-600 mb-4">{action.description}</p>
                    <div className="flex items-center text-blue-600 font-medium">
                      Get Started
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </div>
                  </Card>
                </Link>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Recent Activity */}
      {recentActivity.length > 0 ? (
        <div>
          <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-2">
            <Activity className="h-6 w-6 text-blue-600" />
            Recent Roadmaps
          </h2>
          <div className="space-y-4">
            {recentActivity.map((plan, index) => (
              <motion.div
                key={plan.user_role_id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="p-6 hover:shadow-lg transition-shadow">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="h-12 w-12 rounded-full bg-gradient-to-br from-purple-600 to-pink-600 flex items-center justify-center text-white font-bold">
                        {plan.role_name?.charAt(0).toUpperCase()}
                      </div>
                      <div>
                        <h3 className="text-lg font-bold text-slate-900">{plan.role_name}</h3>
                        <p className="text-sm text-slate-600">{plan.total_days} days • {plan.plans.length} tasks</p>
                      </div>
                    </div>
                    <Link href="/daily-plan">
                      <Button variant="outline" size="sm">
                        View Plan
                        <ArrowRight className="ml-2 h-4 w-4" />
                      </Button>
                    </Link>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      ) : (
        <div>
          <h2 className="text-2xl font-bold text-slate-900 mb-6">Getting Started</h2>
          <Card className="p-8">
            <div className="space-y-4">
              <div className="flex items-start gap-4">
                <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                  <span className="text-blue-600 font-bold">1</span>
                </div>
                <div>
                  <h4 className="font-semibold text-slate-900 mb-1">Create Your Career Roadmap</h4>
                  <p className="text-slate-600 text-sm mb-2">
                    Tell us your target role and timeline, and our AI will generate a personalized learning path.
                  </p>
                  <Link href="/roadmap">
                    <Button size="sm" variant="outline">
                      Create Roadmap
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </Link>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <div className="h-10 w-10 rounded-full bg-purple-100 flex items-center justify-center flex-shrink-0">
                  <span className="text-purple-600 font-bold">2</span>
                </div>
                <div>
                  <h4 className="font-semibold text-slate-900 mb-1">Generate Daily Learning Plans</h4>
                  <p className="text-slate-600 text-sm mb-2">
                    Break down your roadmap into daily actionable tasks with AI-generated plans.
                  </p>
                  <Link href="/daily-plan">
                    <Button size="sm" variant="outline">
                      View Daily Plans
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </Link>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <div className="h-10 w-10 rounded-full bg-emerald-100 flex items-center justify-center flex-shrink-0">
                  <span className="text-emerald-600 font-bold">3</span>
                </div>
                <div>
                  <h4 className="font-semibold text-slate-900 mb-1">Learn Any Topic</h4>
                  <p className="text-slate-600 text-sm mb-2">
                    Get AI-powered explanations, key points, and resources for any topic you want to master.
                  </p>
                  <Link href="/learn">
                    <Button size="sm" variant="outline">
                      Start Learning
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </Link>
                </div>
              </div>
            </div>
          </Card>
        </div>
      )}

      {/* Motivational Section */}
      {stats.totalRoadmaps > 0 && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.7 }}>
          <Card className="p-8 bg-gradient-to-br from-emerald-600 to-teal-600 border-0 text-white">
            <div className="flex items-center gap-4 mb-4">
              <Award className="h-12 w-12" />
              <div>
                <h3 className="text-2xl font-bold">Keep Going!</h3>
                <p className="text-emerald-100">Consistency is the key to success</p>
              </div>
            </div>
            <p className="text-emerald-50 mb-4">
              You're making great progress on your learning journey. Complete today's tasks to maintain your streak!
            </p>
            <Link href="/daily-plan">
              <Button variant="secondary" className="bg-white text-emerald-600 hover:bg-emerald-50">
                Continue Learning
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </Card>
        </motion.div>
      )}
    </div>
  );
}
