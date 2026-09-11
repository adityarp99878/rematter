import { Material, MatchData, Requirement, Notification, DashboardStats, AgentActivityStep } from './types';

export const demoMaterials: Material[] = [
  { id: 1, seller_id: 1, material_type: 'brick', quantity: 2430, unit: 'units', location: 'Thrissur', condition: 'good', reuse_score: 92, risk_level: 'low', ai_confidence: 0.88, estimated_value: 18500, carbon_estimate: 1900, status: 'available', description: 'Reclaimed red clay bricks from traditional Kerala house demolition', age: '15 years' },
  { id: 2, seller_id: 3, material_type: 'steel_beam', quantity: 45, unit: 'units', location: 'Palakkad', condition: 'fair', reuse_score: 78, risk_level: 'medium', ai_confidence: 0.82, estimated_value: 125000, carbon_estimate: 12825, status: 'available', description: 'Steel I-beams from warehouse demolition', age: '20 years' },
  { id: 3, seller_id: 4, material_type: 'wood/door', quantity: 12, unit: 'units', location: 'Kozhikode', condition: 'good', reuse_score: 85, risk_level: 'low', ai_confidence: 0.91, estimated_value: 36000, carbon_estimate: 504, status: 'available', description: 'Teak wood doors with traditional Kerala carvings', age: '25 years' },
  { id: 4, seller_id: 2, material_type: 'window', quantity: 24, unit: 'units', location: 'Kochi', condition: 'fair', reuse_score: 71, risk_level: 'medium', ai_confidence: 0.87, estimated_value: 48000, carbon_estimate: 840, status: 'available', description: 'Aluminium-framed glass windows', age: '12 years' },
  { id: 5, seller_id: 1, material_type: 'tile', quantity: 500, unit: 'sqft', location: 'Thrissur', condition: 'excellent', reuse_score: 88, risk_level: 'low', ai_confidence: 0.93, estimated_value: 15000, carbon_estimate: 1400, status: 'available', description: 'Ceramic floor tiles in excellent condition', age: '10 years' },
  { id: 6, seller_id: 2, material_type: 'wood', quantity: 200, unit: 'sqft', location: 'Kochi', condition: 'good', reuse_score: 91, risk_level: 'low', ai_confidence: 0.90, estimated_value: 85000, carbon_estimate: 1040, status: 'available', description: 'Premium teak wood planks', age: '18 years' },
  { id: 7, seller_id: 3, material_type: 'concrete', quantity: 1500, unit: 'units', location: 'Palakkad', condition: 'fair', reuse_score: 65, risk_level: 'medium', ai_confidence: 0.85, estimated_value: 22000, carbon_estimate: 195, status: 'available', description: 'Concrete blocks from demolition', age: '22 years' },
  { id: 8, seller_id: 1, material_type: 'pipe', quantity: 150, unit: 'meters', location: 'Thrissur', condition: 'good', reuse_score: 82, risk_level: 'low', ai_confidence: 0.89, estimated_value: 45000, carbon_estimate: 525, status: 'available', description: 'Copper pipes in good condition', age: '8 years' },
  { id: 9, seller_id: 4, material_type: 'roof_tile', quantity: 800, unit: 'units', location: 'Kozhikode', condition: 'good', reuse_score: 87, risk_level: 'low', ai_confidence: 0.92, estimated_value: 28000, carbon_estimate: 960, status: 'available', description: 'Clay roof tiles - Mangalore pattern', age: '20 years' },
  { id: 10, seller_id: 2, material_type: 'window', quantity: 18, unit: 'units', location: 'Kochi', condition: 'fair', reuse_score: 76, risk_level: 'medium', ai_confidence: 0.86, estimated_value: 54000, carbon_estimate: 630, status: 'available', description: 'Salvaged wooden-frame windows', age: '15 years' },
  { id: 11, seller_id: 1, material_type: 'granite', quantity: 100, unit: 'sqft', location: 'Thrissur', condition: 'excellent', reuse_score: 94, risk_level: 'low', ai_confidence: 0.95, estimated_value: 120000, carbon_estimate: 820, status: 'available', description: 'Black granite slabs - premium quality', age: '12 years' },
  { id: 12, seller_id: 3, material_type: 'bamboo', quantity: 300, unit: 'units', location: 'Palakkad', condition: 'good', reuse_score: 89, risk_level: 'low', ai_confidence: 0.88, estimated_value: 18000, carbon_estimate: 135, status: 'available', description: 'Treated bamboo poles', age: '3 years' },
];

