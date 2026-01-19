'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { aiService, GenerateRoadmapResponse } from '@/lib/ai-service';
import { Target, Loader2, Sparkles, CheckCircle2, ArrowRight, BookOpen, Lightbulb, TrendingUp, Plus, List } from 'lucide-react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

interface SavedRoadmap {
  id: number;
  user_role_id: number;
  role_name: string;
  duration_days: string;
  roadmap_text: string;
  generated_at: string;
}

export default function RoadmapPage() {
  const router = useRouter();
  const [roleName, setRoleName] = useState('');
  const [durationDays, setDurationDays] = useState('90');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [roadmap, setRoadmap] = useState<GenerateRoadmapResponse | null>(null);
  const [parsedRoadmap, setParsedRoadmap] = useState<any>(null);
  const [savedRoadmaps, setSavedRoadmaps] = useState<SavedRoadmap[]>([]);
  const [showNewRoadmapForm, setShowNewRoadmapForm] = useState(true);

  useEffect(() => {
    // Load saved roadmaps from localStorage
    const saved = localStorage.getItem('user_roadmaps');
    if (saved) {
      try {
        setSavedRoadmaps(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to parse saved roadmaps:', e);
      }
    }
  }, []);

  const saveRoadmapToStorage = (roadmapData: GenerateRoadmapResponse, role: string, duration: string) => {
    const newRoadmap: SavedRoadmap = {
      id: roadmapData.id,
      user_role_id: roadmapData.user_role_id,
      role_name: role,
      duration_days: duration,
      roadmap_text: roadmapData.roadmap_text,
      generated_at: roadmapData.generated_at,
    };

    const updated = [...savedRoadmaps, newRoadmap];
    setSavedRoadmaps(updated);
    localStorage.setItem('user_roadmaps', JSON.stringify(updated));
  };

  const loadSavedRoadmap = (saved: SavedRoadmap) => {
    setRoadmap({
      id: saved.id,
      user_role_id: saved.user_role_id,
      roadmap_text: saved.roadmap_text,
      generated_at: saved.generated_at,
    });
    setRoleName(saved.role_name);
    setDurationDays(saved.duration_days);
    
    try {
      const parsed = JSON.parse(saved.roadmap_text);
      setParsedRoadmap(parsed);
    } catch (e) {
      setParsedRoadmap(null);
    }
    
    setShowNewRoadmapForm(false);
  };

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    // Check if this role already exists with different duration
    const existingRoleRoadmap = savedRoadmaps.find(
      rm => rm.role_name.toLowerCase() === roleName.toLowerCase()
    );
    
    if (existingRoleRoadmap && existingRoleRoadmap.duration_days !== durationDays) {
      const confirmed = window.confirm(
        `⚠️ WARNING\n\n` +
        `You already have a roadmap for "${existingRoleRoadmap.role_name}" with ${existingRoleRoadmap.duration_days} days.\n\n` +
        `Changing to ${durationDays} days will:\n` +
        `• Create a completely new roadmap\n` +
        `• Delete your current daily plan\n` +
        `• Reset all your progress to 0%\n\n` +
        `Do you want to continue?`
      );
      
      if (!confirmed) {
        return; // User cancelled
      }
      
      // Remove old roadmap from localStorage (backend will handle DB cleanup)
      const updatedRoadmaps = savedRoadmaps.filter(
        rm => rm.role_name.toLowerCase() !== roleName.toLowerCase()
      );
      setSavedRoadmaps(updatedRoadmaps);
      localStorage.setItem('user_roadmaps', JSON.stringify(updatedRoadmaps));
      
      // Clear completion progress for this role
      const savedCompleted = localStorage.getItem('completed_daily_plans');
      if (savedCompleted) {
        try {
          const parsed = JSON.parse(savedCompleted);
          delete parsed[existingRoleRoadmap.user_role_id];
          localStorage.setItem('completed_daily_plans', JSON.stringify(parsed));
        } catch (e) {
          console.error('Failed to clear completion data:', e);
        }
      }
    }
    
    setLoading(true);

    try {
      const result = await aiService.generateRoadmap({
        role_name: roleName,
        duration_days: parseInt(durationDays),
      });
      setRoadmap(result);
      
      // Save to localStorage for multi-role support
      saveRoadmapToStorage(result, roleName, durationDays);
      
      // Parse the JSON roadmap text
      try {
        const parsed = JSON.parse(result.roadmap_text);
        setParsedRoadmap(parsed);
      } catch (parseError) {
        console.error('Failed to parse roadmap JSON:', parseError);
        setParsedRoadmap(null);
      }
      
      setShowNewRoadmapForm(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate roadmap. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateDailyPlan = () => {
    if (roadmap) {
      // Store roadmap data in sessionStorage for daily plan page
      sessionStorage.setItem('user_role_id', roadmap.user_role_id.toString());
      sessionStorage.setItem('roadmap_text', roadmap.roadmap_text);
      sessionStorage.setItem('role_name', roleName);
      sessionStorage.setItem('duration_days', durationDays);
      sessionStorage.setItem('roadmap_updated', Date.now().toString()); // Force reload trigger
      router.push('/daily-plan');
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-20 lg:pb-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center">
              <Target className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-slate-900">Career Roadmap</h1>
              <p className="text-slate-600">Manage multiple learning paths for different roles</p>
            </div>
          </div>
          {!showNewRoadmapForm && savedRoadmaps.length > 0 && (
            <Button
              onClick={() => {
                setShowNewRoadmapForm(true);
                setRoadmap(null);
                setParsedRoadmap(null);
                setRoleName('');
                setDurationDays('90');
              }}
              variant="outline"
              className="gap-2"
            >
              <Plus className="h-4 w-4" />
              New Roadmap
            </Button>
          )}
        </div>

        {/* Saved Roadmaps List */}
        {savedRoadmaps.length > 0 && showNewRoadmapForm && (
          <Card className="p-6 mb-6 bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200">
            <div className="flex items-center gap-2 mb-4">
              <List className="h-5 w-5 text-blue-600" />
              <h3 className="text-lg font-bold text-slate-900">Your Roadmaps</h3>
              <Badge variant="secondary">{savedRoadmaps.length}</Badge>
            </div>
            <div className="space-y-2">
              {savedRoadmaps.map((saved) => (
                <button
                  key={saved.id}
                  onClick={() => loadSavedRoadmap(saved)}
                  className="w-full text-left p-4 bg-white rounded-lg border border-blue-200 hover:border-blue-400 hover:shadow-md transition-all"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-semibold text-slate-900">{saved.role_name}</h4>
                      <p className="text-sm text-slate-600">
                        {saved.duration_days} days • Generated on {new Date(saved.generated_at).toLocaleDateString()}
                      </p>
                    </div>
                    <ArrowRight className="h-5 w-5 text-blue-600" />
                  </div>
                </button>
              ))}
            </div>
          </Card>
        )}

        {/* Input Form */}
        {showNewRoadmapForm && (
          <Card className="p-8 mb-6">
            <form onSubmit={handleGenerate} className="space-y-6">
              {error && (
                <Alert variant="destructive">
                  <p>{error}</p>
                </Alert>
              )}

            <div className="space-y-2">
              <Label htmlFor="role">Target Role</Label>
              <Input
                id="role"
                type="text"
                placeholder="e.g., Full Stack Developer, Data Scientist, DevOps Engineer"
                value={roleName}
                onChange={(e) => setRoleName(e.target.value)}
                required
                className="h-12"
                disabled={loading}
              />
              <p className="text-sm text-slate-500">Enter the role you want to prepare for</p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="duration">Duration (Days)</Label>
              <Input
                id="duration"
                type="number"
                min="1"
                max="365"
                placeholder="90"
                value={durationDays}
                onChange={(e) => setDurationDays(e.target.value)}
                required
                className="h-12"
                disabled={loading}
              />
              <p className="text-sm text-slate-500">How many days do you want to dedicate to this goal?</p>
            </div>

            <Button
              type="submit"
              className="w-full h-12 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-lg"
              disabled={loading}
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Generating your roadmap...
                </>
              ) : (
                <>
                  <Sparkles className="mr-2 h-5 w-5" />
                  Generate Roadmap
                </>
              )}
            </Button>
          </form>
        </Card>
        )}

        {/* Generated Roadmap */}
        {roadmap && !showNewRoadmapForm && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <Card className="p-8 border-2 border-green-200 bg-gradient-to-br from-white to-green-50">
              <div className="flex items-center gap-3 mb-6">
                <div className="h-12 w-12 rounded-full bg-green-100 flex items-center justify-center">
                  <CheckCircle2 className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-slate-900">Your Career Roadmap</h2>
                  <p className="text-slate-600">Generated with AI</p>
                </div>
              </div>

              <div className="bg-white rounded-lg p-6 mb-6 border">
                {parsedRoadmap ? (
                  <div className="space-y-8">
                    {/* Required Skills */}
                    {parsedRoadmap.required_skills && (
                      <div>
                        <div className="flex items-center gap-2 mb-4">
                          <Target className="h-5 w-5 text-blue-600" />
                          <h3 className="text-xl font-bold text-slate-900">Required Skills</h3>
                        </div>
                        <div className="flex flex-wrap gap-2">
                          {parsedRoadmap.required_skills.map((skill: string, i: number) => (
                            <Badge key={i} variant="secondary" className="text-sm">
                              {i + 1}. {skill}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Learning Path */}
                    {parsedRoadmap.learning_path && (
                      <div>
                        <div className="flex items-center gap-2 mb-4">
                          <BookOpen className="h-5 w-5 text-purple-600" />
                          <h3 className="text-xl font-bold text-slate-900">Learning Path</h3>
                        </div>
                        <div className="space-y-4">
                          {parsedRoadmap.learning_path.map((phase: any, index: number) => (
                            <div key={index} className="border-l-4 border-purple-500 pl-4 bg-purple-50 p-4 rounded-r-lg">
                              <div className="flex items-center justify-between mb-2">
                                <h4 className="text-lg font-bold text-slate-900">
                                  {index + 1}. {phase.phase}
                                </h4>
                                {phase.duration_weeks && (
                                  <Badge className="bg-purple-600">
                                    {phase.duration_weeks} weeks
                                  </Badge>
                                )}
                              </div>
                              {phase.topics && (
                                <ul className="space-y-1 mt-3">
                                  {phase.topics.map((topic: string, i: number) => (
                                    <li key={i} className="flex items-start gap-2 text-slate-700">
                                      <CheckCircle2 className="h-4 w-4 text-purple-600 mt-1 flex-shrink-0" />
                                      <span>{topic}</span>
                                    </li>
                                  ))}
                                </ul>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Recommended Projects */}
                    {parsedRoadmap.recommended_projects && (
                      <div>
                        <div className="flex items-center gap-2 mb-4">
                          <Lightbulb className="h-5 w-5 text-orange-600" />
                          <h3 className="text-xl font-bold text-slate-900">Recommended Projects</h3>
                        </div>
                        <div className="grid gap-3">
                          {parsedRoadmap.recommended_projects.map((project: string, i: number) => (
                            <div key={i} className="flex items-start gap-3 p-3 bg-orange-50 rounded-lg border border-orange-200">
                              <div className="h-7 w-7 rounded-full bg-orange-600 text-white flex items-center justify-center flex-shrink-0 font-bold text-sm">
                                {i + 1}
                              </div>
                              <p className="text-slate-700 pt-0.5">{project}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <p className="text-slate-600">Roadmap generated! Processing display...</p>
                    <pre className="mt-4 text-left text-xs bg-slate-50 p-4 rounded overflow-auto max-h-96">
                      {roadmap?.roadmap_text}
                    </pre>
                  </div>
                )}
              </div>

              <div className="flex items-center justify-between pt-4 border-t">
                <p className="text-sm text-slate-500">
                  Generated on {new Date(roadmap.generated_at).toLocaleDateString()}
                </p>
                <Button 
                  onClick={handleGenerateDailyPlan}
                  className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
                >
                  Generate Daily Plan
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </Card>
          </motion.div>
        )}

        {/* Info Card */}
        {!roadmap && (
          <Card className="p-6 bg-blue-50 border-blue-200">
            <h3 className="font-semibold text-slate-900 mb-2">How it works</h3>
            <ul className="space-y-2 text-sm text-slate-600">
              <li className="flex items-start gap-2">
                <CheckCircle2 className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
                <span>Our AI analyzes your target role and creates a comprehensive learning path</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
                <span>Get a structured roadmap with topics, skills, and milestones</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
                <span>Break it down into daily plans for actionable progress</span>
              </li>
            </ul>
          </Card>
        )}
      </motion.div>
    </div>
  );
}
