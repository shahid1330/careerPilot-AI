'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Progress } from '@/components/ui/progress';
import { useAuth } from '@/context/AuthContext';
import { aiService, GenerateDailyPlanResponse } from '@/lib/ai-service';
import { User, Mail, Calendar, LogOut, Sparkles, Target, TrendingUp, CheckCircle2 } from 'lucide-react';

export default function ProfilePage() {
  const { user, logout } = useAuth();
  const [stats, setStats] = useState({
    totalRoadmaps: 0,
    totalDays: 0,
    completedDays: 0,
    completionPercentage: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      loadUserStats();
    }
  }, [user]);

  const loadUserStats = async () => {
    try {
      // Load daily plans
      const dailyPlans = await aiService.getDailyPlans();
      
      // Load completed days from localStorage
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

      // Calculate stats
      const totalRoadmaps = dailyPlans.length;
      const totalDays = dailyPlans.reduce((sum, plan) => sum + plan.plans.length, 0);
      
      // Only count completed days for roles that still have daily plans
      const activeRoleIds = new Set(dailyPlans.map(plan => plan.user_role_id!));
      const completedCount = Object.entries(completedDays)
        .filter(([roleId]) => activeRoleIds.has(parseInt(roleId)))
        .reduce((sum, [, set]) => sum + set.size, 0);
      const completionPercentage = totalDays > 0 ? Math.round((completedCount / totalDays) * 100) : 0;

      setStats({
        totalRoadmaps,
        totalDays,
        completedDays: completedCount,
        completionPercentage
      });
    } catch (error) {
      console.error('Failed to load stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!user) return null;

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-20 lg:pb-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="flex items-center gap-3 mb-6">
          <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center">
            <User className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Profile</h1>
            <p className="text-slate-600">Manage your account information</p>
          </div>
        </div>

        {/* Profile Card */}
        <Card className="p-8 mb-6">
          <div className="flex items-start gap-6 mb-8">
            <Avatar className="h-24 w-24">
              <AvatarFallback className="bg-gradient-to-br from-blue-600 to-indigo-600 text-white text-3xl">
                {user.full_name.charAt(0).toUpperCase()}
              </AvatarFallback>
            </Avatar>
            <div className="flex-1">
              <h2 className="text-2xl font-bold text-slate-900 mb-1">{user.full_name}</h2>
              <p className="text-slate-600 mb-3">@{user.username}</p>
              <Badge className="bg-gradient-to-r from-blue-600 to-indigo-600">
                <Sparkles className="h-3 w-3 mr-1" />
                Active User
              </Badge>
            </div>
          </div>

          <Separator className="my-6" />

          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-lg bg-blue-100 flex items-center justify-center">
                <Mail className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <p className="text-sm text-slate-500">Email</p>
                <p className="font-medium text-slate-900">{user.email}</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-lg bg-purple-100 flex items-center justify-center">
                <User className="h-5 w-5 text-purple-600" />
              </div>
              <div>
                <p className="text-sm text-slate-500">Username</p>
                <p className="font-medium text-slate-900">{user.username}</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-lg bg-emerald-100 flex items-center justify-center">
                <Calendar className="h-5 w-5 text-emerald-600" />
              </div>
              <div>
                <p className="text-sm text-slate-500">Member Since</p>
                <p className="font-medium text-slate-900">
                  {new Date(user.created_at).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </p>
              </div>
            </div>
          </div>
        </Card>

        {/* Account Actions */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Account Actions</h3>
          <div className="space-y-3">
            <Button
              variant="outline"
              className="w-full justify-start text-red-600 border-red-200 hover:bg-red-50 hover:text-red-700"
              onClick={logout}
            >
              <LogOut className="mr-2 h-4 w-4" />
              Logout
            </Button>
          </div>
        </Card>

        {/* Stats Card */}
        <Card className="p-8 bg-gradient-to-br from-blue-600 to-indigo-600 border-0 text-white">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-2xl font-bold">Your Learning Journey</h3>
            <TrendingUp className="h-6 w-6" />
          </div>
          
          {loading ? (
            <div className="text-center py-8">
              <p className="text-blue-100">Loading stats...</p>
            </div>
          ) : (
            <>
              <div className="grid grid-cols-3 gap-6 mb-6">
                <div className="text-center">
                  <div className="flex items-center justify-center mb-2">
                    <Target className="h-5 w-5 mr-2" />
                  </div>
                  <p className="text-4xl font-bold mb-1">{stats.totalRoadmaps}</p>
                  <p className="text-sm text-blue-100">Active Roadmaps</p>
                </div>
                <div className="text-center">
                  <div className="flex items-center justify-center mb-2">
                    <CheckCircle2 className="h-5 w-5 mr-2" />
                  </div>
                  <p className="text-4xl font-bold mb-1">{stats.completedDays}</p>
                  <p className="text-sm text-blue-100">Days Completed</p>
                </div>
                <div className="text-center">
                  <div className="flex items-center justify-center mb-2">
                    <Calendar className="h-5 w-5 mr-2" />
                  </div>
                  <p className="text-4xl font-bold mb-1">{stats.totalDays}</p>
                  <p className="text-sm text-blue-100">Total Days</p>
                </div>
              </div>

              <Separator className="my-6 bg-blue-400 opacity-30" />

              <div>
                <div className="flex items-center justify-between mb-3">
                  <p className="text-sm font-medium">Overall Progress</p>
                  <p className="text-2xl font-bold">{stats.completionPercentage}%</p>
                </div>
                <Progress 
                  value={stats.completionPercentage} 
                  className="h-3 bg-blue-400 bg-opacity-30"
                />
                <p className="text-xs text-blue-100 mt-2">
                  {stats.completedDays} of {stats.totalDays} days completed across all roadmaps
                </p>
              </div>
            </>
          )}
        </Card>
      </motion.div>
    </div>
  );
}
