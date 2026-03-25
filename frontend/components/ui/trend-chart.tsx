'use client';

import { useMemo } from 'react';

interface TrendChartProps {
  data: Array<{ date: string; score: number; test_name?: string }>;
  height?: number;
}

export function TrendChart({ data, height = 200 }: TrendChartProps) {
  const chartData = useMemo(() => {
    if (!data || data.length === 0) return null;

    const scores = data.map(d => d.score);
    const maxScore = Math.max(...scores, 100);
    const minScore = Math.min(...scores, 0);
    const range = maxScore - minScore || 100;

    const points = data.map((d, i) => {
      const x = (i / (data.length - 1 || 1)) * 100;
      const y = ((maxScore - d.score) / range) * 80 + 10; // 10% padding top/bottom
      return { x, y, ...d };
    });

    const pathD = points
      .map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`)
      .join(' ');

    return { points, pathD, maxScore, minScore };
  }, [data]);

  if (!chartData || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-48 text-gray-400">
        No test data available yet
      </div>
    );
  }

  const { points, pathD, maxScore, minScore } = chartData;

  return (
    <div className="relative" style={{ height }}>
      <svg
        viewBox="0 0 100 100"
        className="w-full h-full"
        preserveAspectRatio="none"
      >
        {/* Grid lines */}
        <line x1="0" y1="25" x2="100" y2="25" stroke="#e5e7eb" strokeWidth="0.2" />
        <line x1="0" y1="50" x2="100" y2="50" stroke="#e5e7eb" strokeWidth="0.2" />
        <line x1="0" y1="75" x2="100" y2="75" stroke="#e5e7eb" strokeWidth="0.2" />

        {/* Gradient fill */}
        <defs>
          <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.3" />
            <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.05" />
          </linearGradient>
        </defs>

        {/* Area under curve */}
        <path
          d={`${pathD} L 100 90 L 0 90 Z`}
          fill="url(#scoreGradient)"
        />

        {/* Line */}
        <path
          d={pathD}
          fill="none"
          stroke="#3b82f6"
          strokeWidth="1"
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* Data points */}
        {points.map((point, i) => (
          <g key={i}>
            <circle
              cx={point.x}
              cy={point.y}
              r="1.5"
              fill="#3b82f6"
              className="hover:r-2 transition-all cursor-pointer"
            />
          </g>
        ))}
      </svg>

      {/* X-axis labels */}
      <div className="flex justify-between mt-2 text-xs text-gray-500">
        {data.length > 0 && (
          <>
            <span>{new Date(data[0].date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</span>
            {data.length > 1 && (
              <span>{new Date(data[data.length - 1].date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</span>
            )}
          </>
        )}
      </div>

      {/* Y-axis labels */}
      <div className="absolute left-0 top-0 bottom-8 flex flex-col justify-between text-xs text-gray-500 -ml-8">
        <span>{Math.round(maxScore)}%</span>
        <span>{Math.round((maxScore + minScore) / 2)}%</span>
        <span>{Math.round(minScore)}%</span>
      </div>
    </div>
  );
}
