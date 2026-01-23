'use client';

import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { aiService, GenerateDailyPlanResponse } from '@/lib/ai-service';
import { Calendar, Loader2, Sparkles, Target, Trash2, ChevronDown } from 'lucide-react';
import { cleanupCompletionData } from '@/lib/completionUtils';

export default function DailyPlanPage() {
  const [userRoleId, setUserRoleId] = useState('');
  const [roleName, setRoleName] = useState('');
  const [durationDays, setDurationDays] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingPlans, setLoadingPlans] = useState(true);
  const [error, setError] = useState('');
  const [allDailyPlans, setAllDailyPlans] = useState<GenerateDailyPlanResponse[]>([]);
  const [completedDays, setCompletedDays] = useState<Record<number, Set<number>>>({});
  const [showGenerateForm, setShowGenerateForm] = useState(false);
  const [expandedRoles, setExpandedRoles] = useState<Set<number>>(new Set());
  const [deletingRoleId, setDeletingRoleId] = useState<number | null>(null);

  useEffect(() => {
    const storedRoleId = sessionStorage.getItem('user_role_id');
    const storedRoleName = sessionStorage.getItem('role_name');
    const storedDuration = sessionStorage.getItem('duration_days');
    
    if (storedRoleId) {
      setUserRoleId(storedRoleId);
      setShowGenerateForm(true);
    }
    if (storedRoleName) setRoleName(storedRoleName);
    if (storedDuration) setDurationDays(storedDuration);

    loadPlans();
  }, []);

  const loadPlans = async () => {
    setLoadingPlans(true);
    try {
      const plans = await aiService.getDailyPlans();
      setAllDailyPlans(plans);
      
      // Clean up orphaned completion data
      cleanupCompletionData(plans);
      const roleIds = new Set(plans.map(p => p.user_role_id!));
      setExpandedRoles(roleIds);      
      // Load completed days AFTER plans are loaded
      loadCompletedDaysForPlans(plans);    } catch (err) {
      console.error('Failed to load plans:', err);
    } finally {
      setLoadingPlans(false);
    }
  };

  const loadCompletedDaysForPlans = (plans: any[]) => {
    const saved = localStorage.getItem('completed_daily_plans');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        const completed: Record<number, Set<number>> = {};
        
        // Only load completion data for roles that have daily plans
        const activeRoleIds = new Set(plans.map((plan: any) => plan.user_role_id!));
        Object.keys(parsed).forEach(roleId => {
          const roleIdNum = parseInt(roleId);
          if (activeRoleIds.has(roleIdNum)) {
            completed[roleIdNum] = new Set(parsed[roleId]);
          }
        });
        setCompletedDays(completed);
      } catch (e) {
        console.error('Failed to load completed days:', e);
      }
    }
  };

  const saveCompletedDays = (completed: Record<number, Set<number>>) => {
    // Only save completion data for roles that still have daily plans
    const activeRoleIds = new Set(allDailyPlans.map(plan => plan.user_role_id!));
    const toSave: any = {};
    Object.keys(completed).forEach(roleId => {
      const roleIdNum = parseInt(roleId);
      if (activeRoleIds.has(roleIdNum)) {
        toSave[roleId] = Array.from(completed[roleIdNum]);
      }
    });
    localStorage.setItem('completed_daily_plans', JSON.stringify(toSave));
  };

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await aiService.generateDailyPlan({ user_role_id: parseInt(userRoleId) });
      await loadPlans();
      setUserRoleId('');
      setRoleName('');
      setDurationDays('');
      setShowGenerateForm(false);
      sessionStorage.clear();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate daily plan.');
    } finally {
      setLoading(false);
    }
  };

  const toggleDay = (roleId: number, dayNumber: number) => {
    setCompletedDays(prev => {
      const newCompleted = { ...prev };
      if (!newCompleted[roleId]) {
        newCompleted[roleId] = new Set();
      }
      
      const roleSet = new Set(newCompleted[roleId]);
      if (roleSet.has(dayNumber)) {
        roleSet.delete(dayNumber);
      } else {
        roleSet.add(dayNumber);
      }
      newCompleted[roleId] = roleSet;
      
      saveCompletedDays(newCompleted);
      return newCompleted;
    });
  };

  const handleDelete = async (userRoleId: number, roleName: string) => {
    if (!confirm(`Delete daily plan for "${roleName}"? This cannot be undone.`)) return;

    setDeletingRoleId(userRoleId);
    try {
      await aiService.deleteDailyPlan(userRoleId);
      await loadPlans();
      
      // Clear completion data for this role
      setCompletedDays(prev => {
        const newCompleted = { ...prev };
        delete newCompleted[userRoleId];
        saveCompletedDays(newCompleted);
        return newCompleted;
      });
      
      // Remove associated roadmap from localStorage
      const savedRoadmaps = localStorage.getItem('user_roadmaps');
      if (savedRoadmaps) {
        try {
          const roadmaps = JSON.parse(savedRoadmaps);
          const updatedRoadmaps = roadmaps.filter((rm: any) => rm.user_role_id !== userRoleId);
          localStorage.setItem('user_roadmaps', JSON.stringify(updatedRoadmaps));
        } catch (e) {
          console.error('Failed to remove roadmap from storage:', e);
        }
      }
    } catch (err: any) {
      alert(`Failed to delete: ${err.message}`);
    } finally {
      setDeletingRoleId(null);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-20 lg:pb-8">
      <div className="flex items-center gap-3">
        <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-purple-600 to-pink-600 flex items-center justify-center">
          <Calendar className="h-6 w-6 text-white" />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Daily Learning Plan</h1>
          <p className="text-slate-600">Click any day to mark complete/incomplete</p>
        </div>
      </div>

      {showGenerateForm && userRoleId && (
        <Card className="p-6">
          <form onSubmit={handleGenerate} className="space-y-4">
            {error && <Alert variant="destructive"><p>{error}</p></Alert>}
            <div className="p-3 bg-purple-50 rounded-lg border border-purple-200">
              <p className="text-sm"><strong>Role:</strong> {roleName} • <strong>Duration:</strong> {durationDays} days</p>
            </div>
            <Button type="submit" className="w-full bg-purple-600 hover:bg-purple-700" disabled={loading}>
              {loading ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" />Generating...</> : <><Sparkles className="mr-2 h-4 w-4" />Generate Daily Plan</>}
            </Button>
          </form>
        </Card>
      )}

      {loadingPlans && <Card className="p-8 text-center"><Loader2 className="h-8 w-8 animate-spin mx-auto text-purple-600" /><p className="mt-2 text-slate-600">Loading...</p></Card>}

      {!loadingPlans && allDailyPlans.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-2xl font-bold">Your Learning Journeys</h2>
          {allDailyPlans.map((planGroup) => {
            const roleCompleted = completedDays[planGroup.user_role_id!] || new Set();
            const progress = (roleCompleted.size / planGroup.plans.length) * 100;
            const isExpanded = expandedRoles.has(planGroup.user_role_id!);

            return (
              <Card key={planGroup.user_role_id}>
                <div className="p-4 cursor-pointer hover:bg-slate-50" onClick={() => setExpandedRoles(prev => {
                  const newSet = new Set(prev);
                  isExpanded ? newSet.delete(planGroup.user_role_id!) : newSet.add(planGroup.user_role_id!);
                  return newSet;
                })}>
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <ChevronDown className={`h-5 w-5 transition-transform ${isExpanded ? '' : '-rotate-90'}`} />
                      <Target className="h-5 w-5 text-purple-600" />
                      <div>
                        <h3 className="font-bold">{planGroup.role_name}</h3>
                        <p className="text-sm text-slate-600">{planGroup.total_days} days</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge>{roleCompleted.size}/{planGroup.plans.length}</Badge>
                      <Button variant="destructive" size="sm" onClick={(e) => { e.stopPropagation(); handleDelete(planGroup.user_role_id!, planGroup.role_name!); }} disabled={deletingRoleId === planGroup.user_role_id}>
                        {deletingRoleId === planGroup.user_role_id ? <Loader2 className="h-4 w-4 animate-spin" /> : <Trash2 className="h-4 w-4" />}
                      </Button>
                    </div>
                  </div>
                  <Progress value={progress} className="h-2" />
                  <p className="text-xs text-slate-600 mt-1">{Math.round(progress)}% complete</p>
                </div>

                {isExpanded && (
                  <div className="border-t p-3 bg-slate-50 space-y-2">
                    {planGroup.plans.map((plan) => {
                      const isCompleted = roleCompleted.has(plan.day_number);
                      return (
                        <div
                          key={plan.day_number}
                          onClick={() => toggleDay(planGroup.user_role_id!, plan.day_number)}
                          className={`p-3 rounded-lg border-2 cursor-pointer transition ${isCompleted ? 'bg-green-50 border-green-400' : 'bg-white border-slate-200 hover:border-purple-400'}`}
                        >
                          <div className="flex items-start gap-3">
                            <div className={`h-5 w-5 rounded border-2 flex items-center justify-center shrink-0 ${isCompleted ? 'bg-green-600 border-green-600' : 'bg-white border-slate-400'}`}>
                              {isCompleted && <svg className="w-3 h-3 text-white" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" viewBox="0 0 24 24" stroke="currentColor"><path d="M5 13l4 4L19 7"></path></svg>}
                            </div>
                            <div className="flex-1">
                              <div className="flex items-center justify-between mb-1">
                                <h4 className="font-bold">Day {plan.day_number}</h4>
                                <div className="flex items-center gap-2">
                                  <Badge className="bg-purple-600 text-xs">{plan.estimated_hours}h</Badge>
                                  {isCompleted && <span className="text-green-600 text-sm">✓ Done</span>}
                                </div>
                              </div>
                              <p className="text-sm text-slate-700">{plan.topic}</p>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </Card>
            );
          })}
        </div>
      )}

      {!loadingPlans && allDailyPlans.length === 0 && (
        <Card className="p-12 text-center bg-slate-50">
          <Calendar className="h-16 w-16 text-slate-400 mx-auto mb-4" />
          <h3 className="text-xl font-bold mb-2">No Daily Plans Yet</h3>
          <p className="text-slate-600">Generate a roadmap first, then create your daily plan.</p>
        </Card>
      )}
    </div>
  );
}