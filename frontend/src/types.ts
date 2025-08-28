// frontend/src/types.ts
export type Activity = {
  id: number;
  org_id: number;
  scope: "1" | "2" | "3";
  category: string;
  unit: string;
  quantity: number;
  period_start: string; // ISO date
  period_end: string;   // ISO date
  notes?: string;
  data_quality?: string;
  source_id?: number | null;
};

export type CalcLineItem = {
  activity_id: number;
  category: string;
  scope: "1" | "2" | "3";
  unit: string;
  quantity: number;
  factor_value: number;
  factor_unit: string;
  dataset: string;
  region?: string | null;
  year?: number | null;
  version?: string | null;
  co2e_kg: number;
};

export type CalcResult = {
  org_id: number;
  period_start: string;
  period_end: string;
  total_kg: number;
  by_scope: Record<string, number>;
  by_category: Record<string, number>;
  items: CalcLineItem[];
};
