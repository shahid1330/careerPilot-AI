'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Alert } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { aiService, TeachTopicResponse } from '@/lib/ai-service';
import { BookOpen, Loader2, Sparkles, Lightbulb, Link as LinkIcon, Target } from 'lucide-react';

export default function LearnPage() {
  const [topicName, setTopicName] = useState('');
  const [context, setContext] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [teaching, setTeaching] = useState<TeachTopicResponse | null>(null);

  const handleLearn = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const result = await aiService.teachTopic({
        topic: topicName,
        context: context || undefined,
      });
      setTeaching(result);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get topic explanation. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-20 lg:pb-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="flex items-center gap-3 mb-6">
          <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-emerald-600 to-teal-600 flex items-center justify-center">
            <BookOpen className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Interactive Learning</h1>
            <p className="text-slate-600">Get AI-powered explanations for any topic</p>
          </div>
        </div>

        {/* Input Form */}
        <Card className="p-8 mb-6">
          <form onSubmit={handleLearn} className="space-y-6">
            {error && (
              <Alert variant="destructive">
                <p>{error}</p>
              </Alert>
            )}

            <div className="space-y-2">
              <Label htmlFor="topic">Topic Name</Label>
              <Input
                id="topic"
                type="text"
                placeholder="e.g., React Hooks, Database Indexing, Machine Learning"
                value={topicName}
                onChange={(e) => setTopicName(e.target.value)}
                required
                className="h-12"
                disabled={loading}
              />
              <p className="text-sm text-slate-500">What topic do you want to learn about?</p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="context">Additional Context (Optional)</Label>
              <Textarea
                id="context"
                placeholder="Add any specific context or questions about this topic..."
                value={context}
                onChange={(e) => setContext(e.target.value)}
                className="min-h-24"
                disabled={loading}
              />
            </div>

            <Button
              type="submit"
              className="w-full h-12 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-lg"
              disabled={loading}
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Learning...
                </>
              ) : (
                <>
                  <Sparkles className="mr-2 h-5 w-5" />
                  Learn This Topic
                </>
              )}
            </Button>
          </form>
        </Card>

        {/* Teaching Content */}
        {teaching && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className="space-y-6"
          >
            {/* Explanation */}
            <Card className="p-8 border-2 border-emerald-200 bg-gradient-to-br from-white to-emerald-50">
              <div className="flex items-center gap-3 mb-4">
                <div className="h-10 w-10 rounded-full bg-emerald-100 flex items-center justify-center">
                  <BookOpen className="h-5 w-5 text-emerald-600" />
                </div>
                <div className="flex-1">
                  <h2 className="text-2xl font-bold text-slate-900">{teaching.topic}</h2>
                  <p className="text-sm text-slate-600">Detailed Explanation</p>
                </div>
              </div>
              <div className="prose max-w-none">
                <p className="text-slate-700 leading-relaxed whitespace-pre-wrap">
                  {teaching.explanation}
                </p>
              </div>
            </Card>

            {/* Examples */}
            {teaching.examples && teaching.examples.length > 0 && (
              <Card className="p-8">
                <div className="flex items-center gap-3 mb-4">
                  <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                    <Lightbulb className="h-5 w-5 text-blue-600" />
                  </div>
                  <h2 className="text-2xl font-bold text-slate-900">Examples</h2>
                </div>
                <div className="space-y-3">
                  {teaching.examples.map((example, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.1 }}
                      className="flex items-start gap-3 p-4 bg-blue-50 rounded-lg border border-blue-200"
                    >
                      <Badge className="mt-1 bg-blue-600">{index + 1}</Badge>
                      <p className="text-slate-700 flex-1 font-mono text-sm">{example}</p>
                    </motion.div>
                  ))}
                </div>
              </Card>
            )}

            {/* Resources */}
            <Card className="p-8">
              <div className="flex items-center gap-3 mb-4">
                <div className="h-10 w-10 rounded-full bg-purple-100 flex items-center justify-center">
                  <LinkIcon className="h-5 w-5 text-purple-600" />
                </div>
                <h2 className="text-2xl font-bold text-slate-900">Recommended Resources</h2>
              </div>
              <div className="space-y-2">
                {teaching.resources.map((resource, index) => {
                  // Extract URL from resource string (format: "Platform: URL" or just text)
                  const urlMatch = resource.match(/(https?:\/\/[^\s]+)/);
                  const url = urlMatch ? urlMatch[0] : null;
                  
                  return (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.1 }}
                      className="flex items-start gap-3 p-3 rounded-lg hover:bg-purple-50 transition-colors"
                    >
                      <LinkIcon className="h-4 w-4 text-purple-600 mt-1 flex-shrink-0" />
                      {url ? (
                        <a 
                          href={url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-purple-600 hover:text-purple-800 hover:underline flex-1"
                        >
                          {resource}
                        </a>
                      ) : (
                        <p className="text-slate-700 flex-1">{resource}</p>
                      )}
                    </motion.div>
                  );
                })}
              </div>
            </Card>
          </motion.div>
        )}

        {/* Info Card */}
        {!teaching && (
          <Card className="p-6 bg-emerald-50 border-emerald-200">
            <h3 className="font-semibold text-slate-900 mb-2">How it works</h3>
            <ul className="space-y-2 text-sm text-slate-600">
              <li className="flex items-start gap-2">
                <Sparkles className="h-5 w-5 text-emerald-600 flex-shrink-0 mt-0.5" />
                <span>Enter any topic you want to learn and get a comprehensive AI-generated explanation</span>
              </li>
              <li className="flex items-start gap-2">
                <Lightbulb className="h-5 w-5 text-emerald-600 flex-shrink-0 mt-0.5" />
                <span>Receive key points highlighting the most important concepts</span>
              </li>
              <li className="flex items-start gap-2">
                <LinkIcon className="h-5 w-5 text-emerald-600 flex-shrink-0 mt-0.5" />
                <span>Get curated resources and practice suggestions to master the topic</span>
              </li>
            </ul>
          </Card>
        )}
      </motion.div>
    </div>
  );
}
