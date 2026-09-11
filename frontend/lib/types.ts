export interface Material {
  id: number;
  seller_id: number;
  material_type: string;
  quantity: number;
  unit: string;
  location: string;
  latitude?: number;
  longitude?: number;
  condition?: string;
  reuse_score?: number;
  risk_level?: string;
  ai_confidence?: number;
  estimated_value?: number;
  carbon_estimate?: number;
  status: string;
  description?: string;
  age?: string;
  dimensions?: string;
  previous_use?: string;
  created_at?: string;
  images?: MaterialImage[];
  assessment?: AssessmentResult;
  passport?: PassportData;
  seller?: { id: number; name: string; company: string; location: string };
}

export interface MaterialImage {
  id: number;
  image_url: string;
}

export interface AssessmentResult {
  condition: string;
  visible_defects: string[];
  reuse_score: number;
  risk_level: string;
  confidence: number;
  recommendation: string;
  verification_required: boolean;
  reasoning: string[];
  safety_disclaimer?: string;
}

export interface PassportData {
  passport_id: string;
  source_building?: string;
  previous_use?: string;
  material_grade?: string;
  ai_condition: string;
  ai_reuse_score: number;
  carbon_estimate?: number;
  verification_status: string;
  lifecycle_stage: string;
}

export interface Requirement {
  id: number;
  buyer_id: number;
  material_type: string;
  quantity_needed: number;
  unit: string;
  max_budget?: number;
  location: string;
  latitude?: number;
  longitude?: number;
  radius_km: number;
  deadline?: string;
  purpose?: string;
  status: string;
  created_at?: string;
}

export interface MatchData {
  id: number;
  material_id: number;
  requirement_id: number;
  match_score: number;
  quantity_score: number;
  quality_score: number;
  distance_score: number;
  price_score: number;
  carbon_score: number;
  ai_reasoning: string;
  recommended_price?: number;
  transport_cost?: number;
  transport_distance_km?: number;
  co2_avoided_kg?: number;
  status: string;
  material?: Material;
  requirement?: Requirement;
  seller?: { id: number; name: string; company: string };
  buyer?: { id: number; name: string; company: string };
  pricing?: PricingEstimate;
  logistics?: LogisticsEstimate;
  impact?: ImpactEstimate;
  second_life?: SecondLifeOption[];
}

export interface PricingEstimate {
  new_material_price: number;
  new_material_total: number;
  recommended_price: number;
  price_range_min: number;
  price_range_max: number;
  buyer_savings: number;
  buyer_savings_percent: number;
  per_unit_price: number;
  reasoning: string[];
}

export interface LogisticsEstimate {
  direct_distance_km: number;
  total_weight_kg: number;
  recommended_route: string;
  route_options: RouteOption[];
  reasoning: string[];
}

export interface RouteOption {
  route_name: string;
  distance_km: number;
  estimated_cost: number;
  estimated_time_hours: number;
  co2_emissions_kg: number;
  vehicle_type: string;
  recommended: boolean;
}

export interface ImpactEstimate {
  waste_diverted_kg: number;
  waste_diverted_tonnes: number;
  co2_avoided_kg: number;
  co2_avoided_tonnes: number;
  transport_emissions_kg: number;
  net_co2_saved_kg: number;
  economic_savings: number;
  circularity_score: number;
  trees_equivalent: number;
  reasoning: string[];
  disclaimer: string;
}

export interface SecondLifeOption {
  use_case: string;
  suitability_score: number;
  description: string;
  category: string;
}

export interface Notification {
  id: number;
  user_id: number;
  title: string;
  message: string;
  notification_type: string;
  reference_id?: number;
  reference_type?: string;
  is_read: boolean;
  created_at?: string;
}

export interface DashboardStats {
  materials_listed: number;
  active_requirements: number;
  successful_matches: number;
  materials_reused: number;
  co2_avoided: number;
  value_recovered: number;
  recent_materials: Material[];
  recent_matches: MatchData[];
  ai_recommendations: { type: string; message: string; priority: string }[];
}

export interface AgentActivityStep {
  agent: string;
  status: string;
  message: string;
  timestamp: string;
  duration_ms: number;
}