export const demoRequirements: Requirement[] = [
  { id: 1, buyer_id: 2, material_type: 'brick', quantity_needed: 2000, unit: 'units', max_budget: 25000, location: 'Kochi', radius_km: 50, purpose: 'School construction project', status: 'active' },
  { id: 2, buyer_id: 3, material_type: 'steel_beam', quantity_needed: 50, unit: 'units', max_budget: 150000, location: 'Palakkad', radius_km: 50, purpose: 'Commercial building', status: 'active' },
  { id: 3, buyer_id: 4, material_type: 'wood/door', quantity_needed: 20, unit: 'units', max_budget: 50000, location: 'Kozhikode', radius_km: 50, purpose: 'Heritage restoration', status: 'active' },
  { id: 4, buyer_id: 2, material_type: 'tile', quantity_needed: 300, unit: 'sqft', max_budget: 20000, location: 'Kochi', radius_km: 50, purpose: 'School flooring', status: 'active' },
  { id: 5, buyer_id: 1, material_type: 'wood', quantity_needed: 100, unit: 'sqft', max_budget: 100000, location: 'Thrissur', radius_km: 50, purpose: 'Home renovation', status: 'active' },
];

export const demoMatch: MatchData = {
  id: 1, material_id: 1, requirement_id: 1, match_score: 94, quantity_score: 95, quality_score: 92,
  distance_score: 96, price_score: 87, carbon_score: 94, status: 'recommended',
  ai_reasoning: 'Excellent match: 2430 bricks available for 2000 needed (121% coverage). High reuse score of 92/100. Only 66 km apart (Thrissur to Kochi). Within budget at ₹18,500 vs ₹25,000 max. Reusing these bricks avoids an estimated 1.9 tonnes CO₂e.',
  recommended_price: 18500, transport_cost: 2400, transport_distance_km: 66, co2_avoided_kg: 1900,
  material: demoMaterials[0],
  requirement: demoRequirements[0],
  seller: { id: 1, name: 'Arjun Menon', company: 'Demo Construction Co.' },
  buyer: { id: 2, name: 'Priya Nair', company: 'GreenBuild School Project' },
  pricing: {
    new_material_price: 12, new_material_total: 29160, recommended_price: 18500,
    price_range_min: 17020, price_range_max: 19980, buyer_savings: 10660,
    buyer_savings_percent: 36.6, per_unit_price: 7.6, reasoning: [
      'New brick price: ₹12/unit', 'Condition (good): 60% of new',
      'Recommended: ₹7.60/unit', 'Total for 2,430 units: ₹18,500', 'Buyer saves ₹10,660 (36.6%) vs new',
    ],
  },
  logistics: {
    direct_distance_km: 66, total_weight_kg: 7290, recommended_route: 'Highway Route',
    route_options: [
      { route_name: 'Direct Route', distance_km: 66, estimated_cost: 4870, estimated_time_hours: 1.7, co2_emissions_kg: 57.3, vehicle_type: 'Light Truck (5T)', recommended: false },
      { route_name: 'Highway Route', distance_km: 85.8, estimated_cost: 5600, estimated_time_hours: 1.6, co2_emissions_kg: 74.5, vehicle_type: 'Light Truck (5T)', recommended: true },
      { route_name: 'Eco Route', distance_km: 72.6, estimated_cost: 6330, estimated_time_hours: 2.1, co2_emissions_kg: 40.1, vehicle_type: 'CNG Truck', recommended: false },
    ],
    reasoning: ['Distance: 66.0 km', 'Weight: 7,290 kg (7.3t)', 'Highway Route recommended', 'Eco option with 30% lower emissions via CNG Truck'],
  },
  impact: {
    waste_diverted_kg: 7290, waste_diverted_tonnes: 7.29, co2_avoided_kg: 1798.2, co2_avoided_tonnes: 1.8,
    transport_emissions_kg: 57.3, net_co2_saved_kg: 1740.9, economic_savings: 10660,
    circularity_score: 90, trees_equivalent: 81.7,
    reasoning: ['Reusing 2,430 units diverts 7.3t from landfill', 'Estimated 1.8t CO₂e avoided vs new production', 'Net CO₂ saved: 1.74t', 'Equivalent to planting 82 trees for one year', 'Circularity score: 90/100'],
    disclaimer: 'Environmental figures are estimates based on industry-average emission factors.',
  },
};

