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
