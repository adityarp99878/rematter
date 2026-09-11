const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function apiFetch<T>(url: string, options?: RequestInit): Promise<T | null> {
  try {
    const res = await fetch(`${API_BASE}${url}`, {
      ...options,
      headers: { ...options?.headers },
    });
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

export async function getDashboardStats() {
  return apiFetch<any>('/api/dashboard/stats');
}

export async function getMaterials(params?: Record<string, string>) {
  const q = params ? '?' + new URLSearchParams(params).toString() : '';
  return apiFetch<any>(`/api/materials${q}`);
}

export async function getMaterial(id: number) {
  return apiFetch<any>(`/api/materials/${id}`);
}

export async function getMaterialPassport(id: number) {
  return apiFetch<any>(`/api/materials/${id}/passport`);
}

export async function analyzeMaterial(formData: FormData) {
  try {
    const res = await fetch(`${API_BASE}/api/materials/analyze`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

export async function getRequirements(params?: Record<string, string>) {
  const q = params ? '?' + new URLSearchParams(params).toString() : '';
  return apiFetch<any>(`/api/requirements${q}`);
}

export async function createRequirement(data: any) {
  return apiFetch<any>('/api/requirements/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
}

export async function findMatches(requirementId: number) {
  return apiFetch<any>('/api/matches/find', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ requirement_id: requirementId }),
  });
}

export async function getMatches() {
  return apiFetch<any>('/api/matches');
}

export async function getMatch(id: number) {
  return apiFetch<any>(`/api/matches/${id}`);
}

export async function getNotifications() {
  return apiFetch<any>('/api/notifications');
}

export async function markNotificationRead(id: number) {
  return apiFetch<any>(`/api/notifications/${id}/read`, { method: 'PUT' });
}

export async function estimatePricing(data: any) {
  return apiFetch<any>('/api/pricing/estimate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
}

export async function estimateImpact(data: any) {
  return apiFetch<any>('/api/impact/calculate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
}
