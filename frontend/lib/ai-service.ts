import { api } from './api';

export interface GenerateRoadmapRequest {
  role_name: string;
  duration_days: number;
}

export interface GenerateRoadmapResponse {
  id: number;
  user_role_id: number;
  roadmap_text: string;
  generated_at: string;
}

export interface GenerateDailyPlanRequest {
  user_role_id: number;
}

export interface DailyPlanItem {
  id: number;
  user_role_id: number;
  day_number: number;
  topic: string;
  estimated_hours: number;
}

export interface GenerateDailyPlanResponse {
  message: string;
  total_days: number;
  plans: DailyPlanItem[];
  role_name?: string;
  user_role_id?: number;
}

export interface TeachTopicRequest {
  topic: string;
  context?: string;
}

export interface TeachTopicResponse {
  topic: string;
  explanation: string;
  examples: string[];
  resources: string[];
}

export const aiService = {
  async generateRoadmap(data: GenerateRoadmapRequest): Promise<GenerateRoadmapResponse> {
    const response = await api.post<GenerateRoadmapResponse>('/ai/generate-roadmap', data);
    return response.data;
  },

  async generateDailyPlan(data: GenerateDailyPlanRequest): Promise<GenerateDailyPlanResponse> {
    const response = await api.post<GenerateDailyPlanResponse>('/ai/generate-daily-plan', data);
    return response.data;
  },

  async getDailyPlans(): Promise<GenerateDailyPlanResponse[]> {
    const response = await api.get<GenerateDailyPlanResponse[]>('/ai/daily-plans');
    return response.data;
  },

  async deleteDailyPlan(userRoleId: number): Promise<void> {
    await api.delete(`/ai/daily-plans/${userRoleId}`);
  },

  async teachTopic(data: TeachTopicRequest): Promise<TeachTopicResponse> {
    const response = await api.post<TeachTopicResponse>('/ai/teach-topic', data);
    return response.data;
  },
};