export const demoNotifications: Notification[] = [
  { id: 1, user_id: 1, title: 'New Match Found', message: 'Your reclaimed bricks matched with 3 projects', notification_type: 'match', reference_id: 1, reference_type: 'material', is_read: false },
  { id: 2, user_id: 1, title: 'Buyer Nearby', message: 'AI found a potential buyer just 12 km away', notification_type: 'match', is_read: false },
  { id: 3, user_id: 1, title: 'Passport Ready', message: 'Material passport generated for Steel I-Beams', notification_type: 'passport', reference_id: 2, reference_type: 'material', is_read: true },
  { id: 4, user_id: 1, title: 'Requirement Alert', message: 'New requirement posted matching your ceramic tiles', notification_type: 'requirement', reference_id: 4, reference_type: 'requirement', is_read: false },
  { id: 5, user_id: 1, title: 'Verification Update', message: 'Professional verification recommended for concrete blocks', notification_type: 'verification', reference_id: 7, reference_type: 'material', is_read: true },
];

export const demoStats: DashboardStats = {
  materials_listed: 12, active_requirements: 5, successful_matches: 1,
  materials_reused: 0, co2_avoided: 21.4, value_recovered: 614500,
  recent_materials: demoMaterials.slice(0, 6),
  recent_matches: [demoMatch],
  ai_recommendations: [
    { type: 'match', message: '3 projects currently need your reclaimed bricks', priority: 'high' },
    { type: 'opportunity', message: '1 brick(s) available for \'School construction project\'', priority: 'medium' },
  ],
};

export const demoAgentSteps: AgentActivityStep[] = [
  { agent: 'Upload Agent', status: 'success', message: 'Received material photos', timestamp: '', duration_ms: 150 },
  { agent: 'Vision Agent', status: 'success', message: 'Analyzing images with computer vision...', timestamp: '', duration_ms: 800 },
  { agent: 'Vision Agent', status: 'success', message: 'Detected material type and quantity', timestamp: '', duration_ms: 200 },
  { agent: 'Assessment Agent', status: 'success', message: 'Assessing visible condition and defects', timestamp: '', duration_ms: 600 },
  { agent: 'Assessment Agent', status: 'success', message: 'Calculating reuse score', timestamp: '', duration_ms: 300 },
  { agent: 'Pricing Agent', status: 'success', message: 'Evaluating fair market price', timestamp: '', duration_ms: 400 },
  { agent: 'Impact Agent', status: 'success', message: 'Calculating sustainability impact', timestamp: '', duration_ms: 350 },
  { agent: 'Passport Agent', status: 'success', message: 'Generating material passport', timestamp: '', duration_ms: 250 },
  { agent: 'Second Life Agent', status: 'success', message: 'Identifying reuse applications', timestamp: '', duration_ms: 200 },
  { agent: 'Orchestrator', status: 'success', message: 'Analysis complete. Material ready for marketplace.', timestamp: '', duration_ms: 100 },
];
