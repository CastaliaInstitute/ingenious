export interface User {
  id: string;
  email: string;
}

export interface Submission {
  id: string;
  name: string;
  description?: string;
  fileUrl: string;
  fileName: string;
  fileType: string;
  fileSize: number;
  extractedText: string;
  uploadedAt: string;
}

export interface Criterion {
  id: string;
  name: string;
  description: string;
  weight: number;
  maxScore: number;
}

export interface CriteriaSet {
  id: string;
  name: string;
  description?: string;
  criteria: Criterion[];
  createdAt: string;
}

export interface CriterionResult {
  criterionId: string;
  score: number;
  narrative: string;
}

export interface EvaluationResult {
  submissionId: string;
  submissionName: string;
  submissionAuthor?: string;
  overallScore: number;
  criterionResults: CriterionResult[];
  summary: string;
}

export interface Evaluation {
  id: string;
  name: string;
  status: 'draft' | 'running' | 'completed' | 'failed';
  submissionIds: string[];
  criteriaSetId: string;
  criteriaSetName?: string;
  results: EvaluationResult[];
  createdAt: string;
  completedAt?: string;
}

export type TabName = 'evaluations' | 'submissions' | 'criteria';
